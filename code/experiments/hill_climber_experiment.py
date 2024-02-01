import os
import numpy as np  
import matplotlib.pyplot as plt
from code.algorithm.dijckstra import dijckstra
from code.algorithm.random_alg import RandomAlgorithm
from code.experiments.simulate_algorithm import Simulate_Algorithm
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.nearest_object import nearest_object_x
from code.algorithm.nearest_object_y import nearest_object_y
from code.algorithm.nearest_object_rand import nearest_object_rand
from code.algorithm.HillClimber import HillClimber
from code.helpers.visualize import visualize
from code.algorithm.HillClimberTest import HillClimberTest

def hill_climber_experiment(lowest_district,iterations,district_int,depth=4):
    """
    Runs the simulation for each algorithm, saves results in a CSV file, plots a histogram of the resulting costs,
    and saves the lowest cost district data in a JSON file.
    """

    # Create a hill climber instance
    hillclimber = HillClimberTest(lowest_district, depth, iterations)

    # Run the hill climber
    costs, district_states = hillclimber.hill_climb()

    # Visualize the final district
    visualize(district_states,district_int+1,True)

    # A dictionary to store all costs
    all_costs = {}

    # The best depth for this district
    best_depth = None

    # The lowest final cost for this district
    lowest_final_cost = float('inf')
    
    # Store all costs for this district
    all_costs[district_int] = costs

    # Determine if this is the best depth
    if costs[-1] < lowest_final_cost:
        lowest_final_cost = costs[-1]
        best_depth = district_int

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
    
