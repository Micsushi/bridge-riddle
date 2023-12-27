class Zombie_problem(object):
    def __init__(self):
        # create the graph here
        self.crossing_time = {
            "U": 1,  # Undergrad
            "G": 2,  # Grad
            "P": 5,  # Postgrad
            "R": 10,  # Prof
        }


    def heuristic(self, node):
        """Returns the heuristic value of `node`"""
        not_crossed = [letter for letter in node if letter.isupper()]
        if "F" in not_crossed:
            not_crossed.remove("F")
        return sum(self.crossing_time[letter] for letter in not_crossed)/2
        
    def calculate_cost(self, crossers):
        if len(crossers) == 1:
            return self.crossing_time[crossers[0].upper()]
        else:
            return self.crossing_time[max(crossers, key=self.crossing_time.get).upper()]

p=Zombie_problem()
p.heuristic("UGpRf")
p.heuristic("UGPRF")