"""
Simple AMP Video Creator using MoviePy
Creates a 30-second video from script content
"""

import json
import os
from datetime import datetime

def create_simple_video():
    """
    Create a simple video using available tools
    """
    print("🎬 AMP Video Creator")
    print("=" * 40)
    
    # Read the generated script
    script_file = "scripts/amp_video_script.json"
    
    try:
        if os.path.exists(script_file):
            with open(script_file, 'r', encoding='utf-8') as f:
                script = json.load(f)
            print("✅ Script loaded successfully")
        else:
            print("❌ Script file not found. Please run amp_video_generator.py first")
            return
    except Exception as e:
        print(f"❌ Error loading script: {e}")
        return
    
    print("\n📋 Video Creation Options:")
    print("1. Create PowerPoint slides for manual video creation")
    print("2. Generate HTML slides for screen recording")
    print("3. Create text files for video editing software")
    print("4. Export script for external video tools")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        create_powerpoint_template(script)
    elif choice == "2":
        create_html_slides(script)
    elif choice == "3":
        create_text_files(script)
    elif choice == "4":
        export_for_external_tools(script)
    else:
        print("❌ Invalid choice")

def create_powerpoint_template(script):
    """
    Create a PowerPoint template guide
    """
    print("\n📊 Creating PowerPoint template guide...")
    
    template = f"""
# AMP Video PowerPoint Template Guide

## Video: {script['video_info']['title']}
## Duration: {script['video_info']['duration']}

### Slide 1 (0-5 seconds) - Opening
**Background:** Walmart blue gradient (#004c91 to #0066cc)
**Content:**
- Large Walmart spark logo (center)
- Title: "AMP Update"
- Subtitle: "Week 41 - Store Safety & Security"
**Animation:** Fade in logo, then title text

### Slide 2 (5-20 seconds) - Key Actions
**Background:** Light gradient (#f8f9fa to #ffffff)
**Content:**
- Header: "Key Actions This Week" (blue #004c91)
- Bullet point 1: "✓ Review safety checklist with team"
- Bullet point 2: "✓ Implement new security protocols"
- Each bullet in yellow boxes (#ffc220)
**Animation:** Bullets appear one by one

### Slide 3 (20-25 seconds) - Priority
**Background:** Continuation of Slide 2
**Content:**
- Add red priority badge: "Priority: HIGH"
- Add deadline text: "Deadline: End of Week 41, 2026"
**Animation:** Priority badge and deadline slide in

### Slide 4 (25-30 seconds) - Call to Action
**Background:** Return to blue gradient
**Content:**
- Walmart spark logo (smaller, top)
- Main text: "View Full Details"
- CTA button: "Check Your AMP Dashboard"
**Animation:** Button bounce effect

## Audio Script:
{script['voice_script']['full_script']}

## Recording Instructions:
1. Record audio first using script above
2. Create PowerPoint with slides as described
3. Export as video (File > Export > Create Video)
4. Choose 1080p, 30 seconds duration
5. Upload audio file for narration
"""
    
    # Save template
    os.makedirs("output", exist_ok=True)
    with open("output/powerpoint_template.md", 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("✅ PowerPoint template saved to: output/powerpoint_template.md")
    print("📋 Follow the template to create your video in PowerPoint")

def create_html_slides(script):
    """
    Create HTML slides for screen recording
    """
    print("\n🌐 Creating HTML slides...")
    
    os.makedirs("assets/html_slides", exist_ok=True)
    
    slides = [
        # Slide 1 - Opening
        """<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background: linear-gradient(45deg, #004c91, #0066cc);
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .logo {
            width: 120px;
            height: 120px;
            background: #ffc220;
            border-radius: 50%;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            color: #004c91;
            font-weight: bold;
        }
        h1 {
            font-size: 56px;
            margin: 0 0 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 28px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div>
        <div class="logo">★</div>
        <h1>AMP Update</h1>
        <div class="subtitle">Week 41 - Store Safety & Security</div>
    </div>
</body>
</html>""",
        
        # Slide 2 - Key Actions
        """<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background: linear-gradient(45deg, #f8f9fa, #ffffff);
            color: #333;
            font-family: 'Arial', sans-serif;
            padding: 60px;
            height: calc(100vh - 120px);
            margin: 0;
            display: flex;
            align-items: center;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        h2 {
            color: #004c91;
            font-size: 48px;
            margin-bottom: 50px;
            text-align: center;
        }
        .action-item {
            background: #ffc220;
            padding: 25px 30px;
            margin: 20px 0;
            border-radius: 12px;
            font-size: 32px;
            font-weight: 500;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .priority-badge {
            background: #dc3545;
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 30px;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Key Actions This Week</h2>
        <div class="action-item">✓ Review safety checklist with all team members</div>
        <div class="action-item">✓ Implement new security protocols by end of week</div>
        <div class="priority-badge">Priority: HIGH</div>
    </div>
</body>
</html>""",
        
        # Slide 3 - Call to Action
        """<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background: linear-gradient(45deg, #004c91, #0066cc);
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .logo {
            width: 100px;
            height: 100px;
            background: #ffc220;
            border-radius: 50%;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 50px;
            color: #004c91;
            font-weight: bold;
        }
        h2 {
            font-size: 48px;
            margin: 0 0 40px 0;
        }
        .cta-button {
            background: #ffc220;
            color: #333;
            padding: 20px 50px;
            border-radius: 15px;
            font-size: 28px;
            font-weight: bold;
            display: inline-block;
            text-decoration: none;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        .deadline {
            margin-top: 20px;
            font-size: 20px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div>
        <div class="logo">★</div>
        <h2>View Full Details</h2>
        <div class="cta-button">Check Your AMP Dashboard</div>
        <div class="deadline">Deadline: End of Week 41, 2026</div>
    </div>
</body>
</html>"""
    ]
    
    # Save slides
    for i, slide in enumerate(slides, 1):
        filename = f"assets/html_slides/slide{i}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(slide)
        print(f"✅ Created slide: {filename}")
    
    print("\n📋 Screen Recording Instructions:")
    print("1. Open each HTML file in full-screen browser")
    print("2. Use screen recording software (OBS, Camtasia, etc.)")
    print("3. Record each slide for specified duration:")
    print("   - Slide 1: 5 seconds")
    print("   - Slide 2: 15 seconds") 
    print("   - Slide 3: 10 seconds")
    print("4. Add voiceover in post-production")
    print("5. Export as MP4")

def create_text_files(script):
    """
    Create text files for video editing software
    """
    print("\n📝 Creating text files for video editing...")
    
    os.makedirs("output", exist_ok=True)
    
    # Voice script
    voice_script = f"""AMP Video Voice Script
Duration: 30 seconds

{script['voice_script']['full_script']}

Notes: {script['voice_script']['notes']}
"""
    
    # Visual cues
    visual_cues = """AMP Video Visual Cues

0-5 seconds:
Visual: Walmart logo animation with blue background
Text Overlay: "AMP Update - Week 41"

5-20 seconds:
Visual: Clean white background with bullet points
Text Overlay: 
- "Review safety checklist with team"
- "Implement new security protocols"
Colors: Yellow highlights (#ffc220), Blue text (#004c91)

20-25 seconds:
Visual: Priority indicator
Text Overlay: "Priority: HIGH"
Colors: Red badge (#dc3545)

25-30 seconds:
Visual: Return to blue background with logo
Text Overlay: "Check Your AMP Dashboard"
Colors: Yellow CTA button (#ffc220)
"""
    
    # Technical specs
    tech_specs = """AMP Video Technical Specifications

Resolution: 1920x1080 (16:9)
Duration: 30 seconds exactly
Frame Rate: 30 fps
Audio: 44.1kHz, stereo
File Format: MP4 (H.264)

Brand Colors:
- Walmart Blue: #004c91
- Walmart Yellow: #ffc220
- White: #ffffff
- Red (Priority): #dc3545

Fonts:
- Primary: Arial or Helvetica
- Fallback: Sans-serif system font

Logo Usage:
- Walmart Spark logo
- AMP branding elements
"""
    
    # Save files
    files = [
        ("voice_script.txt", voice_script),
        ("visual_cues.txt", visual_cues),
        ("technical_specs.txt", tech_specs)
    ]
    
    for filename, content in files:
        filepath = f"output/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filepath}")

