# simple CSV converter from Luzerner Kantonalbank detailed statement CSV
# to YNAB CSV import format 
# LUKB: Buchungsdatum, Valuta, Buchungstext, Details, Detail, Belastung, Gutschrift, Saldo CHF
# YNAB: Date, Payee, Memo, Outflow, Inflow

import csv
import sys
from datetime import datetime

def csv_transform(input_file, output_file, field_mapping):
    with open(input_file, 'r', encoding='ISO-8859-1') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.DictReader(infile, delimiter=';')

        next(csv_reader)
        next(csv_reader)
        
        fieldnames = list(field_mapping.values())
        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        csv_writer.writeheader()

        for row in csv_reader:
            
            print(row)
            
            if not row['Buchungstext']:
                continue
            
            if "TWINT" in row['Buchungstext']:
                row['Details'] = "TWINT " + row['Details']

            if "Wechselkurs" in row['Details']:
                row['Details'] = "Auslandsüberweisung " + row['Details']
             
            if "Ray" in row['Details']:
                row['Details'] = "Ray " + row['Details']
    
            if row.get("Buchungsdatum"):
                date_str = row['Buchungsdatum']
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                row['Buchungsdatum'] = date_obj.strftime('%m/%d/%Y')
                
            new_row = {new_field: row[old_field] for old_field, new_field in field_mapping.items()}
            new_row['Payee'] = row['Details'].split(" ")[0] + " " + row['Details'].split(" ")[1]

            csv_writer.writerow(new_row)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    field_mapping = {
        "Buchungsdatum": "Date",
        "Belastung": "Outflow",
        "Gutschrift": "Inflow",
        "Buchungstext": "Payee", # dummy mapping
        "Details": "Memo"
    }

    csv_transform(input_file, output_file, field_mapping)
