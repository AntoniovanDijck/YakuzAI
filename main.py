import json
import csv
import random
import datetime
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import code.classes.house
import code.classes.cable 
import code.classes.battery
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.nearest_object_rand import nearest_object_rand
from code.algorithm.nearest_object_y import nearest_object_y
from code.helpers.visualize import visualize
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.dijckstra import dijckstra
from code.experiments.experiment2 import experiment2
from code.experiments.find_lowest_cost_experiment import find_lowest_cost_experiment
from code.algorithm.HillClimber import HillClimber

#Creators: Team YakuzAI
def main():
    """
    
    """

    # Drawing cables for all districts
    districts_houses = ['data/Huizen&Batterijen/district_1/district-1_houses.csv', 'data/Huizen&Batterijen/district_2/district-2_houses.csv', 'data/Huizen&Batterijen/district_3/district-3_houses.csv']
    districts_batteries = ['data/Huizen&Batterijen/district_1/district-1_batteries.csv', 'data/Huizen&Batterijen/district_2/district-2_batteries.csv', 'data/Huizen&Batterijen/district_3/district-3_batteries.csv']
    
    # Iterations for simulate    
    iterations = 100

    # For each district
    for i in range(0, 1):

        # Print district number for clarity
        print(f'District {i+1}')

        # set up experiment To test all algorithms
        lowest_district = find_lowest_cost_experiment(districts_houses[i], districts_batteries[i], iterations, algorithms=[dijckstra, nearest_battery])    

        hillclimber = HillClimber(lowest_district, 4, iterations)

        costs, district_states = hillclimber.hill_climb()

        visualize(district_states,i+1)

        all_costs = {}
        best_depth = None
        lowest_final_cost = float('inf')
        
        all_costs[i] = costs

        # Determine if this is the best depth
        if costs[-1] < lowest_final_cost:
            lowest_final_cost = costs[-1]
            best_depth = i

    # Set plot with a black background
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.axes()
    ax.set_facecolor('black')

    # Plot all costs, highlight the best one in red
    for depth, costs in all_costs.items():
        plt.plot(costs, color='red' if depth == best_depth else 'lime', linestyle='-', linewidth=2 if depth == best_depth else 1, label=f'Depth {depth}' if depth == best_depth else None)

    plt.xlabel('Iterations', fontsize=14, fontweight='bold', color='white')
    plt.ylabel('Total Cost', fontsize=14, fontweight='bold', color='white')
    plt.title('Hill Climber Optimization Progress', fontsize=16, fontweight='bold', color='white')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7, color='gray')
    plt.xticks(fontsize=12, color='white')
    plt.yticks(fontsize=12, color='white')

    plt.gca().invert_yaxis()

    # Add legend to show the best depth
    plt.legend(fontsize=12, facecolor='black', edgecolor='black', labelcolor='white')
    plt.tight_layout()

    plt.show()
       

if __name__ == "__main__":
    main()