import csv
from code.classes.house import House
from code.classes.battery import Battery
from code.classes.cable import Cable
from code.helpers.smart_grid import load_battery_data, load_house_data
import random

class Experiment:
    def __init__(self, houses_file, batteries_file):
        # Load houses and batteries
        house_dict = load_house_data(houses_file)
        battery_dict = load_battery_data(batteries_file)

        # Create houses and batteries using the data
        self.houses = [House(x, y, maxoutput) for (x, y), maxoutput in house_dict.items()]
        self.batteries = [Battery(x, y, capacity) for (x, y), capacity in battery_dict.items()]
        self.cables = []


    def load_houses(self, file_path):
        """
        This method loads in the houses from a csv file and returns a list of houses
        """

        # create empty list for houses
        houses = []

        # open file and read in the data
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house = House(int(row['x']), int(row['y']), float(row['maxoutput']))
                houses.append(house)
        return houses

    def load_batteries(self, file_path):
        """
        This method loads in the batteries from a csv file and returns a list of batteries
        """

        # create empty list for batteries
        batteries = []

        # open file and read in the data and create batteries
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                x, y = map(int, row['positie'].split(','))
                battery = Battery(x, y, float(row['capaciteit']))
                batteries.append(battery)
        return batteries


    def find_nearest_battery(self, house):
        return min(self.batteries, key=lambda battery: abs(battery.x - house.x) + abs(battery.y - house.y))

    def place_cables(self, start_x, start_y, end_x, end_y):
        new_cable = Cable(start_x, start_y, end_x, end_y)

        # Check for duplicate cables
        for cable in self.cables:
            if cable.id == new_cable.id:
                return  # Cable already exists, no need to add again
        
        self.cables.append(new_cable)

    
    def get_cables_for_route(self, house, battery):
        """
        This method returns a set of cables that are part of the route from a house to a battery
        """
        route_cables = set()

        # Generate horizontal cable segments
        for x in range(min(house.x, battery.x), max(house.x, battery.x)):
            cable = Cable(x, house.y, x + 1, house.y)
            route_cables.add(cable)

        # Generate vertical cable segments
        for y in range(min(house.y, battery.y), max(house.y, battery.y)):
            cable = Cable(battery.x, y, battery.x, y + 1)
            route_cables.add(cable)

        return route_cables

    def shared_cables(self):
        """This method checks if a cable segment is already existing"""

        used_cables = {}
        
        for house in self.houses:
            return None

    def is_cable_connected_to_battery(self, cable, battery):
        """
        This method checks if a cable is connected to a battery
        """

        # Check if a cable end point is at the battery location
        return ((cable.end_x, cable.end_y) == (battery.x, battery.y) or
                (cable.start_x, cable.start_y) == (battery.x, battery.y))
    
    def calculate_totals(self):
        """
        Calculates the total output and total cables used per battery
        """

        total_cost = 0

        # Loop over batteries
        for battery in self.batteries:

            total_cost += 5000

            # Calculate total output as a sum of the max output of the connected houses
            total_output = sum(house.maxoutput for house in battery.connected_houses)

            # Create a set of cables to prevent duplicates
            battery_cables = set()

            # Loop over houses connected to the battery
            for house in battery.connected_houses:

                # Loop over cables
                for cable in self.get_cables_for_route(house, battery):
                    
                    # Check if the cable is connected to the battery
                    battery_cables.add(cable.id)


            # Calculate the total cables used
            total_cables = len(battery_cables)

            # Add a cost of 9 per cabkle
            total_cost += total_cables * 9

            # Print the results
            print(f'Battery at ({battery.x}, {battery.y}):')
            print(f'  Total output connected: {total_output}')
            print(f'  Total cables used: {total_cables}')
           
        print(f'  Total cost: {total_cost}')

        return total_cost
    
    def check_50(self): 
        """"""
        output_data = []

        for battery in self.batteries:
            battery_data = {
                "position": f"{battery.x},{battery.y}",
                "capacity": battery.capacity,
                "houses": [] 
            }


            for house in battery.connected_houses:
                #generate cables for each house
                cables = self.get_cables_for_route(house, battery)

                cable_data = [f"{cable.start_x},{cable.start_y}" for cable in cables]
                house_data = {
                    "location": f"{house.x}, {house.y}", "output": house.maxoutput, "cables": cable_data
                }

                battery_data['houses'].append(house_data)
            
            output_data.append(battery_data)

        cost_own = self.calculate_totals()
        cost_shared = 0 # for now zero but here should be the cost of the grid when houses can use the same cables to be connected
        output_data.insert(0, {"district":1, "cost-own": cost_own})

        return output_data
    


# battery_district1_link = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'
# house_district1_link = 'data/Huizen&Batterijen/district_1/district-1_houses.csv'
# experiment = Experiment(house_district1_link, battery_district1_link)
# experiment.calculate_totals()


# output_data = experiment.check_50()

# #to json file
# with open(f'data/output_data/output-{datetime.datetime.now():%Y-%m-%d-%H:%M}.json','w') as outfile:
#     json.dump(output_data, outfile)