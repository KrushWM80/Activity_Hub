"""Quick check: Azure Speech SDK and env var availability."""
import os

try:
    import azure.cognitiveservices.speech as speechsdk
    print(f"azure-cognitiveservices-speech: {speechsdk.__version__}")
except ImportError:
    print("NOT INSTALLED: azure-cognitiveservices-speech")

try:
    import requests
    print(f"requests: {requests.__version__}")
except ImportError:
    print("NOT INSTALLED: requests")

key = os.environ.get("AZURE_SPEECH_KEY", "")
region = os.environ.get("AZURE_SPEECH_REGION", "")
print(f"AZURE_SPEECH_KEY set: {bool(key)}")
print(f"AZURE_SPEECH_REGION set: {bool(region)}")
