import csv
import sys
import os
import datetime

# Function to check if the path is a valid file
def is_valid_file(path):
    return os.path.isfile(path) and path.endswith('.csv')


invoices_csv = sys.argv[1] if len(sys.argv) > 1 else None

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
    "module": None,
    "entity": "1",
    "import_key": None,
    "array_options": [],
    "array_languages": None,
    "contacts_ids": [],
    "linked_objects": [],
    "linkedObjectsIds": None,
    "oldref": None,
    "fk_project": None,
    "contact_id": None,
    "user": None,
    "origin": None,
    "origin_id": None,
    "ref": "TESTTEST",
    "ref_ext": "TESTTEST",
    "statut": "2",
    "status": "2",
    "country_id": None,
    "country_code": None,
    "state_id": None,
    "region_id": None,
    "mode_reglement_id": "6",
    "cond_reglement_id": "1",
    "demand_reason_id": None,
    "transport_mode_id": None,
    "shipping_method_id": None,
    "shipping_method": None,
    "multicurrency_code": None,
    "multicurrency_tx": "1.00000000",
    "model_pdf": "sponge",
    "last_main_doc": "",
    "fk_bank": None,
    "fk_account": "3",
    "note_public": "",
    "note_private": "--＊8800",
    "total_ht": "1.00000000",
    "total_tva": "0.00000000",
    "total_localtax1": "0.00000000",
    "total_localtax2": "0.00000000",
    "total_ttc": "1.00000000",
    "lines": [
    ],
    "name": None,
    "lastname": None,
    "firstname": None,
    "civility_id": None,
    "date_creation": 1699205524,
    "date_validation": 1699142400,
    "date_modification": 1700646892,
    "date_update": None,
    "date_cloture": None,
    "user_author": "4",
    "user_creation": None,
    "user_creation_id": None,
    "user_valid": None,
    "user_validation": None,
    "user_validation_id": None,
    "user_closing_id": None,
    "user_modification": None,
    "user_modification_id": None,
    "specimen": 0,
    "labelStatus": None,
    "showphoto_on_popup": None,
    "nb": [],
    "output": None,
    "extraparams": [],
    "type": "0",
    "subtype": None,
    "totalpaid": 590,
    "totaldeposits": None,
    "totalcreditnotes": None,
    "sumpayed": "590.00000000",
    "sumpayed_multicurrency": None,
    "sumdeposit": None,
    "sumdeposit_multicurrency": None,
    "sumcreditnote": None,
    "sumcreditnote_multicurrency": None,
    "remaintopay": "0",
    "fk_incoterms": None,
    "label_incoterms": None,
    "location_incoterms": None,
    "brouillon": None,
    "socid": "15",
    "fk_user_author": "4",
    "fk_user_valid": None,
    "fk_user_modif": None,
    "date": 1699142400,
    "datem": 1700646892,
    "date_livraison": None,
    "delivery_date": None,
    "ref_client": None,
    "ref_customer": None,
    "remise_absolue": "0",
    "remise_percent": "0",
    "revenuestamp": "0.00000000",
    "resteapayer": None,
    "close_code": None,
    "close_note": None,
    "paye": "1",
    "module_source": None,
    "pos_source": None,
    "fk_fac_rec_source": None,
    "fk_facture_source": None,
    "date_lim_reglement": 1699142400,
    "cond_reglement_code": "RECEP",
    "cond_reglement_doc": "Due upon receipt",
    "mode_reglement_code": "CB",
    "line": None,
    "fac_rec": None,
    "date_pointoftax": "",
    "fk_multicurrency": None,
    "multicurrency_total_ht": "0.00000000",
    "multicurrency_total_tva": "0.00000000",
    "multicurrency_total_ttc": "0.00000000",
    "situation_cycle_ref": None,
    "situation_counter": None,
    "situation_final": None,
    "tab_previous_situation_invoice": [],
    "tab_next_situation_invoice": [],
    "retained_warranty": None,
    "retained_warranty_date_limit": "",
    "retained_warranty_fk_cond_reglement": None
}

