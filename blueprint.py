import market
from market import Mode
import os


class Blueprint:

    def __init__(self, _name, _input_items, _output_quant, runs=1):
        self.input_items = _input_items
        self.name = _name
        self.output_quant = _output_quant
        self.runs = runs


    def get_input_costs(self, buyorders=True):

        total_costs = 0

        for item_name, amount in self.input_items.items():

            buying_mode = Mode.BUYMAX if buyorders else Mode.SELLMIN
            item_price = market.get_market_attr_by_name(item_name, buying_mode)
            total_costs += item_price * amount

        return total_costs


    def get_output_revenue(self, sellorders=True):

        selling_mode = Mode.SELLMIN if sellorders else Mode.BUYMAX
        return market.get_market_attr_by_name(self.name, selling_mode) * self.output_quant



    def get_profit_per_run(self, sellorders=True, buyorders=True):
        return self.get_output_revenue(sellorders) - self.get_input_costs(buyorders)


    def get_total_profit(self, sellorders=True, buyorders=True):

        return self.get_profit_per_run(sellorders, buyorders)*self.runs


    @staticmethod
    def parse_string(str):
        number = int(str[:str.find(' x ')].replace(',', '').strip())
        item_name = str[str.rfind(' x ')+2:].strip()

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

                blueprints.setdefault(outputname, Blueprint(outputname, input_dict, outputquantity, num_runs))

        return blueprints