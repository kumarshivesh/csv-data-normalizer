import os
from decimal import Decimal
from datetime import datetime

# First, make sure we're importing from the correct file
try:
    from csv_normalizer import CSVNormalizer
except ImportError:
    # If the file is named differently
    print("Warning: Unable to import from csv_normalizer.py.")
    print("Make sure the file is named correctly and in the same directory.")
    exit(1)

def print_normalized_data(data, max_rows=None):
    """Print the normalized data in a readable format"""
    if not data:
        print("No data found")
        return
    
    # Print only the specified number of rows
    for i, row in enumerate(data[:max_rows] if max_rows else data):
        print(f"\nRow {i+1}:")
        for key, value in row.items():
            # Format the value based on its type
            if isinstance(value, Decimal):
                formatted_value = f"Decimal('{value}')"
            elif isinstance(value, datetime):
                formatted_value = f"datetime({value.year}, {value.month}, {value.day})"
            else:
                formatted_value = f"'{value}'" if isinstance(value, str) else str(value)
            
            print(f"  '{key}': {formatted_value}")

def create_test_files():
    """Create the test files defined in the assignment"""
    # Test1.csv - Comma-delimited
    test1_content = 'Transaction_Date,Description,Amount,Currency,Status\n'
    test1_content += '2024-01-15,Office Supplies,"1,234.56",USD,COMPLETED\n'
    test1_content += '2024-01-16,Software License,"2,500.00",USD,pending\n'
    test1_content += '2024-01-17,"Lunch, Meeting","1,750.50",USD,COMPLETED'
    
    # Test2.csv - Semicolon-delimited
    test2_content = 'Transaction_Date;Description;Amount;Currency;Status\n'
    test2_content += '2024-01-15;Office Supplies;1.234,56;EUR;COMPLETED\n'
    test2_content += '2024-01-16;Software License;2.500,00;EUR;PENDING\n'
    test2_content += '2024-01-17;Lunch Meeting;1.750,50;EUR;completed'
    
    # Test3.csv - Pipe-delimited
    test3_content = 'Transaction_Date|Description|Amount|Currency|Status\n'
    test3_content += '2024-01-15|Office Supplies|1,234.56|USD|COMPLETED\n'
    test3_content += '2024-01-16|Software, License|2,500.00|USD|PENDING\n'
    test3_content += '2024-01-17|Lunch Meeting|1,750.50|USD|completed'
    
    # No_header.csv - No headers
    no_header_content = '2024-01-15,Office Supplies,"1,234.56",USD,COMPLETED\n'
    no_header_content += '2024-01-16,Software License,"2,500.00",USD,PENDING'
    
    # Write the files
    files_to_create = [
        ("test1.csv", test1_content),
        ("test2.csv", test2_content),
        ("test3.csv", test3_content),
        ("no_header.csv", no_header_content)
    ]
    
    for file_name, content in files_to_create:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {file_name}")

def main():
    # Create sample test files if they don't exist
    create_test_files()
    
    normalizer = CSVNormalizer()
    
    # Test with comma-delimited file
    print("\n=== Processing test1.csv (Comma-delimited) ===")
    test1_result = normalizer.normalize_csv("test1.csv")
    print_normalized_data(test1_result, max_rows=3)
    
    # Test with semicolon-delimited file
    print("\n=== Processing test2.csv (Semicolon-delimited) ===")
    test2_result = normalizer.normalize_csv("test2.csv")
    print_normalized_data(test2_result, max_rows=3)
    
    # Test with pipe-delimited file
    print("\n=== Processing test3.csv (Pipe-delimited) ===")
    test3_result = normalizer.normalize_csv("test3.csv")
    print_normalized_data(test3_result, max_rows=3)
    
    # Test with file without headers
    print("\n=== Processing no_header.csv (No Headers) ===")
    no_header_result = normalizer.normalize_csv("no_header.csv")
    print_normalized_data(no_header_result, max_rows=2)
    
    # Print delimiters detected
    print("\n=== Delimiter Detection ===")
    for file_name in ["test1.csv", "test2.csv", "test3.csv", "no_header.csv"]:
        if os.path.exists(file_name):
            delimiter = normalizer.detect_delimiter(file_name)
            print(f"{file_name}: '{delimiter}'")

if __name__ == "__main__":
    main()