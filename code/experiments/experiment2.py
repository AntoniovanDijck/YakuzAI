import os
import numpy as np  
import matplotlib.pyplot as plt
from code.algorithm.dijckstra import dijckstra
from code.algorithm.random_alg import RandomAlgorithm
from code.experiments.simulate_algorithm import Simulate_Algorithm
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.nearest_object_x import nearest_object_x
from code.algorithm.nearest_object_y import nearest_object_y
from code.algorithm.nearest_object_rand import nearest_object_rand

def experiment2(houses_file, batteries_file, iterations=100,algorithm=RandomAlgorithm):
    # Create instances for each algorithm
    sim_rand_instance = Simulate_Algorithm(algorithm, iterations, houses_file, batteries_file)
 
    # Define the directory to save the results
    save_directory = "simulation_results"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Run simulations and save results for each algorithm
    print(f"1/2: Running {algorithm.__name__} Simulation")
    sim_rand = sim_rand_instance.simulate()
    csv_filename_rand = os.path.join(save_directory, f'{algorithm.__name__}_lowest_cost_order.csv')
    sim_rand_instance.save_lowest_cost_house_order_to_csv(csv_filename_rand)

    # Plotting and saving the histogram
    all_values = sim_rand 
    min_value, max_value = min(all_values), max(all_values)
    bins = np.linspace(min_value, max_value, int(np.sqrt(iterations)))

    plt.hist(sim_rand, bins=bins, alpha=0.5)
    plt.title(f"Comparison of Algorithms with {iterations} iterations")
    plt.xlabel("Total Costs")
    plt.ylabel("Frequency")
    plt.legend(["Random", "Nearest Battery", "Nearest Object X", "Nearest Object Y", "Nearest Object Rand"])

