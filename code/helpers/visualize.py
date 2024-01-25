# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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

    # Set total cost to 0
    total_cost = 0

    # Store the colors of the batteries to later give the cables that color
    battery_colors = ['orange', 'green', 'red', 'blue', 'purple']
    
    # Plot batteries
    for battery in experiment_instance.batteries:
        plot_battery(battery_image, battery.x, battery.y)
        
        # Add 5000 to the total cost for every battery
        total_cost += 5000

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

        # Every cable adds 9 to the total cost, since this is the cost formula
        total_cost += total_cables * 9

        # Annotate the battery with the total output and total cables
        plt.annotate(f'Output: {total_output}\nCables: {total_cables}', 
                    (battery.x, battery.y), textcoords="offset points", 
                    xytext=(0,10), ha='right', fontsize=12, color='black')

    # Plot cables
    for i in range(len(experiment_instance.batteries)):

        #loop over the cables in experiment and look for the colors by ID so it plots cable colors per battery
        for cable in experiment_instance.cables:
            if cable.connected_battery == experiment_instance.batteries[i]:
                plt.plot([cable.start_x, cable.end_x], [cable.start_y, cable.end_y], 
                linewidth=0.5, color=battery_colors[i], zorder=0)
        
    # Add the total cost of the district to the plot
    plt.annotate(f'Total cost: {total_cost}', (0, 0), textcoords="offset points", 
                xytext=(10,10), ha='left', fontsize=12, color='black')

    plt.title('Houses and Batteries with Manhattan-style Cables')
    plt.savefig(f"data/output_data/plots/district{district_number}.png")
    plt.close(fig)

