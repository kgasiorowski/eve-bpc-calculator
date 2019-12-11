import json
from src import market as mk


class Decryptor:

    market = None

    def __init__(self, name, run_modifier=None, prob_modifier=None):

        self.name = name
        self.run_modifier = run_modifier
        self.prob_modifier = prob_modifier

        if Decryptor.market is None:
            Decryptor.market = mk.Market()

        self.price = Decryptor.market.get_market_attr_by_name(self.name, mk.Mode.SELLMIN) if name != "None" else 0

    def __str__(self):
        return f'\'{self.name}\' -> {self.run_modifier} -> {self.prob_modifier} -> {self.price}'


    @staticmethod
    def get_decryptors(path):

        with open(path) as decryptors_file:
           decryptors_dict = json.load(decryptors_file)

        return {decryptor['name']:Decryptor(decryptor['name'], decryptor['runs'], decryptor['prob']) for decryptor in decryptors_dict}
