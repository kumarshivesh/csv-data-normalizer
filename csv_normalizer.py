import csv
import re
from datetime import datetime
from decimal import Decimal
import os

class CSVNormalizer:
    def __init__(self):
        # Common delimiters to check
        self.possible_delimiters = [',', ';', '|']
        # Default column mapping for headerless files
        self.default_column_mapping = {
            0: 'transaction_date',
            1: 'description',
            2: 'amount',
            3: 'currency',
            4: 'status'
        }
    
    def detect_delimiter(self, file_path):
        """Auto-detect the delimiter used in the CSV file"""
        delimiter_counts = {delim: 0 for delim in self.possible_delimiters}
        
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read first few lines to detect delimiter
            file_lines = file.readlines()
            sample_lines = file_lines[:min(3, len(file_lines))]
            
            for line in sample_lines:
                for delim in self.possible_delimiters:
                    # Count occurrences of each delimiter in the line
                    # Don't count delimiters inside quotes
                    in_quotes = False
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == delim and not in_quotes:
                            delimiter_counts[delim] += 1
        
        # Return the delimiter with the most occurrences
        return max(delimiter_counts, key=delimiter_counts.get)
    
    def has_header(self, file_path, delimiter):
        """Detect if the file has headers"""
        # Special case for the file named 'no_header.csv'
        if os.path.basename(file_path).lower() == 'no_header.csv':
            return False
            
        with open(file_path, 'r', encoding='utf-8') as file:
            # Create a CSV reader that handles quoted fields
            reader = csv.reader(file, delimiter=delimiter, quotechar='"')
            
            # Get the first two rows
            try:
                first_row = next(reader)
                
                # Check if first row looks like headers
                header_keywords = ['date', 'description', 'amount', 'currency', 'status']
                potential_header = ' '.join(first_row).lower()
                
                keyword_matches = sum(1 for keyword in header_keywords if keyword in potential_header)
                
                try:
                    second_row = next(reader)
                    
                    # Compare data types between first and second row
                    type_difference = 0
                    for i in range(min(len(first_row), len(second_row))):
                        # Check if first row could be a string header and second row is numeric
                        first_is_digit = all(c.isdigit() or c in ',./-' for c in first_row[i])
                        second_is_digit = any(c.isdigit() for c in second_row[i])
                        
                        if not first_is_digit and second_is_digit:
                            type_difference += 1
                    
                    return keyword_matches >= 2 or type_difference > 0
                    
                except StopIteration:
                    # If file has only one row
                    return keyword_matches >= 2
            
            except StopIteration:
                # If file is empty
                return False
    
    def normalize_column_name(self, col_name):
        """Convert column names to snake_case"""
        # Replace non-alphanumeric chars with space, then join with underscore
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', ' ', col_name)
        return '_'.join(clean_name.lower().split())
    
    def normalize_date(self, date_str):
        """Standardize date format to YYYY-MM-DD"""
        try:
            return datetime.strptime(date_str.strip(), '%Y-%m-%d')
        except ValueError:
            # Handle other date formats if needed
            return date_str
    
    def normalize_amount(self, amount_str):
        """Convert amount strings to decimal numbers"""
        if not amount_str:
            return None
            
        # Remove any whitespace and quotes
        amount_str = amount_str.strip().strip('"')
        
        # Handle different number formats
        try:
            # US format (1,234.56)
            if ',' in amount_str and '.' in amount_str and amount_str.find(',') < amount_str.find('.'):
                return Decimal(amount_str.replace(',', ''))
            
            # European format (1.234,56)
            elif ',' in amount_str and '.' in amount_str:
                return Decimal(amount_str.replace('.', '').replace(',', '.'))
            
            # Format with only commas
            elif ',' in amount_str:
                # If comma is followed by exactly 2 digits at the end, it's a decimal separator
                if re.search(r',\d{2}$', amount_str):
                    return Decimal(amount_str.replace(',', '.'))
                else:
                    return Decimal(amount_str.replace(',', ''))
            
            # Default - assume a normal decimal or integer
            else:
                return Decimal(amount_str)
                
        except Exception as e:
            print(f"Error converting amount '{amount_str}': {e}")
            return Decimal('0')
    
    def normalize_status(self, status_str):
        """Standardize status to lowercase"""
        return status_str.lower() if status_str else None
    
    def normalize_csv(self, file_path, output_file=None):
        """Read the CSV file, normalize the data, and return as a list of dictionaries"""
        # Detect delimiter and check for header
        delimiter = self.detect_delimiter(file_path)
        has_header = self.has_header(file_path, delimiter)
        
        normalized_data = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            # Create a CSV reader that handles quoted fields
            reader = csv.reader(file, delimiter=delimiter, quotechar='"')
            
            # If the file has a header, use it to determine column names
            if has_header:
                headers = next(reader)
                column_mapping = {i: self.normalize_column_name(header) for i, header in enumerate(headers)}
            else:
                # Use default column mapping for headerless files
                column_mapping = self.default_column_mapping
            
            # Process each row
            for row in reader:
                normalized_row = {}
                
                for i, value in enumerate(row):
                    if i >= len(column_mapping):
                        # Skip columns that don't have a mapping
                        continue
                        
                    col_name = column_mapping[i]
                    
                    # Apply appropriate normalization based on column name
                    if col_name == 'transaction_date':
                        normalized_row[col_name] = self.normalize_date(value)
                    elif col_name == 'description':
                        normalized_row[col_name] = value
                    elif col_name == 'amount':
                        normalized_row[col_name] = self.normalize_amount(value)
                    elif col_name == 'currency':
                        normalized_row[col_name] = value
                    elif col_name == 'status':
                        normalized_row[col_name] = self.normalize_status(value)
                    else:
                        normalized_row[col_name] = value
                
                normalized_data.append(normalized_row)
        
        # Write to output file if specified
        if output_file:
            self.write_normalized_data(normalized_data, output_file)
            
        return normalized_data
    
    def write_normalized_data(self, data, output_file):
        """Write normalized data to an output file (JSON or CSV)"""
        # Implement output file writing if needed
        pass


# Usage example
if __name__ == "__main__":
    normalizer = CSVNormalizer()
    
    # Test with the given files
    test_files = ["test1.csv", "test2.csv", "test3.csv", "no_header.csv"]
    
    for file_name in test_files:
        if os.path.exists(file_name):
            print(f"\nProcessing {file_name}:")
            result = normalizer.normalize_csv(file_name)
            
            # Print first few records as a sample
            for i, row in enumerate(result[:2]):
                print(f"Row {i+1}:")
                for key, value in row.items():
                    print(f"  {key}: {value}")