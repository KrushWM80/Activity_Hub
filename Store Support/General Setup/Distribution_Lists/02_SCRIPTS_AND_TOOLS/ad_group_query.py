#!/usr/bin/env python3
"""
AD Group Member Query Tool
Pulls members from specified AD groups
"""

import os
import sys
from typing import List, Dict, Optional
import json

try:
    from ldap3 import Server, Connection, ALL, NTLM
except ImportError:
    print("Error: ldap3 not installed. Installing...")
    os.system(f"{sys.executable} -m pip install ldap3")
    from ldap3 import Server, Connection, ALL, NTLM


class ADGroupQuery:
    """Query Active Directory for group members"""

    def __init__(self, domain: str = None):
        """
        Initialize AD connection
        domain: AD domain (e.g., 'walmart.com' or None for auto-detect)
        """
        self.domain = domain or self._detect_domain()
        self.server = None
        self.connection = None

    def _detect_domain(self) -> str:
        """Auto-detect domain from environment"""
        # Walmart uses specific AD domains
        return "walmart.com"

    def connect(self, username: str = None, password: str = None) -> bool:
        """
        Connect to AD server
        Uses current user credentials if not provided
        """
        try:
            # Walmart AD server
            ldap_server = "ad.walmart.com"
            print(f"Connecting to {ldap_server}...")

            self.server = Server(ldap_server, get_info=ALL, use_ssl=False)

            if username and password:
                self.connection = Connection(
                    self.server, user=username, password=password, authentication=NTLM
                )
            else:
                # Use current user (NTLM authentication)
                self.connection = Connection(self.server, authentication=NTLM)

            if self.connection.bind():
                print("✓ Connected to Active Directory")
                return True
            else:
                print(f"X Failed to bind: {self.connection.last_error}")
                return False
        except Exception as e:
            error_msg = str(e)[:100]  # Limit error length for encoding issues
            print(f"X Connection error: {error_msg}")
            return False

    def get_group_members(
        self, group_name: str, recursive: bool = True
    ) -> List[Dict[str, str]]:
        """
        Get all members of an AD group
        """
        if not self.connection or not self.connection.bound:
            print("X Not connected to AD")
            return []

        try:
            # Build base DN from domain
            base_dn = ",".join([f"dc={part}" for part in self.domain.split(".")])
            print(f"Searching for group: {group_name}")
            print(f"Base DN: {base_dn}")

            # Search for the group
            search_filter = f"(cn={group_name})"
            try:
                self.connection.search(
                    search_base=base_dn,
                    search_filter=search_filter,
                    attributes=["distinguishedName", "cn", "mail"],
                )
            except Exception as inner_e:
                print(f"X Search error: {inner_e}")
                return []

            if not self.connection.entries:
                print(f"X Group '{group_name}' not found")
                return []

            group_dn = self.connection.entries[0].distinguishedName.value
            print(f"+ Found group: {group_dn}")

            # Get members of the group
            members = []
            member_filter = f"(memberOf:1.2.840.113556.1.4.1941:={group_dn})" if recursive else f"(memberOf={group_dn})"

            try:
                self.connection.search(
                    search_base=base_dn,
                    search_filter=f"(&(objectClass=user){member_filter})",
                    attributes=[
                        "mail",
                        "givenName",
                        "sn",
                        "sAMAccountName",
                        "displayName",
                        "title",
                        "department",
                    ],
                )
            except Exception as inner_e:
                print(f"X Member search error: {inner_e}")
                return []

            for entry in self.connection.entries:
                member = {
                    "name": entry.displayName.value if entry.displayName.value else "",
                    "email": entry.mail.value if entry.mail.value else "",
                    "username": entry.sAMAccountName.value if entry.sAMAccountName.value else "",
                    "title": entry.title.value if entry.title.value else "",
                    "department": entry.department.value if entry.department.value else "",
                }
                members.append(member)

            print(f"+ Found {len(members)} members\n")
            return members

        except Exception as e:
            print(f"X Error querying group: {e}")
            return []

    def print_members(self, members: List[Dict[str, str]], group_name: str = ""):
        """Pretty print group members"""
        if not members:
            print(f"No members found for {group_name}")
            return

        print(f"\n{'='*100}")
        print(f"GROUP: {group_name}")
        print(f"{'='*100}")
        print(
            f"{' '*30} | {'EMAIL':<40} | {'TITLE':<25} | {'DEPT':<15}"
        )
        print(f"{'-'*30}-+-{'-'*40}-+-{'-'*25}-+-{'-'*15}")

        for member in members:
            name = member["name"][:28] if member["name"] else "N/A"
            email = member["email"][:38] if member["email"] else "N/A"
            title = member["title"][:23] if member["title"] else "N/A"
            dept = member["department"][:13] if member["department"] else "N/A"
            print(f"{name:<30} | {email:<40} | {title:<25} | {dept:<15}")

    def export_to_json(self, data: Dict, filename: str):
        """Export results to JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"+ Exported to {filename}")
        except Exception as e:
            print(f"X Export failed: {e}")

    def disconnect(self):
        """Close AD connection"""
        if self.connection:
            self.connection.unbind()
            print("\n+ Disconnected from Active Directory")


def main():
    """Main execution"""
    print("\n" + "="*100)
    print("Active Directory Group Member Query Tool")
    print("="*100)

    # Create query object
    query = ADGroupQuery()

    # Connect to AD
    if not query.connect():
        print("\nX Failed to connect to Active Directory")
        print("\nTroubleshooting:")
        print("  - Ensure you're on a Walmart network")
        print("  - Check your VPN connection")
        print("  - Verify your domain credentials")
        return

    # Query groups
    groups = ["OPS_SUP_MARKET_TEAM", "OPS_SUP_REGION_TEAM"]
    results = {}

    for group_name in groups:
        members = query.get_group_members(group_name, recursive=True)
        results[group_name] = members
        query.print_members(members, group_name)

    # Export to JSON
    export_file = "ad_groups_results.json"
    query.export_to_json(results, export_file)

    # Disconnect
    query.disconnect()

    print(f"\n+ Query complete! Results saved to {export_file}")


if __name__ == "__main__":
    main()