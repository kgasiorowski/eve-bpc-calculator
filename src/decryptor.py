import json
import src.market as mk
from src.config import *

class Decryptor:

    market = None

    def __init__(self, name, run_modifier=None, prob_modifier=None, te_modifier=None, me_modifier=None):

        self.name = name
        self.run_modifier = run_modifier
        self.prob_modifier = prob_modifier
        self.te_modifier = te_modifier
        self.me_modifier = me_modifier

        if Decryptor.market is None:
            Decryptor.market = mk.Market()

        self.price = Decryptor.market.apply_mode(Decryptor.market.get_market_attr_by_name(self.name), mk.Mode.SELLMIN) \
            if name != "None" else 0

    def __str__(self):
        return f'\'{self.name}\' -> {self.run_modifier} -> {self.prob_modifier} -> {self.price}'


    @staticmethod
    def load_decryptors():

        with open(DECRYPTORS_JSON) as decryptors_file:
            raw_decryptors_dict = json.load(decryptors_file)

        decryptors = {}
        for decryptor in raw_decryptors_dict:
            decryptors.setdefault(decryptor['name'], Decryptor(decryptor['name'], decryptor['runs'], decryptor['prob']))

        return decryptors
