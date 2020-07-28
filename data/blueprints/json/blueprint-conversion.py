import os
import re
import json
from pprint import pprint


def parse_string(string):
    quantity_number = int(string[:string.find(' x ')].replace(',', '').strip())
    item_name = string[string.rfind(' x ') + 2:].strip()
    return item_name, quantity_number


if __name__ == "__main__":

    blueprints = {}
    number = re.compile('^\d*$')

    for filename in os.listdir('..'):
        if filename == 'json':
            continue
        with open('../' + filename) as blueprint_file:
            first_line = next(blueprint_file)

            # Note that this code directly mirrors whats found in Blueprint.py
            if not number.match(first_line):
                blueprint_file.seek(0)
                num_runs = 1
            else:
                num_runs = int(first_line)

            name_line = next(blueprint_file)
            blueprint_name, quantity = parse_string(name_line)

            print(f"Processing {blueprint_name}")

            blueprints.setdefault(blueprint_name, {})
            blueprints[blueprint_name].setdefault("runs", num_runs)
            blueprints[blueprint_name].setdefault("mats", {})

            for line in blueprint_file:
                name, quantity = parse_string(line)
                blueprints[blueprint_name]["mats"].setdefault(name, quantity)

    pprint(blueprints)

    with open('./blueprints.json', 'w') as blueprint_json:
        blueprint_json.write(json.dumps(blueprints, indent=4, sort_keys=True))
