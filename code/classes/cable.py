# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

class Cable:
    """
    Class that creates a cable with coordinates and an id
    """
    def __init__(self, start_x, start_y, end_x, end_y, battery = None):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

        # Create an id for the cable
        self.id = f"{start_x}, {start_y}-{end_x},{end_y}"

        self.connected_battery = battery

class Greedy3:
    def __init__(self, experiment):
        self.experiment = experiment

    def find_nearest_object(self, house):
        # Combine batteries and cables into a single list
        objects = self.experiment.batteries + self.experiment.cables

        # Sort objects by distance to the house
        sorted_objects = sorted(objects, key=lambda obj: abs(obj.x - house.x) + abs(obj.y - house.y))
        return sorted_objects

    def connect_houses_to_batteries(self):
        for house in self.experiment.houses:
            sorted_objects = self.find_nearest_object(house)

            for obj in sorted_objects:
                if isinstance(obj, battery) and obj.can_connect(house):
                    # Connect to the battery
                    obj.connect(house)
                    break
                elif isinstance(obj, self.cable):
                    connected_battery = obj.connected_battery
                    if connected_battery and connected_battery.can_connect(house):
                        # Connect to the cable, which routes to the battery
                        obj.connect(house)
                        break

    def place_cables(self, house, battery):
        # Place cable along x-axis
        if house.x != battery.x:
            x_start, x_end = sorted([house.x, battery.x])
            for x in range(x_start, x_end):
                # Create a new cable segment for each unit along the x-axis
                self.district.place_cables(x, house.y, x + 1, house.y, battery)

        # Place cable along y-axis
        if house.y != battery.y:
            y_start, y_end = sorted([house.y, battery.y])
            for y in range(y_start, y_end):
                # Create a new cable segment for each unit along the y-axis
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)