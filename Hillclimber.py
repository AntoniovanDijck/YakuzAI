import random
from code.algorithm.dijckstra import dijckstra as dijckstra
from code.classes.district import District
import copy
from code.helpers.visualize import visualize


class HillClimber:
    """
    Hillclimber algorithm to optimize the order of houses connected to batteries
    """
    def __init__(self, district, depth=1, iterations=1000):
        self.district = district
        self.depth = depth
        self.iterations = iterations

    def calculate_total_cost(self):
        return self.district.calculate_totals()

    def save_state(self):
        # Create a deep copy of the district's current state
        return copy.deepcopy(self.district)

    def restore_state(self, saved_state):
        # Restore the district's state from the saved state
        self.district = saved_state

    def modify_house_order(self):
        removed_houses = []
        for _ in range(self.depth):
            connected_battery = random.choice(self.district.batteries)
            if connected_battery.connected_houses:
                house = random.choice(connected_battery.connected_houses)
                removed_houses.append(house)
                self.district.remove_connected_house(house, connected_battery)

        # Reconnect all the houses that are not connected
        dijckstra_instance.connect_houses_to_batteries(removed_houses)



    def hill_climb(self):
        self.current_cost = self.calculate_total_cost()
        self.best_state = self.save_state()
        print(f'Initial cost: {self.current_cost}')

        for _ in range(self.iterations):
            saved_state = self.save_state()
            self.modify_house_order()  # Modify the order of house connections
            new_cost = self.calculate_total_cost()
            print(f'Current cost: {self.current_cost}')
            print(f'New cost: {new_cost}')

            if new_cost < self.current_cost:
                self.current_cost = new_cost
                self.saved_state = self.best_state # Update best state
                print(f'New best cost: {self.current_cost}')
            else:
                self.restore_state(saved_state)  # Revert to previous state

 
        return self.current_cost



## RUN HILLCLIMBER ###
houses_file = "simulation_results/District 1 dijckstra_lowest_cost_order.csv"
batteries_file = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'


district = District(houses_file, batteries_file)
dijckstra_instance = dijckstra(district)
dijckstra_instance.connect_houses_to_batteries()

hillclimber = HillClimber(district)
hillclimber.hill_climb()


# print("DIJCKSTRA BEST RESULTS")
# houses_file = hillclimber.hill_climb(houses_file)

# district = District(houses_file, batteries_file)

# # Apply the Greedy algorithm to connect houses to batteries
# dijckstra = dijckstra(district)
# dijckstra.connect_houses_to_batteries()

# visualize(district, 1)
