import numpy as np
import csv

from code.smart_grid import load_battery_data, load_house_data, show_district

class House():
    def __init__(self, x, y, maxoutput):

        # de x
        self.x = x

        # de y
        self.y = y

        # de output
        self.maxoutput = maxoutput
