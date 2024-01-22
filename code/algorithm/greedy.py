class Greedy:
    def __init__(self, experiment):
        self.experiment = experiment

    def connect_houses_to_batteries(self):
        for house in self.experiment.houses:
            # Sort batteries by distance to the house
            sorted_batteries = sorted(self.experiment.batteries, 
                                      key=lambda battery: abs(battery.x - house.x) + abs(battery.y - house.y))

            for battery in sorted_batteries:
                if battery.can_connect(house):
                    # Align on the x-axis
                    for x in range(min(house.x, battery.x), max(house.x, battery.x) + 1):
                        self.experiment.place_cables(x, house.y, x+1, house.y)

                    # Align on the y-axis
                    for y in range(min(house.y, battery.y), max(house.y, battery.y) + 1):
                        self.experiment.place_cables(battery.x, y, battery.x, y+1)

                    battery.connect_house(house)
                    break  # Stop looking for a battery once connected
            else:
                # This block is executed if the house couldn't be connected to any battery
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")

class Greedy2:
    def __init__(self, district):
        self.district = district

    def distance(self, house, battery):
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def connect_houses_to_batteries(self):
        # Precompute distances
        for house in self.district.houses:
            house.battery_distances = [(battery, self.distance(house, battery)) for battery in self.district.batteries]
            house.battery_distances.sort(key=lambda x: x[1])

        for house in self.district.houses:
            for battery, _ in house.battery_distances:
                if battery.can_connect(house):
                    self.place_cables(house, battery)
                    battery.connect_house(house)
                    break
            else:
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")

    def place_cables(self, house, battery):
        # Place cable along x-axis
        if house.x != battery.x:
            x_start, x_end = sorted([house.x, battery.x])
            self.district.place_cables(x_start, house.y, x_end, house.y)

        # Place cable along y-axis
        if house.y != battery.y:
            y_start, y_end = sorted([house.y, battery.y])
            self.district.place_cables(battery.x, y_start, battery.x, y_end)
