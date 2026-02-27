#!/usr/bin/env python3
"""
Generate thumbnail for Vimeo audio message
Creates: Listen Now - Audio Message thumbnail
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_thumbnail():
    """Generate the audio message thumbnail"""
    
    output_folder = Path("../output/podcasts")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    output_path = output_folder / "merch_msg_thumbnail.jpeg"
    
    # Create image with blue background
    width, height = 1920, 1080
    blue_color = (13, 118, 180)  # Blue background color
    
    img = Image.new('RGB', (width, height), color=blue_color)
    draw = ImageDraw.Draw(img)
    
    # Draw circle for microphone icon background
    circle_x = 300
    circle_y = height // 2
    circle_radius = 200
    circle_color = (200, 220, 240)  # Light blue
    
    draw.ellipse(
        [circle_x - circle_radius, circle_y - circle_radius, 
         circle_x + circle_radius, circle_y + circle_radius],
        fill=circle_color
    )
    
    # Draw microphone icon (simplified)
    # Microphone capsule
    mic_x = circle_x
    mic_y = circle_y - 40
    capsule_width = 80
    capsule_height = 100
    mic_color = (30, 60, 100)
    
    draw.ellipse(
        [mic_x - capsule_width//2, mic_y - capsule_height//2,
         mic_x + capsule_width//2, mic_y + capsule_height//2],
        outline=mic_color,
        width=8
    )
    
    # Microphone stand
    draw.rectangle(
        [mic_x - 15, mic_y + 50, mic_x + 15, mic_y + 150],
        fill=mic_color
    )
    
    # Microphone base
    draw.ellipse(
        [mic_x - 80, mic_y + 140, mic_x + 80, mic_y + 170],
        fill=mic_color
    )
    
    # Add text - "Listen Now"
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 120)
        subtitle_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 80)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Text position
    text_x = 700
    text_y = 350
    text_color = (255, 255, 255)  # White
    
    # Draw "Listen Now"
    draw.text((text_x, text_y), "Listen Now", font=title_font, fill=text_color)
    
    # Draw "Audio Message"
    draw.text((text_x, text_y + 150), "Audio Message", font=subtitle_font, fill=text_color)
    
    # Save image
    img.save(output_path, 'JPEG', quality=95)
    
    print("\n" + "=" * 80)
    print("THUMBNAIL GENERATION")
    print("=" * 80)
    print(f"\n✅ Thumbnail Created: merch_msg_thumbnail.jpeg")
    print(f"   Resolution: {width}x{height}px")
    print(f"   Location: {output_path.absolute()}")
    print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    create_thumbnail()
