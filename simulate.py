#imports
from code.classes.district import District
import json
import os
from code.algorithm.random_alg import RandomAlgorithm as RandomAlgorithm
from code.algorithm.nearest_battery import nearest_battery as nearest_battery
from code.algorithm.nearest_object_x import nearest_object_x as nearest_object_x
from code.algorithm.nearest_object_y import nearest_object_y as nearest_object_y
from code.algorithm.nearest_object_rand import nearest_object_rand as nearest_object_rand
from Hillclimber import HillClimber
import matplotlib.pyplot as plt
from code.algorithm.dijckstra import dijckstra
from code.helpers.visualize import visualize
from code.helpers.visualize import visualize_live
import csv
import numpy as np
from tqdm import tqdm

from tqdm import tqdm

class simulate_algorithm:
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
        self.costs = set() # Using a set for unique total costs
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

            self.costs.add(total_costs)
 
            if not is_initial_cost_set or total_costs < self.lowest_costs:
                self.lowest_costs = total_costs
                self.lowest_district = district
                
                self.lowest_cost_house_order = [(house.x, house.y, house.maxoutput) for house in district.houses]

                is_initial_cost_set = True

        districtname = self.houses_file.split('/')[2].split('_')[1]

        visualize(self.lowest_district,int(districtname))
        visualize_live(self.lowest_district, int(districtname))
        print(f"Lowest costs: {self.lowest_costs} for algorithm {self.algorithm.__name__}")


        district = None

        return self.costs



    def get_lowest_cost_house_order(self):
        """Retrieve the house order for the lowest cost."""
        return self.lowest_cost_house_order
    
    def get_lowest_district(self):
        """Retrieve the district for the lowest cost."""
        return self.lowest_district


    def save_lowest_cost_house_order_to_csv(self, file_name):
        """Saves the house order for the lowest cost to a CSV file."""

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['x', 'y', 'maxoutput'])  # Header

            for house in self.lowest_cost_house_order:
                writer.writerow(house)

def experiment(houses_file, batteries_file, iterations=100):
    # Create instances for each algorithm
    sim_rand_instance = simulate_algorithm(RandomAlgorithm, iterations, houses_file, batteries_file)
    sim_battery_instance = simulate_algorithm(nearest_battery, iterations, houses_file, batteries_file)
    sim_object_x_instance = simulate_algorithm(nearest_object_x, iterations, houses_file, batteries_file)
    sim_object_y_instance = simulate_algorithm(nearest_object_y, iterations, houses_file, batteries_file)
    sim_obj_rand_instance = simulate_algorithm(nearest_object_rand, iterations, houses_file, batteries_file)
    sim_dijckstra_instance = simulate_algorithm(dijckstra, iterations, houses_file, batteries_file)
    # Define the directory to save the results
    save_directory = "simulation_results"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Run simulations and save results for each algorithm
    print("1/5: Running RandomAlgorithm Simulation")
    sim_rand = sim_rand_instance.simulate()
    csv_filename_rand = os.path.join(save_directory, 'random_algorithm_lowest_cost_order.csv')
    sim_rand_instance.save_lowest_cost_house_order_to_csv(csv_filename_rand)

    print("2/5: Running nearest_battery Simulation")
    sim_battery = sim_battery_instance.simulate()
    csv_filename_battery = os.path.join(save_directory, 'nearest_battery_lowest_cost_order.csv')
    sim_battery_instance.save_lowest_cost_house_order_to_csv(csv_filename_battery)

    # Repeat for other algorithms
    print("3/5: Running nearest_object_x Simulation")
    sim_object_x = sim_object_x_instance.simulate()
    csv_filename_object_x = os.path.join(save_directory, 'nearest_object_x_lowest_cost_order.csv')
    sim_object_x_instance.save_lowest_cost_house_order_to_csv(csv_filename_object_x)

    print("4/5: Running nearest_object_y Simulation")
    sim_object_y = sim_object_y_instance.simulate()
    csv_filename_object_y = os.path.join(save_directory, 'nearest_object_y_lowest_cost_order.csv')
    sim_object_y_instance.save_lowest_cost_house_order_to_csv(csv_filename_object_y)

    print("5/6: Running nearest_object_rand Simulation")
    sim_obj_rand = sim_obj_rand_instance.simulate()
    csv_filename_obj_rand = os.path.join(save_directory, 'nearest_object_rand_lowest_cost_order.csv')
    sim_obj_rand_instance.save_lowest_cost_house_order_to_csv(csv_filename_obj_rand)

    print("6/6: Running dijckstra Simulation")
    sim_dijckstra = sim_dijckstra_instance.simulate()
    csv_filename_dijckstra = os.path.join(save_directory, 'dijckstra_lowest_cost_order.csv')
    sim_dijckstra_instance.save_lowest_cost_house_order_to_csv(csv_filename_dijckstra)

    # Convert the sets of costs to lists
    sim_rand_list = list(sim_rand)
    sim_battery_list = list(sim_battery)
    sim_object_x_list = list(sim_object_x)
    sim_object_y_list = list(sim_object_y)
    sim_obj_rand_list = list(sim_obj_rand)
    sim_dijckstra_list = list(sim_dijckstra)

    # Convert the sets of costs to lists
    sim_rand_list = list(sim_rand)
    sim_battery_list = list(sim_battery)
    sim_object_x_list = list(sim_object_x)
    sim_object_y_list = list(sim_object_y)
    sim_obj_rand_list = list(sim_obj_rand)
    sim_dijckstra_list = list(sim_dijckstra)

    # Combine the lists into a list of lists for the histogram
    data_to_plot = [sim_rand_list, sim_battery_list, sim_object_x_list, sim_object_y_list, sim_obj_rand_list, sim_dijckstra_list]

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
    labels = ["Random", "Nearest Battery", "Nearest Object X", "Nearest Object Y", "Nearest Object Rand", "Dijckstra"]
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

    # Save the figure with a higher resolution
    # plt.savefig(os.path.join(save_directory, "simulation_histogram.png"), dpi=300)

    plt.show()  # If you want to display the plot as well