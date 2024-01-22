
class Cable:
    """
    Class that creates a cable with coordinates and an id
    """
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

        # Create an id for the cable
        self.id = f"{start_x}, {start_y}-{end_x},{end_y}"
