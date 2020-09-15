import math

import numpy as np

# Goal:
# n aristocrates
# with a production that is sufficient to make the aristocrats happy.

# TODO: taxes as yield of money.
# TODO: production building operating cost / production building sleep operating cost as consumption of money.

cycle = 60.0  # in seconds

# progression
# pioneer -> settler -> citizen -> merchant -> aristocrat
population_groups = (
    'pioneers',
    'settlers',
    'citizens',
    'merchants',
    'aristocrats'
)

good_names = (
    'money',
    'iron ore',
    'gold',
    'wool',
    'sugar',
    'tobacco',
    'cattle',
    'grain',
    'flour',
    'iron',
    'swords',
    'muskets',
    'cannon',
    'food',
    'tobacco products',
    'spices',
    'cocoa',
    'liquor',
    'cloth',
    'clothes',
    'jewelry',
    'tools',
    'wood',
    'bricks'
)


# consumption or yield rates
# positive number can be interpreted as yield
# negative number can be interpreted as consumption
def create_rates_vector():
    return np.zeros((len(good_names)))


def create_rates(rates):
    consumption_rates_values = create_rates_vector()
    for good_name, consumption_rate in rates.items():
        consumption_rates_values[good_names.index(good_name)] = float(consumption_rate)
    return np.array(consumption_rates_values)


maximum_number_of_people_per_house = np.array((
    2,
    6,
    15,
    25,
    40
))


def calculate_number_of_houses_for_population(population_group, population_size):
    return math.ceil(population_size / maximum_number_of_people_per_house[population_groups.index(population_group)])


# originally: V (Verbrauchsraten)
# rates are per person
consumption_rates = np.array((
    # pioneers
    create_rates(
        {
            'food': 0.13,
        }
    ),
    # settlers
    create_rates(
        {
            'food': 0.13,
            'cloth': 0.06,
            'liquor': 0.05
        }
    ),
    # citizens
    create_rates(
        {
            'food': 0.13,
            'cloth': 0.07,
            'liquor': 0.06,
            'tobacco products': 0.05,
            'spices': 0.05
        }
    ),
    # merchants
    create_rates(
        {
            'food': 0.13,
            'cloth': 0.08,
            'liquor': 0.07,
            'cocoa': 0.07,
            'tobacco products': 0.06,
            'spices': 0.06
        }
    ),
    # aristocrats
    create_rates(
        {
            'food': 0.13,
            'liquor': 0.08,
            'cocoa': 0.06,
            'tobacco products': 0.06,
            'spices': 0.06,
            'clothes': 0.05,
            'jewelry': 0.02
        }
    ),
))

taxes = (
    # pioneers
    0,
    # settlers
    0,
    # citizens
    0,
    # merchants
    0,
    # aristocrats
    0
)


def create_building(building):
    keys_to_add = ('operating cost', 'yield rate')
    for key_to_add in keys_to_add:
        if key_to_add not in building:
            building[key_to_add] = {}
    if 'workload' not in building:
        building['workload'] = 1.0
    return building


def calculate_yield_rate(yield_amount, interval):
    return cycle / (yield_amount * interval)


buildings = (
    create_building({
        'name': 'dirt road',
        'operating cost': {},
        'building cost': {
            'money': 5
        }
    }),
    # ...
    create_building({
        'name': 'quarry',
        'yield rate': {
            'money': 0
        }
    }),
    create_building({
        'name': 'iron mine',
        'yield rate': {
            'money': -60,
            'iron ore': calculate_yield_rate(1, 40)
        }
    }),
    create_building({
        'name': 'deep iron mine',
        'yield rate': {
            'money': -60,
            'iron ore': calculate_yield_rate(1, 40)
        }
    }),
    create_building({
        'name': 'gold-mine',
        'yield rate': {
            'money': -60,
            'gold': calculate_yield_rate(1, 80)
        }
    }),
    create_building({
        'name': 'goldsmith',
        'yield rate': {
            'money': -45,
            'jewelry': calculate_yield_rate(1, 80)
        }
    }),
    create_building({
        'name': 'stonemason',
        'yield rate': {
            'money': -5,
            'jewelry': calculate_yield_rate(1, 80)
        }
    }),
    create_building({
        'name': "fisher's hut",
        'building cost': {
            'money': 100,
            'tools': 3,
            'wood': 5
        },
        'yield rate': {
            'money': -5,
            'food': calculate_yield_rate(3, 28)
        }
    })
)

building_names = (

)

production_building_names = (

)

production_building_build_costs = (

)

production_building_operating_costs = (

)

production_building_sleep_costs = (

)


def calculate_yield_rates_for_building(building):
    return create_rates(building['yield rate'])


yield_rates = np.array(
    tuple(calculate_yield_rates_for_building(building) for building in buildings)
)

current_population = np.zeros((len(population_groups),))
population_group = 'aristocrats'
print('population group', population_group)
number_of_population = 1000
print('number of population', number_of_population)
population = np.zeros((len(population_groups),))
population[population_groups.index(population_group)] = number_of_population
print('population', population)
number_of_houses = calculate_number_of_houses_for_population(population_group, number_of_population)
print('number of houses', number_of_houses)
consumption_rate = number_of_houses * consumption_rates[population_groups.index(population_group)]
print('consumption rate', consumption_rate)


def determine_available_building(population):
    # TODO: Implement
    return buildings


def select_buildings(consumption_rate):
    available_buildings = determine_available_building(current_population)
    number_of_buildings = np.zeros((len(buildings),))
    for index, rate in enumerate(consumption_rate):
        if rate > 0:
            good_name = good_names[index]
            production_building = select_building_with_highest_production_efficiency(available_buildings, good_name)
            if production_building:
                number_of_production_building = int(math.ceil(rate / production_building['yield rate'][good_name]))
                building_index = buildings.index(production_building)
                number_of_buildings[building_index] = number_of_production_building
    return number_of_buildings


def select_building_that_produce_good(buildings, good_name):
    return tuple(building for building in buildings if good_name in building['yield rate'] and building['yield rate'][good_name] > 0)


def calculate_production_efficiency(building):
    building_yield_rate = building['yield rate']
    yield_rate = building_yield_rate.copy()
    del yield_rate['money']
    production_per_cycle = sum(yield_rate.values())
    cost_per_cycle = -building_yield_rate['money']
    return float(production_per_cycle) / float(cost_per_cycle)


def select_building_with_highest_production_efficiency(available_buildings, good):
    buildings_that_produce_good = select_building_that_produce_good(available_buildings, good)
    return max(buildings_that_produce_good, key=calculate_production_efficiency) \
        if len(buildings_that_produce_good) >= 1 \
        else None


number_of_buildings = select_buildings(consumption_rate)
print('number of buildings', number_of_buildings)

production_rate = np.dot(np.transpose(yield_rates), number_of_buildings)
print('production rate', production_rate)

print('production rate - consumption_rate', production_rate - consumption_rate)

# Optimize
# p = v
