# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_battery_data(filename):

    # # new dictionary maken
    battery_data = {}

    with open(filename, 'r') as file:

        csv_reader = csv.reader(file)

        # Overslaan header
        next(csv_reader)
        
        for row in csv_reader:

            positie = map(int, row[0].split(','))
            
            capaciteit = row[1]

            battery_data[tuple(positie)] = capaciteit

    return battery_data


def load_house_data(filename):

    house_dict = {}

    with open(filename, 'r') as file:
            
            csv_reader = csv.reader(file)
    
            # Overslaan header
            next(csv_reader)
            
            for row in csv_reader:
    
                x = row[0]
                y = row[1]
                maxoutput = row[2]
    
                house_dict[tuple((int(x),int(y)))] = float(maxoutput)

    return house_dict

houses_data = ['Huizen&Batterijen/district_1/district-1_houses.csv', 'Huizen&Batterijen/district_2/district-2_houses.csv', 'Huizen&Batterijen/district_3/district-3_houses.csv']

for house in houses_data:
    print(load_house_data(house))
