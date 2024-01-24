from code.classes.cable import Cable
from code.classes.battery import Battery
from code.classes.house import House


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
    """"
    This versio differce from version 2 as this algorithm looks for the nearest cable of battery. Cable that are connected
    to a battery now contain the battery object in the connected_battery attribute. This is used to check if a cable is
    connected to a battery. If this battery has the capacity. This algorithm will connect the house to the cable instead.
    """
    def __init__(self, district):
        self.district = district

    def find_nearest_object(self, house):
        """
        This method finds the nearest battery or cable to a house.
        """

        # Create a list of all batteries and cables
        objects = self.district.batteries + self.district.cables


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

        # Loop over all houses
        for house in self.district.houses:
        
            # Find the nearest battery or cable to the house
            sorted_objects = self.find_nearest_object(house)

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

                            # To keep track of the cables that are used to connect houses to batteries, the overlapping
                            # cables need to be tracked as well
                            self.extend_route_to_battery(house, object, connected_battery)

                            # Connect house to the battery
                            connected_battery.connect_house(house)

                            # Break out of the loop as the house is connected
                            break
                        else:
                            continue

    
    def place_cables(self, house, object):
        """
        This method places cables between houses and batteries. It does this by placing cables along the x-axis and the
        y-axis. It does this by checking the x and y coordinates of the house and the battery. It then places cables
        between these coordinates.
        """
        # Place cable along x-axis

        if house.x != object.x:
            x_start, x_end = sorted([house.x, object.x])

            # Create a new cable segment for each unit along the x-axis
            for x in range(x_start, x_end):
            
                # Create a new cable segment for each unit along the x-axis
                self.district.place_cables(x, house.y, x + 1, house.y, object)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(self.district.cables[-1].id)

        # Place cable along y-axis
        if house.y != object.y:
            y_start, y_end = sorted([house.y, object.y])

            # Create a new cable segment for each unit along the y-axis
            for y in range(y_start, y_end):
            
                # Create a new cable segment for each unit along the y-axis
                self.district.place_cables(object.x, y, object.x, y + 1, object)

                # Keep track of the route of the house by adding the cable to the route
                house.route.append(self.district.cables[-1].id)
                
    def extend_route_to_battery(self, house, cable, battery):
        """
        Extends the route from the cable to the connected battery.
        """

        # Place cable along x-axis from cable end to battery
        if cable.end_x != battery.x:

            # Sort the x coordinates from the cable and the battery
            x_start, x_end = sorted([cable.end_x, battery.x])

            # Loop over the x coordinates
            for x in range(x_start, x_end):
                self.district.place_cables(x, cable.end_y, x + 1, cable.end_y, battery)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(self.district.cables[-1].id)

        # Place cable along y-axis from cable end to battery
        if cable.end_y != battery.y:

            # Sort the y coordinates from the cable and the battery
            y_start, y_end = sorted([cable.end_y, battery.y])
            for y in range(y_start, y_end):

                # Create a new cable segment for each unit along the y-axis
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(self.district.cables[-1].id)