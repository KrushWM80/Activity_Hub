"""Quick API test for Walmart Media Studio"""
import requests
import json

# Get available models
url = 'https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/models'
r = requests.get(url, verify=False, timeout=10)
data = r.json()

print("=" * 60)
print("VIDEO MODELS:")
print("=" * 60)
for model in data.get('video_models', []):
    print(f"  ID: {model['id']}")
    print(f"  Name: {model['display_name']}")
    print(f"  Use Cases: {model.get('supported_use_cases', [])}")
    print()

# Now test video generation with correct parameters
print("=" * 60)
print("TESTING VIDEO GENERATION:")
print("=" * 60)

gen_url = 'https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/videos/generate'
payload = {
    'prompt': 'A Walmart associate stocking shelves in a clean store',
    'duration_seconds': 5,
    'model': 'veo2',  # Using 'model' not 'model_name'
    'aspect_ratio': '16:9'
}

print(f"Endpoint: {gen_url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

r = requests.post(gen_url, json=payload, verify=False, timeout=60)
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)[:2000]}")
