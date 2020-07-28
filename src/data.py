import csv
import json
import pandas
import os
from src.config import *

def generate_lookup_dicts():
    name_id_dict = {}
    id_name_dict = {}

    with open(INVTYPES_CSV) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            name = line['TYPENAME'].strip()
            item_id = line['TYPEID'].strip()

            name_id_dict.setdefault(name, item_id)
            id_name_dict.setdefault(item_id, name)

    os.makedirs(DICTS_PATH)

    with open(NAME_TO_ID_JSON, 'w+') as outfile:
        json.dump(name_id_dict, outfile)

    with open(ID_TO_NAME_JSON, 'w+') as outfile:
        json.dump(id_name_dict, outfile)


def convertXLStoCSVandFilter():
    xls_data = pandas.read_excel(INVTYPES_XLS, 'Sheet1', index_col='TYPEID')
    xls_data = xls_data[['TYPENAME', 'VOLUME']]
    xls_data.to_csv(INVTYPES_CSV)


if __name__ == "__main__":
    convertXLStoCSVandFilter()
    generate_lookup_dicts()
