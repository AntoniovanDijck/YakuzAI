# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from code.classes.house import House
from code.classes.battery import Battery
from code.classes.district import District
from code.helpers.load_battery_data import load_battery_data
from code.helpers.load_house_data import load_house_data

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