"""Quick debug script to see actual API response format"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_base = "https://retina-ds-genai-backend.prod.k8s.walmart.net"

# Request a video generation
print("=" * 80)
print("SUBMITTING VIDEO GENERATION REQUEST")
print("=" * 80)

submit_url = f"{api_base}/api/v1/videos/generate"
headers = {"Content-Type": "application/json"}

payload = {
    "prompt": "a professional training video showing associates learning",
    "model": "veo2",
    "duration": 5,
    "aspect_ratio": "16:9",
    "use_case": "motion_graphics"
}

response = requests.post(submit_url, json=payload, headers=headers, verify=False)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Response: {json.dumps(data, indent=2)}")
request_id = data.get("request_id")
print(f"\nRequest ID: {request_id}")

if request_id:
    print("\n" + "=" * 80)
    print("POLLING FOR COMPLETION")
    print("=" * 80)
    
    import time
    status_url = f"{api_base}/api/v1/videos/status/{request_id}"
    
    for i in range(120):  # Poll for up to 10 minutes
        time.sleep(5)
        status_response = requests.get(status_url, headers=headers, verify=False)
        status_data = status_response.json()
        status = status_data.get("status", "unknown")
        progress = status_data.get("progress", 0)
        
        print(f"[{i*5}s] Status: {status} ({progress}%)")
        
        if status == "completed":
            print("\n" + "=" * 80)
            print("COMPLETED RESPONSE (FULL JSON)")
            print("=" * 80)
            print(json.dumps(status_data, indent=2))
            
            # Try to find download URL
            if "output" in status_data and "video" in status_data["output"]:
                video_data = status_data["output"]["video"]
                print("\n" + "=" * 80)
                print("VIDEO DATA")
                print("=" * 80)
                print(json.dumps(video_data, indent=2))
                
                url = video_data.get("url")
                print(f"\nVideo URL: {url}")
                
                # Check if there's a signed URL or alternative format
                if "video" in status_data["output"]:
                    print(f"\nFull video object keys: {status_data['output']['video'].keys()}")
            break
        elif "error" in status or status == "failed":
            print(f"Error: {status_data}")
            break
