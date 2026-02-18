"""
User ID Lookup Tool
Search for associates by name or email and retrieve their User ID (WIN)
"""

import pandas as pd
import os
from pathlib import Path

class UserIDLookup:
    def __init__(self, data_file=None):
        """
        Initialize the lookup tool with a data file
        If no file specified, will use the most recent export group members dataset
        """
        if data_file is None:
            # Use the most recent group export
            data_file = "exportGroupMembers_2025-12-23.csv"
        
        self.data_file = data_file
        self.df = None
        self.email_column = None
        self.name_column = None
        self.id_column = None
        self.load_data()
    
    def load_data(self):
        """Load the data from CSV file and detect column names"""
        if os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file)
            
            # Detect column names (handle different CSV formats)
            columns = self.df.columns.tolist()
            
            # Find email column
            for col in ['mail', 'Email', 'email', 'EmailAddress']:
                if col in columns:
                    self.email_column = col
                    break
            
            # Find name columns
            if 'displayName' in columns:
                self.name_column = 'displayName'
            elif 'Full_Name' in columns:
                self.name_column = 'Full_Name'
            
            # Find ID column
            for col in ['id', 'WIN', 'EmployeeID', 'employee_number']:
                if col in columns:
                    self.id_column = col
                    break
            
            print(f"✓ Loaded {len(self.df)} records from {self.data_file}")
            print(f"  Email column: {self.email_column}")
            print(f"  ID column: {self.id_column}")
        else:
            print(f"✗ Error: File not found: {self.data_file}")
            return False
        return True
    
    def search_by_name(self, search_term, exact=False):
        """
        Search for associates by display name
        
        Args:
            search_term: Name to search for
            exact: If True, requires exact match (case insensitive)
        
        Returns:
            DataFrame with matching records
        """
        if self.df is None:
            return None
        
        search_term = search_term.strip()
        
        if self.name_column:
            if exact:
                mask = self.df[self.name_column].str.lower() == search_term.lower()
            else:
                mask = self.df[self.name_column].str.contains(search_term, case=False, na=False)
        else:
            # Fallback to First_Name/Last_Name if available
            if 'First_Name' in self.df.columns and 'Last_Name' in self.df.columns:
                if 'Full_Name' not in self.df.columns:
                    self.df['Full_Name'] = self.df['First_Name'].fillna('') + ' ' + self.df['Last_Name'].fillna('')
                
                if exact:
                    mask = (
                        (self.df['First_Name'].str.lower() == search_term.lower()) |
                        (self.df['Last_Name'].str.lower() == search_term.lower()) |
                        (self.df['Full_Name'].str.lower() == search_term.lower())
                    )
                else:
                    mask = (
                        self.df['First_Name'].str.contains(search_term, case=False, na=False) |
                        self.df['Last_Name'].str.contains(search_term, case=False, na=False) |
                        self.df['Full_Name'].str.contains(search_term, case=False, na=False)
                    )
            else:
                print("✗ No name columns found in data")
                return pd.DataFrame()
        
        return self.df[mask]
    
    def search_by_email(self, email):
        """
        Search for associates by email address
        Handles both @walmart.com and @wal-mart.com domains
        
        Args:
            email: Email address to search for (can be partial)
        
        Returns:
            DataFrame with matching records
        """
        if self.df is None or not self.email_column:
            return None
        
        # Normalize the search term to handle both email formats
        email_base = email.lower().replace('@walmart.com', '').replace('@wal-mart.com', '')
        
        # Search using the base email username
        mask = self.df[self.email_column].str.lower().str.contains(email_base, na=False)
        return self.df[mask]
    

    
    def search_multiple(self, search_terms):
        """
        Search for multiple associates at once
        
        Args:
            search_terms: List of names or emails to search for
        
        Returns:
            DataFrame with all matching records
        """
        all_results = []
        
        for term in search_terms:
            # Try email first if it contains @
            if '@' in term:
                results = self.search_by_email(term)
            else:
                results = self.search_by_name(term)
            
            if len(results) > 0:
                all_results.append(results)
        
        if all_results:
            combined = pd.concat(all_results)
            # Drop duplicates using the appropriate ID column
            if self.id_column:
                return combined.drop_duplicates(subset=[self.id_column])
            else:
                return combined.drop_duplicates()
        return pd.DataFrame()
    
    def display_results(self, results, show_all_fields=False):
        """
        Display search results in a formatted way
        
        Args:
            results: DataFrame with search results
            show_all_fields: If True, show all available fields
        """
        if results is None or len(results) == 0:
            print("\n✗ No results found")
            return
        
        print(f"\n✓ Found {len(results)} result(s):\n")
        print("=" * 100)
        
        for idx, row in results.iterrows():
            # Display name
            if self.name_column and pd.notna(row.get(self.name_column)):
                print(f"\n📋 {row[self.name_column]}")
            elif 'First_Name' in row and 'Last_Name' in row:
                print(f"\n📋 {row['First_Name']} {row['Last_Name']}")
            
            # Display ID
            if self.id_column and pd.notna(row.get(self.id_column)):
                print(f"   User ID: {row[self.id_column]}")
            
            # Display email
            if self.email_column and pd.notna(row.get(self.email_column)):
                print(f"   Email: {row[self.email_column]}")
            
            if show_all_fields:
                # Show additional fields if available
                for col in row.index:
                    if col not in [self.name_column, self.id_column, self.email_column]:
                        if pd.notna(row[col]) and str(row[col]).strip():
                            print(f"   {col}: {row[col]}")
        
        print("\n" + "=" * 100)
    
    def export_results(self, results, output_file="lookup_results.csv"):
        """
        Export search results to CSV
        
        Args:
            results: DataFrame with search results
            output_file: Name of output file
        """
        if results is None or len(results) == 0:
            print("\n✗ No results to export")
            return
        
        results.to_csv(output_file, index=False)
        print(f"\n✓ Exported {len(results)} record(s) to {output_file}")


