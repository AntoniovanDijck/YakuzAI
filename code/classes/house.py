# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

class House():
    """
    Class that creates a house with coordinates and max output
    """
    def __init__(self, x, y, maxoutput):
        self.x = x
        self.y = y

        #houses output
        self.maxoutput = maxoutput
        
        # Set the connected route battery to None
        self.route = []