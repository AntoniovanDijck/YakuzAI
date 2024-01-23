# astar.py
# Antonio, Mec, Vincent
# YakuzAI

##TODO: THIS IS STILL GREEDY 2.0, NOT A* YET
class A_star:
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

                    # Stop looking for batteries if connected
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
