import random
from code.algorithm.dijckstra import dijckstra as dijckstra
from code.algorithm.nearest_battery import nearest_battery as NB
from code.classes.district import District
import copy
from code.helpers.visualize import visualize
from code.classes.cable import Cable
from code.classes.battery import Battery
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


class HillClimber:
    """
    Hillclimber algorithm to optimize the order of houses connected to batteries by removing depth amount of houses and reconnecting them.
    """

    # Setting the initial values for the depth and iterations
    def __init__(self, district, depth = 4, iterations=100):
        self.district = district
        self.depth = depth
        self.iterations = iterations


    # Calculate the total cost of a district using the calculate_totals method from the district class
    def calculate_total_cost(self):
        return self.district.calculate_totals()

    # Save a copy of the district's current state in case it needs to be restored
    def save_state(self):
        return copy.deepcopy(self.district)

    # Restore the district's state to the saved state
    def restore_state(self, saved_state):
        self.district = saved_state


    def modify_house_order(self):
        """
        Remove depth amount of random houses from the district. Then reconnected using the logic from Dijckstsra's algorithm..
        """
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
                self.district.remove_connected_house(house, connected_battery)


            # Reconnect all the houses that are not connected
            self.connect_houses_to_batteries(removed_houses)



    def find_nearest_object_x(self, house):
        """
        This method finds the nearest battery or cable to a house.
        """

        # Create a list of all batteries and cables
        objects = self.district.batteries + list(self.district.cables.values())


        def distance_to_object(obj):
            """
            Using this function as a key for the sorted function, we can sort the objects by distance to the house.
            """

            # Check if the object is a battery or a cable
            if isinstance(obj, Battery):

                # Distance from house to battery
                return abs(obj.x - house.x) + abs(obj.y - house.y)

            elif isinstance(obj, Cable):

                # Distance from house to the closest start of the cable
                distances = [abs(house.x - obj.start_x) + abs(house.y - obj.start_y), abs(house.x - obj.end_x) + abs(house.y - obj.end_y)]
                return min(distances)


        # Sort the objects by distance
        sorted_objects = sorted(objects, key=distance_to_object)

        return sorted_objects


    def connect_houses_to_batteries(self, houses):
        """
        This method connects houses to batteries. It does this by finding the nearest battery or cable to a house. If
        this object is a battery, it checks if the battery has the capacity to connect the house. If this object is a
        cable, it checks if the battery connected to the cable has the capacity to connect the house. If the battery
        has the capacity.
        """

        # Shuffle the houses to prevent the algorithm from always connecting the same houses to the same batteries
        random_houses = houses
        #print(houses)

        # Loop over all houses
        for house in random_houses:

            # Find the nearest battery or cable to the house
            sorted_objects = self.find_nearest_object_x(house)

            # Loop over all objects sorted by distance to the house
            for object in sorted_objects:

                # Check if the object is a battery or a cable
                if isinstance(object, Battery):

                    # Check if the battery has the capacity to connect the house
                    if object.can_connect(house):

                        # Place cables and connect to the battery
                        self.place_cables(house, object)
                        object.connect_house(house)
                        break

                    # If the battery does not have the capacity, continue to the next object
                    else:
                        continue

                # Check if the object is a cable
                elif isinstance(object, Cable):

                    # Check if the cable is connected to a battery
                    connected_battery = object.connected_battery

                    # Check if the connected_battery is a battery class to prevent errors
                    if isinstance(connected_battery, Battery):

                        # Place cables and connect to the cable, which routes to the battery
                        if connected_battery.can_connect(house):

                            # Place cables and connect to the battery
                            self.place_cables(house, object)

                            # To keep track of the cables that are used to connect houses to batteries, the overlapping
                            # cables need to be tracked as well
                            self.extend_route_to_battery(house, object, connected_battery)

                            # Connect house to the battery
                            connected_battery.connect_house(house)

                            # Break out of the loop as the house is connected
                            break

                        else:
                            continue
                    else:
                        while True:
                            for alternative_battery in self.district.batteries:
                                if alternative_battery != connected_battery and alternative_battery.can_connect(house):
                                    self.place_cables(house, alternative_battery)
                                    alternative_battery.connect_house(house)
                                    break
                            else:  
                                # Remove the house with the longest y route
                                house = max(connected_battery.connected_houses, key=lambda y: len(y.route))


                                # remove the house from the battery
                                self.district.remove_connected_house(house, connected_battery)
                                house.route = []
                                break
                                # Check of there are more or less than 150 houses connected to batteries, if so, restore the state
            total_houses = 0
            for battery in self.district.batteries:
                total_houses += len(battery.connected_houses)
            if total_houses != 150:
                saved_state = self.save_state()
                self.restore_state(saved_state)



    def place_cables(self, house, object):
        """
        This method places cables between houses and batteries. It does this by placing cables along the x-axis and the
        y-axis. It does this by checking the x and y coordinates of the house and the battery. It then places cables
        between these coordinates.
        """
        # Place cable along x-axis
        if isinstance(object, Cable):
            object = object.connected_battery

        x_distance = abs(house.x - object.x)
        y_distance = abs(house.y - object.y)

        if x_distance > y_distance:
            if house.x != object.x:
                x_start, x_end = sorted([house.x, object.x])

                # Create a new cable segment for each unit along the x-axis
                for x in range(x_start, x_end):
                    cable_id = f"{x},{object.y},{x+1},{object.y}"
                    self.district.place_cables(x, object.y, x + 1, object.y, object)
                    house.route.append(cable_id)

            # Place cable along y-axis
            if house.y != object.y:
                y_start, y_end = sorted([house.y, object.y])

                # Create a new cable segment for each unit along the y-axis
                for y in range(y_start, y_end):
                        cable_id = f"{house.x},{y},{house.x},{y+1}"
                        self.district.place_cables(house.x, y, house.x, y + 1, object)
                        house.route.append(cable_id)
        else:
            # Place cable along x-axis
            if house.x != object.x:
                x_start, x_end = sorted([house.x, object.x])
                for x in range(x_start, x_end):
                    # Create a new cable segment for each unit along the x-axis
                    cable_id = f"{x},{house.y},{x+1},{house.y}"
                    self.district.place_cables(x, house.y, x + 1, house.y, object)
                    house.route.append(cable_id)

            # Place cable along y-axis
            if house.y != object.y:
                y_start, y_end = sorted([house.y, object.y])
                for y in range(y_start, y_end):
                    
                    # Create a new cable segment for each unit along the y-axis
                    cable_id = f"{object.x},{y},{object.x},{y+1}"
                    self.district.place_cables(object.x, y, object.x, y + 1, object)
                    house.route.append(cable_id)
            



    def extend_route_to_battery(self, house, cable, battery):
        """
        Extends the route from the cable to the connected battery.
        """

        # Place cable along x-axis from cable end to battery
        if cable.end_x != battery.x:

            # Sort the x coordinates from the cable and the battery
            x_start, x_end = sorted([cable.end_x, battery.x])

            # Loop over the x coordinates
            for x in range(x_start, x_end):

                cable_id = f"{x},{cable.end_y},{x+1},{cable.end_y}"
                self.district.place_cables(x, cable.end_y, x + 1, cable.end_y, battery)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(cable_id)


        # Place cable along y-axis from cable end to battery
        if cable.end_y != battery.y:

            # Sort the y coordinates from the cable and the battery
            y_start, y_end = sorted([cable.end_y, battery.y])
            for y in range(y_start, y_end):

                # Create a new cable segment for each unit along the y-axis
                cable_id = f"{battery.x},{y},{battery.x},{y+1}"
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)
                # Keep track of the route of the house by adding the cable id to the route



    def hill_climb(self):
        self.current_cost = self.calculate_total_cost()
        costs = [self.current_cost]  # Initialize list to store costs
        saved_districts = []
        
        for iteration in tqdm(range(self.iterations), desc="Climbing the hill: "):
            saved_state = self.save_state()
            self.modify_house_order()
            new_cost = self.calculate_total_cost()

            if new_cost < self.current_cost:
                self.current_cost = new_cost
                self.saved_state = self.district
                # print(f"New cost: {self.current_cost}")
            else:
                self.restore_state(saved_state)

            costs.append(self.current_cost)  # Store cost after each iteration

            if iteration % 250 == 0:
                plt.cla()
                visualize(saved_state, iteration, True)
                plt.pause(0.0001)

        return costs, saved_state# Return the list of costs




