from Blueprint import Blueprint
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('-b', '--buyorders', action='store_true')
    parser.add_argument('-s', '--sellorders', action='store_true')

    args = parser.parse_args()

    if args.sellorders:
        print('Selling using sell orders!')

    if args.buyorders:
        print("Buying using buy orders!")

    blueprints = Blueprint.initialize_blueprints('./data/blueprints/')

    profit_dict = {}

    for blueprint in blueprints:
        print(f'Fetching {blueprint.name} things...')
        profit_dict.setdefault(blueprint, blueprint.get_total_profit(sellorders=args.sellorders, buyorders=args.buyorders))

    print('Sorting...')
    profit_dict = reversed(sorted(profit_dict.items(), key=lambda kv: kv[1]))

    counter = 0
    for item, profit in profit_dict:
        counter += 1
        print(f'{counter:3d}. {item.name:50s}{profit:>20,.2f}{profit/item.runs:>20,.2f} x {item.runs}')
