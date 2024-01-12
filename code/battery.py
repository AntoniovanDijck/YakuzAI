import numpy as np
import csv

from code.smart_grid import load_battery_data, load_house_data, show_district


class Battery():
    def __init__(self, x, y, capacity):

        #coordinates
        self.x = x
        self.y = y

        # capacity of battery
        self.capacity = capacity
        
        # list of houses connected to battery per battery is stored here
        self.connected_houses = []

        # list of cables connecxted to battery per battery is stored here
        self.cables = []

    def connect_house(self, house, cable):
        if house not in self.connect_houses:
            self.connected_houses.append(house)
            self.cables.append(cable)

    def disconnect_house(self, house, cable):
        if house in self.connected_houses:
            index = self.connected_houses.index(house)
            self.connected_houses.remove(house)
            self.cables[index]
            del self.cables[index]
    
        