import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def visualize_best(district):
    """
    Visualizes the district state with houses, batteries, and cables.
    Assumes 'district' is an instance of the District class with the desired state.
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xticks(np.arange(0, 51, 1))
    ax.set_yticks(np.arange(0, 51, 1))
    ax.grid(linestyle='-', linewidth='0.5', alpha=0.25, color='grey', zorder=0)
    for i in range(0, 51, 10):
        ax.axvline(x=i, color='grey', linestyle='-', linewidth=1.5, alpha=0.25, zorder=0)
        ax.axhline(y=i, color='grey', linestyle='-', linewidth=1.5, alpha=0.25, zorder=0)
    ax.set_xticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])
    ax.set_yticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(0, 51, 1)])

    # Load images for houses and batteries (replace with your actual image paths)
    house_image = plt.imread("path/to/house_image.png")
    battery_image = plt.imread("path/to/battery_image.png")

    def plot_house(img, x, y):
        image = OffsetImage(img, zoom=0.03)
        ab = AnnotationBbox(image, (x, y), frameon=False)
        ax.add_artist(ab)

    def plot_battery(img, x, y):
        image = OffsetImage(img, zoom=0.01)
        ab = AnnotationBbox(image, (x, y), frameon=False)
        ax.add_artist(ab)

    total_cost = 0
    battery_colors = ['orange', 'green', 'red', 'blue', 'purple']

    # Plot houses and batteries
    for house in district.houses:
        plot_house(house_image, house.x, house.y)

    for i, battery in enumerate(district.batteries):
        plot_battery(battery_image, battery.x, battery.y)
        total_cost += 5000  # Assuming each battery adds 5000 to the total cost

        total_output = sum(house.maxoutput for house in battery.connected_houses)
        battery_cables = set()
        for house in battery.connected_houses:
            for cable_id in house.route:
                battery_cables.add(cable_id)
        total_cables = len(battery_cables)
        total_cost += total_cables * 9  # Assuming each cable segment costs 9

        plt.annotate(f'Output: {total_output}\nCables: {total_cables}', 
                     (battery.x, battery.y), textcoords="offset points", 
                     xytext=(0, 10), ha='right', fontsize=12, color='black')

    # Plot cables
    for i, battery in enumerate(district.batteries):
        for cable_id, cable in district.cables.items():
            if cable.connected_battery == battery:
                plt.plot([cable.start_x, cable.end_x], [cable.start_y, cable.end_y], 
                         linewidth=0.5, color=battery_colors[i], zorder=0)
        
    plt.annotate(f'Total cost: {total_cost}', (0, 0), textcoords="offset points", 
                 xytext=(10, 10), ha='left', fontsize=12, color='black')

    plt.title('Houses and Batteries with Manhattan-style Cables')
    plt.show()

