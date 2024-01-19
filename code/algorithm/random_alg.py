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

    def place_cables(self, house, battery):
        # Align on the x-axis
        for x in range(min(house.x, battery.x), max(house.x, battery.x) + 1):
            # Correctly passing the start and end coordinates for each cable segment
            self.experiment.place_cables(x, house.y, x + 1, house.y)

        # Align on the y-axis
        for y in range(min(house.y, battery.y), max(house.y, battery.y) + 1):
            # Correctly passing the start and end coordinates for each cable segment
            self.experiment.place_cables(battery.x, y, battery.x, y + 1)
