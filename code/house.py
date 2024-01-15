import numpy as np
import csv

from code.smart_grid import load_battery_data, load_house_data, show_district

class Cable:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def identifier(self):
        """
        Returns a unique identifier for the cable to prevent duplicates
        """
        return f"{self.start_x}-{self.start_y}-{self.end_x}-{self.end_y}"



class House():
    """
    Class that creates a house with coordinates and max output
    """
    def __init__(self, x, y, maxoutput):
        self.x = x
        self.y = y

        #houses output
        self.maxoutput = maxoutput


    #attribute that tracks connections for houses
def connect_houses_to_batteries(self):
    """
    Connects houses to batteries
    """

    # create a list for the cables to prevent duplicates
    unique_cables_identifiers = set()

    # loop over houses
    for house in self.houses:

        # find nearest battery
        nearest_battery = min(self.batteries, key=lambda battery: abs(battery.x - house.x) + abs(battery.y - house.y))

        # Create horizontal cables
        start_x, end_x = sorted([house.x, nearest_battery.x])

        # creates a cable for every x coordinate between the house and the battery
        for x in range(start_x, end_x):
            cable = Cable(x, house.y, x+1, house.y)

            # checks if the cable is already in the set
            cable_id = cable.identifier()
            if cable_id not in unique_cables_identifiers:
                unique_cables_identifiers.add(cable_id)
                self.cables.append(cable)

        # Generate vertical cables
        start_y, end_y = sorted([house.y, nearest_battery.y])

        # creates a cable for every y coordinate between the house and the battery
        for y in range(start_y, end_y):
            cable = Cable(nearest_battery.x, y, nearest_battery.x, y+1)

            # checks if the cable is already in the set
            cable_id = cable.identifier()
            if cable_id not in unique_cables_identifiers:
                unique_cables_identifiers.add(cable_id)
                self.cables.append(cable)

        # Connect the house to the battery
        nearest_battery.connect_house(house)
