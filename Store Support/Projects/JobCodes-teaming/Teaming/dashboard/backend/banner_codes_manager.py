#!/usr/bin/env python3
"""
Banner Codes Manager - Provides banner code data from ELM datasource
"""

import json
import os
from datetime import datetime
from typing import List, Dict

class BannerCodesManager:
    """Manages banner codes for the Aligned dashboard"""
    
    # Division 1 (WM US Stores) and Division 10 (H&W) Banner Codes from ELM
    # Source: wmt-loc-cat-prod.catalog_location_views.division_view
    # wmt-loc-cat-prod.catalog_location_views.businessunit_view
    DEFAULT_BANNER_CODES = [
        # Division 1 - WM US Stores (Primary Retail Formats)
        {"code": "A1", "desc": "WM Supercenter", "division": 1},
        {"code": "B2", "desc": "Walmart Express", "division": 1},
        {"code": "B4", "desc": "Neighborhood Market", "division": 1},
        {"code": "C7", "desc": "Wal-Mart", "division": 1},
        {"code": "D7", "desc": "Sam's Club", "division": 1},
        {"code": "H8", "desc": "walmart.com", "division": 1},
        {"code": "H9", "desc": "samsclub.com", "division": 1},
        {"code": "O3", "desc": "WM On Campus/RX Facilities", "division": 1},
        {"code": "S3", "desc": "WALMART NEIGHBORHOOD MARKET", "division": 1},
        {"code": "Z1", "desc": "STAND ALONE PICKUP", "division": 1},
        
        # Division 10 - Health & Wellness
        {"code": "N7", "desc": "Pharmacy", "division": 10},
        {"code": "O3", "desc": "WM On Campus/RX Facilities", "division": 10},
    ]
    
    def __init__(self, data_dir=None):
        """Initialize banner codes manager"""
        if data_dir is None:
            data_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.data_dir = data_dir
        self.banner_codes_file = os.path.join(data_dir, 'banner_codes_cache.json')
        self.banner_codes = self._load_banner_codes()
    
    def _load_banner_codes(self) -> List[Dict]:
        """Load banner codes from cache or return defaults"""
        if os.path.exists(self.banner_codes_file):
            try:
                with open(self.banner_codes_file, 'r') as f:
                    data = json.load(f)
                    if 'banner_codes' in data and isinstance(data['banner_codes'], list):
                        return data['banner_codes']
            except Exception as e:
                print(f"⚠️  Error loading banner codes cache: {e}")
        
        return self.DEFAULT_BANNER_CODES
    
    def save_banner_codes(self, banner_codes: List[Dict]) -> bool:
        """Save banner codes to cache"""
        try:
            output = {
                'generated_at': datetime.now().isoformat(),
                'total_banners': len(banner_codes),
                'banner_codes': banner_codes
            }
            
            with open(self.banner_codes_file, 'w') as f:
                json.dump(output, f, indent=2)
            
            self.banner_codes = banner_codes
            return True
        except Exception as e:
            print(f"❌ Error saving banner codes: {e}")
            return False
    
    def get_banner_codes(self) -> List[Dict]:
        """Get all banner codes"""
        return self.banner_codes
    
    def get_dropdown_options(self) -> List[str]:
        """
        Get formatted banner codes for dropdown (deduplicated by code)
        Format: "{CODE} - {DESC}"
        """
        options = []
        seen_codes = set()
        for banner in sorted(self.banner_codes, key=lambda x: x.get('code', '')):
            code = banner.get('code', '').strip()
            desc = banner.get('desc', '').strip()
            if code and desc and code not in seen_codes:
                options.append(f"{code} - {desc}")
                seen_codes.add(code)
        
        return options
    
    def add_banner_code(self, code: str, desc: str) -> bool:
        """Add a banner code if it doesn't exist"""
        code = code.strip().upper()
        desc = desc.strip()
        
        # Check if exists
        for banner in self.banner_codes:
            if banner.get('code', '').upper() == code:
                return False  # Already exists
        
        self.banner_codes.append({'code': code, 'desc': desc})
        return True
    
    def update_banner_codes_from_elm(self, elm_data: List[Dict]) -> int:
        """
        Update banner codes from ELM datasource
        
        Args:
            elm_data: List of dicts with 'banner_code' and 'banner_desc'
        
        Returns:
            Count of new/updated banners
        """
        updated_count = 0
        codes_map = {b['code']: b for b in self.banner_codes}
        
        for item in elm_data:
            code = item.get('banner_code', '').strip().upper()
            desc = item.get('banner_desc', '').strip()
            
            if code and desc:
                if code not in codes_map:
                    self.banner_codes.append({'code': code, 'desc': desc})
                    updated_count += 1
                elif codes_map[code].get('desc') != desc:
                    codes_map[code]['desc'] = desc
                    updated_count += 1
        
        # Re-sort
        self.banner_codes = sorted(self.banner_codes, key=lambda x: x.get('code', ''))
        
        return updated_count

def get_banner_codes_api() -> Dict:
    """Generate API response with banner codes"""
    manager = BannerCodesManager()
    
    return {
        'status': 'ok',
        'banner_codes': manager.get_banner_codes(),
        'dropdown_options': manager.get_dropdown_options(),
        'total': len(manager.get_banner_codes()),
        'generated_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    manager = BannerCodesManager()
    print("\n📊 Banner Codes:")
    print("="*60)
    for code, option in zip(
        [b['code'] for b in manager.get_banner_codes()],
        manager.get_dropdown_options()
    ):
        print(f"  {option}")
    print("="*60)
