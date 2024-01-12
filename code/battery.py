import numpy as np
import csv

from code.smart_grid import load_battery_data, load_house_data, show_district


class Battery():
    def __init__(self, x, y, capacity):

        # de x en y
        self.x = x
        self.y = y

        # de capaciteit en de maximale output
        self.capacity = capacity

        # Connect huizen met batterij
        self.connected = []
        