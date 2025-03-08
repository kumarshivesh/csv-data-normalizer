# CSV Data Normalizer
A Python utility for normalizing CSV data from various formats into a standardized schema.

## Overview
This tool automatically processes CSV files with different delimiters and normalizes the data into a consistent format. It handles various challenges such as:

- Auto-detecting delimiters (comma, semicolon, pipe)
- Handling quoted fields with delimiters inside them
- Processing different number formats (US and European)
- Normalizing column names to snake_case
- Standardizing date formats, number representations, and text case
- Supporting files with or without headers

## Features

**Delimiter Auto-detection**: Automatically detects if a file uses commas, semicolons, or pipes as delimiters

**Smart Parsing**: Correctly handles delimiters within quoted fields

**Number Format Handling**:

- US format: `1,234.56` → `1234.56`
- European format: `1.234,56` → `1234.56`


**Data Normalization**:

- Column names to snake_case
- Dates to YYYY-MM-DD format
- Status values to lowercase


**Headerless Files**: Process files without headers using a configurable column mapping

## Target Schema

The normalizer converts data to the following schema:

| Field            | Type     | Description                  |
|------------------|----------|------------------------------|
| transaction_date | datetime | Date in YYYY-MM-DD format    |
| description      | str      | Text description             |
| amount           | decimal  | Numeric value                |
| currency         | str      | 3-letter currency code       |
| status           | str      | Lowercase status             |

## Installation

```bash
git clone https://github.com/kumarshivesh/csv-data-normalizer.git
cd csv-data-normalizer
```

No additional dependencies required beyond the Python standard library.

## Usage
```python

from csv_normalizer import CSVNormalizer

# Create a normalizer
normalizer = CSVNormalizer()

# Process a CSV file
normalized_data = normalizer.normalize_csv("your_file.csv")

# Print the normalized data
for row in normalized_data:
    print(row)
```

## Example Output
```
{
    'transaction_date': datetime(2024, 1, 15),
    'description': 'Office Supplies',
    'amount': Decimal('1234.56'),
    'currency': 'USD',
    'status': 'completed'
}
```

## Testing
Run the test script to see the normalizer in action:
```bash
python test_normalizer.py
```

This will create sample test files with different formats and process them to demonstrate the normalizer's capabilities.


## Sample Files
The test script creates and processes the following sample files:

- **test1.csv** - Comma-delimited with US number format
- **test2.csv** - Semicolon-delimited with European number format
- **test3.csv** - Pipe-delimited with US number format
- **no_header.csv** - File without headers


