import random
from code.algorithm.dijckstra import dijckstra_max as dijckstra
from code.classes.district import District
import copy


class HillClimber:
    """
    Hillclimber algorithm to optimize the order of houses connected to batteries
    """
    def __init__(self, district, depth=1, iterations=500):
        self.district = district
        self.depth = depth
        self.iterations = iterations
        self.dijckstra_max = dijckstra(district)

    def calculate_total_cost(self):
        return district.calculate_totals()

    def save_state(self):
        # Create a deep copy of the district's current state
        return copy.deepcopy(self.district)

    def restore_state(self, saved_state):
        # Restore the district's state from the saved state
        self.district = saved_state

    def modify_house_order(self):
        for _ in range(self.depth):
            batteries_with_houses = [b for b in district.batteries if b.connected_houses]
            if not batteries_with_houses:
                continue

            connected_battery = random.choice(batteries_with_houses)
            if connected_battery.connected_houses:
                house = random.choice(connected_battery.connected_houses)
                district.remove_connected_house(house, connected_battery)

        for _ in range(self.depth):
            batteries_without_houses = [b for b in district.batteries if not b.connected_houses]
            if not batteries_without_houses:
                continue

            battery = random.choice(batteries_without_houses)
            house = random.choice(district.houses)
            dijckstra.connect_houses_to_batteries(self.district)

    def hill_climb(self):
        best_cost = self.calculate_total_cost()
        best_state = self.save_state()

        for _ in range(self.iterations):
            saved_state = self.save_state()  # Save current state
            self.modify_house_order()
            new_cost = self.calculate_total_cost()
            print(f'New cost: {new_cost}')
            print(f'Best cost: {best_cost}')

            if new_cost < best_cost:
                best_cost = new_cost
                best_state = saved_state  # Update best state
                print(f'New best cost: {best_cost}')
            else:
                self.restore_state(saved_state)  # Revert to previous state

        # After finishing, restore the best state found
        self.restore_state(best_state)
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
