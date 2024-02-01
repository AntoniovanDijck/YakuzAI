# main.py
# Antonio, Vincent, Mec
# YakuzAI

import json
import csv
import random
import datetime
import argparse
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import code.classes.house
import code.classes.cable 
import code.classes.battery
from code.classes.district import District
from code.algorithm.RandomAlgorithm import RandomAlgorithm
from code.algorithm.Greedy_Object_Distance_Randomized import Greedy_Object_Distance_Randomized as nearest_object_rand
from code.algorithm.Greedy_Object_Distance_Reversed import Greedy_Object_Distance_Reversed as nearest_object_y
from code.algorithm.Greedy_Object_Distance import Greedy_Object_Distance as nearest_object_x
from code.helpers.visualize import visualize
from code.algorithm.Greedy_Battery_Distance import Greedy_Battery_Distance as nearest_battery
from code.algorithm.DijckstraAlgorithm import DijckstraAlgorithm as dijckstra
from code.experiments.find_lowest_cost_experiment import find_lowest_cost_experiment
from code.algorithm.HillClimber import HillClimber
from code.experiments.hill_climber_experiment import hill_climber_experiment

def main(iterations, district_selection, algorithm_selection):
    """
    The main function of the program. It runs the selected algorithm for the selected district.
    """
    
    # Maps for district files and algorithms
    districts_houses = {
        '1': 'data/Huizen&Batterijen/district_1/district-1_houses.csv',
        '2': 'data/Huizen&Batterijen/district_2/district-2_houses.csv',
        '3': 'data/Huizen&Batterijen/district_3/district-3_houses.csv'
    }
    districts_batteries = {
        '1': 'data/Huizen&Batterijen/district_1/district-1_batteries.csv',
        '2': 'data/Huizen&Batterijen/district_2/district-2_batteries.csv',
        '3': 'data/Huizen&Batterijen/district_3/district-3_batteries.csv'
    }

    # Maps for algorithms
    algorithms = {
        'dijckstra': dijckstra,
        'nearest_battery': nearest_battery,
        'nearest_object_x': nearest_object_x,
        'nearest_object_y': nearest_object_y,
        'nearest_object_rand': nearest_object_rand,
        'random': RandomAlgorithm
    }

    # Verify and select the district and algorithm
    houses_file = districts_houses.get(district_selection)
    batteries_file = districts_batteries.get(district_selection)
    algorithm = [algorithms.get(algorithm_selection)]

    # If all algorithms or no algorithms are selected, run all algorithms
    if algorithm_selection == 'all':

        # Select all algorithms
        algorithm = [dijckstra, nearest_battery, nearest_object_x, nearest_object_y, nearest_object_rand, RandomAlgorithm]

    # If the district or algorithm is invalid, return an error
    if houses_file is None or batteries_file is None or algorithm is None:
        print("Invalid district or algorithm selection.")
        return

    # Print the selected district and algorithm
    print(f'Running {algorithm_selection} for District {district_selection}')

    # Run the experiment
    lowest_district = find_lowest_cost_experiment(houses_file, batteries_file, iterations, algorithms=algorithm)
    hill_climber_experiment(lowest_district, iterations, int(district_selection)-1, depth=4)

if __name__ == "__main__":
    # Parse the arguments for CLI commands
    parser = argparse.ArgumentParser(description='Run the YakuzAI Smart Grid simulation.')

    # Add the arguments
    parser.add_argument('-i', '--iterations', type=int, default=100, help='Number of iterations for the simulation')
    parser.add_argument('-d', '--district', type=str, choices=['1', '2', '3'], required=True, help='District number to simulate')
    parser.add_argument('-a', '--algorithm', type=str, choices=['all','dijckstra', 'nearest_battery', 'nearest_object_x', 'nearest_object_y', 'nearest_object_rand', 'random'], required=True, help='Algorithm to use for the simulation')

    # Parse the arguments   
    args = parser.parse_args()

    main(args.iterations, args.district, args.algorithm)