blank_line = {
        "module": None,
        "id": "274",
        "entity": None,
        "import_key": None,
        "array_options": [],
        "array_languages": None,
        "contacts_ids": None,
        "linked_objects": None,
        "linkedObjectsIds": None,
        "oldref": None,
        "origin": None,
        "origin_id": None,
        "ref": "Bacon_Egg_Cheese_Biscuit",
        "ref_ext": None,
        "statut": None,
        "status": None,
        "state_id": None,
        "region_id": None,
        "demand_reason_id": None,
        "transport_mode_id": None,
        "shipping_method": None,
        "multicurrency_tx": None,
        "last_main_doc": None,
        "fk_bank": None,
        "fk_account": None,
        "total_ht": "250.00000000",
        "total_tva": "0.00000000",
        "total_localtax1": "0.00000000",
        "total_localtax2": "0.00000000",
        "total_ttc": "250.00000000",
        "lines": None,
        "date_creation": None,
        "date_validation": None,
        "date_modification": None,
        "date_update": None,
        "date_cloture": None,
        "user_author": None,
        "user_creation": None,
        "user_creation_id": None,
        "user_valid": None,
        "user_validation": None,
        "user_validation_id": None,
        "user_closing_id": None,
        "user_modification": None,
        "user_modification_id": None,
        "specimen": 0,
        "labelStatus": None,
        "showphoto_on_popup": None,
        "nb": [],
        "output": None,
        "extraparams": [],
        "rowid": "274",
        "fk_unit": None,
        "date_debut_prevue": None,
        "date_debut_reel": None,
        "date_fin_prevue": None,
        "date_fin_reel": None,
        "weight": None,
        "weight_units": None,
        "width": None,
        "width_units": None,
        "height": None,
        "height_units": None,
        "length": None,
        "length_units": None,
        "surface": None,
        "surface_units": None,
        "volume": None,
        "volume_units": None,
        "multilangs": None,
        "product_type": "0",
        "fk_product": "2",
        "desc": "Bacon Egg and Cheese $250.0",
        "description": "Bacon Egg and Cheese $250.0",
        "product": None,
        "product_ref": "Bacon_Egg_Cheese_Biscuit",
        "product_label": "Bacon Egg Cheese Biscuit",
        "product_barcode": None,
        "product_desc": "",
        "fk_product_type": "0",
        "qty": "1",
        "duree": None,
        "remise_percent": "0",
        "info_bits": "0",
        "special_code": "0",
        "subprice": None,
        "tva_tx": "0.0000",
        "label": None,
        "libelle": "Bacon Egg Cheese Biscuit",
        "price": None,
        "vat_src_code": None,
        "localtax1_tx": "0.0000",
        "localtax2_tx": "0.0000",
        "localtax1_type": None,
        "localtax2_type": None,
        "remise": None,
        "date_start_fill": None,
        "date_end_fill": None,
        "buy_price_ht": None,
        "buyprice": None,
        "pa_ht": "0.00000000",
        "marge_tx": "",
        "marque_tx": "",
        "multicurrency_subprice": "0.00000000",
        "multicurrency_total_ht": "0.00000000",
        "multicurrency_total_tva": "0.00000000",
        "multicurrency_total_ttc": "0.00000000",
        "fk_user_author": None,
        "fk_user_modif": None,
        "fk_accounting_account": "0",
        "fk_facture": "731",
        "fk_parent_line": None,
        "fk_remise_except": None,
        "rang": "0",
        "fk_fournprice": None,
        "fk_code_ventilation": 0,
        "date_start": 1699205524,
        "date_end": 1699205524,
        "situation_percent": "100",
        "fk_prev_id": None,
        "code_ventilation": "0"
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
        invoice_time = datetime.datetime.strptime(
            row[3], "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        current_invoice['date'] = invoice_time
        current_invoice['datem'] = invoice_time
        current_invoice['date_lim_reglement'] = invoice_time
        current_invoice['date_validation'] = invoice_time
        current_invoice['sumpayed'] = "0"
        current_invoice['paye'] = "1"
        current_invoice['total_ttc'] = row[12]
        current_invoice['total_ht'] = row[12]
        current_invoice['status'] = "1"
        current_invoice[''] = "1"
        current_invoice[''] = "1"
        current_invoice[''] = "1"
        items = row[20].split(',')
        for item in items:
            item_separated = item.split('$')
            item_name = item_separated[0].strip()
            item_price = item_separated[1]
            current_line = blank_line.copy()
            current_line['fk_facture'] = row[1]
            current_line['fk_product'] = product_map.get(item_name)
            current_line['description'] = item
            current_line['desc'] = item
            current_line['qty'] = 1
            current_line['total_ttc'] = item_price
            current_line['total_ht'] = item_price
            current_line['date_start'] = invoice_time
            current_line['date_end'] = invoice_time
            current_invoice['lines'].append(current_line)
            invoices_to_send.append(current_invoice)

print(invoices_to_send)
