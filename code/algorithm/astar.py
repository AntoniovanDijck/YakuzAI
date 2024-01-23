class A_star:
    def __init__(self, district):
        self.district = district

    def distance(self, house, battery):
        ''' Function that calculates the Manhattan distance between a house and a battery'''
        return abs(battery.x - house.x) + abs(battery.y - house.y)
    def connect_houses_to_batteries(self):
        for house in self.district.houses:
            # maak een lijst met de batterijen en hun afstand t.o.v huis
            batteries_sorted = [(self.distance(house, battery), battery.x, battery) for battery in self.district.batteries]
 
            # Sort batteries weer op afstand
            batteries_sorted.sort()

            # Loop door de batterijen heen en kijk of het huis verbonden kan worden
            for h, d, battery in batteries_sorted:
                if battery.can_connect(house):
                    self.place_cables(house, battery)
                    battery.connect_house(house)
                    break
            else:
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")

    def place_cables(self, house, battery):
        ''' Function that places cables between house and battery'''

        # Place cable on y-axis if the house and battery are not on the same y-axis
        if house.x != battery.x:

            # Sort x-coordinates and take the smallest and largest value
            x_start, x_end = sorted([house.x, battery.x])

            # Place cables between house and battery
            self.district.place_cables(x_start, house.y, x_end, house.y)

        # Place cable on y-axis if the house and battery are not on the same y-axis
        if house.y != battery.y:

            # Sort y-coordinates and take the smallest and largest value
            y_start, y_end = sorted([house.y, battery.y])

            # Place cables between house and battery
            self.district.place_cables(battery.x, y_start, battery.x, y_end)