#Team Yakuzai: Antonio van Dijck, Mec Glandorff, Vincent D'Andolfi

import json
import csv
import numpy as np
import random
import datetime
import code.classes.house
import code.classes.cable 
import code.classes.battery
import code.helpers.smart_grid 
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.greedy import Greedy2
from code.helpers.visualize import visualize

def algorithm_costs(Algoritmh):

    districts_houses = ['data/Huizen&Batterijen/district_1/district-1_houses.csv', 'data/Huizen&Batterijen/district_2/district-2_houses.csv', 'data/Huizen&Batterijen/district_3/district-3_houses.csv']
    districts_batteries = ['data/Huizen&Batterijen/district_1/district-1_batteries.csv', 'data/Huizen&Batterijen/district_2/district-2_batteries.csv', 'data/Huizen&Batterijen/district_3/district-3_batteries.csv']
    
    for i in range(0, 3):
        print(f'District {i+1}')
        # set up experiment
        experiment = District(districts_houses[i], districts_batteries[i])
        random_instance = Algoritmh(experiment)
        random_instance.connect_houses_to_batteries()
        experiment.calculate_totals()

# test 
algorithm_costs(Greedy2)


    

