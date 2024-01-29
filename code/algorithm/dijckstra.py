from code.classes.cable import Cable
from code.classes.battery import Battery
from code.classes.house import House
import random

class dijckstra:
    """"
    This versio differce from version 2 as this algorithm looks for the nearest cable of battery. Cable that are connected
    to a battery now contain the battery object in the connected_battery attribute. This is used to check if a cable is
    connected to a battery. If this battery has the capacity. This algorithm will connect the house to the cable instead.
    """
    def __init__(self, district):
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

        # Shuffle the houses to prevent the algorithm from always connecting the same houses to the same batteries
        random_houses = self.district.houses
        random.shuffle(random_houses)

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

                            # To keep track of the cables that are used to connect houses to batteries, the overlapping
                            # cables need to be tracked as well
                            # TODO: Fix this --> uncomment the following line and check simulation for weird grid
                            # self.extend_route_to_battery(house, object, connected_battery)

                            # Connect house to the battery
                            connected_battery.connect_house(house)

                            # Break out of the loop as the house is connected
                            break

                        else:
                            continue
                    else:
                        while True:
                            
                            # If no battery has the capacity, remove the house with the longest x or y route and try again
                            if random.choice([True, False]):

                                # Remove the house with the longest x route
                                house = max(connected_battery.connected_houses, key=lambda x: len(x.route))


                                # remove the house from the battery
                                self.district.remove_connected_house(house, connected_battery)

                                break
                            else:  
                                # Remove the house with the longest y route
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

        x_distance = abs(house.x - object.x)
        y_distance = abs(house.y - object.y)

        if x_distance > y_distance:
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
        else:
            # Place cable along x-axis
            if house.x != object.x:
                x_start, x_end = sorted([house.x, object.x])
                for x in range(x_start, x_end):
                    # Create a new cable segment for each unit along the x-axis
                    cable_id = f"{x},{house.y},{x+1},{house.y}"
                    self.district.place_cables(x, house.y, x + 1, house.y, object)
                    house.route.append(cable_id)

            # Place cable along y-axis
            if house.y != object.y:
                y_start, y_end = sorted([house.y, object.y])
                for y in range(y_start, y_end):
                    
                    # Create a new cable segment for each unit along the y-axis
                    cable_id = f"{object.x},{y},{object.x},{y+1}"
                    self.district.place_cables(object.x, y, object.x, y + 1, object)
                    house.route.append(cable_id)
            



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

                cable_id = f"{x},{cable.end_y},{x+1},{cable.end_y}"
                self.district.place_cables(x, cable.end_y, x + 1, cable.end_y, battery)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(cable_id)


        # Place cable along y-axis from cable end to battery
        if cable.end_y != battery.y:

            # Sort the y coordinates from the cable and the battery
            y_start, y_end = sorted([cable.end_y, battery.y])
            for y in range(y_start, y_end):

                # Create a new cable segment for each unit along the y-axis
                cable_id = f"{battery.x},{y},{battery.x},{y+1}"
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)
                # Keep track of the route of the house by adding the cable id to the route



class dijckstra_sum:
    """"
    This versio differce from version 2 as this algorithm looks for the nearest cable of battery. Cable that are connected
    to a battery now contain the battery object in the connected_battery attribute. This is used to check if a cable is
    connected to a battery. If this battery has the capacity. This algorithm will connect the house to the cable instead.
    """
    def __init__(self, district):
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

        # Shuffle the houses to prevent the algorithm from always connecting the same houses to the same batteries
        random_houses = self.district.houses
        random.shuffle(random_houses)

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

                            # To keep track of the cables that are used to connect houses to batteries, the overlapping
                            # cables need to be tracked as well
                            # TODO: Fix this --> uncomment the following line and check simulation for weird grid
                            # self.extend_route_to_battery(house, object, connected_battery)

                            # Connect house to the battery
                            connected_battery.connect_house(house)

                            # Break out of the loop as the house is connected
                            break

                        else:
                            continue
                    else:
                        while True:
                            # Calculate the total length of the x and y routes using the sum 
                            total_x_route_length = sum([abs(house.x - connected_battery.x) for house in connected_battery.connected_houses])
                            total_y_route_length = sum([abs(house.y - connected_battery.y) for house in connected_battery.connected_houses])

                            # if the total lenght horizontal is longer than the total length vertical, remove the house with the longest x route
                            if total_x_route_length > total_y_route_length:

                                # Remove the house with the longest X route
                                removed_house = max(connected_battery.connected_houses, key=lambda h: abs(h.x - connected_battery.x))
                            
                            else:

                                # Remove the house with the longest Y route
                                removed_house = max(connected_battery.connected_houses, key=lambda h: abs(h.y - connected_battery.y))


                            self.district.remove_connected_house(removed_house, connected_battery)
                            
                            #stop
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

        x_distance = abs(house.x - object.x)
        y_distance = abs(house.y - object.y)

        if x_distance > y_distance:
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
        else:
            # Place cable along x-axis
            if house.x != object.x:
                x_start, x_end = sorted([house.x, object.x])
                for x in range(x_start, x_end):
                    # Create a new cable segment for each unit along the x-axis
                    cable_id = f"{x},{house.y},{x+1},{house.y}"
                    self.district.place_cables(x, house.y, x + 1, house.y, object)
                    house.route.append(cable_id)

            # Place cable along y-axis
            if house.y != object.y:
                y_start, y_end = sorted([house.y, object.y])
                for y in range(y_start, y_end):
                    
                    # Create a new cable segment for each unit along the y-axis
                    cable_id = f"{object.x},{y},{object.x},{y+1}"
                    self.district.place_cables(object.x, y, object.x, y + 1, object)
                    house.route.append(cable_id)
            



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

                cable_id = f"{x},{cable.end_y},{x+1},{cable.end_y}"
                self.district.place_cables(x, cable.end_y, x + 1, cable.end_y, battery)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(cable_id)


        # Place cable along y-axis from cable end to battery
        if cable.end_y != battery.y:

            # Sort the y coordinates from the cable and the battery
            y_start, y_end = sorted([cable.end_y, battery.y])
            for y in range(y_start, y_end):

                # Create a new cable segment for each unit along the y-axis
                cable_id = f"{battery.x},{y},{battery.x},{y+1}"
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)
                # Keep track of the route of the house by adding the cable id to the route




