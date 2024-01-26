#imports
from code.classes.district import District
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
        simulates the algorithm x mount of times
        """
        count = 0
        for i in range(self.iterations):


            district = District(self.houses_file, self.batteries_file)
            # Apply the Greedy algorithm to connect houses to batteries
            algorithm_instance = self.algorithm(district)
            algorithm_instance.connect_houses_to_batteries()


            # print the percentage of the simulation in 10% steps
            if i % (self.iterations / 10) == 0:
                count += 10
                print(f"{count}%")

            # Calculate the total costs
            total_costs = district.calculate_totals()

            self.costs.append(total_costs)
            if total_costs < self.lowest_costs or self.lowest_costs == 0:
                self.lowest_costs = total_costs
                self.lowest_district = district

        print(f"Lowest costs: {self.lowest_costs} for algorithm {self.algorithm.__name__}")

        return self.costs
    
    
def experiment(houses_file, batteries_file, iterations=100):


    print("1/5")
    sim_rand = simulate_algorithm(RandomAlgorithm, iterations, houses_file, batteries_file).simulate()
    print("2/5")
    sim_battery = simulate_algorithm(nearest_battery, iterations, houses_file, batteries_file).simulate()
    print("3/5")
    sim_object_x = simulate_algorithm(nearest_object_x, iterations, houses_file, batteries_file).simulate()
    print("4/5")
    # run the algorithm for nearest battery and plot
    sim_object_y = simulate_algorithm(nearest_object_y, iterations, houses_file, batteries_file).simulate()
    print("5/5")
    # run the algorithm for nearest object and plot
    sim_obj_rand = simulate_algorithm(nearest_object_rand, iterations, houses_file, batteries_file).simulate()

    # Determine the common range for all histograms
    all_values = sim_rand + sim_battery + sim_object_x + sim_obj_rand
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

    plt.show()

# run the algorithm for district 1
district1_houses = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
district1_batteries = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'

experiment(district1_houses, district1_batteries,iterations = 100000)

