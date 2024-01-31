# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation
import os

def visualize(district, district_number):
    """
    This file contains the code to plot the houses and batteries with the Manhattan-style cables used in the experiment class
    """
    # Create an instance of the Experiment clas
    experiment_instance = district



    # Create a figure and 50x50 grid
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xticks(np.arange(0, 51, 1))
    ax.set_yticks(np.arange(0, 51, 1))

    # Draw grid with grey lines
    ax.grid(linestyle='-', linewidth='0.5', alpha=0.25, color='grey', zorder=0)

    # Draw thicker grey lines for every 10th line
    for i in range(0, 51, 10):
        ax.axvline(x=i, color='grey', linestyle='-', linewidth=1.5, alpha=0.25, zorder=0)
        ax.axhline(y=i, color='grey', linestyle='-', linewidth=1.5, alpha=0.25, zorder=0)

    # Set labels for every 10th line
    ax.set_xticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])
    ax.set_yticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])

    #load the image for houses and batteries
    house_image = plt.imread("data/Huizen&Batterijen/Images/housy.png")
    battery_image = plt.imread("data/Huizen&Batterijen/Images/battery.png")

    def plot_house(img, x, y):
        image = OffsetImage(img, zoom=0.03)
        ab = AnnotationBbox(image, (x,y), frameon=False)
        ax.add_artist(ab)

    def plot_battery(img, x, y):
        image = OffsetImage(img, zoom=0.01)
        ab = AnnotationBbox(image, (x,y), frameon=False)
        ax.add_artist(ab)

    # Plot houses
    for house in experiment_instance.houses:
        plot_house(house_image, house.x, house.y)


    # Store the colors of the batteries to later give the cables that color
    battery_colors = ['orange', 'green', 'red', 'blue', 'purple']
    # Plot batteries
    for battery in experiment_instance.batteries:
        plot_battery(battery_image, battery.x, battery.y)
        

        # Calculate and annotate total output and total cables for each battery
        total_output = sum(house.maxoutput for house in battery.connected_houses)

        # Create a set of all cables connected to the battery
        battery_cables = set()

        # Add all cables connected to the battery to the set
        for house in battery.connected_houses:

            # Loop over cables
            for cable_id in house.route:

                # Check if the cable is connected to the battery
                battery_cables.add(cable_id)

        # Calculate the total cables used
        total_cables = len(battery_cables)


        # Annotate the battery with the total output and total cables
        plt.annotate(f'Output: {total_output}\nCables: {total_cables}', 
                    (battery.x, battery.y), textcoords="offset points", 
                    xytext=(0,10), ha='right', fontsize=12, color='black')


    # Calculate and annotate the total cost of the district
    total_cost = experiment_instance.calculate_totals()

    # Plot cables
    for i in range(len(experiment_instance.batteries)):

        #loop over the cables in experiment and look for the colors by ID so it plots cable colors per battery
        for cable_id, cable in experiment_instance.cables.items():
            if cable.connected_battery == experiment_instance.batteries[i]:
                plt.plot([cable.start_x, cable.end_x], [cable.start_y, cable.end_y], 
                linewidth=3.5, color=battery_colors[i], zorder=0)
        
    # Add the total cost of the district to the plot
    plt.annotate(f'Total cost: {total_cost}', (0, 0), textcoords="offset points", 
                xytext=(10,10), ha='left', fontsize=12, color='black')

    plt.title('Houses and Batteries with Manhattan-style Cables')
    #check for directory and create if not
    output_dir = "data/output_data/plots"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.savefig(f"data/output_data/plots/district{district_number}.png")
    # plt.show()


def visualize_live(district_states):
    """
    This function animates the algorithms like hillclimber
    """

    #initialize/plot the grid
    fig, ax = plt.subplots()

    #loading images from data
    house_image = plt.imread("data/Huizen&Batterijen/Images/housy.png")
    battery_image = plt.imread("data/Huizen&Batterijen/Images/battery.png")

    #images for house in plot
    def plot_house(x, y):
        image = OffsetImage(house_image, zoom=0.03)
        ab = AnnotationBbox(image, (x, y), frameon=False)
        ax.add_artist(ab)

    #images for battery in plot
    def plot_battery(x, y):
        image = OffsetImage(battery_image, zoom=0.01)
        ab = AnnotationBbox(image, (x, y), frameon=False)
        ax.add_artist(ab)


    def update(frame):
        ax.clear()
        ax.set_xlim(0, 50)
        ax.set_ylim(0, 50)

        # Set up grid and labels
        ax.grid(linestyle='-', linewidth='0.5', alpha=0.25, color='grey', zorder=0)
        for i in range(0, 51, 10):
            ax.axvline(x=i, color='grey', linestyle='-', linewidth=1.5, alpha=0.25, zorder=0)
            ax.axhline(y=i, color='grey', linestyle='-', linewidth=1.5, alpha=0.25, zorder=0)
        ax.set_xticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])
        ax.set_yticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])

        district = district_states[frame]

        # Plotting houses and batteries
        for house in district.houses:
            plot_house(house.x, house.y)

        battery_colors = ['orange', 'green', 'red', 'blue', 'purple']
        for i, battery in enumerate(district.batteries):
            plot_battery(battery.x, battery.y)
            for house in battery.connected_houses:
                for cable_id in house.route:
                    cable = district.cables[cable_id]
                    ax.plot([cable.start_x, cable.end_x], [cable.start_y, cable.end_y], color=battery_colors[i], linewidth=2)

    ani = FuncAnimation(fig, update, frames=len(district_states), repeat=False, interval=1)

    plt.show()
    plt.show()
