# find_lowest_cost_experiment.py
# Antonio, Mec, Vincent
# YakuzAI

import os
import numpy as np  
import matplotlib.pyplot as plt
from code.algorithm.DijckstraAlgorithm import DijckstraAlgorithm as dijckstra
from code.algorithm.RandomAlgorithm import RandomAlgorithm
from code.experiments.Simulate_Algorithm import Simulate_Algorithm
from code.algorithm.Greedy_Battery_Distance import Greedy_Battery_Distance as nearest_battery
from code.algorithm.Greedy_Object_Distance import Greedy_Object_Distance as nearest_object_x
from code.algorithm.Greedy_Object_Distance_Reversed import Greedy_Object_Distance_Reversed as nearest_object_y
from code.algorithm.Greedy_Object_Distance_Randomized import Greedy_Object_Distance_Randomized as nearest_object_rand


def find_lowest_cost_experiment(houses_file, batteries_file, iterations=100,algorithms=[dijckstra]):
    """
    the experiment function runs the simulation for each algorithm and saves the results in a csv file and plots a histogram of the resultings costs
    the input is the filepaths of the houses and batteries, the amount of iterations and the algorithms to be tested
    """

    # Number of algorithms to test
    count = 1

    # Directory to save the csv files
    save_directory = "data/output_data/algorithm_results"

    # List to store the data for each algorithm
    data_to_plot = []

    # Variables to store the lowest cost and district
    lowest_district = None
    lowest_cost = float('inf')

    # If the directory does not exist, create it first
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Create instances for each algorithm
    for i in range(len(algorithms)):

        # Instance of the algorithm
        alg = algorithms[i]

        # Print the algorithm name and number
        print(f"{count}/{len(algorithms)}: Running {alg.__name__} Simulation")
        
        # Create instances for each algorithm
        algorithm_instance = Simulate_Algorithm(alg, iterations, houses_file, batteries_file)
        
        # Run the simulation
        sim_alg = algorithm_instance.simulate()

        count += 1
        
        # CSV filename
        csv_filename = os.path.join(save_directory, f'{alg.__name__}_lowest_cost_order.csv')
        print("")

        # Save the results to a CSV file
        algorithm_instance.save_lowest_cost_house_order_to_csv(csv_filename)
        
        if algorithm_instance.lowest_costs < lowest_cost:
            lowest_cost = algorithm_instance.lowest_costs
            lowest_district = algorithm_instance.lowest_district

        # Convert the sets of costs to lists
        sim_alg_list = list(sim_alg)
        data_to_plot.append(sim_alg_list)

    # Find the global minimum and maximum to set the bins
    min_value = min(map(min, data_to_plot))
    max_value = max(map(max, data_to_plot))

    # Determine the number of bins to use
    number_of_bins = int(np.sqrt(iterations))  # Experiment with this value

    # Create evenly spaced bins from the min to max value
    bins = np.linspace(min_value, max_value, number_of_bins)

    # Increase figure size
    plt.figure(figsize=(12, 8))  # Width, Height in inches

    # Using the "tab10" colorpallet, as it should work with the overlapping colors and is colorblind friendly
    colors = plt.cm.tab10(np.linspace(0, 1, 10))

    # Plot each algorithm's histogram
    labels = [str(alg.__name__) for alg in algorithms]

    for i, (data, label) in enumerate(zip(data_to_plot, labels)):
        plt.hist(data, bins=bins, alpha=0.5, color=colors[i], label=label)

    # Add grid
    plt.grid(True)

    # Rotate x-axis labels if they are overlapping
    plt.xticks(rotation=45)

    # Increase font size for labels and title
    plt.xlabel("Total Costs", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.title(f"Comparison of Algorithms with {iterations} iterations", fontsize=16)

    # Increase font size for legend and place it outside the plot area
    plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.1, 1))

    # Show the plot
    plt.show()  
    
    return lowest_district