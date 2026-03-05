#!/usr/bin/env python3
"""
Extract HTML code from text files and save as proper HTML files.
This script reads the text files containing embedded HTML and extracts the actual HTML content.
"""

import re
import os

def extract_html_from_text_file(text_file_path, output_html_path):
    """
    Extract HTML code from a text file that contains embedded HTML.
    Finds the first <!DOCTYPE html> and extracts everything from that point.
    """
    try:
        # Read the text file
        with open(text_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find where HTML starts (<!DOCTYPE html>)
        html_start = content.find('<!DOCTYPE html>')
        
        if html_start == -1:
            print(f"ERROR: No HTML found in {text_file_path}")
            return False
        
        # Extract HTML from that point onwards
        html_content = content[html_start:]
        
        # Find the last </html> tag to ensure we get the complete HTML document
        html_end = html_content.rfind('</html>')
        if html_end != -1:
            html_content = html_content[:html_end + 7]  # +7 to include </html>
        
        # Write the HTML to the output file
        os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        file_size = len(html_content)
        print(f"✓ Successfully extracted HTML to {output_html_path}")
        print(f"  File size: {file_size:,} bytes")
        return True
        
    except Exception as e:
        print(f"ERROR processing {text_file_path}: {str(e)}")
        return False

# Main execution
if __name__ == "__main__":
    base_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Refresh Guide"
    
    # Define the files to process
    files_to_extract = [
        {
            "input": os.path.join(base_path, "Store Refresh Business Overview 2-16-26.txt"),
            "output": os.path.join(base_path, "business-overview-dashboard-v3-2-23-26.html"),
            "description": "Main Business Overview Dashboard"
        },
        {
            "input": os.path.join(base_path, "Store_Refresh_Business_Overview_Comparison.txt"),
            "output": os.path.join(base_path, "business-overview-comparison-dashboard-2-23-26.html"),
            "description": "Comparison Dashboard"
        }
    ]
    
    print("=" * 70)
    print("EXTRACTING HTML FROM TEXT FILES")
    print("=" * 70)
    
    success_count = 0
    for file_info in files_to_extract:
        print(f"\nProcessing: {file_info['description']}")
        print(f"Input:  {file_info['input']}")
        print(f"Output: {file_info['output']}")
        
        if extract_html_from_text_file(file_info['input'], file_info['output']):
            success_count += 1
    
    print("\n" + "=" * 70)
    print(f"COMPLETED: {success_count}/{len(files_to_extract)} files extracted successfully")
    print("=" * 70)
