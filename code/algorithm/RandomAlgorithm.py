# RandomAlgorithm.py
# Antonio, Mec, Vincent
# YakuzAI

import random 

class RandomAlgorithm:
    """
    A class that implements a random pathfinding algorithm.
    """

    def __init__(self, district):
        self.district = district

    def connect_houses_to_batteries(self):
        """
        Connects houses to batteries using a random pathfinding algorithm.
        """

        # Shuffle the district houses
        random_houses = self.district.houses
        random.shuffle(random_houses)
   
        # Keep track of which batteries have been tried
        tried_batteries = set()

        # Keep track of which batteries are still possible
        possible_batteries = self.district.batteries.copy()


        # Try to connect each house to a battery
        for house in enumerate(random_houses):
            house = house[1]

            while len(tried_batteries) != len(self.district.batteries):
                selected_battery = random.choice(possible_batteries)

                # Add the battery to the tried batteries
                tried_batteries.add(selected_battery)
                    
                # Remove the battery from the possible batteries
                possible_batteries.remove(selected_battery)

                # Check if the battery has enough capacity  
                if selected_battery.can_connect(house):

                    # Connect the house to the battery
                    self.place_cables(house, selected_battery)  
                    selected_battery.connect_house(house)

                    # Reset the tried batteries and possible batteries
                    tried_batteries = set()
                    possible_batteries = self.district.batteries.copy()

                    break   
           
            else:

                # Remove the house with the longest x connection
                while True:

                    # Remove the house with the most non shared cables
                    house = max(selected_battery.connected_houses, key=lambda x: len(x.route))


                    # remove the house from the battery
                    self.district.remove_connected_house(house, selected_battery)

                    break
                
            # This is a FAILCHECK: Check if all houses are connected
            total_houses = 0

            # For every battery in the district
            for battery in self.district.batteries:

                # Add the number of connected houses to the total houses
                total_houses += len(battery.connected_houses)

                # If the total houses is not 150, continue the loop
                if total_houses != 150:
                    continue

                # If the total houses is 150, break the loop
                else:
                        break

                
    def place_cables(self, house, battery):
        """
        This function places cables between a house and a battery.
        """

        # Place cable along x-axis
        if house.x != battery.x:

            # Get the start and end of the x-axis
            x_start, x_end = sorted([house.x, battery.x])

            # For every x along the x-axis
            for x in range(x_start, x_end):
                
                # Create a new cable id 
                cable_id = f"{x},{house.y},{x + 1},{house.y}"

                # see if cable id already exists
                if cable_id not in battery.cables:

                    # make new cable segment along the x-axis
                    new_cable = self.district.place_cables(x, house.y, x + 1, house.y, battery)

                    # append the new cable to the battery's cables dictionary
                    battery.cables[cable_id] = new_cable

                    # append the cable ID to the route of house
                    house.route.append(cable_id)
                    
        # Place cable along y-axis
        if house.y != battery.y:

            # Get the start and end of the y-axis
            y_start, y_end = sorted([house.y, battery.y])

            # For every y along the y-axis
            for y in range(y_start, y_end):

                #create new cable id
                cable_id = f"{battery.x},{y},{battery.x},{y + 1}"

                # see if cable id already exists
                if cable_id not in battery.cables:

                    # make new cable segment along the x-axis
                    new_cable = self.district.place_cables(battery.x, y, battery.x, y + 1, battery)

                    # append the new cable to the battery's cables dictionary
                    battery.cables[cable_id] = new_cable

                    # append the cable ID to the route of house
                    house.route.append(cable_id)
            
