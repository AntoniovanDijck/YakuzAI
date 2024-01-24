class nearest_battery:
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
                    self.place_cables(house, battery)  # Place cables one by one
                    battery.connect_house(house)
                    break
            else:
                print(f"House at ({house.x}, {house.y}) could not be connected to any battery.")


    def place_cables(self, house, battery):

        # Place cable along x-axis
        if house.x != battery.x:
            x_start, x_end = sorted([house.x, battery.x])
            for x in range(x_start, x_end):
                # Create a new cable segment for each unit along the x-axis
                self.district.place_cables(x, house.y, x + 1, house.y, battery)

                house.route.append(self.district.cables[-1].id)

        # Place cable along y-axis
        if house.y != battery.y:
            y_start, y_end = sorted([house.y, battery.y])
            for y in range(y_start, y_end):
                
                # Create a new cable segment for each unit along the y-axis
                self.district.place_cables(battery.x, y, battery.x, y + 1, battery)

                house.route.append(self.district.cables[-1].id)