## DEPTH TEST ALGORITHM ##
# all_costs = {}
# best_depth = None
# lowest_final_cost = float('inf')

# for i in range(1,6):
#     houses_file = "simulation_results/District 1 dijckstra_lowest_cost_order.csv"
#     batteries_file = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'


#     district = District(houses_file, batteries_file)
#     dijckstra_instance = dijckstra(district)
#     dijckstra_instance.connect_houses_to_batteries()

#     hillclimber = HillClimber(district, i, 100)
#     costs = hillclimber.hill_climb()
#     all_costs[i] = costs

#     # Determine if this is the best depth
#     if costs[-1] < lowest_final_cost:
#         lowest_final_cost = costs[-1]
#         best_depth = i

# # Set plot with a black background
# plt.figure(figsize=(10, 6), facecolor='black')
# ax = plt.axes()
# ax.set_facecolor('black')

# # Plot all costs, highlight the best one in red
# for depth, costs in all_costs.items():
#     plt.plot(costs, color='red' if depth == best_depth else 'lime', linestyle='-', linewidth=2 if depth == best_depth else 1, label=f'Depth {depth}' if depth == best_depth else None)

# plt.xlabel('Iterations', fontsize=14, fontweight='bold', color='white')
# plt.ylabel('Total Cost', fontsize=14, fontweight='bold', color='white')
# plt.title('Hill Climber Optimization Progress', fontsize=16, fontweight='bold', color='white')
# plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7, color='gray')
# plt.xticks(fontsize=12, color='white')
# plt.yticks(fontsize=12, color='white')

# plt.gca().invert_yaxis()

# # Add legend to show the best depth
# plt.legend(fontsize=12, facecolor='black', edgecolor='black', labelcolor='white')
# plt.tight_layout()

# plt.show()






# ## RUNNING 1 DEPTH ##
# houses_file = "simulation_results/District 1 dijckstra_lowest_cost_order.csv"
# batteries_file = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'
# district = District(houses_file, batteries_file)
# dijckstra_instance = dijckstra(district)
# dijckstra_instance.connect_houses_to_batteries()
# hillclimber = HillClimber(district, 4, 200)
# costs, saved_district = hillclimber.hill_climb()

# visualize_route(saved_district,994)



