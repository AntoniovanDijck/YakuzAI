#imports
from code.classes.district import District
import json
import os
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.nearest_object_x import nearest_object_x
from code.algorithm.nearest_object_y import nearest_object_y
from code.algorithm.nearest_object_rand import nearest_object_rand
import matplotlib.pyplot as plt
import csv
import numpy as np

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
        Simulates the algorithm x number of times, optimized for efficiency.
        """
        self.costs = set()  # Using a set for unique total costs
        progress_step = self.iterations // 10
        is_initial_cost_set = self.lowest_costs != 0

        for i in range(self.iterations):
            district = District(self.houses_file, self.batteries_file)
            algorithm_instance = self.algorithm(district)
            algorithm_instance.connect_houses_to_batteries()

            # Efficient progress reporting
            if i % progress_step == 0:
                print(f"{(i // progress_step) * 10}%")

            total_costs = district.calculate_totals()

            self.costs.add(total_costs)

            if not is_initial_cost_set or total_costs < self.lowest_costs:
                self.lowest_costs = total_costs
                self.lowest_district = district
                self.lowest_cost_house_order = [(house.x, house.y, house.maxoutput) for house in district.houses]

                is_initial_cost_set = True

        print(f"Lowest costs: {self.lowest_costs} for algorithm {self.algorithm.__name__}")

        return self.costs

    
    def get_lowest_cost_house_order(self):
        """Retrieve the house order for the lowest cost."""
        return self.lowest_cost_house_order
    

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

    print("5/5: Running nearest_object_rand Simulation")
    sim_obj_rand = sim_obj_rand_instance.simulate()
    csv_filename_obj_rand = os.path.join(save_directory, 'nearest_object_rand_lowest_cost_order.csv')
    sim_obj_rand_instance.save_lowest_cost_house_order_to_csv(csv_filename_obj_rand)

    # Plotting and saving the histogram
    all_values = sim_rand | sim_battery | sim_object_x | sim_object_y | sim_obj_rand
    min_value, max_value = min(all_values), max(all_values)
    bins = np.linspace(min_value, max_value, int(np.sqrt(iterations)))

    plt.hist(sim_rand, bins=bins, alpha=0.5)
    plt.hist(sim_battery, bins=bins, alpha=0.5)
    plt.hist(sim_object_x, bins=bins, alpha=0.5)
    plt.hist(sim_object_y, bins=bins, alpha=0.5)
    plt.hist(sim_obj_rand, bins=bins, alpha=0.5)
    plt.title(f"Comparison of Algorithms with {iterations} iterations")
    plt.xlabel("Total Costs")
    plt.ylabel("Frequency")
    plt.legend(["Random", "Nearest Battery", "Nearest Object X", "Nearest Object Y", "Nearest Object Rand"])
    plt.savefig(os.path.join(save_directory, "simulation_histogram.png"))
 


# run the algorithm for district 1
district1_houses = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
district1_batteries = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'

experiment(district1_houses, district1_batteries,iterations = 100)