def main():
    """Interactive command-line interface for user lookup"""
    print("\n" + "=" * 100)
    print("USER ID LOOKUP TOOL")
    print("=" * 100)
    
    # Initialize the lookup tool
    lookup = UserIDLookup()
    
    if lookup.df is None:
        return
    
    while True:
        print("\n\nOptions:")
        print("1. Search by Name")
        print("2. Search by Email")
        print("3. Search Multiple (comma-separated)")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            name = input("Enter name to search: ").strip()
            exact = input("Exact match? (y/n): ").strip().lower() == 'y'
            results = lookup.search_by_name(name, exact=exact)
            show_all = input("Show all fields? (y/n): ").strip().lower() == 'y'
            lookup.display_results(results, show_all_fields=show_all)
            
            if results is not None and len(results) > 0:
                export = input("Export results to CSV? (y/n): ").strip().lower() == 'y'
                if export:
                    filename = input("Enter filename (or press Enter for default): ").strip()
                    if not filename:
                        filename = "lookup_results.csv"
                    lookup.export_results(results, filename)
        
        elif choice == '2':
            email = input("Enter email to search: ").strip()
            results = lookup.search_by_email(email)
            show_all = input("Show all fields? (y/n): ").strip().lower() == 'y'
            lookup.display_results(results, show_all_fields=show_all)
            
            if results is not None and len(results) > 0:
                export = input("Export results to CSV? (y/n): ").strip().lower() == 'y'
                if export:
                    filename = input("Enter filename (or press Enter for default): ").strip()
                    if not filename:
                        filename = "lookup_results.csv"
                    lookup.export_results(results, filename)
        
        elif choice == '3':
            terms = input("Enter search terms (comma-separated): ").strip()
            search_list = [t.strip() for t in terms.split(',')]
            results = lookup.search_multiple(search_list)
            show_all = input("Show all fields? (y/n): ").strip().lower() == 'y'
            lookup.display_results(results, show_all_fields=show_all)
            
            if results is not None and len(results) > 0:
                export = input("Export results to CSV? (y/n): ").strip().lower() == 'y'
                if export:
                    filename = input("Enter filename (or press Enter for default): ").strip()
                    if not filename:
                        filename = "lookup_results.csv"
                    lookup.export_results(results, filename)
        
        elif choice == '4':
            print("\nGoodbye!")
            break
        
        else:
            print("\n✗ Invalid option. Please try again.")


# Quick lookup function for programmatic use
def quick_lookup(search_term, data_file=None):
    """
    Quick lookup function for single searches
    Returns list of (Name, WIN, Email) tuples
    """
    lookup = UserIDLookup(data_file)
    
    if '@' in search_term:
        results = lookup.search_by_email(search_term)
    else:
        results = lookup.search_by_name(search_term)
    
    if results is None or len(results) == 0:
        return []
    
    return [(f"{row['First_Name']} {row['Last_Name']}", row['WIN'], row['Email']) 
            for _, row in results.iterrows()]


if __name__ == "__main__":
    main()
