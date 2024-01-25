#imports
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.nearest_battery import nearest_battery
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
            random_battery_instance = RandomAlgorithm(district1)
            random_battery_instance.connect_houses_to_batteries()

            count += 1
            print(count)         

            # Calculate the total costs
            total_costs = district1.calculate_totals()
            self.costs.append(total_costs)

            

        return self.costs
    
    
#run the algorithm for district 1

district1_houses = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
district1_batteries = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'

sim = Simulate_algorithm(RandomAlgorithm, 100).simulate()

#plot the sim in a simple bar chart with bins of 100, the amount of times the total costs are in a bin is the frequency
plt.hist(sim, bins=300)

# title and labels
plt.title("Random algorithm")
plt.xlabel("Total costs")
plt.ylabel("Frequency")

plt.show()

#run the algorithm for nearest battery and plot
sim = Simulate_algorithm(nearest_battery, 100).simulate()
plt.hist(sim, bins=300)

# title and labels
plt.title("Nearest battery algorithm")
plt.xlabel("Total costs")
plt.ylabel("Frequency")

plt.show()

