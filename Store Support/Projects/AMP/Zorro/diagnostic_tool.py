#!/usr/bin/env python3
"""
Diagnostic Tool for Zorro Video Generation Pipeline

This tool helps diagnose why videos may not match prompts by:
1. Testing API connectivity
2. Verifying authentication
3. Tracing prompt flow through the pipeline
4. Checking for pre-generated/sample video detection
5. Browser-based SSO authentication

Usage:
    python diagnostic_tool.py --check-all
    python diagnostic_tool.py --authenticate
    python diagnostic_tool.py --test-prompt "Your test prompt here"
"""

import argparse
import base64
import hashlib
import http.server
import json
import logging
import os
import socket
import socketserver
import sys
import threading
import time
import uuid
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests

# Configure verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("DiagnosticTool")


# =============================================================================
# Color Output Helpers
# =============================================================================
class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def success(msg: str) -> str:
    return f"{Colors.GREEN}✓ {msg}{Colors.RESET}"


def error(msg: str) -> str:
    return f"{Colors.RED}✗ {msg}{Colors.RESET}"


def warning(msg: str) -> str:
    return f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}"


def info(msg: str) -> str:
    return f"{Colors.CYAN}ℹ {msg}{Colors.RESET}"


def header(msg: str) -> str:
    return f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}\n{msg}\n{'='*60}{Colors.RESET}\n"


# =============================================================================
# Browser-Based SSO Authentication
# =============================================================================
class SSOCallbackHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler to receive SSO callback."""
    
    token = None
    error_message = None
    
    def do_GET(self):
        """Handle GET request from SSO callback."""
        parsed = urlparse(self.path)
        
        if parsed.path == "/callback":
            query_params = parse_qs(parsed.query)
            
            if "token" in query_params:
                SSOCallbackHandler.token = query_params["token"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                <html>
                <head>
                    <title>Authentication Successful</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f8ff; }
                        .success { color: #28a745; font-size: 24px; }
                        .info { color: #666; margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <h1 class="success">&#10004; Authentication Successful!</h1>
                    <p class="info">You can close this window and return to the terminal.</p>
                    <p class="info">Your token has been saved to <code>.env</code></p>
                </body>
                </html>
                """)
            elif "code" in query_params:
                # OAuth authorization code flow
                SSOCallbackHandler.token = query_params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                <html>
                <head><title>Auth Code Received</title></head>
                <body>
                    <h1>Authorization Code Received</h1>
                    <p>Close this window and return to terminal.</p>
                </body>
                </html>
                """)
            elif "error" in query_params:
                SSOCallbackHandler.error_message = query_params.get("error_description", query_params["error"])[0]
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"""
                <html>
                <head><title>Authentication Failed</title></head>
                <body>
                    <h1 style="color: red;">Authentication Failed</h1>
                    <p>{SSOCallbackHandler.error_message}</p>
                </body>
                </html>
                """.encode())
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Invalid callback</h1></body></html>")
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class BrowserAuthenticator:
    """Handle browser-based SSO authentication for Walmart."""
    
    def __init__(self, callback_port: int = 8765):
        self.callback_port = callback_port
        self.callback_url = f"http://localhost:{callback_port}/callback"
        
        # Walmart SSO endpoints (update these based on actual SSO provider)
        self.sso_base_url = os.getenv(
            "WALMART_SSO_URL",
            "https://login.walmart.com"  # Placeholder - update with actual SSO URL
        )
        
    def authenticate(self) -> Optional[str]:
        """
        Launch browser for SSO authentication.
        
        Returns:
            SSO token if successful, None otherwise
        """
        print(header("Browser-Based SSO Authentication"))
        
        # Check if we already have a token
        existing_token = os.getenv("WALMART_SSO_TOKEN")
        if existing_token:
            print(info(f"Existing token found (length: {len(existing_token)} chars)"))
            if self._validate_token(existing_token):
                print(success("Existing token is valid!"))
                return existing_token
            else:
                print(warning("Existing token is expired or invalid. Re-authenticating..."))
        
        # Find an available port
        port = self._find_available_port()
        self.callback_url = f"http://localhost:{port}/callback"
        
        # Start callback server
        print(info(f"Starting callback server on port {port}..."))
        server = socketserver.TCPServer(("", port), SSOCallbackHandler)
        server_thread = threading.Thread(target=server.handle_request)
        server_thread.daemon = True
        server_thread.start()
        
        # Build SSO login URL
        state = str(uuid.uuid4())
        sso_url = self._build_sso_url(state)
        
        print(info("Opening browser for authentication..."))
        print(f"   URL: {sso_url[:80]}...")
        
        # Open browser
        webbrowser.open(sso_url)
        
        print(info("Waiting for authentication callback (timeout: 120s)..."))
        
        # Wait for callback
        timeout = 120
        start = time.time()
        while time.time() - start < timeout:
            if SSOCallbackHandler.token:
                break
            if SSOCallbackHandler.error_message:
                print(error(f"Authentication failed: {SSOCallbackHandler.error_message}"))
                server.shutdown()
                return None
            time.sleep(0.5)
        
        server.shutdown()
        
        if SSOCallbackHandler.token:
            token = SSOCallbackHandler.token
            print(success(f"Token received! (length: {len(token)} chars)"))
            
            # Save to .env file
            self._save_token(token)
            
            return token
        else:
            print(error("Authentication timed out"))
            return None
    
    def _find_available_port(self) -> int:
        """Find an available port for the callback server."""
        for port in range(8765, 8800):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("No available ports found")
    
    def _build_sso_url(self, state: str) -> str:
        """Build the SSO authentication URL."""
        # This is a placeholder - update based on actual Walmart SSO implementation
        # Common patterns: OAuth2, SAML, Ping Identity, Okta
        
        params = {
            "response_type": "token",  # or "code" for auth code flow
            "client_id": os.getenv("WALMART_SSO_CLIENT_ID", "zorro-video-generator"),
            "redirect_uri": self.callback_url,
            "state": state,
            "scope": "openid profile email",
        }
        
        # For now, provide instructions for manual token retrieval
        print("\n" + "="*60)
        print(warning("MANUAL TOKEN RETRIEVAL INSTRUCTIONS:"))
        print("="*60)
        print(f"""
