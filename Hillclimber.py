import random
from code.algorithm.dijckstra import dijckstra
from code.classes.district import District

class Hillclimber:
    def __init__(self, district, depth=1):
        self.district = district
        self.best_cost = float("inf")
        self.depth = depth
        #here the state before the step is saved in case the cost increases after the step meaning the 
        #previous state had a better cost
        self.previous_state = None 

    def initial_solution(self):
        """Generate start population based upon the dijckstra"""
        self.dijckstra.connect_houses_to_batteries()
        self.best_solution = self.current_solution()
        self.best_cost = self.evaluate_solution(self.best_solution)

    def current_solution(self):
        """Get the current solution from the algoritmh"""

        return {house: house.route for house in self.district.houses}
    

    def evaluate_solution(self):
        """evaluate the current solution"""

        return self.district.calculate_totals()

    def solution_change(self):
        """Add a minor change to the cables or connections"""

        for i in range(self.depth):

            if random.choice([True, False]):

                # select a random battery
                connected_battery = random.choice(self.district.batteries)

                # select a random house connected to this battery
                house = random.choice(connected_battery.connected_houses)

                # remove the house from the battery
                self.district.remove_connected_house(house, connected_battery)

                break

        # Reconnect the houses using dijckstra
        
        self.dijckstra.connect_houses_to_batteries()


    def hillclimber(self, iterations=100):
        """Here the hillclimb optimization is performed for a given iterations"""
        

        for _ in range(iterations):
            self.solution_change()
            current_solution = self.current_solution()
            current_cost = self.evaluate_solution(current_solution)

            if current_cost < self.best_cost:
                self.best_cost = current_solution
                self.best_cost = current_cost
                print("New best cost: ", self.best_cost)
            
            else:
                self.undo_change()

    def undo_change(self):
        """undo the last change if it increased the cost"""

        for house, route in self.previous_state.items():
            house.route = route



# Run the hillclimber
            
houses_file = 'simulation_results/dijckstra_lowest_cost_order.csv'
batteries_file = 'data/Huizen&Batterijen/district_1/district-1_batteries.csv'


district = District(houses_file, batteries_file)


hillclimber = Hillclimber(dijckstra)
hillclimber.hillclimber()
