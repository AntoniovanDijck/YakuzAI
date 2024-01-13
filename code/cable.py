# import numpy as np
# import csv

# from code.smart_grid import load_battery_data, load_house_data, show_district
# from code.house import House
# from code.battery import Battery


# class Cable():
#     def __init__(self, house, battery):

#         # de batterij
#         self.battery = battery

#         # het huis
#         self.house = house
#         self.length = self.calculate_length()

#     def calculate_length(self):
#         return abs(self.house.x - self.battery.x)+(self.house.y - self.battery.y)