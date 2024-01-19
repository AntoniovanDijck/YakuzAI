class Greedy:
    def __init__(self, experiment):
        self.experiment = experiment

    def connect_houses_to_batteries(self):
        for house in self.experiment.houses:
            nearest_battery = self.experiment.find_nearest_battery(house)

            # Align on the x-axis
            for x in range(min(house.x, nearest_battery.x), max(house.x, nearest_battery.x)):
                self.experiment.place_cables(x, house.y, x+1, house.y)

            # Align on the y-axis
            for y in range(min(house.y, nearest_battery.y), max(house.y, nearest_battery.y)):
                self.experiment.place_cables(nearest_battery.x, y, nearest_battery.x, y+1)

            nearest_battery.connect_house(house)