class dijckstra_max:
    """"
    This versio differce from version 2 as this algorithm looks for the nearest cable of battery. Cable that are connected
    to a battery now contain the battery object in the connected_battery attribute. This is used to check if a cable is
    connected to a battery. If this battery has the capacity. This algorithm will connect the house to the cable instead.
    """
    def __init__(self, district):
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

        # Shuffle the houses to prevent the algorithm from always connecting the same houses to the same batteries
        random_houses = self.district.houses
        random.shuffle(random_houses)

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

                            # To keep track of the cables that are used to connect houses to batteries, the overlapping
                            # cables need to be tracked as well
                            # TODO: Fix this --> uncomment the following line and check simulation for weird grid
                            # self.extend_route_to_battery(house, object, connected_battery)

                            # Connect house to the battery
                            connected_battery.connect_house(house)

                            # Break out of the loop as the house is connected
                            break

                        else:
                            continue
                    else:
                        while True:
                           
                            house_longest_x_route = max(connected_battery.connected_houses, key=lambda house: max([abs(house.x - cable.x) for cable in connected_battery.connected_houses]))
                            house_longest_y_route = max(connected_battery.connected_houses, key=lambda house: max([abs(house.y - cable.y) for cable in connected_battery.connected_houses]))
                       
                            longest_x_route_length = max([abs(house_longest_x_route.x - cable.x) for cable in connected_battery.connected_houses])
                            longest_y_route_length = max([abs(house_longest_y_route.y - cable.y) for cable in connected_battery.connected_houses])

                            # Remove the house with the longer route
                            if longest_x_route_length > longest_y_route_length:
                                # Remove the house with the longest x route
                                self.district.remove_connected_house(house_longest_x_route, connected_battery)
                            
                            
                            else:
                                # Remove the house with the longest y route
                                self.district.remove_connected_house(house_longest_y_route, connected_battery)

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

        x_distance = abs(house.x - object.x)
        y_distance = abs(house.y - object.y)

        if x_distance > y_distance:
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
        else:
            # Place cable along x-axis
            if house.x != object.x:
                x_start, x_end = sorted([house.x, object.x])
                for x in range(x_start, x_end):
                    # Create a new cable segment for each unit along the x-axis
                    cable_id = f"{x},{house.y},{x+1},{house.y}"
                    self.district.place_cables(x, house.y, x + 1, house.y, object)
                    house.route.append(cable_id)

            # Place cable along y-axis
            if house.y != object.y:
                y_start, y_end = sorted([house.y, object.y])
                for y in range(y_start, y_end):
                    
                    # Create a new cable segment for each unit along the y-axis
                    cable_id = f"{object.x},{y},{object.x},{y+1}"
                    self.district.place_cables(object.x, y, object.x, y + 1, object)
                    house.route.append(cable_id)
            



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

                cable_id = f"{x},{cable.end_y},{x+1},{cable.end_y}"
                self.district.place_cables(x, cable.end_y, x + 1, cable.end_y, battery)

                # Keep track of the route of the house by adding the cable id to the route
                house.route.append(cable_id)


        # Place cable along y-axis from cable end to battery
        if cable.end_y != battery.y:

            # Sort the y coordinates from the cable and the battery
            y_start, y_end = sorted([cable.end_y, battery.y])
            for y in range(y_start, y_end):

                # Create a new cable segment for each unit along the y-axis
                cable_id = f"{battery.x},{y},{battery.x},{y+1}"
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)
                # Keep track of the route of the house by adding the cable id to the route

