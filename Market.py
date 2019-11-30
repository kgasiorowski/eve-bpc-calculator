import requests
from enum import Enum
import json

JITA = 30000142

id_to_name = None
name_to_id = None

market_cache = {}

class Mode(Enum):
    BUY = ('buy', 'max')
    SELL = ('sell', 'min')


def load_dicts():
    global id_to_name
    global name_to_id

    if id_to_name is None:
        with open('./data/dicts/id_to_name.json') as infile:
            id_to_name = json.load(infile)

    if name_to_id is None:
        with open('./data/dicts/name_to_id.json') as infile:
            name_to_id = json.load(infile)


def get_id_by_name(name):

    load_dicts()
    return name_to_id[name]


def get_name_by_id(item_id):

    load_dicts()
    return id_to_name[item_id]


def get_market_attr_by_id(itemid, mode):

    global market_cache

    if itemid not in market_cache:
        market_cache[itemid] = {}

    if mode not in market_cache[itemid]:

        URL = r'http://api.evemarketer.com/ec/marketstat/json'
        PARAMS = {'typeid': itemid,
                  'usesystem': JITA}

        json_response = requests.get(URL, PARAMS).json()

        market_cache[itemid][mode] = [response[mode.value[0]][mode.value[1]] for response in json_response]

    return market_cache[itemid][mode]


def get_market_attr_by_name(name, mode):

    return get_market_attr_by_id(get_id_by_name(name), mode)
