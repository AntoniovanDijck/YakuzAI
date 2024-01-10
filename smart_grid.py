# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_battery_data(filename):
    '''
    reads the csv file and returns a dictionary with the positions of the batteries and their capacity

    '''

    # # new dictionary maken
    battery_data = {}

    with open(filename, 'r') as f:

        csv_reader = csv.reader(f)

        # Overslaan header
        next(csv_reader)
        
        for row in csv_reader:

            positie = map(int, row[0].split(','))
            
            capaciteit = row[1]

            battery_data[tuple(positie)] = float(capaciteit)

    return battery_data


def load_house_data(house_data):
    """
    reads the csv file and returns a dictionary with the x and y positions of the houses and their max output

    """

    house_dict = {}

    with open(house_data, 'r') as file:
            
            reader = csv.reader(file)
    
            # Overslaan header
            next(reader)
            
            for row in reader:
    
                x = row[0]
                y = row[1]
                maxoutput = row[2]
    
                house_dict[tuple((int(x),int(y)))] = float(maxoutput)

    return house_dict

def show_district(houses_data, battery_data):
    
    # load data
    houses = load_house_data(houses_data)
    batteries = load_battery_data(battery_data)

    x1 = []
    y1 = []
    for house in houses:
        x1.append(house[0])
        y1.append(house[1])

    x2 = []
    y2 = []
    for battery in batteries:
        x2.append(battery[0])
        y2.append(battery[1])

    # plot data
    plt.scatter(x1, y1, color='red')
    plt.scatter(x2, y2, color='blue')
    plt.show()

