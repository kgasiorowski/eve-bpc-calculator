from src.market import Mode
from src.decryptor import Decryptor
from src.config import *
import json


class Blueprint:

    market = None
    decryptors = None

    def __init__(self):
        self.input_items = None
        self.name = None
        self.output_quant = None
        self.runs = None

        self.invented = False
        self.base_invention_chance = None
        self.invented_runs = None
        self.invented_TE = None
        self.invented_ME = None
        self.datacore1 = None
        self.datacore2 = None
        self.invention_cost = None

    def get_market_results(self, buyorders=True, sellorders=True, decryptor=None):

        results = BlueprintMarketResults()

        results.runs = self.runs
        results.input_costs = self.__calculate_costs(buyorders)

        if self.invented:
            if decryptor is None:
                decryptor = Blueprint.decryptors['None']
            results.invention_costs = self.__calculate_invention_costs(decryptor)
            results.input_costs += results.invention_costs
            results.runs += decryptor.run_modifier

        results.revenue = self.__calculate_revenue(sellorders)
        results.profit = results.revenue - results.input_costs
        results.profit_per_bpc = results.profit * results.runs
        results.profit_margin = results.profit / results.input_costs
        return results

    def __calculate_costs(self, buyorders):

        input_costs = 0

        for item_name, amount in self.input_items.items():
            buying_mode = Mode.BUYMAX if buyorders else Mode.SELLMIN
            item_price = Blueprint.market.get_market_attr_by_name(item_name, buying_mode)
            input_costs += item_price * amount

        return input_costs

    def __calculate_revenue(self, sellorders):

        selling_mode = Mode.SELLMIN if sellorders else Mode.BUYMAX
        return Blueprint.market.get_market_attr_by_name(self.name, selling_mode) * self.output_quant

    def __calculate_invention_costs(self, decryptor: Decryptor):

        datacores = 2 * Blueprint.market.get_market_attr_by_name(self.datacore1, Mode.SELLMIN) +\
                    2 * Blueprint.market.get_market_attr_by_name(self.datacore2, Mode.SELLMIN)

        derived_invention_chance = self.base_invention_chance * (1+decryptor.prob_modifier)
        derived_runs = self.invented_runs + decryptor.run_modifier

        cost_per_invention = datacores + decryptor.price
        num_invention_runs_ratio = derived_invention_chance * derived_runs
        price_per_invented_run = cost_per_invention/num_invention_runs_ratio
        return price_per_invented_run

    @staticmethod
    def load_blueprints():

        blueprints = {}

        invention_json = json.load(open(INVENTION_PATH))
        blueprints_json = json.load(open(BLUEPRINTS_PATH))

        for blueprint_name, blueprint_attributes in blueprints_json.items():
            blueprint = Blueprint()
            blueprint.name = blueprint_name
            blueprint.input_items = blueprint_attributes['mats']
            blueprint.output_quant = blueprint_attributes['output_quantity']
            blueprint.runs = blueprint_attributes['runs']

            if blueprint_name in invention_json:
                invention_json_object = invention_json[blueprint_name]
                blueprint.invented = True
                blueprint.base_invention_chance = invention_json_object['base_invention_chance']
                blueprint.invented_runs = invention_json_object['invented_runs']
                blueprint.invented_ME = invention_json_object['invented_ME']
                blueprint.invented_TE = invention_json_object['invented_TE']
                blueprint.datacore1 = invention_json_object['datacore1']
                blueprint.datacore2 = invention_json_object['datacore2']

            blueprints.setdefault(blueprint.name, blueprint)

        return blueprints


class BlueprintMarketResults:

    def __init__(self):
        self.runs = None
        self.input_costs = None
        self.invention_costs = None
        self.revenue = None
        self.profit_per_run = None
        self.profit_per_bpc = None
        self.profit_margin = None
