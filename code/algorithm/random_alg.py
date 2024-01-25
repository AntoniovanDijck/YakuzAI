# Smart_grid.py
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
                # Remove a random house from the battery and try again until it works

                    # print("A house was removed and a new connection was tried")

                    battery = random.choice(self.district.batteries)

                    # select a random house that is connected to this battery
                    house = random.choice(battery.connected_houses)

                    # remove the house from the battery
                    self.district.remove_connected_house(house, battery)


                    continue
                
                
    def place_cables(self, house, battery):

        # Place cable along x-axis
        if house.x != battery.x:
            x_start, x_end = sorted([house.x, battery.x])
            for x in range(x_start, x_end):
                # Create a new cable segment for each unit along the x-axis
                self.district.place_cables(x, house.y, x + 1, house.y, battery)

                house.route.append(self.district.cables[-1].id)

        # Place cable along y-axis
        if house.y != battery.y:
            y_start, y_end = sorted([house.y, battery.y])
            for y in range(y_start, y_end):
                
                # Create a new cable segment for each unit along the y-axis
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)

                house.route.append(self.district.cables[-1].id)
        
