from src.market import Mode
from src.decryptor import Decryptor
import os

invention_path = './data/invention/'
decryptors_path = './data/decryptors/decryptors.json'

decryptors = Decryptor.get_decryptors(decryptors_path)

class Blueprint:

    market = None

    def __init__(self):
        self.input_items = None
        self.name = None
        self.output_quant = None
        self.runs = None
        self.market = None

        self.invented = False
        self.base_invention_chance = None
        self.invented_runs = None
        self.invented_TE = None
        self.invented_ME = None
        self.datacore1 = None
        self.datacore2 = None
        self.invention_cost = None

    def get_market_results(self, buyorders=True, sellorders=True):

        results = BlueprintMarketResults()

        results.runs = self.runs
        results.input_costs = self.__calculate_costs(buyorders)

        if self.invented:
            results.invention_costs = self.__calculate_invention_costs(decryptors['Attainment Decryptor'])
            results.input_costs += results.invention_costs

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

        print(f'Invention cost for {self.name}: {price_per_invented_run} using {decryptor.name}')

        return price_per_invented_run


    @staticmethod
    def parse_string(string):

        number = int(string[:string.find(' x ')].replace(',', '').strip())
        item_name = string[string.rfind(' x ') + 2:].strip()

        return item_name, number


    @staticmethod
    def initialize_blueprints(blueprints_path):

        blueprints = {}

        for filename in os.listdir(blueprints_path):
            with open(blueprints_path + filename) as blueprint_file:

                firstline = blueprint_file.readline()

                # Try to extract the first line as the number of runs
                try:
                    num_runs = int(firstline)
                except:
                    blueprint_file.seek(0)
                    num_runs = 1

                # Second line has our outputs
                outputname, outputquantity = Blueprint.parse_string(blueprint_file.readline())
                input_dict = {}

                for line in blueprint_file:
                    item_name, item_quantity = Blueprint.parse_string(line)
                    input_dict.setdefault(item_name, item_quantity)

                blueprint = Blueprint()
                blueprint.name = outputname
                blueprint.input_items = input_dict
                blueprint.output_quant = outputquantity
                blueprint.runs = num_runs

                try:
                    with open(invention_path + filename) as invention_file:
                        blueprint.invented = True
                        blueprint.base_invention_chance,\
                        blueprint.invented_runs,\
                        blueprint.invented_ME,\
                        blueprint.invented_TE = (float(token) for token in next(invention_file).strip().split())
                        blueprint.datacore1 = Blueprint.parse_string(next(invention_file).strip())[0]
                        blueprint.datacore2 = Blueprint.parse_string(next(invention_file).strip())[0]
                except FileNotFoundError:
                    pass

                blueprints.setdefault(outputname, blueprint)

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
