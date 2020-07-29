import json
import src.market as mk
from src.config import DECRYPTORS_JSON

class Decryptor:

    market = None

    @staticmethod
    def load_decryptors():
        with open(DECRYPTORS_JSON) as decryptors_file:
            decryptors = json.load(decryptors_file)
            for decryptor_name, decryptor_attr in decryptors.items():
                decryptor_attr.setdefault('price', Decryptor.market.apply_mode(
                    Decryptor.market.get_market_attr_by_name(decryptor_name),
                    mk.Mode.SELLMIN
                ) if decryptor_name != "None" else 0)
            return decryptors
