"""
Simple HTML to Image Converter for WorkVivo
Uses selenium with Chrome to capture screenshot
"""
import os
import time

def convert_to_image():
    print("🖼️  Converting HTML to PNG for WorkVivo...")
    print()
    
    # File paths
    html_file = os.path.join(os.path.dirname(__file__), 'workvivo_social_post.html')
    output_file = os.path.join(os.path.dirname(__file__), 'workvivo_winter_health.png')
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("✅ Selenium found! Creating image...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1080,1920')
        chrome_options.add_argument('--hide-scrollbars')
        
        # Launch browser
        driver = webdriver.Chrome(options=chrome_options)
        
        # Load HTML file
        file_url = f'file:///{os.path.abspath(html_file).replace(os.sep, "/")}'
        driver.get(file_url)
        
        # Wait for content to load
        time.sleep(2)
        
        # Find the social post element and screenshot it
        element = driver.find_element('class name', 'social-post')
        element.screenshot(output_file)
        
        driver.quit()
        
        print(f"✅ Image created successfully!")
        print(f"📁 Location: {output_file}")
        print(f"📊 Size: 1080 x 1920 pixels")
        print(f"📱 Ready to upload to WorkVivo!")
        
        return True
        
    except ImportError:
        print("❌ Selenium not installed")
        print()
        print("📦 Install with:")
        print("   pip install selenium")
        print()
        print("📦 Also need Chrome WebDriver:")
        print("   pip install webdriver-manager")
        print()
        return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        return False

def show_manual_instructions():
    print("=" * 60)
    print("📸 MANUAL SCREENSHOT INSTRUCTIONS FOR WORKVIVO")
    print("=" * 60)
    print()
    print("EASIEST METHOD - Using Windows Snipping Tool:")
    print("1. Open 'workvivo_social_post.html' in browser")
    print("2. Press Windows + Shift + S")
    print("3. Select the entire white post area")
    print("4. Open Paint (Win + R, type 'mspaint')")
    print("5. Paste (Ctrl + V)")
    print("6. Save as 'workvivo_winter_health.png'")
    print()
    print("BROWSER METHOD - Using Chrome/Edge:")
    print("1. Open 'workvivo_social_post.html'")
    print("2. Press F12 (Developer Tools)")
    print("3. Press Ctrl + Shift + P")
    print("4. Type 'screenshot'")
    print("5. Select 'Capture node screenshot'")
    print("6. Click on the white post area")
    print("7. Image will auto-download")
    print()
    print("FIREFOX METHOD:")
    print("1. Open 'workvivo_social_post.html'")
    print("2. Right-click on the post")
    print("3. Select 'Take a Screenshot'")
    print("4. Click 'Save visible'")
    print()
    print("=" * 60)
    print()

if __name__ == "__main__":
    success = convert_to_image()
    
    if not success:
        print("⚠️  Automated conversion not available")
        print("📸 Using manual screenshot method instead...")
        print()
        show_manual_instructions()
        
        # Open the HTML file in browser
        html_file = os.path.join(os.path.dirname(__file__), 'workvivo_social_post.html')
        os.system(f'start "" "{html_file}"')
        print("✅ HTML file opened in browser")
        print("👆 Follow the instructions above to capture the screenshot")
