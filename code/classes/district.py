# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import Cable
from code.helpers.smart_grid import load_battery_data, load_house_data

class District:
    """
    Class that creates a district with houses and batteries
    """
    def __init__(self, houses_file, batteries_file):
        # Load houses and batteries
        house_dict = load_house_data(houses_file)
        battery_dict = load_battery_data(batteries_file)

        # Create houses and batteries using the data
        self.houses = [House(x, y, maxoutput) for (x, y), maxoutput in house_dict.items()]
        self.batteries = [Battery(x, y, capacity) for (x, y), capacity in battery_dict.items()]
        self.cables = []


    def load_houses(self, file_path):
        """
        This method loads in the houses from a csv file and returns a list of houses
        """

        # create empty list for houses
        houses = []

        # open file and read in the data
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house = House(int(row['x']), int(row['y']), float(row['maxoutput']))
                houses.append(house)
        return houses

    def load_batteries(self, file_path):
        """
        This method loads in the batteries from a csv file and returns a list of batteries
        """

        # create empty list for batteries
        batteries = []
    
        # open file and read in the data and create batteries
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                x, y = map(int, row['positie'].split(','))
                battery = Battery(x, y, float(row['capaciteit']))
                batteries.append(battery)
        return batteries


    def find_nearest_battery(self, house):
        """
        Finds the nearest battery to house using the manhattan distance
        """
        return min(self.batteries, key=lambda battery: abs(battery.x - house.x) + abs(battery.y - house.y))
    
        
    def find_closest_cable(self, house):
        """
        Finds the closest cable to a house and returns the cable and the distance
        """

        closest_cable = None
        min_distance = float('inf')

        # Find closest cable.
        for cable in self.cables:
            # Check distance from the house to the cable's endpoints
            distances = [
                abs(house.x - cable.start_x) + abs(house.y - cable.start_y),
                abs(house.x - cable.end_x) + abs(house.y - cable.end_y)
            ]
            
            # Find the minimum distance for this cable
            distance = min(distances)
            
            # If this is the shortest distance, update closest_cable and min_distance
            if distance < min_distance:
                min_distance = distance
                closest_cable = cable

        return closest_cable, min_distance

    def place_cables(self, start_x, start_y, end_x, end_y, battery=None):
        """
        This method places a cable between two points and adds it to the list of cables
        """

    
        # Create a unique cable id
        cable_id = f"{start_x},{start_y}-{end_x},{end_y}"

        # Check if the cable with this id already exists
        if not any(cable.id == cable_id for cable in self.cables):

            # Create a new cable with the given coordinates
            new_cable = Cable(start_x, start_y, end_x, end_y, battery)

            # Add the cable to the list of cables
            self.cables.append(new_cable)


    def is_cable_connected_to_battery(self, cable, battery):
        """
        This method checks if a cable is connected to a battery
        """

        # Check if a cable end point is at the battery location
        return ((cable.end_x, cable.end_y) == (battery.x, battery.y) 
                or
                (cable.start_x, cable.start_y) == (battery.x, battery.y))
    
    def calculate_totals(self):
        """
        This method calculates the total cost and total output of the district
        """

        # Initialize variables
        total_cost = 0
        unique_cable_ids = set()  

        # Loop over all batteries
        for battery in self.batteries:

            # Add the battery cost to the total cost
            total_cost += 5000

            # Loop over all houses connected to the battery
            for house in battery.connected_houses:

                # Add the cost of the cable to the total cost
                for cable in house.route:
                    unique_cable_ids.add(cable)  # Add unique cable IDs

        # Calculate the total amount of unique cables
        total_cables = len(unique_cable_ids)

        # Add the cost of the cables to the total cost
        total_cost += total_cables * 9 

        # Calculate the total output of the district
        total_output = sum(house.maxoutput for house in battery.connected_houses)


        # Print the results
        print(f'Battery at ({battery.x}, {battery.y}):')
        print(f'  Total output connected: {total_output}')
        print(f'  Total cables used: {total_cables}')
        
        print(f'  Total cost: {total_cost}')

        return total_cost
    
    def check_50(self): 
        """"""
        output_data = []

        for battery in self.batteries:
            battery_data = {
                "position": f"{battery.x},{battery.y}",
                "capacity": battery.capacity,
                "houses": [] 
            }


            for house in battery.connected_houses:
                #generate cables for each house
                cables = house.route

                cable_data = cables
                house_data = {
                    "location": f"{house.x}, {house.y}", "output": house.maxoutput, "cables": cable_data
                }

                battery_data['houses'].append(house_data)
            
            output_data.append(battery_data)

        cost_own = self.calculate_totals()
        cost_shared = 0 # for now zero but here should be the cost of the grid when houses can use the same cables to be connected
        output_data.insert(0, {"district":1, "cost-own": cost_own})

        return output_data
    