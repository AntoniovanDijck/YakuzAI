import numpy as np
import csv

from code.smart_grid import load_battery_data, load_house_data, show_district
from code.cable import Cable

class House():
    def __init__(self, x, y, maxoutput):
        self.x = x
        self.y = y
        #houses output
        self.maxoutput = maxoutput
        self.connected_battery = None
        self.cable = None

    #attribute that tracks connections for houses
    def connect_house_to_battery(self, battery, ):

        if self.connected_battery != None:
            print("Connected")  
            return 
        
        cable = Cable(self, battery)
        self.connected_battery = battery
        self.cable = cable
        battery.connect_house(self, cable)

    def disconnect_house_from_battery(self, house):
        if self.connected_battery == None:
            print("House is not connected")
            return 
        self.connected_battery.disconnect_house(self)
        self.connected_battery = None
        self.cable = None
