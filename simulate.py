#imports
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.nearest_object import nearest_object
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

            count += 1
            print(count)         

            # Calculate the total costs
            total_costs = district1.calculate_totals()
            self.costs.append(total_costs)

            

        return self.costs
    
    
#run the algorithm for district 1

district1_houses = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
district1_batteries = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'

sim_rand = Simulate_algorithm(RandomAlgorithm, 1000).simulate()

#run the algorithm for nearest battery and plot
sim_near_batt = Simulate_algorithm(nearest_battery, 1000).simulate()

#run the algorithm for nearest object and plot
sim_near_obj = Simulate_algorithm(nearest_object, 1000).simulate()

#plot the sim in a simple bar chart with bins of 100, the amount of times the total costs are in a bin is the frequency
plt.hist(sim_rand, bins=50)
plt.hist(sim_near_batt, bins=50)
plt.hist(sim_near_obj, bins=50)
# title and labels
plt.title("Random algorithm")
plt.xlabel("Total costs")
plt.ylabel("Frequency")

# indicate what color is what
plt.legend(['Random', 'Nearest battery', 'Nearest object'])

plt.show()

