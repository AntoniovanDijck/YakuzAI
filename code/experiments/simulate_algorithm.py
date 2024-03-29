# Simulate_Algorithm.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import numpy as np
from tqdm import tqdm
from code.classes.district import District
from code.helpers.visualize import visualize
from code.algorithm.RandomAlgorithm import RandomAlgorithm as RandomAlgorithm
from code.algorithm.Greedy_Battery_Distance import Greedy_Battery_Distance as nearest_battery
from code.algorithm.Greedy_Object_Distance import Greedy_Object_Distance as nearest_object_x
from code.algorithm.Greedy_Object_Distance_Reversed import Greedy_Object_Distance_Reversed as nearest_object_y
from code.algorithm.Greedy_Object_Distance_Randomized import Greedy_Object_Distance_Randomized as nearest_object_rand
from code.algorithm.DijckstraAlgorithm import DijckstraAlgorithm as dijckstra

class Simulate_Algorithm:
    """
    simulates x mount of itterations of a given algorithm and saves the frequency of the total costs in a list
    """
    def __init__(self, algorithm, iterations=100, houses_file=None, batteries_file=None):
        self.algorithm = algorithm
        self.iterations = iterations
        self.costs = []
        self.houses_file = houses_file
        self.batteries_file = batteries_file
        self.lowest_costs = 0
        self.lowest_district = None


    def simulate(self):
        """
        Simulates the algorithm x number of times, optimized for efficiency and shows progress using tqdm.
        """
        self.costs = [] # Using a set for unique total costs
        is_initial_cost_set = self.lowest_costs != 0
        self.lowest_district = None

        # Use tqdm for progress display
        for _ in tqdm(range(self.iterations), desc=f"Simulating {self.algorithm.__name__}"):
            district = District(self.houses_file, self.batteries_file)
            algorithm_instance = self.algorithm(district) 
            algorithm_instance.connect_houses_to_batteries()

            #visualize(district, 1)

            total_costs = district.calculate_totals()
            #print(total_costs)

            self.costs.append(total_costs)
 
            if not is_initial_cost_set or total_costs < self.lowest_costs:
                self.lowest_costs = total_costs
                self.lowest_district = district
                
                self.lowest_cost_house_order = [(house.x, house.y, house.maxoutput) for house in district.houses]

                is_initial_cost_set = True

        districtname = self.houses_file.split('/')[2].split('_')[1]
        algo_name = str(self.algorithm.__name__)

        visualize(self.lowest_district,int(districtname),algorithm_name=algo_name,iterations=self.iterations)
       
        print(f"Lowest costs: {self.lowest_costs} for algorithm {self.algorithm.__name__}")


        district = None

        return self.costs

    def get_lowest_cost_house_order(self):
        """Retrieve the house order for the lowest cost."""
        return self.lowest_cost_house_order
    
    def get_lowest_district(self):
        """Retrieve the district for the lowest cost."""
        return self.lowest_district

    def get_lowest_cost(self):
        """Retrieve the lowest cost."""
        return self.lowest_costs
    
    def save_lowest_cost_house_order_to_csv(self, file_name):
        """Saves the house order for the lowest cost to a CSV file."""

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['x', 'y', 'maxoutput'])  # Header

            for house in self.lowest_cost_house_order:
                writer.writerow(house)