def export_for_external_tools(script):
    """
    Export script for external video tools
    """
    print("\n📤 Exporting for external video tools...")
    
    os.makedirs("output", exist_ok=True)
    
    # Create comprehensive export
    export_data = {
        "project_info": {
            "title": script['video_info']['title'],
            "duration": 30,
            "resolution": "1920x1080",
            "fps": 30
        },
        "scenes": [
            {
                "start_time": 0,
                "end_time": 5,
                "background": "linear-gradient(45deg, #004c91, #0066cc)",
                "elements": [
                    {"type": "logo", "content": "Walmart Spark", "size": "120px"},
                    {"type": "title", "content": "AMP Update", "font_size": "56px"},
                    {"type": "subtitle", "content": "Week 41 - Store Safety & Security", "font_size": "28px"}
                ],
                "audio": "Important update: Store Safety and Security Update - Week 41."
            },
            {
                "start_time": 5,
                "end_time": 20,
                "background": "linear-gradient(45deg, #f8f9fa, #ffffff)",
                "elements": [
                    {"type": "heading", "content": "Key Actions This Week", "font_size": "48px", "color": "#004c91"},
                    {"type": "bullet", "content": "✓ Review safety checklist with all team members", "background": "#ffc220"},
                    {"type": "bullet", "content": "✓ Implement new security protocols by end of week", "background": "#ffc220"}
                ],
                "audio": "Key actions this week: Review safety checklist with all team members, Implement new security protocols by end of week."
            },
            {
                "start_time": 20,
                "end_time": 30,
                "background": "linear-gradient(45deg, #004c91, #0066cc)",
                "elements": [
                    {"type": "logo", "content": "Walmart Spark", "size": "100px"},
                    {"type": "title", "content": "View Full Details", "font_size": "48px"},
                    {"type": "cta_button", "content": "Check Your AMP Dashboard", "background": "#ffc220"},
                    {"type": "priority", "content": "Priority: HIGH", "background": "#dc3545"},
                    {"type": "deadline", "content": "Deadline: End of Week 41, 2026"}
                ],
                "audio": "Priority level: High. Deadline: End of Week 41, 2026. Check your AMP dashboard for complete details."
            }
        ],
        "brand_guidelines": {
            "colors": {
                "primary_blue": "#004c91",
                "walmart_yellow": "#ffc220", 
                "white": "#ffffff",
                "priority_red": "#dc3545"
            },
            "fonts": ["Arial", "Helvetica", "Sans-serif"],
            "logo_usage": "Walmart Spark logo, centered placement"
        }
    }
    
    # Save export
    with open("output/video_export_data.json", 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)
    
    print("✅ Export data saved to: output/video_export_data.json")
    print("\n📋 Compatible Tools:")
    print("- Adobe After Effects (import JSON data)")
    print("- Adobe Premiere Pro (manual setup using specs)")
    print("- DaVinci Resolve (manual setup)")
    print("- Canva Pro (manual recreation)")
    print("- InVideo (template creation)")

if __name__ == "__main__":
    create_simple_video()