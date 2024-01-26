#imports
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.nearest_object_x import nearest_object_x
import code.algorithm.nearest_object_y as nearest_object_y
from code.algorithm.nearest_object_rand import nearest_object_rand
import matplotlib.pyplot as plt


class Simulate_algorithm:
    """
    simulates x mount of itterations of a given algorithm and saves the frequency of the total costs in a list
    """
    def __init__(self, algorithm, iterations):
        self.algorithm = algorithm
        self.iterations = iterations
        self.costs = []
    
    def simulate(self):
        """
        simulates the algorithm x mount of times
        """
        count = 0
        for i in range(self.iterations):


            district1 = District(district1_houses, district1_batteries)
            # Apply the Greedy algorithm to connect houses to batteries
            algorithm_instance = self.algorithm(district1)
            algorithm_instance.connect_houses_to_batteries()


            # print the percentage of the simulation in 10% steps
            if i % (self.iterations / 10) == 0:
                count += 10
                print(f"{count}%")

            # Calculate the total costs
            total_costs = district1.calculate_totals()
            self.costs.append(total_costs)


        return self.costs
    
    
#run the algorithm for district 1

district1_houses = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
district1_batteries = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'

print("1/5")
sim_rand = Simulate_algorithm(RandomAlgorithm, 100).simulate()
print("2/5")
sim_battery = Simulate_algorithm(nearest_battery, 100).simulate()
print("3/5")
sim_object_x = Simulate_algorithm(nearest_object_x, 100).simulate()
print("4/5")
# run the algorithm for nearest battery and plot
# sim_object_y = Simulate_algorithm(nearest_object_y, 100).simulate()
print("5/5")
# run the algorithm for nearest object and plot
sim_obj_rand = Simulate_algorithm(nearest_object_rand, 100).simulate()

# plot the sim in a simple bar chart with bins of 100, the amount of times the total costs are in a bin is the frequency
plt.hist(sim_rand, bins=50)
plt.hist(sim_battery, bins=50)
plt.hist(sim_object_x, bins=50)
plt.hist(sim_object_y, bins=50)
plt.hist(sim_obj_rand, bins=50)
# title and labels
plt.title("Random algorithm")
plt.xlabel("Total costs")
plt.ylabel("Frequency")

# indicate what color is what
plt.legend(["Random", "Nearest battery", "Nearest object x", "Nearest object rand"])

plt.show()

