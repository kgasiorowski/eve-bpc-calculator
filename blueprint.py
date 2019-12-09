from market import Mode
import os

invention_path = './data/invention/'

class Blueprint:

    def __init__(self):
        self.input_items = None
        self.name = None
        self.output_quant = None
        self.runs = None
        self.market = None

        self.inventable = False
        self.base_invention_chance = None
        self.invented_runs = None
        self.invented_TE = None
        self.invented_ME = None
        self.datacore1 = None
        self.datacore2 = None

    def get_market_results(self, buyorders=True, sellorders=True):

        results = BlueprintMarketResults()

        results.runs = self.runs
        results.input_costs = 0

        for item_name, amount in self.input_items.items():

            buying_mode = Mode.BUYMAX if buyorders else Mode.SELLMIN
            item_price = self.market.get_market_attr_by_name(item_name, buying_mode)
            results.input_costs += item_price * amount

        selling_mode = Mode.SELLMIN if sellorders else Mode.BUYMAX
        results.revenue = self.market.get_market_attr_by_name(self.name, selling_mode) * self.output_quant

        results.profit = results.revenue - results.input_costs
        results.total_profit = results.profit * results.runs

        results.profit_margin = results.profit / results.input_costs

        return results


    @staticmethod
    def parse_string(string):

        number = int(string[:string.find(' x ')].replace(',', '').strip())
        item_name = string[string.rfind(' x ') + 2:].strip()

        return item_name, number


    @staticmethod
    def initialize_blueprints(blueprints_path, market_reference):

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
                blueprint.market = market_reference
                blueprint.runs = num_runs

                try:
                    with open(invention_path + filename) as invention_file:
                        blueprint.inventable = True
                        blueprint.base_invention_chance,\
                        blueprint.invented_runs,\
                        blueprint.invented_ME,\
                        blueprint.invented_TE = next(invention_file).split()
                        blueprint.datacore1 = next(invention_file)
                        blueprint.datacore2 = next(invention_file)
                except FileNotFoundError:
                    pass

                blueprints.setdefault(outputname, blueprint)

        return blueprints


class BlueprintMarketResults:

    def __init__(self):

        self.runs = None
        self.input_costs = None
        self.revenue = None
        self.profit_per_run = None
        self.total_profit = None
        self.profit_margin = None
