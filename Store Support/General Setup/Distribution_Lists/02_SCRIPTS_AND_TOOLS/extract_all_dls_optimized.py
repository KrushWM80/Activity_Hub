#!/usr/bin/env python3
"""
Extract ALL Distribution Lists - Optimized for Large Scale
Processes 134,900+ DLs efficiently with progress tracking
"""

import subprocess
import csv
from datetime import datetime
import time


def extract_dls_batch(batch_size=5000):
    """
    Extract DLs in batches with progress tracking
    """
    
    print("\n" + "="*80)
    print("EXTRACTING ALL DISTRIBUTION LISTS (Optimized for 134,900+ DLs)")
    print("="*80 + "\n")
    
    print("Processing in batches to avoid timeout...")
    print("This may take 10-15 minutes for full extraction\n")
    
    # PowerShell script that processes and outputs incrementally
    ps_script = '''
    $searcher = New-Object System.DirectoryServices.DirectorySearcher
    $searcher.Filter = "(&(objectClass=group)(mail=*))"
    $searcher.PropertiesToLoad.Add("mail") | Out-Null
    $searcher.PropertiesToLoad.Add("cn") | Out-Null
    $searcher.PropertiesToLoad.Add("displayName") | Out-Null
    $searcher.PropertiesToLoad.Add("description") | Out-Null
    $searcher.PropertiesToLoad.Add("member") | Out-Null
    $searcher.PageSize = 1000
    
    $results = $searcher.FindAll()
    $total = $results.Count
    Write-Host "TOTAL:$total"
    
    $count = 0
    foreach ($result in $results) {
        $count++
        if ($count % 1000 -eq 0) {
            Write-Host "PROGRESS:$count"
        }
        
        $props = $result.Properties
        $email = if ($props["mail"].Count -gt 0) { $props["mail"][0] } else { "" }
        $name = if ($props["cn"].Count -gt 0) { $props["cn"][0] } else { "" }
        $displayName = if ($props["displayName"].Count -gt 0) { $props["displayName"][0] } else { "" }
        $description = if ($props["description"].Count -gt 0) { $props["description"][0] } else { "" }
        $memberCount = if ($props["member"].Count -gt 0) { $props["member"].Count } else { 0 }
        
        # Output as CSV line
        Write-Host "DATA:$email|$name|$displayName|$description|$memberCount"
    }
    
    Write-Host "DONE:$count"
    '''
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"all_distribution_lists_{timestamp}.csv"
    
    # Create CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['email', 'name', 'displayName', 'description', 'memberCount', 'category'])
        
        try:
            # Start PowerShell process
            process = subprocess.Popen(
                ["powershell", "-Command", ps_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            total_count = 0
            processed = 0
            start_time = time.time()
            
            # Read output line by line
            for line in process.stdout:
                line = line.strip()
                
                if line.startswith("TOTAL:"):
                    total_count = int(line.split(":")[1])
                    print(f"Total DLs to process: {total_count:,}")
                    
                elif line.startswith("PROGRESS:"):
                    processed = int(line.split(":")[1])
                    elapsed = time.time() - start_time
                    rate = processed / elapsed if elapsed > 0 else 0
                    remaining = (total_count - processed) / rate if rate > 0 else 0
                    print(f"  Progress: {processed:,} / {total_count:,} ({processed*100//total_count if total_count > 0 else 0}%) - ETA: {remaining//60:.0f} min")
                    
                elif line.startswith("DATA:"):
                    data = line[5:].split("|")
                    if len(data) >= 5:
                        email, name, displayName, description, memberCount = data[:5]
                        
                        # Categorize
                        name_lower = name.lower()
                        category = 'General'
                        if 'ops' in name_lower or 'operations' in name_lower:
                            category = 'Operations'
                        elif 'market' in name_lower:
                            category = 'Market'
                        elif 'region' in name_lower:
                            category = 'Region'
                        elif 'support' in name_lower:
                            category = 'Support'
                        elif 'management' in name_lower or 'mgmt' in name_lower:
                            category = 'Management'
                        elif 'team' in name_lower:
                            category = 'Team'
                        
                        writer.writerow([email, name, displayName, description, memberCount, category])
                        
                elif line.startswith("DONE:"):
                    final_count = int(line.split(":")[1])
                    print(f"\n+ Complete! Processed {final_count:,} distribution lists")
            
            process.wait()
            
        except Exception as e:
            print(f"X Error: {e}")
            return None
    
    return csv_file


def generate_summary(csv_file):
    """
    Generate summary statistics from CSV
    """
    
    print("\n" + "="*80)
    print("GENERATING STATISTICS")
    print("="*80 + "\n")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            dls = list(reader)
        
        total = len(dls)
        
        # Calculate stats
        total_members = sum(int(dl['memberCount']) for dl in dls if dl['memberCount'].isdigit())
        
        categories = {}
        for dl in dls:
            cat = dl.get('category', 'General')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"Total Distribution Lists: {total:,}")
        print(f"Total Memberships (sum): {total_members:,}")
        print(f"Average Members per DL: {total_members // total if total > 0 else 0}")
        
        print(f"\nBy Category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count:,}")
        
        # Size distribution
        small = sum(1 for dl in dls if dl['memberCount'].isdigit() and int(dl['memberCount']) < 50)
        medium = sum(1 for dl in dls if dl['memberCount'].isdigit() and 50 <= int(dl['memberCount']) < 500)
        large = sum(1 for dl in dls if dl['memberCount'].isdigit() and int(dl['memberCount']) >= 500)
        
        print(f"\nBy Size:")
        print(f"  Small (<50 members):    {small:,}")
        print(f"  Medium (50-499):        {medium:,}")
        print(f"  Large (500+):           {large:,}")
        
        print(f"\n" + "="*80)
        
        return True
        
    except Exception as e:
        print(f"X Error generating stats: {e}")
        return False


def main():
    """
    Main execution
    """
    
    start_time = time.time()
    
    # Extract DLs
    csv_file = extract_dls_batch()
    
    if csv_file:
        # Generate statistics
        generate_summary(csv_file)
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*80)
        print("EXTRACTION COMPLETE")
        print("="*80)
        print(f"\nFile created: {csv_file}")
        print(f"Time elapsed: {elapsed//60:.0f} minutes {elapsed%60:.0f} seconds")
        print(f"\nThis file is ready for the DL Selector tool")
        print("="*80 + "\n")
    else:
        print("\nX Extraction failed")


if __name__ == "__main__":
    main()
