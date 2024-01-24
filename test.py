# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

from code.helpers.smart_grid import load_battery_data, load_house_data, show_district
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from code.classes.battery import Battery
from code.classes.house import House
from code.classes.cable import Cable
from code.classes.district import District
from code.helpers.visualize import visualize
from code.algorithm.greedy import Greedy3
from code.algorithm.random_alg import RandomAlgorithm
from code.helpers.draw_cables import draw_cables

districts_houses = ['data/Huizen&Batterijen/district_1/district-1_houses.csv', 'data/Huizen&Batterijen/district_2/district-2_houses.csv', 'data/Huizen&Batterijen/district_3/district-3_houses.csv']
districts_batteries = ['data/Huizen&Batterijen/district_1/district-1_batteries.csv', 'data/Huizen&Batterijen/district_2/district-2_batteries.csv', 'data/Huizen&Batterijen/district_3/district-3_batteries.csv']

experiment_instance = District(districts_houses[0], districts_batteries[0])

# Apply the Greedy algorithm to connect houses to batteries
greedy_instance = Greedy3(experiment_instance)
greedy_instance.connect_houses_to_batteries()

visualize(experiment_instance, 0)
draw_cables(experiment_instance)

