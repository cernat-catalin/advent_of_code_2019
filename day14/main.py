import re, math
from typing import NamedTuple, List, Tuple
from collections import defaultdict


class Reaction(NamedTuple):
    left: List[Tuple[int, str]]
    right: Tuple[int, str]


def create_reaction(unparsed_reaction: List[str]) -> Reaction:
    parse_element = lambda x: (int(x.split(' ')[0]), x.split(' ')[1])
    left = [parse_element(element) for element in unparsed_reaction[:-1]]
    right = parse_element(unparsed_reaction[-1])
    return Reaction(left, right)


def reduce(reactions: List[Reaction], fuel_quntity: int) -> int:
    stock = defaultdict(int)
    stock['FUEL'] = -fuel_quntity

    deficient_stock = lambda stock: len([k for (k, v) in stock.items() if k != 'ORE' and v < 0]) > 0
    pick_deficient_element = lambda stock: next((k, v) for (k, v) in stock.items() if k != 'ORE' and v < 0)
    pick_element_reaction = lambda e, reactions: next(x for x in reactions if x.right[1] == e)

    # loop until we only have 'ORE' deficiency in the stock
    while deficient_stock(stock):
        element, quantity = pick_deficient_element(stock)
        reaction = pick_element_reaction(element, reactions)
        mult = math.ceil(abs(quantity) / reaction.right[0])

        stock[element] += mult * reaction.right[0]
        for l_quantity, l_element in reaction.left:
            stock[l_element] -= mult * l_quantity
    
    return abs(stock['ORE'])


def binary_search(reactions: List[Reaction], available_ore: int) -> int:
    one_fuel_cost = reduce(reactions, 1)
    lower_bound = math.floor(available_ore / one_fuel_cost)
    upper_bound = 2 * lower_bound

    fuel_cost = 0
    while lower_bound < upper_bound:
        m = math.floor((upper_bound + lower_bound) / 2)
        # print('{} {} {}'.format(lower_bound, m, upper_bound))
        fuel_cost = reduce(reactions, m)
        if fuel_cost < available_ore:
            lower_bound = m + 1
        else:
            upper_bound = m

    return lower_bound - 1


with open ('day14/input') as f:
    reactions = [re.findall(r'[\d]+ [\w]+', line) for line in f.readlines()]
    reactions = [create_reaction(reaction) for reaction in reactions]

    print(reduce(reactions, 1)) # part one

    available_ore = int(1e12)
    print(binary_search(reactions, available_ore))