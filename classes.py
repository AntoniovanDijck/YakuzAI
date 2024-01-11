#Main classes for github
# Antonio, Mec, Vincent
# YakuzAI

import numpy as np
import csv

from smart_grid import load_battery_data, load_house_data, show_district

class Battery():
    def __init__(self, x, y, capacity):

        # de x en y
        self.x = x
        self.y = y

        # de capaciteit en de maximale output
        self.capacity = capacity

class House():
    def __init__(self, x, y, maxoutput):

        # de x
        self.x = x

        # de y
        self.y = y

        # de output
        self.maxoutput = maxoutput


class Cable():
    def __init__(self, house, battery):

        # de batterij
        self.battery = battery

        # het huis
        self.house = house

class District():
    def __init__(self, houses, batteries):

        show_district(houses, batteries)
