import random 

class RandomAlgorithm:
    """
    A class that implements a random pathfinding algorithm.
    """
    def __init__(self, experiment):
        self.experiment = experiment

    def connect_houses_to_batteries(self):
        """
        Connects houses to batteries using a random pathfinding algorithm.
        """

        # Shuffle the list of houses
        random.shuffle(self.experiment.houses)

        # Try to connect each house to a battery
        for house in self.experiment.houses:
            connected = False
            tried_batteries = set()

            # while the house is not connected and there are still batteries to try
            while not connected and len(tried_batteries) < len(self.experiment.batteries):
                selected_battery = random.choice(self.experiment.batteries) 

                # Check if the battery has not been tried yet
                if selected_battery not in tried_batteries:
                    tried_batteries.add(selected_battery)

                    # Check if the battery has enough capacity
                    if selected_battery.can_connect(house) == True:  

                        # Connect the house to the battery
                        selected_battery.connect_house(house)

                        # Place cables
                        self.place_cables(house, selected_battery)
                        connected = True
            if not connected:
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")

    # # VERSION 1.0
    # def place_cables(self, house, battery):
    #         closest_cable, cable_distance = self.experiment.find_closest_cable(house)
    #         battery_distance = abs(house.x - battery.x) + abs(house.y - battery.y)

    #         if cable_distance < battery_distance:
    #             # Connect to the closest cable segment instead of directly to the battery.
    #             # Let's assume the closest cable segment is horizontal for simplicity.
    #             for x in range(min(house.x, closest_cable.start_x), max(house.x, closest_cable.start_x) + 1):
    #                 self.experiment.place_cables(x, house.y, x + 1, house.y)
    #             # Now connect vertically to the actual closest cable point.
    #             for y in range(min(house.y, closest_cable.start_y), max(house.y, closest_cable.start_y) + 1):
    #                 self.experiment.place_cables(closest_cable.start_x, y, closest_cable.start_x, y + 1)
    #         else:
    #             # Connect directly to the battery, same as before.
    #             # Align on the x-axis
    #             for x in range(min(house.x, battery.x), max(house.x, battery.x) + 1):
    #                 self.experiment.place_cables(x, house.y, x + 1, house.y)
    #             # Align on the y-axis
    #             for y in range(min(house.y, battery.y), max(house.y, battery.y) + 1):
    #                 self.experiment.place_cables(battery.x, y, battery.x, y + 1)

    # VERSION 2.0
    # Nieuwe standaard versie van place_cables :) x antonio
    ## TODO pas deze aan om het leggen van kabels ook random te maken, 
    ## nu is het eerst x-as en dan y-as kabels leggen...     
    # def place_cables(self, house, battery):
    #     # Place cable on x
    #     if house.x != battery.x:
    #         x_start, x_end = sorted([house.x, battery.x])
    #         self.experiment.place_cables(x_start, house.y, x_end, house.y)

    #     # Place cable on y
    #     if house.y != battery.y:
    #         y_start, y_end = sorted([house.y, battery.y])
    #         self.experiment.place_cables(battery.x, y_start, battery.x, y_end)

    # VERSION 3.0
                
    def connect_to_cable(self, house, closest_cable):
        """This method connects houses to the cable"""

        # horizontal connection
        if house.x != closest_cable.start_x:
            x_start, x_end = sorted([house.x, closest_cable.start_x])
            for x in range(x_start, x_end):
                self.experiment.place_cables(x, house.y, x + 1, house.y)

        # vertical connection
        if house.y != closest_cable.start_y:
            y_start, y_end = sorted([house.y, closest_cable.start_y])
            for y in range(y_start, y_end):
                self.experiment.place_cables(closest_cable.start_x, y, closest_cable.start_x, y + 1)

    def connect_directly(self, house, battery):
        """This method connects house to the battery"""

        # horizontal connection
        if house.x != battery.x:
            x_start, x_end = sorted([house.x, battery.x])
            for x in range(x_start, x_end):
                self.experiment.place_cables(x, house.y, x + 1, house.y)

        # vertical connection
        if house.y != battery.y:
            y_start, y_end = sorted([house.y, battery.y])
            for y in range(y_start, y_end):
                self.experiment.place_cables(battery.x, y, battery.x, y + 1)

    def place_cables(self, house, battery):
        closest_cable, cable_distance = self.experiment.find_closest_cable(house)
        battery_distance = abs(house.x - battery.x) + abs(house.y - battery.y)

        # See what is closest battery connection or cable connection
        if cable_distance < battery_distance and closest_cable != None:
            self.connect_to_cable(house, closest_cable)
        
        else:
            self.connect_directly(house, battery)
        
