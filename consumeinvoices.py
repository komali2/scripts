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
invoices_csv = sys.argv[2] if len(sys.argv) > 2 else None

# Check if both arguments were provided
if not input_csv or not invoices_csv:
    print("Error: Both input and output CSV paths must be provided.")
    sys.exit(1)

# Check if the input CSV path is valid
if not is_valid_file(input_csv):
    print(f"Error: The input CSV path '{input_csv}' is not a valid file.")
    sys.exit(1)


# Check if the directory for the output CSV is valid
if not is_valid_output_directory(invoices_csv):
    print(f"Error: The directory for the output CSV path '{invoices_csv}' does not exist.")
    sys.exit(1)
# Check if the directory for the output CSV is valid

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
with open(input_csv, newline='') as csvin:
    with open(invoices_csv, 'a+', newline='') as invoicescsv:
        inreader = csv.reader(csvin, delimiter=',')
        invoicewriter = csv.writer(
            invoicescsv,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )
        invoicewriter.writerow([
            'Invoice ref.* (f.ref)',
            'Ref. extern (f.ref_ext)',
            'Customer* (f.fk_soc)',
            'Invoice creation date (f.datec)',
            'Invoice date (f.datef)',
            'Validation Date (f.date_valid)',
            'Invoice paid (f.paye)',
            'RemisePercent (f.remise_percent)',
            'RemiseAbsolue (f.remise_absolue)',
            'Remise (f.remise)',
            'Total tax (f.total_tva)',
            'Total (excl. tax) (f.total_ht)',
            'Total (inc. tax) (f.total_ttc)',
            'Invoice status (f.fk_statut)',
            'Modifier Id (f.fk_user_modif)',
            'Validator Id (f.fk_user_valid)',
            'Closer Id (f.fk_user_closing)',
            'Invoice Source Id (f.fk_facture_source)',
            'Project Id (f.fk_projet)',
            'Bank Account (f.fk_account)',
            'Currency* (f.fk_currency)',
            'Payment Condition (f.fk_cond_reglement)',
            'Payment Mode (f.fk_mode_reglement)',
            'Payment due on (f.date_lim_reglement)',
            'Invoice note (f.note_public)',
            'Doc template (f.model_pdf)',
        ])
        next(inreader, None)
        for row in inreader:
            invoicewriter.writerow([
                # Receipt number > 'Invoice ref.* (f.ref)',
                row[1],
                # Receipt number > 'Ref. extern (f.ref_ext)',
                row[1],
                # Order Type > 'Customer* (f.fk_soc)',
                customer_type.get(row[7].strip(), None),
                # payment time > 'Invoice creation date (f.datec)',
                row[3],
                # payment time > 'Invoice date (f.datef)',
                row[3],
                # payment time > 'Validation Date (f.date_valid)',
                row[3],
                # 'Invoice paid (f.paye)',
                1,
                # 'RemisePercent (f.remise_percent)',
                0,
                # 'RemiseAbsolue (f.remise_absolue)',
                0,
                # 'Remise (f.remise)',
                0,
                # 'Total tax (f.total_tva)',
                0,
                # payment amount > 'Total (excl. tax) (f.total_ht)',
                row[12],
                # payment amount >'Total (inc. tax) (f.total_ttc)',
                row[12],
                # 'Invoice status (f.fk_statut)',
                1,
                # 'Modifier Id (f.fk_user_modif)',
                None,
                # 'Validator Id (f.fk_user_valid)',
                None,
                # 'Closer Id (f.fk_user_closing)',
                None,
                # 'Invoice Source Id (f.fk_facture_source)',
                None,
                # 'Project Id (f.fk_projet)',
                None,
                # 'Bank Account (f.fk_account)',
                bank_account.get(row[13].strip(), None),
                # 'Currency* (f.fk_currency)',
                'TWD',
                # 'Payment Condition (f.fk_cond_reglement)',
                'RECEP',
                # 'Payment Mode (f.fk_mode_reglement)',
                # Even line pay is cash because it's a direct transfer
                4,
                # payment time > 'Payment due on (f.date_lim_reglement)',
                row[3],
                # items > 'Invoice note (f.note_public)',
                row[20],
                # 'Doc template (f.model_pdf)',
                'sponge',
            ])
