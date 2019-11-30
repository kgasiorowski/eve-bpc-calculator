from Blueprint import Blueprint

if __name__ == "__main__":

    blueprints = Blueprint.initialize_blueprints('./data/blueprints/')

    profit_dict = {blueprint:blueprint.get_total_profit() for blueprint in blueprints}
    profit_dict = reversed(sorted(profit_dict.items(), key=lambda kv: kv[1]))

    counter = 0
    for item, profit in profit_dict:
        counter += 1
        print(f'{counter:3d}. {item.name:50s}{profit:>20,.2f}{profit/item.runs:>20,.2f} x {item.runs}')
