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
