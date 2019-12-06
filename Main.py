from Blueprint import Blueprint
import argparse
import Market

def print_item(item, profit, counter=1):
    print(f'{counter:3d}. {item.name:50s}{profit:>20,.2f}{profit/item.runs:>20,.2f} x {item.runs}')

def print_header(buyorders=True, sellorders=True):
    print(f'\nUsing buy orders: {"Yes" if buyorders else "No"}\nUsing sell orders: {"Yes" if sellorders else "No"}\n')
    print(f'{"":3s}  {"Blueprint Name":50s}{"Total profit":>20s}{"Breakdown":>20s} x {"runs"}')

def main():

    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('-b', '--buyorders', action='store_true')
    parser.add_argument('-s', '--sellorders', action='store_true')
    parser.add_argument('-n', '--name')
    parser.add_argument('-p', '--print', action='store_true')

    args = parser.parse_args()

    if args.sellorders:
        print('Selling using sell orders!')

    if args.buyorders:
        print("Buying using buy orders!")

    blueprints = Blueprint.initialize_blueprints('./data/blueprints/')

    if args.name is not None:

        blueprint = blueprints[args.name] if args.name in blueprints else None
        print(f'Fetching {blueprint.name} things...')
        profit = blueprint.get_total_profit(sellorders=args.sellorders, buyorders=args.buyorders)
        print_header(buyorders=args.buyorders, sellorders=args.sellorders)
        print_item(blueprint, profit)

    else:

        profit_dict = {}

        for blueprint in blueprints.values():
            print(f'Fetching {blueprint.name} things...')
            profit_dict.setdefault(blueprint,
                                   blueprint.get_total_profit(sellorders=args.sellorders, buyorders=args.buyorders))

        print('Sorting...')
        profit_dict = reversed(sorted(profit_dict.items(), key=lambda kv: kv[1]))

        print_header(sellorders=args.sellorders, buyorders=args.buyorders)

        counter = 0
        for item, profit in profit_dict:
            counter += 1
            print_item(item, profit, counter)

    if args.print:
        Market.print_cache()


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')