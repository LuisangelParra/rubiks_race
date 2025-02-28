from board import display_grid
import heapq
from collections import deque

class IDA:
    def __init__(self, initial_state, n):
        self._n = n
        self.initial_state = initial_state
        self.threshold = None
        self.pruned = None

    def searchNumMisplacedTiles(self):
        self.pruned = deque()
        self.threshold = self.initial_state.path_cost + self.initial_state.numberOfMisplacedHeuristic()
        #heapq.heappush(self.pruned, (self.initial_state.path_cost + self.initial_state.numberOfMisplacedHeuristic(), self.initial_state))
        self.pruned.append((self.initial_state.path_cost + self.initial_state.numberOfMisplacedHeuristic(), self.initial_state))
        print(f"Initial threshold: {self.threshold}")
        c = 0
        while True:
            c += 1
            print(f"ITERATION: {c}")
            result = self.NumMisplacedTiles_search_depth(self.initial_state, self.initial_state.path_cost)
            if result:
                print("Goal state reached!")
                return result

            else:
                
                self.threshold = max(self.pruned)[0]
                self.pruned.remove(max(self.pruned))
                print(f"Threshold: {self.threshold}")

    def NumMisplacedTiles_search_depth(self, current_state, g):
        f = g + current_state.numberOfMisplacedHeuristic()

        if f > self.threshold:
            #heapq.heappush(self.pruned, (current_state.path_cost + current_state.numberOfMisplacedHeuristic(), current_state))
            self.pruned.append((current_state.path_cost + current_state.numberOfMisplacedHeuristic(), current_state))

            return None

        if current_state.is_goal_state():
            return current_state

        for move in current_state.get_possible_moves():
            new_state = current_state.copy()
            new_state.applyMove(move)

            child_result = self.NumMisplacedTiles_search_depth(new_state, g + 1)

            if child_result:
                return child_result

        return None