# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


def draw_cables(district):
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

    # Plot houses
    for house in experiment_instance.houses:
        plt.scatter(house.x, house.y, color='blue', label='House')

    # Set total cost to 0
    total_cost = 0

    # Plot batteries
    for battery in experiment_instance.batteries:
        plt.scatter(battery.x, battery.y, color='yellow', edgecolors='black', linewidth=0.5, marker='s', label='Battery')
        
        # Add 5000 to the total cost for every battery
        total_cost += 5000

        # Calculate and annotate total output and total cables for each battery
        total_output = sum(house.maxoutput for house in battery.connected_houses)

        # Create a set of all cables connected to the battery
        battery_cables = set()

        # Add all cables connected to the battery to the set
        for house in battery.connected_houses:

            # Loop over cables
            for cable in house.route:

                # Check if the cable is connected to the battery
                battery_cables.add(cable.id)

        # Calculate the total cables used
        total_cables = len(battery_cables)

        # Ecery cable adds 9 to the total cost
        total_cost += total_cables * 9

        # Annotate the battery with the total output and total cables
        plt.annotate(f'Output: {total_output}\nCables: {total_cables}', 
                    (battery.x, battery.y), textcoords="offset points", 
                    xytext=(0,10), ha='right', fontsize=12, color='black')

    # Plot cables
    for cable in experiment_instance.cables:
        plt.plot([cable.start_x, cable.end_x], [cable.start_y, cable.end_y], 
                'b-', linewidth=0.5)
        
    # Add the total cost of the district to the plot
    plt.annotate(f'Total cost: {total_cost}', (0, 0), textcoords="offset points", 
                xytext=(10,10), ha='left', fontsize=12, color='black')

    plt.title('Houses and Batteries with Manhattan-style Cables')
    plt.show()

