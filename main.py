from blueprint import Blueprint
import argparse
import market as mk
from random import random
import json

def print_item(item, result, counter=1):
    print(f'{counter:3d}. {item.name:50s}{result.total_profit:>20,.2f}{result.profit:>20,.2f} x {item.runs:4} {result.profit_margin*100:10,.2f}%')

def print_header(buyorders=True, sellorders=True):
    print(f'\nUsing buy orders: {"Yes" if buyorders else "No"}\nUsing sell orders: {"Yes" if sellorders else "No"}\n')
    print(f'{"":3s}  {"Blueprint Name":50s}{"Total profit":>20s}{"Breakdown":>20s} x {"runs":4} {"Margin":>10}')

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

    market = mk.Market()
    blueprints = Blueprint.initialize_blueprints('./data/blueprints/', market)

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
            results_dict = reversed(sorted(results_dict.items(), key=lambda kv: kv[1].total_profit))

        print_header(sellorders=args.sellorders, buyorders=args.buyorders)

        counter = 0
        for item, results in results_dict:
            counter += 1
            print_item(item, results, counter)

def temp_script():

    m = mk.Market()

    datacores = 2*m.get_market_attr_by_name('Datacore - Electronic Engineering', mk.Mode.SELLMIN)+\
                2*m.get_market_attr_by_name('Datacore - Mechanical Engineering', mk.Mode.SELLMIN)

    decryptors = {
        'att': (14, .734, m.get_market_attr_by_name('Attainment Decryptor', mk.Mode.SELLMIN)),
        'aug': (19, .245, m.get_market_attr_by_name('Augmentation Decryptor', mk.Mode.SELLMIN)),
        'opti_att': (12, .775, m.get_market_attr_by_name('Optimized Attainment Decryptor', mk.Mode.SELLMIN)),
        'opti_aug': (17, .367, m.get_market_attr_by_name('Optimized Augmentation Decryptor', mk.Mode.SELLMIN))
    }

    num_simulations = 100000

    num_bpcs = 9
    runs_per = 5

    total_runs = num_bpcs * runs_per

    for decryptor in decryptors.keys():

        num_runs_per_decryptor, prob, decryptor_price = decryptors[decryptor]
        total_cost = (decryptor_price+datacores) * total_runs

        total = 0
        for run in range(total_runs):

            randval = random()

            if randval <= prob:
                total += num_runs_per_decryptor

        print(decryptor, total)
        print(f'Price per run: {total_cost/total:,.2f}')


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')