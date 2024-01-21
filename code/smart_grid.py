# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_battery_data(filename):
    '''
    reads the csv file and returns a dictionary with the positions of the batteries and their capacity

    '''

    # # create new dict
    battery_data = {}

    with open(filename, 'r') as f:

        csv_reader = csv.reader(f)

        # skip the header
        next(csv_reader)
        
        for row in csv_reader:

            position = map(int, row[0].split(','))
            
            capacity = row[1]

            battery_data[tuple(position)] = float(capacity)

    return battery_data


def load_house_data(house_data):
    """
    reads the csv file and returns a dictionary with the x and y positions of the houses and their max output

    """

    house_dict = {}

    with open(house_data, 'r') as file:
            
            reader = csv.reader(file)
    
            # skip the header
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

    # grid of 50 x 50 with small lines
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(0, 51, 1))
    ax.set_yticks(np.arange(0, 51, 1))

    # Design of the grid (thin lines and in background)
    ax.grid(linestyle='-', linewidth='0.5', alpha=0.25, color='grey', zorder = 0)


    # thicken every 10th line for overview
    for i in range(0, 51, 10):
        ax.axvline(x=i, color='grey', linestyle='-', linewidth = 1.5, alpha=0.25, zorder = 0)
        ax.axhline(y=i, color='grey', linestyle='-', linewidth = 1.5, alpha = 0.25, zorder = 0)
        
    # label every 10th line for overview
    ax.set_xticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])
    ax.set_yticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])

   
    #plotting houses and batteries
    for house in houses.values():
        ax.scatter(house.x, house.y, color="blue", label="house")
    
    for battery in batteries.values():
        ax.scatter(battery.x, battery.y, color="red", marker="s", label="battery")
    
    #label every 10th line 
    ax.set_xticklabels([str(i) if i % 10 == 0 else '' for i in range(0, 51)])
    ax.set_yticklabels([str(i) if i % 10 == 0 else '' for i in range(0, 51)])

    # Show the plot
    plt.show()


def get_5_total_length(batteries):
    total_cable_length = 0
    
    battery_list = list(batteries.values())[:5]
    for battery in battery_list:
        #get first 50 batteries
        for cable in battery.cables:
            total_cable_length += cable.length
    
    return total_cable_length


#running for testing on district 1

# #Load data for district 1 
# houses = load_house_data("Huizen&Batterijen/district_1/district-1_houses.csv")
# batteries = load_battery_data("Huizen&Batterijen/district_1/district-1_batteries.csv")

# #get total length of 50 first batteries
# total_length = get_50_total_length(batteries)
# print(total_length)

# show_district(houses, batteries)