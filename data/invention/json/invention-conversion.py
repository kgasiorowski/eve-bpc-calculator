import os
import re
import json
from pprint import pprint


def parse_string(string):
    quantity_number = int(string[:string.find(' x ')].replace(',', '').strip())
    item_name = string[string.rfind(' x ') + 2:].strip()
    return item_name, quantity_number


if __name__ == "__main__":

    invention = {}
    number = re.compile('^\d*$')

    for filename in os.listdir('..'):
        if filename == 'json':
            continue

        invention.setdefault(filename, {})

        with open('../' + filename) as invention_file:
            base_invention_chance, \
            invented_runs, \
            invented_ME, \
            invented_TE = (float(token) for token in next(invention_file).strip().split())

            invention[filename].setdefault("base_invention_chance", base_invention_chance)
            invention[filename].setdefault("invented_runs", invented_runs)
            invention[filename].setdefault("invented_ME", invented_ME)
            invention[filename].setdefault("invented_TE", invented_TE)

            datacore1 = parse_string(next(invention_file).strip())[0]
            datacore2 = parse_string(next(invention_file).strip())[0]

            invention[filename].setdefault("datacore1", datacore1)
            invention[filename].setdefault("datacore2", datacore2)

    pprint(invention)

    with open('./invention.json', 'w') as invention_json:
        invention_json.write(json.dumps(invention, indent=4, sort_keys=True))
