
class Battery():
    """
    Class that creates a battery with coordinates and capacity
    """
    def __init__(self, x, y, capacity):

        #coordinates
        self.x = x
        self.y = y

        # capacity of battery
        self.capacity = capacity
        
        # list of houses connected to battery per battery is stored here
        self.connected_houses = []

        # list of cables connecxted to battery per battery is stored here
        self.cables = []

    def connect_house(self, house):
        """
        If a house is not connected to a battery yet, it is added to the list of connected houses
        """
        if house not in self.connected_houses:
            self.connected_houses.append(house)


    
        