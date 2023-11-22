import csv
import sys
import os

# Function to check if the path is a valid file
def is_valid_file(path):
    return os.path.isfile(path) and path.endswith('.csv')

# Function to check if the path is a valid path for writing
def is_valid_output_path(path):
    # Check if the path ends with '.csv'
    if not path.endswith('.csv'):
        return False
    # Check if the directory of the path exists, if not, it's not a valid output path
    directory = os.path.dirname(path)
    return os.path.exists(directory) if directory else True

# Function to check if the directory of the output path exists or if the path is at the root directory
def is_valid_output_directory(path):
    directory = os.path.dirname(path)
    # If there's no directory part, we assume current directory which is valid
    return os.path.exists(directory) or not directory

input_csv = sys.argv[1] if len(sys.argv) > 1 else None
output_csv = sys.argv[2] if len(sys.argv) > 2 else None

# Check if both arguments were provided
if not input_csv or not output_csv:
    print("Error: Both input and output CSV paths must be provided.")
    sys.exit(1)

# Check if the input CSV path is valid
if not is_valid_file(input_csv):
    print(f"Error: The input CSV path '{input_csv}' is not a valid file.")
    sys.exit(1)


# Check if the directory for the output CSV is valid
if not is_valid_output_directory(output_csv):
    print(f"Error: The directory for the output CSV path '{output_csv}' does not exist.")
    sys.exit(1)



# If both checks pass, proceed with the rest of the script
print(f"Input CSV: {input_csv}")
print(f"Output CSV: {output_csv}")

product_map = {
    'Bacon Egg and Cheese': 2,
    'Chicken Tender Box': 31,
    'Original Chicken Biscuit': 1,
    'Combo Meal': 44,
    'Bundaberg': 43,
    'Soda': 42,
    'Sweet Tea': 41,
    'Fries': 4,
    'Biscuit': 3,
    'Chicken Tenders': 32,
}

with open(input_csv, newline='') as csvin:
    with open(output_csv, 'w', newline='') as csvout:
        inreader = csv.reader(csvin, delimiter=',')
        outwriter = csv.writer(
            csvout,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )
        outwriter.writerow([
            'Invoice ref.* (fd.fk_facture)',
            'FacParentLine (fd.fk_parent_line)',
            'IdProduct (fd.fk_product)',
            'Label (fd.label)',
            'Description of line* (fd.description)',
            'Vat Source Code (fd.vat_src_code)',
            'VAT Rate of line* (fd.tva_tx)',
            'Quantity for line (fd.qty)',
            'Reduc. (%) (fd.remise_percent)',
            'Amount excl. tax for line (fd.total_ht)',
            'Amount of VAT for line (fd.total_tva)',
            'Amount with tax for line (fd.total_ttc)',
            'Type of line (0=product/ 1=service) (fd.product_type)',
            'Start Date (fd.date_start)',
            'End Date (fd.date_end)',
            'Unit (fd.fk_unit)',
        ])
        next(inreader, None)
        for row in inreader:
            items = row[26].split(',')
            for item in items:
                item_separated = item.split('$')
                item_name = item_separated[0].strip()
                item_price = item_separated[1]
                outwriter.writerow([
                    # Invoice ref.* (fd.fk_facture)
                    row[1],
                    # FacParentLine (fd.fk_parent_line)
                    None,
                    # 'IdProduct (fd.fk_product)',
                    product_map.get(item_name, None),
                    # Label (fd.label)
                    None,
                    # 'Description of line* (fd.description)',
                    item,
                    # 'Vat Source Code (fd.vat_src_code)',
                    None,
                    # 'VAT Rate of line* (fd.tva_tx)',
                    0,
                    # 'Quantity for line (fd.qty)',
                    1,
                    # 'Reduc. (%) (fd.remise_percent)',
                    0,
                    # 'Amount excl. tax for line (fd.total_ht)',
                    item_price,
                    # 'Amount of VAT for line (fd.total_tva)',
                    0,
                    # 'Amount with tax for line (fd.total_ttc)',
                    item_price,
                    # 'Type of line (0=product/ 1=service) (fd.product_type)',
                    0,
                    # 'Start Date (fd.date_start)',
                    row[5],
                    # 'End Date (fd.date_end)',
                    row[5],
                    # 'Unit (fd.fk_unit)',
                    None,
                ])
