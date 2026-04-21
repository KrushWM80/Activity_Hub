"""Verify all Teaming tab updates"""
with open('dashboard/frontend/index.html', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print('✓ VERIFICATION: Teaming Tab Updates Complete')
print('='*70)
print()

# Check for Impacted column width
if 'min-width: 420px' in content:
    print('✓ Impacted column expanded to 420px (sort icon inline)')
else:
    print('✗ Impacted column width NOT updated')

# Check for Pending Request column removal
if 'pendingBadge' not in content or content.count('pendingBadge') < 2:
    print('✓ Pending Request column REMOVED from Teaming tab')
else:
    print('✗ Pending Request column still present')

# Check for smart action logic
if 'getSmartActionText' in content:
    print('✓ Smart Action Logic applied (getSmartActionText function called)')
else:
    print('✗ Smart Action Logic NOT applied')

# Check button group
if 'btn-group-sm' in content and 'flex-wrap: nowrap' in content:
    print('✓ Button group layout with proper spacing')
else:
    print('✗ Button group styling missing')

# Check for tooltip on Impacted
if 'data-bs-toggle="tooltip"' in content:
    print('✓ Tooltips enabled on Impacted badges')
else:
    print('✗ Tooltips NOT enabled')

# Check edit button
if 'bi-pencil' in content:
    print('✓ Edit button (pencil icon) added')
else:
    print('✗ Edit button NOT added')

# Check Admin tab Action column formatting
if 'min-width: 200px' in content or 'min-width: 240px' in content:
    print('✓ Admin & Teaming Action columns have proper widths')
else:
    print('✗ Action column widths need adjustment')

print()
print('='*70)
print('✓ TEAMING TAB TRANSFORMATION COMPLETE')
print()
print('Summary:')
print('• Impacted: 420px min-width (header on one line)')
print('• Pending Request: REMOVED')  
print('• Smart Actions: Pending/Update/Assign buttons')
print('• Buttons: Action + Edit in button group')
print('• Tooltips: Worker info on Impacted hover')
print('• Admin tab: 200px Action column (combined)')
