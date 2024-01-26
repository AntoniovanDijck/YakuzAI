# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

class Cable:
    """
    Class that creates a cable with coordinates and an id
    """
    def __init__(self, start_x, start_y, end_x, end_y, battery = None):

        # Coordinates
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

        # As the cables are used in the algorithm, the x and y coordinates are used as the current position of the cable
        self.x = start_x
        self.y = start_y

        # Create an id for the cable
        self.id = f"{start_x},{start_y}, {end_x}, {end_y}"

        # Every cable can be connected to a battery and this is stored in this attribute
        self.connected_battery = battery

