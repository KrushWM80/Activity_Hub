#!/usr/bin/env python3
import base64

# Read the PNG file and encode to base64
with open(r'Interface\Spark_Blank.png', 'rb') as f:
    image_data = f.read()
    base64_string = base64.b64encode(image_data).decode('utf-8')

print("Spark Logo Base64 (copy this for email templates):")
print(base64_string)
