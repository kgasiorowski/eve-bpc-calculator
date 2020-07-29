import json
from src.market import *
from src.config.config import DECRYPTORS_JSON


class Decryptor:

    # Singleton
    decryptors = None

    @staticmethod
    def load_decryptors():
        if Decryptor.decryptors is None:
            market = Market.get_reference()
            with open(DECRYPTORS_JSON) as decryptors_file:
                decryptors = json.load(decryptors_file)
                for decryptor_name, decryptor_attr in decryptors.items():
                    decryptor_attr.setdefault('price', market.apply_mode(
                        market.get_market_attr_by_name(decryptor_name),
                        Mode.SELLMIN
                    ) if decryptor_name != "None" else 0)
                Decryptor.decryptors = decryptors
        return Decryptor.decryptors
