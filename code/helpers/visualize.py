# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import plotly.graph_objects as go

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
    # plt.savefig(f"data/output_data/plots/district{district_number}.png")
    # plt.show()


def visualize_live(district, district_number):
    """
    This function visualizes the houses, batteries, and cables in an interactive Plotly plot. This is meant for 
    the 
    """
    experiment_instance = district

    # create the start plot
    fig = go.Figure()

    # plot the houses
    fig.add_trace(go.Scatter(
        x=[house.x for house in experiment_instance.houses],
        y=[house.y for house in experiment_instance.houses],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='Houses'
    ))

    # plot the batteries
    battery_colors = ['orange', 'green', 'red', 'blue', 'purple']
    for i, battery in enumerate(experiment_instance.batteries):
        fig.add_trace(go.Scatter(
            x=[battery.x],
            y=[battery.y],
            mode='markers',
            marker=dict(size=15, color=battery_colors[i]),
            name=f'Battery {i + 1}'
        ))

        # plot the house info
        fig.add_annotation(
            x=battery.x,
            y=battery.y,
            text=f'Output: {sum(house.maxoutput for house in battery.connected_houses)}\nCables: {len(set(cable_id for house in battery.connected_houses for cable_id in house.route))}',
            showarrow=True,
            arrowhead=1
        )

        # add cables
        for house in battery.connected_houses:
            for cable_id in house.route:
                cable = experiment_instance.cables[cable_id]
                fig.add_trace(go.Scatter(
                    x=[cable.start_x, cable.end_x],
                    y=[cable.start_y, cable.end_y],
                    mode='lines',
                    line=dict(width=2, color=battery_colors[i]),
                    name=f'Cable {cable_id}'
                ))

    # set up the layout
    fig.update_layout(
        title=f'Houses and Batteries with Manhattan-style Cables in District {district_number}',
        xaxis=dict(range=[0, 50], autorange=False),
        yaxis=dict(range=[0, 50], autorange=False),
        showlegend=False
    )

    fig.show()