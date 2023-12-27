
from heapq import heappush, heappop


class Zombie_problem(object):
    def __init__(self):
        # create the graph here
        self.crossing_time = {
            "U": 1,  # Undergrad
            "G": 2,  # Grad
            "P": 5,  # Postgrad
            "R": 10,  # Prof
        }

        # start with UGPRF
        self.start = "UGPRF"

        self.crosses = self.possible_crossing(self.start)

        # use a stack to generate each path till it reaches ugprf
        self.graph = {}
        stack = [(self.start, [])]

        while stack:
            node, path = stack.pop()

            if node in self.graph:
                continue

            self.graph[node] = []

            if self.is_goal(node):
                continue

            self.crosses = self.possible_crossing(node)

            for cross in self.crosses:
                new_node = self.crossing(node, cross)
                cost = self.calculate_cost(cross)
                self.graph[node].append((new_node, cost))
                stack.append((new_node, path + [(node, new_node, cost)]))

    def possible_crossing(self, node):
        letters = node[:]
        if "F" in node:
            # going to end
            letters = [letter for letter in node if letter.isupper()][:-1]
            pairs = []
            for i in range(len(letters)):
                for j in range(i + 1, len(letters)):
                    pairs.append((letters[i], letters[j]))
            return pairs
        else:
            # going back to start
            letters = [letter for letter in node if letter.islower()][:-1]
            return [(letter,) for letter in letters]

    def crossing(self, node, crossers):
        new_node = ""
        crossers = list(crossers)
        if crossers[0].isupper():
            crossers.append("F")
        else:
            crossers.append("f")
        for letter in node:
            if letter in crossers:
                if letter.isupper():
                    new_node += letter.lower()
                else:
                    new_node += letter.upper()
            else:
                new_node += letter
        return new_node

    def calculate_cost(self, crossers):
        if len(crossers) == 1:
            return self.crossing_time[crossers[0].upper()]
        else:
            return self.crossing_time[max(crossers, key=self.crossing_time.get).upper()]

    def start_node(self):
        """returns start node"""
        return "UGPRF"

    def is_goal(self, node):
        """is True if `node` is a goal"""
        return node == "ugprf"

    def neighbors(self, node):
        """returns a list of the arcs for the neighbors of `node`"""
        return self.graph.get(node, [])

    def arc_cost(self, arc):
        """Returns the cost of `arc`"""
        return arc[1]

    def cost(self, path):
        """Returns the cost of `path`"""
        return sum(self.arc_cost(arc) for arc in path)

    def heuristic(self, node):
        """Returns the heuristic value of `node`"""
        not_crossed = [letter for letter in node if letter.isupper()]
        if "F" in not_crossed:
            not_crossed.remove("F")
        return sum(self.crossing_time[letter] for letter in not_crossed) / 2

    def search(self):
        """Return a solution path"""
        frontier = Frontier()  # Initialize the frontier

        # Start node and path are pushed onto the frontier
        start_node = self.start_node()
        frontier.add((start_node, []), 0)

        while not frontier.is_empty():
            (
                node,
                path,
            ), cost_so_far = (
                frontier.remove()
            )  # Get the next path with the highest priority

            if self.is_goal(node):
                return path

            for neighbor, arc_cost in self.neighbors(node):
                new_path = path + [(neighbor, arc_cost)]
                total_cost = (
                    cost_so_far + arc_cost + self.heuristic(neighbor)
                )  # Include heuristic in total cost
                frontier.add((neighbor, new_path), total_cost)
        return None


class Frontier(object):
    """
    Convenience wrapper for a priority queue usable as a frontier
    implementation.
    """

    def __init__(self):
        self.heap = []

    def add(self, path, priority):
        """Add `path` to the frontier with `priority`"""
        # Push a ``(priority, item)`` tuple onto the heap so that `heappush`
        # and `heappop` will order them properly
        heappush(self.heap, (priority, path))

    def remove(self):
        """Remove and return the smallest-priority path from the frontier"""
        priority, path = heappop(self.heap)
        return path, priority

    def is_empty(self):
        return len(self.heap) == 0


def unit_tests():
    """
    Some trivial tests to check that the implementation even runs.
    Feel free to add additional tests.
    """
    print("testing...")
    p = Zombie_problem()
    assert p.start_node() is not None
    assert not p.is_goal(p.start_node())
    assert p.heuristic(p.start_node()) >= 0

    ns = p.neighbors(p.start_node())
    assert len(ns) > 0

    soln = p.search()
    assert p.cost(soln) > 0
    print("tests ok")


def main():
    unit_tests()
    p = Zombie_problem()
    soln = p.search()
    if soln:
        print("Solution found (cost=%s)\n%s" % (p.cost(soln), soln))
    else:
        raise RuntimeError("Empty solution")


if __name__ == "__main__":
    main()
