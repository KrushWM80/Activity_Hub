"""
Digital Egg Hunt - QR Code Generator
Generates printable HTML pages with colorful Easter eggs containing QR code links
- Test eggs: 10 small eggs (T1-T10)
- Production eggs: 50 eggs in 4 different sizes (2", 4", 6", 8")
Uses QR Server API for QR code generation - no dependencies needed!
"""

import json
from pathlib import Path
from datetime import datetime
import urllib.parse

# Colors for Easter eggs (festive Easter colors)
EGG_COLORS = [
    "#FF6B6B",  # Red
    "#4ECDC4",  # Teal
    "#FFE66D",  # Yellow
    "#95E1D3",  # Mint
    "#F38181",  # Pink
    "#AA96DA",  # Purple
    "#FCBAD3",  # Light Pink
    "#A8D8EA",  # Light Blue
    "#FCF781",  # Light Yellow
    "#FF8C94",  # Salmon
    "#A8E6CF",  # Light Green
    "#FFD3B6",  # Peach
]

def get_qr_code_url(egg_id, size=300, app_url="http://10.97.114.181:4326/Digital_Egg_Hunt"):
    """
    Get QR code URL from qr-server.com API
    This generates a QR code that when scanned directs to the app with egg ID
    """
    # Create the full URL with egg parameter
    full_url = f"{app_url}?egg={egg_id}"
    encoded = urllib.parse.quote(full_url)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={encoded}"

