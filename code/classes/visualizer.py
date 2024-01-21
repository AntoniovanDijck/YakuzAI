

import csv
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#importing our modules 
from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import Cable
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.greedy import Greedy

class Visualizer:
    def __init__(self, district):
        self.district = district

    def draw_grid(self, ax):
        ax.set_xticks(np.arange(0,51,1))
        ax.set_yticks(np.arange(0,51,1))
        ax.grid(linestyle='-', linewidth='0.5', alpha=0.25, color='grey', zorder=0)

    def plot_houses_and_batteries(self, ax):
        for house in self.district.houses:
            ax.scatter(house.x, house.y, color="blue", label="house")
        
        for battery in self.district.batteries:
            ax.scatter(battery.x, battery.y, color="red", edgecolors='black', linewidth=0.5, marker='s', label='Battery')

    def draw_cables(self,ax):
        for cable in self.district.cables:
            ax.plot([cable.start_x, cable.end_x], [cable.start_y, cable.end_y], 'b-', linewidth=0.5)
        
    def visualize(self, algorithm, district_number):
        fig, ax = plt.subplots(figsize=(12, 12))
        self.draw_grid(ax)
        self.plot_houses_and_batteries(ax)

        algorithm_instance = algorithm(self.district)
        algorithm_instance.connect_houses_to_batteries()
        self.draw_cables(ax)

        # Corrected line for setting the title
        plt.title(f'Visualization of {algorithm.__name__} Algorithm for District {district_number}')

        # Save the figure before showing it
        filename = f'district_{district_number}_visualization.png'
        plt.savefig(filename)

        # Handling labels
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = dict(zip(labels, handles))
        ax.legend(unique_labels.values(), unique_labels.keys())

        plt.show()
