"""
Convert WorkVivo HTML post to PNG image using Playwright
"""
from playwright.sync_api import sync_playwright
import os

def html_to_image():
    print("🖼️  Converting HTML to PNG image...")
    
    # Get the file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, 'workvivo_social_post.html')
    output_file = os.path.join(script_dir, 'workvivo_winter_health.png')
    
    # Convert to file:// URL
    html_url = f'file:///{html_file.replace(os.sep, "/")}'
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1080, 'height': 1920})
        
        # Load the HTML file
        print(f"📄 Loading: {html_file}")
        page.goto(html_url)
        
        # Wait for content to load
        page.wait_for_timeout(1000)
        
        # Take screenshot of the social post element
        print("📸 Capturing screenshot...")
        page.locator('.social-post').screenshot(path=output_file)
        
        browser.close()
    
    print(f"✅ Image saved: {output_file}")
    print(f"📊 Size: 1080x1920 pixels")
    print(f"📱 Ready to upload to WorkVivo!")
    
    return output_file

if __name__ == "__main__":
    try:
        output = html_to_image()
        print(f"\n✨ Success! Upload this file to WorkVivo:")
        print(f"   {output}")
    except ImportError:
        print("\n❌ Playwright not installed!")
        print("📦 Install with: pip install playwright")
        print("🔧 Then run: playwright install chromium")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTrying alternative method...")
