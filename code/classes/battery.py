# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

class Battery():
    """
    Class that creates a battery with coordinates and capacity
    """
    def __init__(self, x, y, capacity):

        #coordinates
        self.x = x
        self.y = y

        # capacity of battery
        self.max_capacity = capacity

        self.current_capacity = 0
        
        # list of houses connected to battery per battery is stored here
        self.connected_houses = []

        # list of cables connecxted to battery per battery is stored here
        self.cables = {}

        self.color = None


    def connect_house(self, house):
        """
        If a house is not connected to a battery yet, it is added to the list of connected houses
        """
        if house not in self.connected_houses:
            self.connected_houses.append(house)
            self.current_capacity += house.maxoutput

    def can_connect(self, house):
            """
            Checks if a house can be connected to the battery without exceeding its capacity.
            """
            total_power = sum(house.maxoutput for house in self.connected_houses)
            if (total_power + house.maxoutput) <= self.max_capacity:
                return True  # The house can be connected
            else:
                return False  # The house cannot be connected due to capacity constraints
    
        