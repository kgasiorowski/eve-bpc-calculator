import requests
from enum import Enum
import json
from time import time
import os

JITA = 30000142


class Mode(Enum):
    BUYMAX = ('buy', 'max')
    SELLMIN = ('sell', 'min')

    SELLMAX = ('sell', 'max')
    BUYMIN = ('buy', 'min')

    BUYAVG = ('buy', 'avg')
    SELLAVG = ('sell', 'avg')


class Market:

    def __init__(self):
        self.id_to_name = None
        self.name_to_id = None
        self.market_cache = None

    def load_dicts(self):

        if self.id_to_name is None:
            with open('./data/dicts/id_to_name.json') as infile:
                self.id_to_name = json.load(infile)

        if self.name_to_id is None:
            with open('./data/dicts/name_to_id.json') as infile:
                self.name_to_id = json.load(infile)


    def load_cache(self):

        if self.market_cache is None:
            if not os.path.exists('./data/cache/market_cache.json'):
                self.generate_cache_file()
            with open('./data/cache/market_cache.json') as cache_file:
                self.market_cache = json.load(cache_file)
        return self.market_cache

    def generate_cache_file(self):
        os.makedirs('./data/cache/')
        with open('./data/cache/market_cache.json', 'w') as new_cache_file:
            new_cache_file.write('{}')

    def save_cache(self):

        with open('./data/cache/market_cache.json', 'w') as cache_file:
            json.dump(self.market_cache, cache_file)

    def get_id_by_name(self, name):

        self.load_dicts()
        return self.name_to_id[name]


    def get_name_by_id(self, item_id):

        self.load_dicts()
        return self.id_to_name[item_id]


    def get_market_attr_by_id(self, itemid, mode):

        self.load_cache()

        try:

            current_time = time()
            difference = current_time - self.market_cache[itemid][mode.value[0]][mode.value[1]]['time']

            if difference < 3600:
                return self.market_cache[itemid][mode.value[0]][mode.value[1]]['val']
            else:
                raise KeyError

        except KeyError:

            URL = r'http://api.evemarketer.com/ec/marketstat/json'
            PARAMS = {'typeid': itemid,
                      'usesystem': JITA}

            json_response = requests.get(URL, PARAMS).json()

            self.market_cache.setdefault(itemid, {})
            self.market_cache[itemid].setdefault(mode.value[0], {})
            self.market_cache[itemid][mode.value[0]].setdefault(mode.value[1], {})

            self.market_cache[itemid][mode.value[0]][mode.value[1]]['val'] = [response[mode.value[0]][mode.value[1]] for response in json_response][0]
            self.market_cache[itemid][mode.value[0]][mode.value[1]]['time'] = int(time())
            self.save_cache()

        return self.market_cache[itemid][mode.value[0]][mode.value[1]]['val']


    def get_market_attr_by_name(self, name, mode):
        return self.get_market_attr_by_id(self.get_id_by_name(name), mode)
