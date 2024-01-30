import random
from code.algorithm.dijckstra import dijckstra as dijckstra
from code.classes.district import District
import copy
from code.helpers.visualize import visualize
from code.algorithm.nearest_battery import nearest_battery


class HillClimber:
    """
    Hillclimber algorithm to optimize the order of houses connected to batteries
    """
    def __init__(self, district, depth=1, iterations=5):
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

        # Remove a random house from a random battery
        for _ in range(self.depth):

            # select a random battery
            connected_battery = random.choice(self.district.batteries)

            # If the battery has a house connected
            if connected_battery.connected_houses:

                # Select a random house from the battery and add it to the removed houses list
                house = random.choice(connected_battery.connected_houses)
                removed_houses.append(house)

                # Remve the house from the battery
                district.remove_connected_house(house, connected_battery)

            # Reconnect all the houses that are not connected
            dijckstra_instance.connect_houses_to_batteries(removed_houses)


    def hill_climb(self):
        self.current_cost = self.calculate_total_cost()
        print(f'Initial cost: {self.current_cost}')

        for _ in range(self.iterations):

            # Save the current state
            saved_state = self.save_state()

            # Modify the state by removing and adding houses
            self.modify_house_order()  

            # Calculate the new cost 
            new_cost = self.calculate_total_cost()

            # Print the new cost
            print(f'Current cost: {self.current_cost}')
            print(f'New cost: {new_cost}')

            # Check if the new cost is better than the current cost
            if new_cost < self.current_cost:
                self.current_cost = new_cost
                self.saved_state = self.district# Update best state
                print(f'New best cost: {self.current_cost}')

            # If the new cost is not better, revert to the previous state
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
