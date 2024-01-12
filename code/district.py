import numpy as np
import csv

from code.smart_grid import load_battery_data, load_house_data, show_district
from code.house import House
from code.battery import Battery

class District():
    def __init__(self, houses, batteries):

        show_district(houses, batteries)