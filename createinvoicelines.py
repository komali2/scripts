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

invoices_csv = sys.argv[1] if len(sys.argv) > 1 else None
invoices_lines_csv = sys.argv[2] if len(sys.argv) > 2 else None

# Check if both arguments were provided
if not invoices_csv or not invoices_lines_csv:
    print("Error: Both input and output CSV paths must be provided.")
    sys.exit(1)

# Check if the input CSV path is valid
if not is_valid_file(invoices_csv):
    print(f"Error: The input CSV path '{invoices_csv}' is not a valid file.")
    sys.exit(1)


# Check if the directory for the output CSV is valid
if not is_valid_output_directory(invoices_lines_csv):
    print(f"Error: The directory for the output CSV path '{invoices_lines_csv}' does not exist.")
    sys.exit(1)


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

customer_type = {
    'Dine In': 14,
    'take out': 15,
}

bank_account = {
    'line pay(LINE Pay physical store payment module)': 3,
    'Cash(Cash payment module)': 2,
}

with open(invoices_csv, 'r', newline='') as invoicescsv:
    with open(invoices_lines_csv, 'w', newline='') as csvout:
        invoicereader = csv.reader(invoicescsv, delimiter=',', quotechar='|')
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
        next(invoicereader, None)
        for row in invoicereader:
            items = row[24].split(',')
            for item in items:
                print(item)
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
                    # 'Type of line (0=product/ 1=service) (fd.product_type)'
                    0,
                    # 'Start Date (fd.date_start)',
                    row[3],
                    # 'End Date (fd.date_end)',
                    row[3],
                    # 'Unit (fd.fk_unit)',
                    None,
                ])
