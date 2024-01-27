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
                self.lowest_cost_house_order = [house for house in district.houses]
                is_initial_cost_set = True

        print(f"Lowest costs: {self.lowest_costs} for algorithm {self.algorithm.__name__}")

        return self.costs

    
    def get_lowest_cost_house_order(self):
        """Retrieve the house order for the lowest cost."""
        return self.lowest_cost_house_order
    


    def save_results_to_file(self, file_name_prefix, save_directory):
        """Save the results to a file in the specified directory."""
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        file_path = os.path.join(save_directory, f"{file_name_prefix}_results.json")
        results = {
            'lowest_cost': self.lowest_costs,
            'house_order': [(house.x, house.y) for house in self.lowest_cost_house_order]
        }
        with open(file_path, 'w') as file:
            json.dump(results, file, indent=4)



def experiment(houses_file, batteries_file, iterations=100):


    # Create instances for each algorithm
    sim_rand_instance = simulate_algorithm(RandomAlgorithm, iterations, houses_file, batteries_file)
    sim_battery_instance = simulate_algorithm(nearest_battery, iterations, houses_file, batteries_file)
    sim_object_x_instance = simulate_algorithm(nearest_object_x, iterations, houses_file, batteries_file)
    sim_object_y_instance = simulate_algorithm(nearest_object_y, iterations, houses_file, batteries_file)
    sim_obj_rand_instance = simulate_algorithm(nearest_object_rand, iterations, houses_file, batteries_file)

    # Run simulations
    print("1/5")
    sim_rand = sim_rand_instance.simulate()
    print("2/5")
    sim_battery = sim_battery_instance.simulate()
    print("3/5")
    sim_object_x = sim_object_x_instance.simulate()
    print("4/5")
    sim_object_y = sim_object_y_instance.simulate()
    print("5/5")
    sim_obj_rand = sim_obj_rand_instance.simulate()

    # Determine the common range for all histograms
    all_values = sim_rand | sim_battery | sim_object_x | sim_obj_rand
    min_value, max_value = min(all_values), max(all_values)

    # Standardize bin edges
    bins = np.linspace(min_value, max_value, int(np.sqrt(iterations)))

    # Plot the histograms
    plt.hist(sim_rand, bins=bins, alpha=0.5)
    plt.hist(sim_battery, bins=bins, alpha=0.5)
    plt.hist(sim_object_x, bins=bins, alpha=0.5)
    plt.hist(sim_object_y, bins=bins, alpha=0.5)
    plt.hist(sim_obj_rand, bins=bins, alpha=0.5)

    # Title and labels
    plt.title(f"Comparison of Algorithms with {iterations} iterations")
    plt.xlabel("Total Costs")
    plt.ylabel("Frequency")

    # Legend
    plt.legend(["Random", "Nearest Battery", "Nearest Object X", "Nearest Object Y", "Nearest Object Rand"])

    # plt.show()

    # Define the directory to save the results
    save_directory = "simulation_results"

    # Save results for each algorithm
    save_directory = "simulation_results"
    sim_rand_instance.save_results_to_file("random_algorithm", save_directory)
    sim_battery_instance.save_results_to_file("nearest_battery", save_directory)
    sim_object_x_instance.save_results_to_file("nearest_object_x", save_directory)
    sim_object_y_instance.save_results_to_file("nearest_object_y", save_directory)
    sim_obj_rand_instance.save_results_to_file("nearest_object_rand", save_directory)

    # Save the figure
    plt.savefig(os.path.join(save_directory, "simulation_histogram.png"))   


# run the algorithm for district 1
district1_houses = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
district1_batteries = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'

experiment(district1_houses, district1_batteries,iterations = 10)


