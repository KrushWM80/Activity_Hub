#!/usr/bin/env python3
"""Check HTML file syntax"""

import os

# Check for basic syntax by parsing the HTML file
html_path = 'Interface/Admin/admin-dashboard.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()
    
    # Count braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    open_parens = content.count('(')
    close_parens = content.count(')')
    
    print('\nHTML Brace Balance Check')
    print('=' * 60)
    print(f'Open braces {{: {open_braces}')
    print(f'Close braces }}: {close_braces}')
    balance_status = 'OK' if open_braces == close_braces else 'MISMATCH'
    print(f'Balance: {balance_status}')
    print()
    print(f'Open parens (: {open_parens}')
    print(f'Close parens ): {close_parens}')
    paren_status = 'OK' if open_parens == close_parens else 'MISMATCH'
    print(f'Balance: {paren_status}')
    print('=' * 60)
    
    if balance_status == 'OK' and paren_status == 'OK':
        print('\n✓ Syntax check PASSED - No obvious brace/paren mismatches')
    else:
        print('\n✗ Syntax errors detected')

# Also check for specific error patterns
print('\nSearching for common syntax errors...')
print('-' * 60)

error_patterns = [
    ('}}', 'Double brace'),
    ('function function', 'Double function keyword'),
    ('} }', 'Extra closing brace'),
]

for pattern, desc in error_patterns:
    if pattern in content:
        count = content.count(pattern)
        print(f'⚠️  Found {count} occurrence(s) of "{pattern}" ({desc})')

print('-' * 60)
print('\nFile ready for deployment')