def generate_html_eggs(egg_type="production", size_inches=None, start_egg=1, end_egg=30):
    """
    Generate an HTML page with oval-shaped eggs containing QR codes
    egg_type: "production" for eggs, "test" for 10 test eggs
    size_inches: 2, 4, 6, or 8 for production eggs (test eggs are always small)
    start_egg: starting egg number (for distributing 50 eggs across sizes)
    end_egg: ending egg number
    """
    if egg_type == "production":
        eggs = [(f"EGG-{i:03d}", i) for i in range(start_egg, end_egg + 1)]
        egg_count = end_egg - start_egg + 1
        if size_inches:
            filename = f"Digital_Egg_Hunt_Production_{size_inches}in.html"
            title = f"Digital Egg Hunt - Production Eggs {size_inches}\" ({egg_count} eggs)"
        else:
            filename = "Digital_Egg_Hunt_Production.html"
            title = "Digital Egg Hunt - Production Eggs"
        watermark = ""
    else:
        eggs = [(f"T{i}", i) for i in range(1, 11)]
        filename = "Digital_Egg_Hunt_Test.html"
        title = "Digital Egg Hunt - Test Eggs (T1-T10) - FOR TESTING ONLY"
        watermark = '<div style="background: #ff6b6b; color: white; padding: 20px; text-align: center; font-weight: bold; font-size: 24px; margin-bottom: 30px;">⚠️ TEST EGGS ONLY - FOR TESTING PURPOSES ⚠️</div>'
    
    # Determine egg SVG size based on inches (at 96 DPI)
    if egg_type == "test":
        svg_size = 200  # Small for test eggs
        qr_size = 120   # QR code size with padding
    else:
        # Map inches to SVG sizes
        size_map = {
            2: 192,   # 2 inches = 192px at 96 DPI
            4: 384,   # 4 inches = 384px at 96 DPI
            6: 576,   # 6 inches = 576px at 96 DPI
            8: 768,   # 8 inches = 768px at 96 DPI
        }
        svg_size = size_map.get(size_inches, 288)  # Default to 3 inches
        qr_size = int(svg_size * 0.5)  # QR is 50% of egg size (with padding)
    
    # Generate eggs HTML
    eggs_html = ""
    for idx, (egg_id, number) in enumerate(eggs):
        color = EGG_COLORS[idx % len(EGG_COLORS)]
        qr_url = get_qr_code_url(egg_id, 200)
        
        # Calculate positions
        egg_cx = svg_size / 2
        egg_cy = svg_size / 2.2
        egg_rx = (svg_size - 20) / 2
        egg_ry = (svg_size - 10) / 1.8
        
        # QR code position (centered with padding)
        qr_x = (svg_size - qr_size) / 2
        qr_y = (svg_size - qr_size) / 2.5
        
        # Text position (lower on the egg)
        text_y = svg_size - 20
        
        eggs_html += f"""
        <div class="egg-container">
            <svg class="egg-oval" viewBox="0 0 {svg_size} {svg_size}" xmlns="http://www.w3.org/2000/svg">
                <!-- Oval egg shape -->
                <ellipse cx="{egg_cx}" cy="{egg_cy}" rx="{egg_rx}" ry="{egg_ry}" fill="{color}" stroke="#333" stroke-width="2"/>
                
                <!-- QR Code embedded in center with padding -->
                <image href="{qr_url}" x="{qr_x}" y="{qr_y}" width="{qr_size}" height="{qr_size}" preserveAspectRatio="none"/>
                
                <!-- Egg name at bottom -->
                <text x="{svg_size/2}" y="{text_y}" font-size="{int(svg_size * 0.1)}" font-weight="bold" text-anchor="middle" fill="#333">{egg_id}</text>
            </svg>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            color: white;
            margin-bottom: 20px;
            font-size: 28px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .watermark {{
            background: #ff6b6b;
            color: white;
            padding: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 24px;
            margin-bottom: 30px;
            border-radius: 10px;
        }}
        
        .instructions {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .instructions h2 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .instructions ol {{
            margin-left: 20px;
            line-height: 1.8;
        }}
        
        .instructions li {{
            margin-bottom: 10px;
        }}
        
        .egg-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
            padding: 0 20px;
        }}
        
        .egg-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s, filter 0.3s;
            min-height: 300px;
        }}
        
        .egg-container:hover {{
            transform: scale(1.05);
            filter: drop-shadow(0 8px 15px rgba(0,0,0,0.3));
        }}
        
        .egg-oval {{
            width: 100%;
            height: auto;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
        }}
        
        .print-info {{
            text-align: center;
            color: white;
            font-size: 14px;
            margin-top: 20px;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .print-info {{
                display: none;
            }}
            
            .instructions {{
                display: none;
            }}
            
            .egg-grid {{
                gap: 20px;
            }}
            
            .egg-card {{
                page-break-inside: avoid;
            }}
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 20px;
            }}
            
            .egg-grid {{
                grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🥚 {title} 🥚</h1>
        
        {watermark}
        
        <div class="instructions">
            <h2>📋 Printing Instructions</h2>
            <ol>
                <li><strong>Print this page</strong> on cardstock or regular white paper</li>
                <li><strong>Cut out each egg</strong> along the border (careful with the QR code)</li>
                <li><strong>Optional:</strong> Laminate eggs for durability</li>
                <li><strong>Hide eggs</strong> around the building</li>
                <li><strong>Participants scan QR codes</strong> with their smartphones</li>
            </ol>
            <p style="margin-top: 15px;"><strong>📱 How it works:</strong> When someone scans a QR code with their phone camera, they'll be taken directly to the leaderboard app to start counting their eggs.</p>
        </div>
        
        <div class="egg-grid">
            {eggs_html}
        </div>
        
        <div class="print-info">
            <strong>Print this page to create eggs for the Digital Egg Hunt</strong><br>
            Use Print function (Ctrl+P) and select "Print to PDF" or print directly
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    output_path = Path(__file__).parent / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return str(output_path), len(eggs)

def generate_egg_list_json(egg_type="production"):
    """Generate a JSON file with all egg IDs for reference"""
    if egg_type == "production":
        eggs = [f"EGG-{i:03d}" for i in range(1, 51)]
        filename = "egg_Hunt_Production_IDs.json"
    else:
        eggs = [f"T{i}" for i in range(1, 11)]
        filename = "egg_Hunt_Test_IDs.json"
    
    data = {
        "type": egg_type,
        "generated": datetime.now().isoformat(),
        "total_eggs": len(eggs),
        "egg_ids": eggs
    }
    
    output_path = Path(__file__).parent / filename
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return str(output_path)

def generate_all():
    """Generate test and production eggs (4 sizes)"""
    print("🥚 Digital Egg Hunt - QR Code Generator 🥚")
    print("=" * 70)
    print()
    
    # Generate test eggs
    test_html, test_count = generate_html_eggs("test")
    test_json = generate_egg_list_json("test")
    print(f"✅ Test eggs HTML created: {test_html}")
    print(f"   Contains: {test_count} test eggs (T1-T10)")
    print(f"✅ Test eggs JSON reference: {test_json}")
    print()
    
    # Generate production eggs in 4 sizes with specific egg ranges
    # Distribution: 2"=30, 4"=25, 6"=15, 8"=10 (Total=80 eggs)
    print("📦 Production Eggs (50 eggs in 4 sizes):")
    
    # 2 inch: EGG-001 to EGG-030 (30 eggs)
    prod_html, prod_count = generate_html_eggs("production", size_inches=2, start_egg=1, end_egg=30)
    print(f"   ✅ 2\" eggs: {prod_html} ({prod_count} eggs: EGG-001 to EGG-030)")
    
    # 4 inch: EGG-031 to EGG-055 (25 eggs)
    prod_html, prod_count = generate_html_eggs("production", size_inches=4, start_egg=31, end_egg=55)
    print(f"   ✅ 4\" eggs: {prod_html} ({prod_count} eggs: EGG-031 to EGG-055)")
    
    # 6 inch: EGG-056 to EGG-070 (15 eggs)
    prod_html, prod_count = generate_html_eggs("production", size_inches=6, start_egg=56, end_egg=70)
    print(f"   ✅ 6\" eggs: {prod_html} ({prod_count} eggs: EGG-056 to EGG-070)")
    
    # 8 inch: EGG-071 to EGG-080 (10 eggs)
    prod_html, prod_count = generate_html_eggs("production", size_inches=8, start_egg=71, end_egg=80)
    print(f"   ✅ 8\" eggs: {prod_html} ({prod_count} eggs: EGG-071 to EGG-080)")
    
    prod_json = generate_egg_list_json("production")
    print(f"✅ Production eggs JSON reference: {prod_json}")
    print()
    
    print("=" * 70)
    print("📋 NEXT STEPS:")
    print()
    print("1️⃣  OPEN THE HTML FILES IN YOUR BROWSER:")
    print(f"   - Test eggs: Digital_Egg_Hunt_Test.html")
    print(f"   - Production 2\" eggs: Digital_Egg_Hunt_Production_2in.html (30 eggs)")
    print(f"   - Production 4\" eggs: Digital_Egg_Hunt_Production_4in.html (25 eggs)")
    print(f"   - Production 6\" eggs: Digital_Egg_Hunt_Production_6in.html (15 eggs)")
    print(f"   - Production 8\" eggs: Digital_Egg_Hunt_Production_8in.html (10 eggs)")
    print()
    print("2️⃣  PRINT THE EGGS:")
    print("   - Use Ctrl+P to open print dialog")
    print("   - Select 'Print to PDF' or print directly to color printer")
    print("   - Use cardstock for durability")
    print()
    print("3️⃣  CUT AND HIDE:")
    print("   - Cut out each egg (be careful with QR codes)")
    print("   - Optionally laminate for extra durability")
    print("   - Hide eggs around the building")
    print()
    print("4️⃣  PARTICIPANTS SCAN QR CODES:")
    print("   - When scanned, QR codes point to the leaderboard app")
    print("   - App URL: http://weus42608431466:4326/Digital_Egg_Hunt")
    print()
    print("=" * 70)

if __name__ == "__main__":
    generate_all()
