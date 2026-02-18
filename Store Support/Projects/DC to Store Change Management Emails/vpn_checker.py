#!/usr/bin/env python3
"""
VPN Connectivity Checker
Detects if we're on VPN and can access SDL/internal systems.
"""

import requests
import socket
from typing import Tuple
import time

def check_vpn_connectivity() -> Tuple[bool, str]:
    """
    Check if we're connected to VPN and can access internal systems.
    
    Returns:
        Tuple of (is_connected: bool, message: str)
    """
    checks = []
    
    # Check 1: Try to resolve SDL hostname
    sdl_host = "elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com"
    try:
        socket.gethostbyname(sdl_host)
        checks.append((True, f"DNS resolution successful for {sdl_host}"))
    except socket.gaierror:
        checks.append((False, f"Cannot resolve {sdl_host} - likely not on VPN"))
        return False, "VPN not detected: Cannot resolve internal hostnames"
    
    # Check 2: Try to access SDL endpoint
    try:
        response = requests.get(
            f"https://{sdl_host}/",
            timeout=10,
            verify=False  # Internal certs may not verify
        )
        if response.status_code < 500:  # Any response is good (even 401/403)
            checks.append((True, f"SDL endpoint accessible (status: {response.status_code})"))
            return True, "VPN connected: SDL accessible"
        else:
            checks.append((False, f"SDL returned {response.status_code}"))
    except requests.exceptions.SSLError:
        # SSL error often means we reached the server but cert issue
        checks.append((True, "SSL error - but server is reachable"))
        return True, "VPN connected: Server reachable (SSL issue)"
    except requests.exceptions.ConnectionError as e:
        checks.append((False, f"Connection error: {e}"))
        return False, f"VPN not detected: Cannot connect to SDL ({e})"
    except Exception as e:
        checks.append((False, f"Unexpected error: {e}"))
    
    # Check 3: Try LAS API (DC alignment endpoint)
    try:
        las_url = "http://dcalignment.telocmdm.prod.us.walmart.com/alignment/api/dcalign/dc/US/6036"
        response = requests.get(las_url, timeout=10)
        if response.status_code == 200:
            checks.append((True, "LAS API accessible"))
            return True, "VPN connected: LAS API accessible"
    except:
        checks.append((False, "LAS API not accessible"))
    
    # If we got here, connectivity is unclear
    return False, "VPN status unclear - internal systems not accessible"

def wait_for_vpn(max_retries: int = 8, retry_delay_minutes: int = 30) -> Tuple[bool, str]:
    """
    Wait for VPN connectivity with retries (legacy - for single-run mode).
    
    Args:
        max_retries: Maximum number of retry attempts (default 8 = 4 hours with 30min delay)
        retry_delay_minutes: Minutes to wait between retries
    
    Returns:
        Tuple of (connected: bool, message: str)
    """
    print(f"\n[VPN CHECK] Checking VPN connectivity...")
    print(f"[VPN CHECK] Will retry up to {max_retries} times with {retry_delay_minutes} minute delays")
    print(f"[VPN CHECK] Total retry window: {max_retries * retry_delay_minutes} minutes\n")
    
    for attempt in range(1, max_retries + 1):
        print(f"[VPN CHECK] Attempt {attempt}/{max_retries}...")
        
        connected, message = check_vpn_connectivity()
        
        if connected:
            print(f"[VPN CHECK] OK: {message}\n")
            return True, message
        else:
            print(f"[VPN CHECK] FAIL: {message}")
            
            if attempt < max_retries:
                print(f"[VPN CHECK] Waiting {retry_delay_minutes} minutes before retry...\n")
                time.sleep(retry_delay_minutes * 60)
            else:
                print(f"[VPN CHECK] All retry attempts exhausted.\n")
    
    return False, f"VPN not available after {max_retries} attempts over {max_retries * retry_delay_minutes} minutes"

def quick_vpn_check() -> Tuple[bool, str]:
    """
    Quick single VPN check (no retries).
    Use this when Task Scheduler runs hourly.
    
    Returns:
        Tuple of (connected: bool, message: str)
    """
    print(f"\n[VPN CHECK] Checking VPN connectivity...")
    connected, message = check_vpn_connectivity()
    
    if connected:
        print(f"[VPN CHECK] OK: {message}\n")
    else:
        print(f"[VPN CHECK] FAIL: {message}\n")
    
    return connected, message

if __name__ == "__main__":
    print("Testing VPN Connectivity...\n")
    
    # Quick check
    connected, message = check_vpn_connectivity()
    print(f"Result: {'CONNECTED' if connected else 'NOT CONNECTED'}")
    print(f"Message: {message}")
