import json
from src.config import *
from pprint import pprint

if __name__ == "__main__":

    invention_json = json.load(open(INVENTION_PATH))
    blueprints_json = json.load(open(BLUEPRINTS_PATH))

    for item_name, invention_data in invention_json.items():
        blueprints_json[item_name].setdefault('invention', invention_data)

    with open(BLUEPRINTS_PATH, 'w') as blueprints:
        blueprints.write(json.dumps(blueprints_json, indent=4, sort_keys=True))
