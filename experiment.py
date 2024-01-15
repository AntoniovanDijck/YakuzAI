import numpy as np
import csv
from code.house import House, Cable
from code.battery import Battery
from code.smart_grid import load_battery_data, load_house_data

class Experiment:
    """
    Class the runs a single district as an experiment. 
    """
    def __init__(self, houses_file, batteries_file):
        """
        Creates a dictionary and loads in houses and batteries in a dictionary and creates a list of houses and batteries
        """

        # load data and save them in a dictionary
        house_dict = load_house_data(houses_file)
        battery_dict = load_battery_data(batteries_file)

        # create lists of houses and batteries and save them as attributes
        self.houses = [House(x, y, maxoutput) for (x, y), maxoutput in house_dict.items()]
        self.batteries = [Battery(x, y, capacity) for (x, y), capacity in battery_dict.items()]

        # create a list for the cables
        self.cables = []

        # connect houses to batteries
        self.connect_houses_to_batteries()


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

    def connect_houses_to_batteries(self):
        """
        method that connects houses to batteries
        """
        # create empty set for cables to make sure there are no duplicates
        unique_cables = set()

        # loop over houses
        for house in self.houses:
            
            # Find the nearest battery
            nearest_battery = min(self.batteries, key=lambda battery: abs(battery.x - house.x) + abs(battery.y - house.y))
            
            # Generate individual cable pieces for the x axis and add them to the set
            for x in range(min(house.x, nearest_battery.x), max(house.x, nearest_battery.x)):
                cable = Cable(x, house.y, x+1, house.y)
                unique_cables.add(cable)

            # Generate individual cable pieces for the y axis and add them to the set
            for y in range(min(house.y, nearest_battery.y), max(house.y, nearest_battery.y)):
                cable = Cable(nearest_battery.x, y, nearest_battery.x, y+1)
                unique_cables.add(cable)

            # Connect the house to the battery
            nearest_battery.connect_house(house)
        
        # Save the cables as a list
        self.cables = list(unique_cables)

    """
    This method returns a set of cables that are part of the route from a house to a battery
    """
    def get_cables_for_route(self, house, battery):
        route_cables = set()

        # Generate horizontal cable segments
        for x in range(min(house.x, battery.x), max(house.x, battery.x)):
            cable = Cable(x, house.y, x + 1, house.y)
            route_cables.add(cable)

        # Generate vertical cable segments
        for y in range(min(house.y, battery.y), max(house.y, battery.y)):
            cable = Cable(battery.x, y, battery.x, y + 1)
            route_cables.add(cable)

        return route_cables


    def is_cable_connected_to_battery(self, cable, battery):
        """
        This method checks if a cable is connected to a battery
        """
        
        # Check if a cable end point is at the battery location
        return ((cable.end_x, cable.end_y) == (battery.x, battery.y) or
                (cable.start_x, cable.start_y) == (battery.x, battery.y))
    
    def calculate_totals(self):
        """
        Calculates the total output and total cables used per battery
        """

        # Loop over batteries
        for battery in self.batteries:

            # Calculate total output for this battery
            total_output = sum(house.maxoutput for house in battery.connected_houses)

            # Count unique cables for this battery
            battery_cables = set()

            for house in battery.connected_houses:

                # Add all cables that are part of the route from this house to the battery
                battery_cables.update(self.get_cables_for_route(house, battery))

            total_cables = len(battery_cables)
            print(f'Battery at ({battery.x}, {battery.y}):')
            print(f'  Total output connected: {total_output}')
            print(f'  Total cables used: {total_cables}')

battery_district1_link = 'Huizen&Batterijen/district_1/district-1_batteries.csv'
house_district1_link = 'Huizen&Batterijen/district_1/district-1_houses.csv'
experiment = Experiment(house_district1_link, battery_district1_link)
experiment.calculate_totals()
