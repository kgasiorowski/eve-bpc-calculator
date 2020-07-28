import json
import src.market as mk
from src.config import *

class Decryptor:

    market = None

    def __init__(self, name, run_modifier=None, prob_modifier=None, TE_modifier=None, ME_modifier=None):

        self.name = name
        self.run_modifier = run_modifier
        self.prob_modifier = prob_modifier
        self.TE_modifier = TE_modifier
        self.ME_modifier = ME_modifier

        if Decryptor.market is None:
            Decryptor.market = mk.Market()

        self.price = Decryptor.market.get_market_attr_by_name(self.name, mk.Mode.SELLMIN) if name != "None" else 0

    def __str__(self):
        return f'\'{self.name}\' -> {self.run_modifier} -> {self.prob_modifier} -> {self.price}'


    @staticmethod
    def get_decryptors():

        with open(DECRYPTORS_JSON) as decryptors_file:
           decryptors_dict = json.load(decryptors_file)

        return {decryptor['name']:Decryptor(decryptor['name'], decryptor['runs'], decryptor['prob']) for decryptor in decryptors_dict}
