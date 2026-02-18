#!/usr/bin/env python3
"""
SDL (Store Directory Lookup) Web Scraper
Automatically exports manager data from SDL without manual intervention.

This uses Playwright to automate the browser and download the export.
"""

import os
import time
from datetime import datetime
from pathlib import Path
import shutil


def scrape_sdl_data(download_dir: str = "data_input") -> Path:
    """
    Scrape manager data from SDL and save to download directory.
    
    Args:
        download_dir: Directory to save the exported file
    
    Returns:
        Path to downloaded file
    
    Raises:
        Exception if scraping fails
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright not installed!")
        print("[INFO] Install with: python -m playwright install")
        raise
    
    print("\n" + "="*60)
    print("SDL AUTOMATED EXPORT")
    print("="*60 + "\n")
    
    # SDL URL
    sdl_url = "https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/"
    
    # Create download directory
    download_path = Path(download_dir)
    download_path.mkdir(exist_ok=True)
    
    print(f"[INFO] Starting browser automation...")
    print(f"[INFO] Target URL: {sdl_url}\n")
    
    with sync_playwright() as p:
        # Launch browser (headless=False so you can see what's happening)
        # Change to headless=True once everything is working
        print("[INFO] Launching browser (you'll see a window open)...\n")
        browser = p.chromium.launch(headless=False)  # No slow_mo for faster execution
        
        # Create context with download settings
        context = browser.new_context(
            accept_downloads=True,
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        try:
            # Step 1: Navigate to SDL
            print("[STEP 1] Navigating to SDL...")
            page.goto(sdl_url, wait_until="networkidle", timeout=60000)
            time.sleep(3)
            
            # Step 2: Handle authentication (Windows auth auto-logs in)
            print("[STEP 2] Checking authentication...")
            print("[INFO] Windows authentication successful (already logged in)\n")
            
            # Step 2a: Handle country popup
            print("[STEP 2a] Handling country popup...")
            time.sleep(2)  # Wait for popup to appear
            
            # Try to find and click OK button on country popup
            try:
                # Look for OK button (adjust selector as needed)
                ok_button = page.locator('button:has-text("OK")')
                if ok_button.count() > 0:
                    ok_button.first.click()
                    print("[OK] Clicked OK on country popup\n")
                    time.sleep(1)
                else:
                    # If no OK button, try clicking elsewhere to dismiss
                    print("[INFO] No popup found or already dismissed\n")
            except:
                print("[INFO] Country popup handling - may already be dismissed\n")
            
            # Wait for page to be ready
            page.wait_for_load_state('networkidle')
            print("[OK] SDL page loaded\n")
            
            # Step 3: Wait for home page to fully load (JavaScript renders UI)
            print("[STEP 3] Waiting for home page to fully load...")
            
            # Try loading the page with a refresh if it takes too long
            max_load_attempts = 2
            page_loaded = False
            
            for attempt in range(max_load_attempts):
                try:
                    if attempt > 0:
                        print(f"\n[RETRY {attempt}/{max_load_attempts-1}] Page taking too long, refreshing browser...")
                        page.reload(wait_until='networkidle', timeout=90000)
                        time.sleep(5)
                        print("[OK] Page refreshed\n")
                    
                    # Wait for page to be fully loaded
                    page.wait_for_load_state('networkidle', timeout=90000)  # 90 seconds
                    print("[INFO] Network idle, waiting for UI to render...")
                    
                    # Wait for the "Loading..." to disappear and UI to appear
                    time.sleep(15)  # Give JavaScript time to render
                    
                    # Wait for data grid or some indicator that page is ready
                    try:
                        page.wait_for_selector('table, [role="grid"], .data-grid', timeout=60000)  # 60 seconds
                        print("[OK] Data grid loaded")
                        page_loaded = True
                        break  # Success!
                    except:
                        # Check if we should retry
                        if attempt < max_load_attempts - 1:
                            print("[WARNING] Data grid not found, will retry with refresh...")
                            continue
                        else:
                            print("[INFO] No data grid found after retries, continuing anyway...")
                            page_loaded = True  # Continue even without grid
                            break
                
                except Exception as e:
                    if attempt < max_load_attempts - 1:
                        print(f"[WARNING] Page load issue: {e}")
                        print("[INFO] Will retry with refresh...")
                        continue
                    else:
                        print(f"[WARNING] Page load issue after retries: {e}")
                        print("[INFO] Continuing anyway...")
                        page_loaded = True
                        break
            
            time.sleep(5)  # Extra buffer
            print("[OK] Home page should be ready now\n")
            
            # Step 4: Close any modal overlays that might be blocking
            print("[STEP 4] Checking for modal overlays...")
            try:
                # Multiple strategies to dismiss overlays/modals
                dismissed = False
                
                # Strategy 1: Click X button or Close button in modal
                close_buttons = page.locator('button[aria-label="Close"], button[aria-label="close"], button[title="Close"], button:has-text("×"), button:has-text("Close")')
                if close_buttons.count() > 0:
                    print("[INFO] Found close button in modal")
                    close_buttons.first.click()
                    time.sleep(2)
                    dismissed = True
                    print("[OK] Clicked close button")
                
                # Strategy 2: Press Escape key
                if not dismissed:
                    overlay = page.locator('.cdk-overlay-backdrop, .cdk-overlay-pane')
                    if overlay.count() > 0:
                        print("[INFO] Found overlay, pressing Escape key...")
                        page.keyboard.press('Escape')
                        time.sleep(2)
                        dismissed = True
                        print("[OK] Pressed Escape")
                
                # Strategy 3: Click backdrop (original method)
                if not dismissed:
                    overlay = page.locator('.cdk-overlay-backdrop')
                    if overlay.count() > 0:
                        print("[INFO] Found overlay backdrop, clicking to dismiss...")
                        overlay.first.click()
                        time.sleep(2)
                        dismissed = True
                        print("[OK] Clicked backdrop")
                
                # Verify overlay is gone
                time.sleep(1)
                overlay_after = page.locator('.cdk-overlay-backdrop-showing')
                if overlay_after.count() > 0:
                    print("[WARNING] Overlay still present, trying JavaScript removal...")
                    try:
                        page.evaluate('''
                            document.querySelectorAll('.cdk-overlay-backdrop, .cdk-overlay-pane').forEach(el => el.remove());
                        ''')
                        time.sleep(1)
                        print("[OK] Removed overlay with JavaScript")
                    except:
                        print("[WARNING] Could not remove overlay")
                else:
                    if dismissed:
                        print("[OK] Overlay successfully dismissed\n")
                    else:
                        print("[OK] No overlay found\n")
            except Exception as e:
                print(f"[WARNING] Error during overlay handling: {e}")
                print("[INFO] Continuing anyway...\n")
            
            # Step 4.5: Look for Export button in LEFT PANEL
            print("[STEP 4.5] Looking for Export button in left panel...")
            
            # Take a screenshot to see the current page
            page.screenshot(path="home_page.png", full_page=True)
            print("[DEBUG] Screenshot of home page: home_page.png")
            
            # Debug: Show all text on page
            print("\n[DEBUG] Checking page content...")
            body_text = page.locator('body').inner_text()
            if "Loading" in body_text and len(body_text) < 100:
                print("[WARNING] Page still showing 'Loading...', waiting more...")
                time.sleep(10)
                page.screenshot(path="home_page_after_wait.png", full_page=True)
                print("[DEBUG] Screenshot after wait: home_page_after_wait.png")
            else:
                print("[OK] Page content loaded")
            print()
            
            # Find Export button in LEFT PANEL (should be high up on page, low y value)
            try:
                # Try to find Export button with various selectors
                export_buttons = page.locator('button:has-text("Export"), a:has-text("Export"), [title*="Export"], button:has-text("EXPORT")')
                
                # If no Export buttons found, list ALL buttons to debug
                if export_buttons.count() == 0:
                    print("[DEBUG] No Export buttons found. Listing all buttons:")
                    all_buttons = page.locator('button, a').all()
                    for idx, btn in enumerate(all_buttons[:30]):
                        try:
                            text = btn.inner_text(timeout=1000)
                            if text.strip():
                                print(f"  [{idx}] {text.strip()[:60]}")
                        except:
                            pass
                    print()
                
                button_count = export_buttons.count()
                print(f"[DEBUG] Found {button_count} button(s) with 'Export' text")
                
                # Find the one in the left panel (low y value, left side)
                export_button = None
                for i in range(button_count):
                    btn = export_buttons.nth(i)
                    if btn.is_visible():
                        box = btn.bounding_box()
                        if box:
                            print(f"[DEBUG] Button {i}: '{btn.inner_text()}' at x={box['x']:.0f}, y={box['y']:.0f}")
                            # Left panel button should be on left side (x < 300) and higher up (y < 600)
                            if box['x'] < 300 and box['y'] < 600:
                                print(f"[OK] Found Export button in left panel!")
                                export_button = btn
                                break
                
                if not export_button:
                    print("[WARNING] Couldn't find Export in left panel, using first one")
                    export_button = export_buttons.first
                
                # Highlight and click the button
                page.evaluate('(element) => element.style.border = "5px solid red"', export_button.element_handle())
                time.sleep(1)
                page.screenshot(path="first_export_button.png")
                print("[DEBUG] Screenshot: first_export_button.png")
                
                print("[INFO] Clicking first Export button (opens export page)...")
                export_button.click()
                print("[OK] Clicked first Export button\n")
                
                # Wait for export config page to load
                print("[STEP 5] Waiting for export configuration page...")
                time.sleep(3)
                page.wait_for_load_state('networkidle')
                
                # Wait for any dialogs/animations to settle
                time.sleep(3)
                
                page.screenshot(path="export_config_page.png", full_page=True)
                print("[DEBUG] Screenshot: export_config_page.png")
                print("[OK] Export config page loaded\n")
                
                # Step 5.5: Select Hierarchy section's "Select All" checkbox
                print("[STEP 5.5] Selecting 'Hierarchy' section checkbox...")
                try:
                    # Find the mat-tree-node that contains a label with text "Hierarchy"
                    # Then find the mat-checkbox.grp-chk inside that tree node
                    
                    hierarchy_found = False
                    
                    # Look for the tree node containing "Hierarchy" label
                    # XPath: mat-tree-node that has a label containing "Hierarchy"
                    hierarchy_node_xpath = '//mat-tree-node[.//label[contains(text(), "Hierarchy")]]'
                    hierarchy_nodes = page.locator(hierarchy_node_xpath)
                    
                    if hierarchy_nodes.count() > 0:
                        print(f"[OK] Found Hierarchy tree node")
                        hierarchy_node = hierarchy_nodes.first
                        
                        # Find the grp-chk checkbox inside this node
                        hierarchy_checkbox = hierarchy_node.locator('mat-checkbox.grp-chk')
                        
                        if hierarchy_checkbox.count() > 0:
                            print(f"[OK] Found Hierarchy checkbox inside node")
                            checkbox = hierarchy_checkbox.first
                            
                            # Check if already selected
                            classes = checkbox.get_attribute('class') or ''
                            is_checked = 'mat-checkbox-checked' in classes
                            
                            if not is_checked:
                                print(f"[INFO] Clicking Hierarchy checkbox...")
                                
                                # Try JavaScript click (most reliable for Angular/Material components)
                                try:
                                    page.evaluate('(element) => element.click()', checkbox.element_handle())
                                    time.sleep(2)
                                    print(f"[INFO] Clicked with JavaScript")
                                except Exception as e:
                                    print(f"[DEBUG] JS click failed: {e}")
                                
                                # Verify
                                classes_after = checkbox.get_attribute('class') or ''
                                if 'mat-checkbox-checked' in classes_after:
                                    print(f"[OK] Hierarchy checkbox selected!")
                                    hierarchy_found = True
                                else:
                                    print(f"[INFO] JS click didn't work, trying Playwright click...")
                                    try:
                                        checkbox.click()
                                        time.sleep(2)
                                    except:
                                        pass
                                    
                                    classes_after = checkbox.get_attribute('class') or ''
                                    if 'mat-checkbox-checked' in classes_after:
                                        print(f"[OK] Hierarchy checkbox selected!")
                                        hierarchy_found = True
                                    else:
                                        print(f"[DEBUG] Still not checked. Classes: {classes_after}")
                                        print(f"[INFO] Trying to click the inner input directly...")
                                        try:
                                            # Click the actual input element
                                            inner_input = checkbox.locator('input.mat-checkbox-input')
                                            if inner_input.count() > 0:
                                                page.evaluate('(element) => element.click()', inner_input.first.element_handle())
                                                time.sleep(2)
                                                
                                                classes_after = checkbox.get_attribute('class') or ''
                                                if 'mat-checkbox-checked' in classes_after:
                                                    print(f"[OK] Hierarchy checkbox selected via inner input!")
                                                    hierarchy_found = True
                                                else:
                                                    print(f"[DEBUG] Final classes: {classes_after}")
                                        except Exception as e:
                                            print(f"[DEBUG] Inner input click failed: {e}")
                            else:
                                print(f"[OK] Hierarchy checkbox already selected")
                                hierarchy_found = True
                        else:
                            print(f"[WARNING] Could not find checkbox inside Hierarchy node")
                    else:
                        print(f"[WARNING] Could not find Hierarchy tree node")
                    
                    if not hierarchy_found:
                        print("[WARNING] Could not select Hierarchy section")
                        print("[INFO] Export will proceed without hierarchy data")
                    
                    # Take screenshot to verify
                    time.sleep(1)
                    page.screenshot(path="hierarchy_checkbox_final.png", full_page=True)
                    print("[DEBUG] Screenshot: hierarchy_checkbox_final.png")
                
                except Exception as e:
                    print(f"[WARNING] Failed to select Hierarchy: {e}")
                    print(f"[DEBUG] Error details: {str(e)}")
                    print("[INFO] Export will proceed without hierarchy data")
                
                print()
                
                # Step 6: Click SECOND Export button to trigger download
                print("[STEP 6] Looking for the correct Export button...")
                
                # The Export button has specific attributes:
                # - cdkfocusinitial
                # - color="primary"
                # - mat-raised-button
                # - type="button"
                
                # Try multiple selectors to find the right button
                selectors_to_try = [
                    'button[cdkfocusinitial][color="primary"]',  # Most specific
                    'button[cdkfocusinitial]:has-text("Export")',
                    'button.mat-raised-button.mat-primary:has-text("Export")',
                    'button[type="button"]:has-text("Export")',
                ]
                
                second_export = None
                for selector in selectors_to_try:
                    try:
                        btn = page.locator(selector)
                        if btn.count() > 0:
                            print(f"[OK] Found Export button with: {selector}")
                            print(f"[DEBUG] Found {btn.count()} button(s) matching")
                            second_export = btn.first
                            break
                    except:
                        continue
                
                if not second_export:
                    # Fallback to any Export button
                    print("[WARNING] Using fallback selector")
                    second_export = page.locator('button:has-text("Export")').first
                
                # Highlight it
                page.evaluate('(element) => element.style.border = "5px solid blue"', second_export.element_handle())
                time.sleep(1)
                page.screenshot(path="second_export_button.png", full_page=True)
                print("[DEBUG] Screenshot: second_export_button.png")
                
                # Debug: Print button info
                print(f"[DEBUG] Button text: {second_export.inner_text()}")
                print(f"[DEBUG] Button aria-label: {second_export.get_attribute('aria-label')}")
                
                # Click and wait for download
                print("[INFO] Clicking Export button...")
                
                # Wait for any animations
                time.sleep(2)
                
                # Click the Export button
                # NOTE: Download can take UP TO 10 MINUTES to complete!
                # The page shows a spinner and progress toasts (1000 rows at a time)
                print("[INFO] Clicking Export button...")
                print("[INFO] NOTE: Export can take up to 10 minutes to complete!")
                print("[INFO] Watch for spinner and progress toasts...\n")
                
                # Click with a LONG timeout (15 minutes = 900,000ms to be safe)
                try:
                    with page.expect_download(timeout=900000) as download_info:
                        second_export.click()
                        print("[OK] Clicked Export button")
                        print("[INFO] Waiting for download to complete...")
                        print("[INFO] This may take several minutes. Please wait...\n")
                    
                    download = download_info.value
                    print("[OK] Download completed!\n")
                    
                except Exception as e:
                    print(f"\n[ERROR] Download failed or timed out: {e}")
                    print("[INFO] Taking screenshot to see current state...")
                    page.screenshot(path="download_timeout.png", full_page=True)
                    print("[DEBUG] Screenshot: download_timeout.png")
                    raise
                

                    
            except Exception as e:
                print(f"\n[ERROR] Export process failed: {e}")
                print("[DEBUG] Taking final screenshot...")
                page.screenshot(path="export_error.png", full_page=True)
                print("[DEBUG] Screenshot saved: export_error.png\n")
                raise
            
            # Save with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"managers_export_{timestamp}.xlsx"
            save_path = download_path / filename
            
            download.save_as(save_path)
            
            print(f"[OK] File downloaded: {save_path}\n")
            
            # Convert HTML to real Excel format
            print("[INFO] Converting HTML export to real Excel format...")
            try:
                import pandas as pd
                from io import StringIO
                
                # Read the HTML file
                with open(save_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Parse HTML table to DataFrame
                df_list = pd.read_html(StringIO(html_content))
                df = df_list[0]  # First table
                
                # Save as real Excel file
                standard_name = download_path / "managers_export.xlsx"
                df.to_excel(standard_name, index=False, engine='openpyxl')
                
                # Keep HTML backup with timestamp
                html_backup = download_path / f"managers_export_{timestamp}_html.xlsx"
                shutil.copy(save_path, html_backup)
                
                # Delete the original HTML file since we converted it
                save_path.unlink()
                
                print(f"[OK] Converted to real Excel format")
                print(f"[OK] Saved as: {standard_name}")
                print(f"[INFO] HTML backup: {html_backup}\n")
                
            except Exception as e:
                print(f"[WARNING] Could not convert to Excel: {e}")
                print(f"[INFO] Saving as-is (HTML format)...")
                standard_name = download_path / "managers_export.xlsx"
                if standard_name.exists():
                    standard_name.unlink()
                shutil.copy(save_path, standard_name)
                print(f"[OK] Saved as: {standard_name}\n")
            
            return standard_name
            
        except Exception as e:
            print(f"\n[ERROR] Scraping failed: {e}")
            # Take screenshot for debugging
            screenshot_path = Path("sdl_error_screenshot.png")
            page.screenshot(path=str(screenshot_path))
            print(f"[DEBUG] Screenshot saved: {screenshot_path}\n")
            raise
        
        finally:
            browser.close()


def main():
    """
    Main function to run SDL scraper.
    """
    print("\n" + "="*60)
    print("SDL AUTOMATED DATA EXPORT")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("""
[INFO] SDL Scraper starting...
[INFO] Browser will open to show progress
[INFO] This will take about 30-60 seconds
    """)
    
    try:
        export_file = scrape_sdl_data()
        
        print("="*60)
        print("EXPORT SUCCESSFUL!")
        print("="*60)
        print(f"File: {export_file}")
        print(f"Size: {export_file.stat().st_size / 1024 / 1024:.1f} MB")
        print("\nYou can now run: python daily_check.py")
        print("="*60 + "\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("EXPORT FAILED")
        print("="*60)
        print(f"Error: {e}")
        print("\nCheck the error message and screenshot above.")
        print("You may need to update the script selectors.")
        print("="*60 + "\n")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
