import csv
import json
import pandas

def generate_lookup_dicts():

    name_id_dict = {}
    id_name_dict = {}

    with open('./data/invTypes.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:

            name = line['TYPENAME'].strip()
            item_id = line['TYPEID'].strip()

            name_id_dict.setdefault(name, item_id)
            id_name_dict.setdefault(item_id, name)


    with open('./data/dicts/name_to_id.json', 'w+') as outfile:
        json.dump(name_id_dict, outfile)

    with open('./data/dicts/id_to_name.json', 'w+') as outfile:
        json.dump(id_name_dict, outfile)

def convertXLStoCSVandFilter():

    xls_data = pandas.read_excel('invTypes.xls', 'Sheet1', index_col='TYPEID')
    xls_data = xls_data[['TYPENAME', 'VOLUME']]
    xls_data.to_csv('invTypes.csv')