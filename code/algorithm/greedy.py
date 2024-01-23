class Greedy:
    def __init__(self, experiment):
        self.experiment = experiment

    def connect_houses_to_batteries(self):
        for house in self.experiment.houses:
            # Sort batteries by distance to the house
            sorted_batteries = sorted(self.experiment.batteries, 
                                      key=lambda battery: abs(battery.x - house.x) + abs(battery.y - house.y))

            for battery in sorted_batteries:
                if battery.can_connect(house):
                    # Align on the x-axis
                    for x in range(min(house.x, battery.x), max(house.x, battery.x) + 1):
                        self.experiment.place_cables(x, house.y, x+1, house.y)

                    # Align on the y-axis
                    for y in range(min(house.y, battery.y), max(house.y, battery.y) + 1):
                        self.experiment.place_cables(battery.x, y, battery.x, y+1)

                    battery.connect_house(house)
                    break  # Stop looking for a battery once connected
            else:
                # This block is executed if the house couldn't be connected to any battery
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")

class Greedy2:
    def __init__(self, district):
        self.district = district

    def distance(self, house, battery):
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def connect_houses_to_batteries(self):
        # Precompute distances
        for house in self.district.houses:
            house.battery_distances = [(battery, self.distance(house, battery)) for battery in self.district.batteries]
            house.battery_distances.sort(key=lambda x: x[1])


        for house in self.district.houses:
            for battery, _ in house.battery_distances:
                if battery.can_connect(house):
                    self.place_cables(house, battery)  # Place cables one by one
                    battery.connect_house(house)
                    break
            else:
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")


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