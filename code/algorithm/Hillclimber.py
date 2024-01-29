
from nearest_object_y import nearest_object_y


class Hillclimber:
    def __init__(self, district):
        self.district = district
        self.near_obj_y = nearest_object_y(district)
        self.best_solution = None
        self.best_cost = float("inf")

    def initial_solution(self):
        """Generate start population based upon the nearest obj y algorithm"""
        self.near_obj_y.connect_houses_to_batteries()
        self.best_solution = self.current_solution()
        self.best_cost = self.evaluate_solution(self.best_solution)

    def current_solution(self):
        """Get the current solution from the algoritmh"""
        
        #implement later
        pass

    def evaluate_solution(self):
        """evaluate the current solution"""

        #implement later
        pass

    def solution_change(self):
        """Add a minor change to the cables or connections"""

        #implement later
        pass

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