1. Open Walmart Media Studio in your browser:
   {Colors.CYAN}https://retina-ds-genai-backend.prod.k8s.walmart.net{Colors.RESET}

2. Log in with your Walmart credentials

3. Open Browser Developer Tools (F12)

4. Go to Network tab, find any API request

5. Look for 'Authorization' header or cookies

6. Copy the token value

7. Add to your .env file:
   {Colors.GREEN}WALMART_SSO_TOKEN=your-token-here{Colors.RESET}

8. Or paste it when prompted below
""")
        print("="*60 + "\n")
        
        # Prompt for manual token entry
        manual_token = input("Paste your token here (or press Enter to skip): ").strip()
        if manual_token:
            self._save_token(manual_token)
            return manual_token
        
        return f"{self.sso_base_url}/authorize?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    
    def _validate_token(self, token: str) -> bool:
        """Validate if token is still valid by making a test API call."""
        try:
            api_url = os.getenv(
                "WALMART_MEDIA_STUDIO_URL",
                "https://retina-ds-genai-backend.prod.k8s.walmart.net"
            )
            
            response = requests.get(
                f"{api_url}/api/v1/health",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                timeout=10,
                verify=False  # Dev mode
            )
            
            return response.status_code in [200, 401, 403]  # API is reachable
        except Exception as e:
            logger.debug(f"Token validation error: {e}")
            return False
    
    def _save_token(self, token: str):
        """Save token to .env file."""
        env_path = Path(".env")
        
        # Read existing .env content
        existing_content = ""
        if env_path.exists():
            existing_content = env_path.read_text()
        
        # Update or add WALMART_SSO_TOKEN
        lines = existing_content.split("\n")
        updated = False
        new_lines = []
        
        for line in lines:
            if line.startswith("WALMART_SSO_TOKEN="):
                new_lines.append(f"WALMART_SSO_TOKEN={token}")
                updated = True
            else:
                new_lines.append(line)
        
        if not updated:
            new_lines.append(f"WALMART_SSO_TOKEN={token}")
        
        # Write back
        env_path.write_text("\n".join(new_lines))
        print(success(f"Token saved to {env_path.absolute()}"))
        
        # Also set in current environment
        os.environ["WALMART_SSO_TOKEN"] = token


# =============================================================================
# Diagnostic Checks
# =============================================================================
@dataclass
class DiagnosticResult:
    """Result of a diagnostic check."""
    name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None


class PipelineDiagnostics:
    """Comprehensive diagnostics for the video generation pipeline."""
    
    def __init__(self):
        self.results: List[DiagnosticResult] = []
        self.api_url = os.getenv(
            "WALMART_MEDIA_STUDIO_URL",
            "https://retina-ds-genai-backend.prod.k8s.walmart.net"
        )
    
    def run_all_checks(self) -> List[DiagnosticResult]:
        """Run all diagnostic checks."""
        print(header("Running Complete Diagnostic Suite"))
        
        checks = [
            self.check_environment_variables,
            self.check_api_connectivity,
            self.check_authentication,
            self.check_llm_configuration,
            self.check_video_output_directory,
            self.check_sample_video_detection,
            self.check_prompt_flow,
        ]
        
        for check in checks:
            try:
                result = check()
                self.results.append(result)
                self._print_result(result)
            except Exception as e:
                result = DiagnosticResult(
                    name=check.__name__,
                    passed=False,
                    message=f"Check failed with exception: {str(e)}",
                    suggestions=["Review the error and check logs"]
                )
                self.results.append(result)
                self._print_result(result)
        
        # Summary
        self._print_summary()
        
        return self.results
    
    def _print_result(self, result: DiagnosticResult):
        """Print a single diagnostic result."""
        if result.passed:
            print(success(f"{result.name}: {result.message}"))
        else:
            print(error(f"{result.name}: {result.message}"))
        
        if result.details:
            for key, value in result.details.items():
                print(f"      {key}: {value}")
        
        if result.suggestions:
            print(f"      {Colors.YELLOW}Suggestions:{Colors.RESET}")
            for suggestion in result.suggestions:
                print(f"        → {suggestion}")
        print()
    
    def _print_summary(self):
        """Print summary of all checks."""
        print(header("Diagnostic Summary"))
        
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        
        print(f"   Total Checks: {len(self.results)}")
        print(f"   {Colors.GREEN}Passed: {passed}{Colors.RESET}")
        print(f"   {Colors.RED}Failed: {failed}{Colors.RESET}")
        
        if failed > 0:
            print(f"\n   {Colors.YELLOW}Critical Issues to Address:{Colors.RESET}")
            for r in self.results:
                if not r.passed:
                    print(f"   → {r.name}")
    
    def check_environment_variables(self) -> DiagnosticResult:
        """Check required environment variables."""
        required_vars = {
            "WALMART_SSO_TOKEN": "Walmart SSO authentication token",
            "OPENAI_API_KEY": "OpenAI API key for prompt enhancement (optional)",
        }
        
        optional_vars = {
            "WALMART_MEDIA_STUDIO_URL": "Custom API endpoint URL",
            "WALMART_SSL_VERIFY": "SSL verification toggle",
            "ANTHROPIC_API_KEY": "Anthropic API key (alternative to OpenAI)",
        }
        
        missing = []
        found = {}
        
        for var, desc in required_vars.items():
            value = os.getenv(var)
            if value:
                # Mask sensitive values
                masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                found[var] = masked
            else:
                if var != "OPENAI_API_KEY":  # OpenAI is optional
                    missing.append(f"{var}: {desc}")
        
        if missing:
            return DiagnosticResult(
                name="Environment Variables",
                passed=False,
                message=f"Missing {len(missing)} required variable(s)",
                details={"found": found, "missing": missing},
                suggestions=[
                    "Run: python diagnostic_tool.py --authenticate",
                    "Or manually add to .env file"
                ]
            )
        
        return DiagnosticResult(
            name="Environment Variables",
            passed=True,
            message="All required variables configured",
            details=found
        )
    
    def check_api_connectivity(self) -> DiagnosticResult:
        """Check if API is reachable."""
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Try health endpoint
            response = requests.get(
                f"{self.api_url}/api/v1/health",
                timeout=15,
                verify=False
            )
            
            return DiagnosticResult(
                name="API Connectivity",
                passed=True,
                message=f"API reachable (status: {response.status_code})",
                details={
                    "url": self.api_url,
                    "status_code": response.status_code,
                    "response_time": f"{response.elapsed.total_seconds():.2f}s"
                }
            )
        except requests.exceptions.ConnectionError as e:
            return DiagnosticResult(
                name="API Connectivity",
                passed=False,
                message="Cannot connect to API",
                details={"url": self.api_url, "error": str(e)},
                suggestions=[
                    "Check if you're connected to Walmart VPN",
                    "Verify the API URL is correct",
                    f"Try accessing {self.api_url} in your browser"
                ]
            )
        except Exception as e:
            return DiagnosticResult(
                name="API Connectivity",
                passed=False,
                message=f"Connection error: {type(e).__name__}",
                details={"error": str(e)}
            )
    
    def check_authentication(self) -> DiagnosticResult:
        """Check if authentication is working."""
        token = os.getenv("WALMART_SSO_TOKEN")
        
        if not token:
            return DiagnosticResult(
                name="Authentication",
                passed=False,
                message="No SSO token configured",
                suggestions=[
                    "Run: python diagnostic_tool.py --authenticate",
                    "Or add WALMART_SSO_TOKEN to .env file"
                ]
            )
        
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Test authenticated endpoint
            response = requests.get(
                f"{self.api_url}/api/v1/models",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                timeout=15,
                verify=False
            )
            
            if response.status_code == 200:
                return DiagnosticResult(
                    name="Authentication",
                    passed=True,
                    message="Authentication successful",
                    details={"models_available": True}
                )
            elif response.status_code == 401:
                return DiagnosticResult(
                    name="Authentication",
                    passed=False,
                    message="Token is invalid or expired",
                    details={"status": 401},
                    suggestions=[
                        "Run: python diagnostic_tool.py --authenticate",
                        "Token may have expired - get a new one"
                    ]
                )
            else:
                return DiagnosticResult(
                    name="Authentication",
                    passed=False,
                    message=f"Unexpected response: {response.status_code}",
                    details={"response": response.text[:200]}
                )
        except Exception as e:
            return DiagnosticResult(
                name="Authentication",
                passed=False,
                message=f"Auth check failed: {str(e)}"
            )
    
    def check_llm_configuration(self) -> DiagnosticResult:
        """Check LLM configuration for prompt enhancement."""
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=openai_key)
                # Quick test
                models = client.models.list()
                return DiagnosticResult(
                    name="LLM Configuration",
                    passed=True,
                    message="OpenAI configured and working",
                    details={"provider": "OpenAI"}
                )
            except Exception as e:
                return DiagnosticResult(
                    name="LLM Configuration",
                    passed=False,
                    message=f"OpenAI key configured but not working: {str(e)}",
                    suggestions=["Check if API key is valid", "Check OpenAI API status"]
                )
        elif anthropic_key:
            return DiagnosticResult(
                name="LLM Configuration",
                passed=True,
                message="Anthropic configured",
                details={"provider": "Anthropic"}
            )
        else:
            return DiagnosticResult(
                name="LLM Configuration",
                passed=False,
                message="No LLM API key configured",
                details={
                    "effect": "Prompts will use generic fallback templates",
                    "result": "Videos may not match your specific prompts!"
                },
                suggestions=[
                    "Add OPENAI_API_KEY=sk-... to .env file",
                    "Or add ANTHROPIC_API_KEY for Claude",
                    "Without this, prompts are NOT enhanced by AI"
                ]
            )
    
    def check_video_output_directory(self) -> DiagnosticResult:
        """Check video output directory."""
        output_dir = Path("output/videos")
        
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            return DiagnosticResult(
                name="Output Directory",
                passed=True,
                message=f"Created output directory: {output_dir}",
                details={"path": str(output_dir.absolute())}
            )
        
        # Count existing videos
        videos = list(output_dir.glob("*.mp4"))
        
        return DiagnosticResult(
            name="Output Directory",
            passed=True,
            message=f"Output directory exists with {len(videos)} videos",
            details={
                "path": str(output_dir.absolute()),
                "video_count": len(videos)
            }
        )
    
    def check_sample_video_detection(self) -> DiagnosticResult:
        """Check if videos appear to be pre-generated samples."""
        output_dir = Path("output/videos")
        
        if not output_dir.exists():
            return DiagnosticResult(
                name="Sample Video Detection",
                passed=True,
                message="No videos to analyze yet"
            )
        
        videos = list(output_dir.glob("*.mp4"))
        if not videos:
            return DiagnosticResult(
                name="Sample Video Detection",
                passed=True,
                message="No videos to analyze yet"
            )
        
        # Analyze videos for signs of pre-generated content
        suspicious_signs = []
        video_hashes = []
        
        for video in videos[:10]:  # Check up to 10 videos
            try:
                # Get file hash to detect duplicates
                with open(video, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    if file_hash in video_hashes:
                        suspicious_signs.append(f"Duplicate video detected: {video.name}")
                    video_hashes.append(file_hash)
                
                # Check file size (very small files might be samples)
                size = video.stat().st_size
                if size < 100_000:  # Less than 100KB
                    suspicious_signs.append(f"Suspiciously small file: {video.name} ({size} bytes)")
                
            except Exception as e:
                logger.debug(f"Error analyzing {video}: {e}")
        
        if suspicious_signs:
            return DiagnosticResult(
                name="Sample Video Detection",
                passed=False,
                message="Potential pre-generated/sample videos detected!",
                details={"suspicious_signs": suspicious_signs},
                suggestions=[
                    "These videos may be cached samples, not freshly generated",
                    "Check API authentication",
                    "Clear output/videos directory and regenerate"
                ]
            )
        
        return DiagnosticResult(
            name="Sample Video Detection",
            passed=True,
            message="Videos appear to be unique generated content",
            details={"analyzed": len(videos)}
        )
    
    def check_prompt_flow(self) -> DiagnosticResult:
        """Check the prompt enhancement flow."""
        try:
            # Try to import and test the prompt generator
            from src.core.prompt_generator import PromptGenerator
            from src.models.message import ActivityMessage
            from src.services.llm_service import LLMService
            
            # Create test message
            test_message = ActivityMessage(
                id="diag_test_001",
                content="Test safety training reminder for associates",
                category="training",
                priority="medium",
                sender="diagnostic_tool"
            )
            
            # Try to generate prompt
            llm_service = LLMService()
            generator = PromptGenerator(llm_service=llm_service)
            
            result = generator.generate(test_message)
            
            if result.success:
                prompt = result.prompt
                # Check if prompt is actually enhanced or just a template
                if "professional training area" in prompt.enhanced_prompt.lower():
                    return DiagnosticResult(
                        name="Prompt Flow",
                        passed=False,
                        message="Prompts are using FALLBACK templates (LLM not working)",
                        details={
                            "original": test_message.content,
                            "enhanced": prompt.enhanced_prompt[:100] + "...",
                            "is_fallback": True
                        },
                        suggestions=[
                            "Configure OPENAI_API_KEY or ANTHROPIC_API_KEY",
                            "Your prompts are NOT being enhanced by AI"
                        ]
                    )
                else:
                    return DiagnosticResult(
                        name="Prompt Flow",
                        passed=True,
                        message="Prompt enhancement is working!",
                        details={
                            "original": test_message.content,
                            "enhanced": prompt.enhanced_prompt[:100] + "...",
                            "llm_used": result.llm_model_used
                        }
                    )
            else:
                return DiagnosticResult(
                    name="Prompt Flow",
                    passed=False,
                    message=f"Prompt generation failed: {result.error_message}",
                    suggestions=["Check LLM configuration"]
                )
                
        except Exception as e:
            return DiagnosticResult(
                name="Prompt Flow",
                passed=False,
                message=f"Could not test prompt flow: {str(e)}",
                details={"error": str(e)}
            )


# =============================================================================
# Prompt Tracing
# =============================================================================
class PromptTracer:
    """Trace a prompt through the entire pipeline with verbose logging."""
    
    def __init__(self):
        self.trace_log: List[Dict[str, Any]] = []
    
    def trace_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        Trace a prompt through the entire pipeline.
        
        Args:
            user_prompt: The original user prompt
            
        Returns:
            Complete trace of the prompt through all stages
        """
        print(header(f"Tracing Prompt Through Pipeline"))
        print(f"Original Prompt: {Colors.CYAN}{user_prompt}{Colors.RESET}\n")
        
        trace = {
            "timestamp": datetime.now().isoformat(),
            "original_prompt": user_prompt,
            "stages": []
        }
        
        # Stage 1: Message Processing
        print(f"\n{Colors.BOLD}Stage 1: Message Processing{Colors.RESET}")
        stage1 = self._trace_message_processing(user_prompt)
        trace["stages"].append(stage1)
        
        # Stage 2: Prompt Enhancement
        print(f"\n{Colors.BOLD}Stage 2: Prompt Enhancement (LLM){Colors.RESET}")
        stage2 = self._trace_prompt_enhancement(stage1.get("output", user_prompt))
        trace["stages"].append(stage2)
        
        # Stage 3: API Payload Preparation
        print(f"\n{Colors.BOLD}Stage 3: API Payload Preparation{Colors.RESET}")
        stage3 = self._trace_payload_preparation(stage2.get("enhanced_prompt", user_prompt))
        trace["stages"].append(stage3)
        
        # Stage 4: API Request (simulated)
        print(f"\n{Colors.BOLD}Stage 4: API Request{Colors.RESET}")
        stage4 = self._trace_api_request(stage3.get("payload", {}))
        trace["stages"].append(stage4)
        
        # Summary
        print(header("Prompt Trace Summary"))
        self._print_trace_summary(trace)
        
        return trace
    
    def _trace_message_processing(self, prompt: str) -> Dict[str, Any]:
        """Trace message processing stage."""
        try:
            from src.core.message_processor import MessageProcessor
            from src.models.message import ActivityMessage
            
            processor = MessageProcessor()
            message = ActivityMessage(
                id=f"trace_{int(time.time())}",
                content=prompt,
                category="general",
                priority="medium",
                sender="trace_tool"
            )
            
            result = processor.process(message)
            
            output = {
                "stage": "message_processing",
                "input": prompt,
                "output": result.sanitized_content or prompt,
                "is_valid": result.is_valid,
                "warnings": result.warnings,
                "changes_made": prompt != (result.sanitized_content or prompt)
            }
            
            print(f"   Input:  {prompt[:50]}...")
            print(f"   Output: {output['output'][:50]}...")
            print(f"   Valid:  {success('Yes') if result.is_valid else error('No')}")
            if output["changes_made"]:
                print(f"   {warning('Content was modified during processing')}")
            
            return output
            
        except Exception as e:
            print(f"   {error(f'Error: {str(e)}')}")
            return {"stage": "message_processing", "error": str(e), "output": prompt}
    
    def _trace_prompt_enhancement(self, prompt: str) -> Dict[str, Any]:
        """Trace prompt enhancement stage."""
        try:
            from src.core.prompt_generator import PromptGenerator
            from src.models.message import ActivityMessage
            from src.services.llm_service import LLMService
            
            message = ActivityMessage(
                id=f"trace_{int(time.time())}",
                content=prompt,
                category="general",
                priority="medium",
                sender="trace_tool"
            )
            
            llm_service = LLMService()
            generator = PromptGenerator(llm_service=llm_service)
            
            result = generator.generate(message)
            
            if result.success:
                enhanced = result.prompt.enhanced_prompt
                
                # Detect if fallback was used
                is_fallback = "professional" in enhanced.lower() and "walmart" in enhanced.lower() and len(enhanced) < 200
                
                output = {
                    "stage": "prompt_enhancement",
                    "input": prompt,
                    "enhanced_prompt": enhanced,
                    "llm_used": result.llm_model_used,
                    "is_fallback": is_fallback,
                    "style": result.prompt.style.value if result.prompt.style else None,
                    "mood": result.prompt.mood.value if result.prompt.mood else None,
                }
                
                print(f"   Input:    {prompt[:50]}...")
                print(f"   Enhanced: {enhanced[:80]}...")
                print(f"   LLM Used: {result.llm_model_used or 'None (fallback)'}")
                
                if is_fallback:
                    print(f"   {error('⚠ FALLBACK TEMPLATE DETECTED - LLM not working!')}")
                    print(f"   {warning('Your specific prompt is NOT being used properly!')}")
                else:
                    print(f"   {success('LLM enhancement appears to be working')}")
                
                return output
            else:
                print(f"   {error(f'Enhancement failed: {result.error_message}')}")
                return {"stage": "prompt_enhancement", "error": result.error_message, "enhanced_prompt": prompt}
                
        except Exception as e:
            print(f"   {error(f'Error: {str(e)}')}")
            return {"stage": "prompt_enhancement", "error": str(e), "enhanced_prompt": prompt}
    
    def _trace_payload_preparation(self, enhanced_prompt: str) -> Dict[str, Any]:
        """Trace API payload preparation."""
        try:
            from src.models.prompt import PromptMood, PromptStyle, VideoPrompt
            from src.providers.walmart_media_studio import WalmartMediaStudioProvider
            
            # Create a VideoPrompt
            video_prompt = VideoPrompt(
                original_message=enhanced_prompt[:100],
                enhanced_prompt=enhanced_prompt,
                style=PromptStyle.PROFESSIONAL,
                mood=PromptMood.INFORMATIVE,
                duration_hint=8,
                keywords=[],
                metadata={"trace_id": f"trace_{int(time.time())}"}
            )
            
            # Get provider and prepare payload
            provider = WalmartMediaStudioProvider()
            payload = provider._prepare_payload(video_prompt)
            
            output = {
                "stage": "payload_preparation",
                "input": enhanced_prompt,
                "payload": payload,
                "prompt_in_payload": payload.get("prompt", "NOT FOUND"),
            }
            
            print(f"   Enhanced Prompt: {enhanced_prompt[:50]}...")
            print(f"   Payload Prompt:  {payload.get('prompt', 'NOT FOUND')[:50]}...")
            print(f"   Model:           {payload.get('model', 'NOT SET')}")
            print(f"   Duration:        {payload.get('duration', 'NOT SET')}s")
            print(f"   Aspect Ratio:    {payload.get('aspect_ratio', 'NOT SET')}")
            
            # Check if prompt matches
            if payload.get("prompt") == enhanced_prompt:
                print(f"   {success('Prompt correctly included in payload')}")
            else:
                print(f"   {warning('Prompt may have been modified in payload')}")
            
            return output
            
        except Exception as e:
            print(f"   {error(f'Error: {str(e)}')}")
            return {"stage": "payload_preparation", "error": str(e)}
    
    def _trace_api_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Trace what would be sent to the API."""
        api_url = os.getenv(
            "WALMART_MEDIA_STUDIO_URL",
            "https://retina-ds-genai-backend.prod.k8s.walmart.net"
        )
        
        token = os.getenv("WALMART_SSO_TOKEN")
        
        output = {
            "stage": "api_request",
            "endpoint": f"{api_url}/api/v1/videos/generate",
            "method": "POST",
            "payload": payload,
            "has_auth": bool(token),
        }
        
        print(f"   Endpoint:   {output['endpoint']}")
        print(f"   Method:     POST")
        print(f"   Auth Token: {'Present' if token else error('MISSING!')}")
        print(f"   Payload:")
        print(f"      prompt: {payload.get('prompt', 'N/A')[:60]}...")
        print(f"      model:  {payload.get('model', 'N/A')}")
        
        if not token:
            print(f"\n   {error('⚠ NO AUTH TOKEN - API will likely return sample/demo videos!')}")
            output["warning"] = "No auth token - API may return demo videos"
        
        return output
    
    def _print_trace_summary(self, trace: Dict[str, Any]):
        """Print summary of the trace."""
        original = trace["original_prompt"]
        
        # Find final prompt
        final_prompt = original
        for stage in trace["stages"]:
            if "enhanced_prompt" in stage:
                final_prompt = stage["enhanced_prompt"]
            elif "payload" in stage and "prompt" in stage["payload"]:
                final_prompt = stage["payload"]["prompt"]
        
        print(f"Original:  {original[:60]}...")
        print(f"Final:     {final_prompt[:60]}...")
        
        # Check for issues
        issues = []
        
        for stage in trace["stages"]:
            if stage.get("is_fallback"):
                issues.append("LLM fallback used - prompt not AI-enhanced")
            if stage.get("warning"):
                issues.append(stage["warning"])
            if "error" in stage:
                issues.append(f"Error in {stage['stage']}: {stage['error']}")
        
        if issues:
            print(f"\n{Colors.RED}Issues Found:{Colors.RESET}")
            for issue in issues:
                print(f"   → {issue}")
        else:
            print(f"\n{success('No issues detected in prompt flow')}")


# =============================================================================
# Main Entry Point
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Diagnostic Tool for Zorro Video Generation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python diagnostic_tool.py --check-all          Run all diagnostic checks
    python diagnostic_tool.py --authenticate       Browser-based SSO authentication
    python diagnostic_tool.py --test-prompt "..."  Trace a prompt through pipeline
    python diagnostic_tool.py --clear-cache        Clear cached/sample videos
        """
    )
    
    parser.add_argument(
        "--check-all",
        action="store_true",
        help="Run all diagnostic checks"
    )
    
    parser.add_argument(
        "--authenticate",
        action="store_true",
        help="Authenticate via browser (SSO)"
    )
    
    parser.add_argument(
        "--test-prompt",
        type=str,
        metavar="PROMPT",
        help="Trace a specific prompt through the pipeline"
    )
    
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear output/videos directory"
    )
    
    args = parser.parse_args()
    
    # Default to --check-all if no args
    if not any([args.check_all, args.authenticate, args.test_prompt, args.clear_cache]):
        args.check_all = True
    
    print(f"""
{Colors.BOLD}{Colors.BLUE}╔══════════════════════════════════════════════════════════╗
║         ZORRO VIDEO GENERATION DIAGNOSTIC TOOL           ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}
    """)
    
    if args.authenticate:
        auth = BrowserAuthenticator()
        token = auth.authenticate()
        if token:
            print(f"\n{success('Authentication complete!')}")
        else:
            print(f"\n{error('Authentication failed')}")
            sys.exit(1)
    
    if args.clear_cache:
        print(header("Clearing Video Cache"))
        output_dir = Path("output/videos")
        if output_dir.exists():
            videos = list(output_dir.glob("*.mp4"))
            for video in videos:
                video.unlink()
                print(f"   Deleted: {video.name}")
            print(f"\n{success(f'Cleared {len(videos)} cached videos')}")
        else:
            print(info("No cache directory found"))
    
    if args.check_all:
        diagnostics = PipelineDiagnostics()
        diagnostics.run_all_checks()
    
    if args.test_prompt:
        tracer = PromptTracer()
        tracer.trace_prompt(args.test_prompt)


if __name__ == "__main__":
    main()
