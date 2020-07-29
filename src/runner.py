from src.blueprint import Blueprint
import argparse
from src import market
from src.decryptor import Decryptor
import src.data as data

def print_item(item, result, counter=1):
    print(f'{counter:3d}. '
          f'{item.name:50s}'
          f'{result.profit_per_bpc:>20,.2f}'
          f'{result.profit:>20,.2f} x {result.runs:4} '
          f'{result.profit_margin*100:10,.2f}% '
          f'{result.invention_costs if result.invention_costs is not None else 0:>14,.2f}')


def print_header(buyorders=True, sellorders=True):
    print(f'\nUsing buy orders: {"Yes" if buyorders else "No"}\nUsing sell orders: {"Yes" if sellorders else "No"}\n')
    print(f'{"":3s}  {"Blueprint Name":50s}{"Total profit":>20s}{"Breakdown":>20s} x {"runs":4} {"Margin":>11} {"Invention cost"}')


def main():

    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('-b', '--buyorders', action='store_true')
    parser.add_argument('-s', '--sellorders', action='store_true')
    parser.add_argument('-n', '--name')
    parser.add_argument('-a', '--alphabetical', action='store_true')

    args = parser.parse_args()

    if args.sellorders:
        print('Selling using sell orders!')

    if args.buyorders:
        print("Buying using buy orders!")

    if args.alphabetical:
        print('Sorting alphabetically!')

    # Initialize generated stuff
    data.init()

    # Initialize our list of blueprints
    blueprints = Blueprint.load_blueprints()

    if args.name is not None:

        blueprint = blueprints[args.name] if args.name in blueprints else None
        print(f'Fetching {blueprint.name} things...')
        results = blueprint.get_market_results(sellorders=args.sellorders, buyorders=args.buyorders)
        print_header(buyorders=args.buyorders, sellorders=args.sellorders)
        print_item(blueprint, results)

    else:

        results_dict = {}

        for blueprint in blueprints.values():
            print(f'Fetching {blueprint.name} things...')
            results_dict.setdefault(blueprint,
                                   blueprint.get_market_results(sellorders=args.sellorders, buyorders=args.buyorders))

        print('Sorting...')
        if args.alphabetical:
            results_dict = sorted(results_dict.items(), key=lambda kv: kv[0].name)
        else:
            results_dict = reversed(sorted(results_dict.items(), key=lambda kv: kv[1].profit_per_bpc))

        print_header(sellorders=args.sellorders, buyorders=args.buyorders)

        counter = 0
        for item, results in results_dict:
            counter += 1
            print_item(item, results, counter)
