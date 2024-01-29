import random
from nearest_object_y import nearest_object_y


class Hillclimber:
    def __init__(self, district):
        self.district = district
        self.near_obj_y = nearest_object_y(district)
        self.best_solution = None
        self.best_cost = float("inf")

        #here the state before the step is saved in case the cost increases after the step meaning the 
        #previous state had a better cost
        self.previous_state = None 

    def initial_solution(self):
        """Generate start population based upon the nearest obj y algorithm"""
        self.near_obj_y.connect_houses_to_batteries()
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

        house = random.choice(self.district.houses)

        #previous state method doesn't exist yet, will be made in a minute
        self.previous_state = {house: list(house.route)}


    def hillclimber(self, iterations=100):
        """Here the hillclimb optimization is performed for a given iterations"""
        
        self.current_solution

        for _ in range(iterations):
            self.solution_change()
            current_solution = self.current_solution()
            current_cost = self.evaluate_solution(current_solution)

            if current_cost < self.best_cost:
                self.best_cost = current_solution
                self.best_cost = current_cost
            
            else:
                self.undo_change()

    def undo_change(self):
        """undo the last change if it increased the cost"""

        #implement later
        pass



