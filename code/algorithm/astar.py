class A_star:
    def __init__(self, district):
        self.district = district

    def distance(self, house, battery):
        ''' Function that calculates the Manhattan distance between a house and a battery'''
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def a_star_search(self, house, battery):
        batteries_sorted = [(self.distance(house, battery), house)]
        vorige_node = {}
        g_score = {node: float("inf") for node in self.district.batteries}
        g_score[house] = 0

        while batteries_sorted:
            batteries_sorted.sort(key=lambda x: x[0])
            current = batteries_sorted.pop(0)[1]

            if current == battery:
                break

            for next in current.connections:
                new_g_score = g_score[current] + self.distance(current, next)

                if new_g_score < g_score[next]:
                    vorige_node[next] = current
                    g_score[next] = new_g_score

                    # Check if next is already in batteries_sorted
                    for i, (existing_f_score, existing_node) in enumerate(batteries_sorted):
                        if existing_node == next:
                            if new_g_score + self.distance(next, battery) < existing_f_score:
                                batteries_sorted[i] = (new_g_score + self.distance(next, battery), next)
                            break
                    else:
                        batteries_sorted.append((new_g_score + self.distance(next, battery), next))

        return vorige_node
    
    def connect_houses_to_batteries2(self):
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