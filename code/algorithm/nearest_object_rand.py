from code.classes.cable import Cable
from code.classes.battery import Battery
from code.classes.house import House
import random


class nearest_object_rand:
    """"
    version of the nearest_object_rand algorithm that that randomly chooses between the x-axis and the y-axis
    """
    def __init__(self, district):
        self.district = district

    def find_nearest_object_rand(self, house):
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
            sorted_objects = self.find_nearest_object_rand(house)

            # Loop over all objects sorted by distance to the house
            for object in sorted_objects:
                
                # Check if the object is a battery or a cable
                if isinstance(object, Battery):
                    
                    connected_battery = object
                    # Check if the battery has the capacity to connect the house
                    if connected_battery.can_connect(house):
                    
                        # Place cables and connect to the battery
                        self.place_cables(house, object, connected_battery)
                        object.connect_house(house) 
                        break
                    
                    # If the battery does not have the capacity, continue to the next object
                    else:
                        continue

                # Check if the object is a cable
                elif isinstance(object, Cable):

                    # Ensure the connected object is a Battery
                    connected_battery = object.connected_battery

                    if isinstance(connected_battery, Battery) and connected_battery.can_connect(house):

                        self.place_cables(house, object, connected_battery)
                        self.extend_route_to_battery(house, object, connected_battery)
                        connected_battery.connect_house(house)

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

        
    def place_cables(self, house, object, connected_battery):
        """
        places the cables with a 50/50 chance of choosing between the x-axis and y-axis first
        """
        if house.y != object.y != house.x != object.x:
            y_start, y_end = sorted([house.y, object.y])
            x_start, x_end = sorted([house.x, object.x])

            if random.choice([True, False]):
                # Place the cable along y-axis first
                for y in range(y_start, y_end):
                    cable_id = f"{object.x},{y},{object.x},{y+1}"
                    self.district.place_cables(object.x, y, object.x, y + 1, object)
                    house.route.append(cable_id)

                if house.x != object.x:
                    # Then place the cable along x-axis
                    for x in range(x_start, x_end):
                        cable_id = f"{x},{object.y},{x+1},{object.y}"
                        self.district.place_cables(x, object.y, x + 1, object.y, connected_battery)

                        # Keep track of the route of the house by adding the cable id to the route
                        house.route.append(cable_id)
            else:
                # Place the cable along x-axis first
                for x in range(x_start, x_end):
                    cable_id = f"{x},{object.y},{x+1},{object.y}"
                    self.district.place_cables(x, object.y, x + 1, object.y, connected_battery)

                    # Keep track of the route of the house by adding the cable id to the route
                    house.route.append(cable_id)

                if house.y != object.y:
                    # Then place the cable along y-axis
                    for y in range(y_start, y_end):
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
