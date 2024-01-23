class Greedy1:
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
        ''' Function that calculates the distance between a house and a battery'''

        # Calculate distance between house and battery using the Manhattan distance
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def connect_houses_to_batteries(self):
        ''' Function that connects houses to batteries'''

        # loop through houses in the district
        for house in self.district.houses:

            # add battery and distance to list using the distance function
            house.battery_distances = [(battery, self.distance(house, battery)) for battery in self.district.batteries]

            # Sort by distance, second culumn [1] using lamda function. 
            house.battery_distances.sort(key=lambda x: x[1])

        # Connect houses to batteries
        for house in self.district.houses:
            
            # Try to connect to the closest battery first
            for battery, y in house.battery_distances:

                # If the battery can connect to the house, connect them
                if battery.can_connect(house):

                    # Place cables
                    self.place_cables(house, battery)
                    battery.connect_house(house)
                    break
            else:
                # if house could not be connected to any battery print error
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")

    def place_cables(self, house, battery):
        ''' Function that places cables between house and battery'''

        # Place cable on y-axis if the house and battery are not on the same y-axis
        if house.x != battery.x:

            # Sort x-coordinates and take the smallest and largest value
            x_start, x_end = sorted([house.x, battery.x])

            # Place cables between house and battery
            self.district.place_cables(x_start, house.y, x_end, house.y)

        # Place cable on y-axis if the house and battery are not on the same y-axis
        if house.y != battery.y:

            # Sort y-coordinates and take the smallest and largest value
            y_start, y_end = sorted([house.y, battery.y])

            # Place cables between house and battery
            self.district.place_cables(battery.x, y_start, battery.x, y_end)
