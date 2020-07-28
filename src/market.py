import requests
import json
import os
from enum import Enum
from time import time
from src.config import *


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
        self.request_counter = 0

        self.load_dicts()
        self.load_cache()

    def load_dicts(self):
        if self.id_to_name is None:
            with open(ID_TO_NAME_JSON) as infile:
                self.id_to_name = json.load(infile)

        if self.name_to_id is None:
            with open(NAME_TO_ID_JSON) as infile:
                self.name_to_id = json.load(infile)

    def load_cache(self):
        if self.market_cache is None:
            if not os.path.exists(MARKET_CACHE_JSON):
                with open(MARKET_CACHE_JSON, 'w') as new_cache_file:
                    new_cache_file.write('{}')
            with open(MARKET_CACHE_JSON) as cache_file:
                self.market_cache = json.load(cache_file)
        return self.market_cache

    def save_cache(self):
        with open(MARKET_CACHE_JSON, 'w') as cache_file:
            cache_file.write(json.dumps(self.market_cache, indent=4, sort_keys=True))

    def get_id_by_name(self, name):
        return self.name_to_id[name]

    def get_name_by_id(self, item_id):
        return self.id_to_name[item_id]

    def get_market_attr_by_id(self, itemid, mode):
        try:
            # Attempt to access the cache age for this item.
            cache_timestamp = self.market_cache[itemid][mode.value[0]][mode.value[1]]['time']
        except KeyError:
            # If unable to timestamp, guarantee refresh
            cache_timestamp = 0

        current_time = time()
        cache_age = current_time - cache_timestamp
        if cache_age < CACHE_LIFETIME:
            return self.market_cache[itemid][mode.value[0]][mode.value[1]]['val']
        else:
            URL = r'http://api.evemarketer.com/ec/marketstat/json'
            PARAMS = {'typeid': itemid,
                      'usesystem': JITA_ID}

            json_response = requests.get(URL, PARAMS).json()[0]

            self.market_cache.setdefault(itemid, {})
            self.market_cache[itemid].setdefault('buy', {})
            self.market_cache[itemid].setdefault('sell', {})

            self.market_cache[itemid]['buy'].setdefault('min', {})
            self.market_cache[itemid]['buy'].setdefault('max', {})
            self.market_cache[itemid]['buy'].setdefault('avg', {})
            self.market_cache[itemid]['sell'].setdefault('min', {})
            self.market_cache[itemid]['sell'].setdefault('max', {})
            self.market_cache[itemid]['sell'].setdefault('avg', {})

            self.market_cache[itemid]['buy']['min'].setdefault('time', current_time)
            self.market_cache[itemid]['buy']['max'].setdefault('time', current_time)
            self.market_cache[itemid]['buy']['avg'].setdefault('time', current_time)
            self.market_cache[itemid]['sell']['min'].setdefault('time', current_time)
            self.market_cache[itemid]['sell']['max'].setdefault('time', current_time)
            self.market_cache[itemid]['sell']['avg'].setdefault('time', current_time)

            self.market_cache[itemid]['buy']['min'].setdefault('val', json_response['buy']['min'])
            self.market_cache[itemid]['buy']['max'].setdefault('val', json_response['buy']['max'])
            self.market_cache[itemid]['buy']['avg'].setdefault('val', json_response['buy']['avg'])
            self.market_cache[itemid]['sell']['min'].setdefault('val', json_response['sell']['min'])
            self.market_cache[itemid]['sell']['max'].setdefault('val', json_response['sell']['max'])
            self.market_cache[itemid]['sell']['avg'].setdefault('val', json_response['sell']['avg'])

            self.save_cache()

        return self.market_cache[itemid][mode.value[0]][mode.value[1]]['val']

    def get_market_attr_by_name(self, name, mode):
        return self.get_market_attr_by_id(self.get_id_by_name(name), mode)
