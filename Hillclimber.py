import random
from code.algorithm.dijckstra import dijckstra_max as dijckstra
from code.classes.district import District

class HillClimber:
    def __init__(self, district, depth=1, iterations=500):
        self.district = district
        self.depth = depth
        self.iterations = iterations
        self.dijckstra_max = dijckstra(district)  # Initialize dijckstra_max

    def calculate_total_cost(self):
        return district.calculate_totals()

    def modify_house_order(self):
        # Randomly remove houses
        for _ in range(self.depth):
            batteries_with_houses = [b for b in district.batteries if b.connected_houses]
            if not batteries_with_houses:
                continue

            connected_battery = random.choice(batteries_with_houses)
            if connected_battery.connected_houses:
                house = random.choice(connected_battery.connected_houses)
                district.remove_connected_house(house, connected_battery)

        # Reconnect houses using dijckstra_max
        dijckstra.connect_houses_to_batteries(self.district)

    def hill_climb(self):
        best_cost = self.calculate_total_cost()

        for _ in range(self.iterations):
            self.modify_house_order()
            new_cost = self.calculate_total_cost()
            print(f'New cost: {new_cost}')
            print(f'Best cost: {best_cost}')
            if new_cost < best_cost:
                best_cost = new_cost
                print(f'New best cost: {best_cost}')

                ### SAVE THE BEST ###
                
            else:
                ### REVERT TO THE BEST ###

        return best_cost



## RUN HILLCLIMBER ###
houses_file = 'simulation_results/dijckstra_lowest_cost_order.csv'
batteries_file = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'


district = District(houses_file, batteries_file)
dijckstra_instance = dijckstra(district)
dijckstra_instance.connect_houses_to_batteries()

hillclimber = HillClimber(dijckstra_instance)
hillclimber.hill_climb()


# print("DIJCKSTRA BEST RESULTS")
# houses_file = hillclimber.hill_climb(houses_file)

# district = District(houses_file, batteries_file)

# # Apply the Greedy algorithm to connect houses to batteries
# dijckstra = dijckstra(district)
# dijckstra.connect_houses_to_batteries()

# visualize(district, 1)
