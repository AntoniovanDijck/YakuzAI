# Greedy_Object_Distance.py
# Antonio, Vincent, Mec
# YakuzAI

from code.classes.cable import Cable
from code.classes.battery import Battery
from code.classes.house import House
import random

class Greedy_Object_Distance:
    """"
    This version differences  the random algorithm as this algorithm looks for the nearest cable of battery. Cable that are connected
    to a battery now contain the battery object in the connected_battery attribute. This is used to check if a cable is
    connected to a battery. If this battery has the capacity. This algorithm will connect the house to the cable instead.
    """
    def __init__(self, district, shuffle=True):
        self.shuffle = shuffle
        self.district = district

    def find_nearest_object_x(self, house):
        """
        This method finds the nearest battery or cable to a house.
        """

        # Create a list of all batteries and cables
        objects = self.district.batteries + list(self.district.cables.values())


        def distance_to_object(obj):
            """
            Using this function as a key for the sorted function, we can sort the objects by distance to the house.
            """

            # Check if the object is a battery or a cable
            if isinstance(obj, Battery):

                # Distance from house to battery
                return abs(obj.x - house.x) + abs(obj.y - house.y)

            elif isinstance(obj, Cable):

                # Distance from house to the closest start of the cable
                distances = [abs(house.x - obj.start_x) + abs(house.y - obj.start_y), abs(house.x - obj.end_x) + abs(house.y - obj.end_y)]
                return min(distances)


        # Sort the objects by distance
        sorted_objects = sorted(objects, key=distance_to_object)

        return sorted_objects

    def connect_houses_to_batteries(self):
        """
        This method connects houses to batteries. It does this by finding the nearest battery or cable to a house. If
        this object is a battery, it checks if the battery has the capacity to connect the house. If this object is a
        cable, it checks if the battery connected to the cable has the capacity to connect the house. If the battery
        has the capacity.
        """
        if self.shuffle:
        # Shuffle the houses to prevent the algorithm from always connecting the same houses to the same batteries
            random_houses = self.district.houses
            random.shuffle(random_houses)
        else:
            random_houses = self.district.houses

        # Loop over all houses
        for house in random_houses:

            # Find the nearest battery or cable to the house
            sorted_objects = self.find_nearest_object_x(house)

            # Loop over all objects sorted by distance to the house
            for object in sorted_objects:

                # Check if the object is a battery or a cable
                if isinstance(object, Battery):

                    # Check if the battery has the capacity to connect the house
                    if object.can_connect(house):

                        # Place cables and connect to the battery
                        self.place_cables(house, object)
                        object.connect_house(house)
                        break

                    # If the battery does not have the capacity, continue to the next object
                    else:
                        continue

                # Check if the object is a cable
                elif isinstance(object, Cable):

                    # Check if the cable is connected to a battery
                    connected_battery = object.connected_battery

                    # Check if the connected_battery is a battery class to prevent errors
                    if isinstance(connected_battery, Battery):

                        # Place cables and connect to the cable, which routes to the battery
                        if connected_battery.can_connect(house):

                            # Place cables and connect to the battery
                            self.place_cables(house, object)

                            # Connect house to the battery
                            connected_battery.connect_house(house)

                            # Break out of the loop as the house is connected
                            break

                        else:
                            continue
                    else:
                        # if no battery is found, remove the house with the longest route on y, as we want to avoid long y
                        while True:
                            # Remove the house with the longest x route
                            house = max(connected_battery.connected_houses, key=lambda y: len(y.route))

                            # remove the house from the battery
                            self.district.remove_connected_house(house, connected_battery)

                            break


    def place_cables(self, house, object):
        """
        This method places cables between houses and batteries. It does this by placing cables along the x-axis and the
        y-axis. It does this by checking the x and y coordinates of the house and the battery. It then places cables
        between these coordinates.
        """
        # Place cable along x-axis
        if isinstance(object, Cable):
            object = object.connected_battery

        if house.x != object.x:
            x_start, x_end = sorted([house.x, object.x])

            # Create a new cable segment for each unit along the x-axis
            for x in range(x_start, x_end):
                cable_id = f"{x},{object.y},{x+1},{object.y}"
                self.district.place_cables(x, object.y, x + 1, object.y, object)
                house.route.append(cable_id)

        # Place cable along y-axis
        if house.y != object.y:
            y_start, y_end = sorted([house.y, object.y])

            # Create a new cable segment for each unit along the y-axis
            for y in range(y_start, y_end):
                    cable_id = f"{house.x},{y},{house.x},{y+1}"
                    self.district.place_cables(house.x, y, house.x, y + 1, object)
                    house.route.append(cable_id)