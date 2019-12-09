import requests
from enum import Enum
import json
from time import time

JITA = 30000142

id_to_name = None
name_to_id = None
market_cache = None

class Mode(Enum):
    BUYMAX = ('buy', 'max')
    SELLMIN = ('sell', 'min')

    SELLMAX = ('sell', 'max')
    BUYMIN = ('buy', 'min')

    BUYAVG = ('buy', 'avg')
    SELLAVG = ('sell', 'avg')


def load_dicts():
    global id_to_name
    global name_to_id

    if id_to_name is None:
        with open('./data/dicts/id_to_name.json') as infile:
            id_to_name = json.load(infile)

    if name_to_id is None:
        with open('./data/dicts/name_to_id.json') as infile:
            name_to_id = json.load(infile)


def load_cache():
    global market_cache

    if market_cache is None:
        with open('./data/cache/market_cache.json') as cache_file:
            market_cache = json.load(cache_file)

    return market_cache

def save_cache():

    with open('./data/cache/market_cache.json', 'w') as cache_file:
        json.dump(market_cache, cache_file)

def get_id_by_name(name):

    load_dicts()
    return name_to_id[name]


def get_name_by_id(item_id):

    load_dicts()
    return id_to_name[item_id]


def get_market_attr_by_id(itemid, mode):

    load_cache()

    try:

        current_time = time()
        difference = current_time - market_cache[itemid][mode.value[0]][mode.value[1]]['time']

        if difference < 3600:
            return market_cache[itemid][mode.value[0]][mode.value[1]]['val']
        else:
            raise KeyError

    except KeyError:

        URL = r'http://api.evemarketer.com/ec/marketstat/json'
        PARAMS = {'typeid': itemid,
                  'usesystem': JITA}

        json_response = requests.get(URL, PARAMS).json()

        market_cache.setdefault(itemid, {})
        market_cache[itemid].setdefault(mode.value[0], {})
        market_cache[itemid][mode.value[0]].setdefault(mode.value[1], {})

        market_cache[itemid][mode.value[0]][mode.value[1]]['val'] = [response[mode.value[0]][mode.value[1]] for response in json_response][0]
        market_cache[itemid][mode.value[0]][mode.value[1]]['time'] = int(time())
        save_cache()

    return market_cache[itemid][mode.value[0]][mode.value[1]]['val']


def get_market_attr_by_name(name, mode):

    return get_market_attr_by_id(get_id_by_name(name), mode)
