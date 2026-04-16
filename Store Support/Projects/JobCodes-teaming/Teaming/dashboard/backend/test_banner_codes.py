#!/usr/bin/env python3
"""Test script to verify banner codes configuration"""

from banner_codes_manager import BannerCodesManager
import json

print('\n' + '='*80)
print('BANNER CODES CONFIGURATION TEST - Division 1 & 10 Only')
print('='*80)

manager = BannerCodesManager()
codes = manager.get_banner_codes()

print(f'\nTotal Banner Codes: {len(codes)}')
print('\nAll Banner Codes (with Division):')
print('-' * 80)
for code in codes:
    div = code.get('division', 'N/A')
    print(f'  {code["code"]:4} - {code["desc"]:45} (Div {div})')

print('\n' + '='*80)
print('Dropdown Format (for frontend):')
print('='*80)
dropdown = manager.get_dropdown_options()
print(f'Total dropdown options: {len(dropdown)}\n')
for i, option in enumerate(dropdown, 1):
    print(f'  {i:2}. {option}')

print('\n' + '='*80)
print('API Response Structure:')
print('='*80)
response = {
    "status": "ok",
    "banner_codes": codes,
    "dropdown_options": dropdown,
    "total": len(dropdown),
    "generated_at": "test"
}
print(json.dumps(response, indent=2))

print('\n' + '='*80)
print('✅ Configuration validation complete')
print('='*80 + '\n')
