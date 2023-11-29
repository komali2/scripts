import json
import csv
import sys
import os
import datetime
import requests

api_url = "https://"

# Function to check if the path is a valid file
def is_valid_file(path):
    return os.path.isfile(path) and path.endswith('.csv')


invoices_csv = sys.argv[1] if len(sys.argv) > 1 else None
key = sys.argv[2] if len(sys.argv) > 2 else None

# Check if both arguments were provided
if not invoices_csv:
    print("Error: input csv needs provided")
    sys.exit(1)

# Check if the input CSV path is valid
if not is_valid_file(invoices_csv):
    print(f"Error: The input CSV path '{invoices_csv}' is not a valid file.")
    sys.exit(1)

CASH = 4

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

blank_invoice = {
    "mode_reglement_id": CASH,
    "model_pdf": "sponge",
    "fk_account": "3",
    "lines": [
    ],
    "fk_user_author": "4",
    "remise_absolue": "0",
    "remise_percent": "0",
    "revenuestamp": "0.00000000",
    "cond_reglement_code": "RECEP",
    "cond_reglement_doc": "Due upon receipt",
    "mode_reglement_code": "CB",
}

blank_line = {
        "qty": "1",
}

invoices_to_send = []

with open(invoices_csv, newline='') as csvin:
    inreader = csv.reader(csvin, delimiter=',')
    next(inreader, None)
    for row in inreader:
        current_invoice = blank_invoice.copy()

        current_invoice['ref'] = row[1]
        current_invoice['ref_ext'] = row[1]
        current_invoice['socid'] = customer_type.get(row[7].strip())
        invoice_time = int(datetime.datetime.strptime(
            row[3], "%Y-%m-%d %H:%M:%S"
        ).timestamp())
        current_invoice['date'] = invoice_time
        current_invoice['datem'] = invoice_time
        current_invoice['date_lim_reglement'] = invoice_time
        current_invoice['date_validation'] = invoice_time
        current_invoice['sumpayed'] = "0"
        current_invoice['paye'] = "1"

        # 8 0s after decimal
        invoice_price = format(float(int(row[12])), f".{8}f")
        current_invoice['total_ttc'] = invoice_price
        current_invoice['total_ht'] = invoice_price
        current_invoice['totalpaid'] = invoice_price
        current_invoice['sumpaid'] = invoice_price
        current_invoice['sumpayed'] = invoice_price
        current_invoice['status'] = "1"
        current_invoice['statut'] = "1"
        # items = row[20].split(',')
        # for item in items:
        #     item_separated = item.split('$')
        #     item_name = item_separated[0].strip()
        #     item_price = str(int(float(item_separated[1])))
        #     current_line = blank_line.copy()

        #     current_line['fk_facture'] = row[1]
        #     current_line['fk_product'] = product_map.get(item_name)
        #     current_line['description'] = item
        #     current_line['desc'] = item
        #     current_line['qty'] = 1
        #     current_line['total_ttc'] = item_price
        #     current_line['total_ht'] = item_price
        #     current_line['date_start'] = invoice_time
        #     current_line['date_end'] = invoice_time
        #     current_invoice['lines'].append(current_line)
        invoices_to_send.append(current_invoice)

thing = json.dumps(invoices_to_send, indent=2)
print(thing)
