import heapq
from collections import defaultdict
from board import PuzzleState, get_internal_matrix_index, get_coordinates_from_index, get_index_from_coordinates, move_tile

class AStarSearchGraph:
    def __init__(self, initial_state,  goal_state, n):
        self.n = n
        self.initial_state = initial_state
        self.goal_state = goal_state

    #Manhattan distance heuristic functions
    def calculate_colors_goal_positions(self, goal_state):
        goal_positions = defaultdict(list)
        for i, color in enumerate(goal_state):
            goal_positions[color].append((i // (self.n-2) + 1, i % (self.n-2) + 1)) 
        return goal_positions
    
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    # Function to calculate the heuristic (Manhattan distance)
    def manhattan_distance_heuristic(self, board, colors_goal_positions):
        total_distance = 0
        colors_goal_positions = colors_goal_positions
        for i, color in enumerate(board):
            for y,x in [divmod(i, 5)]:
                if i in get_internal_matrix_index(self.n):
                    if board[i] != '*' and colors_goal_positions[color]:
                        total_distance += min(self.manhattan_distance((y,x), pos) for pos in colors_goal_positions[color])
                    if color != self.goal_state[(y-1)*(self.n-2)+(x-1)]:
                        total_distance += 1
        return total_distance

    # Function to calculate the heuristic (Missplaced tiles)
    def missplaced_tiles_heuristic(self, board, colors_goal_positions):
        missplaced_tiles = 0
        colors_goal_positions = colors_goal_positions
        for i, color in enumerate(board):
            for y,x in [divmod(i, 5)]:
                if color != '*':
                    if (y,x) not in colors_goal_positions[color]:
                        missplaced_tiles += 1
        return missplaced_tiles

    
    # A* search algorithm
    def a_star(self, heuristic):
        start_state = self.initial_state
        goal_state = self.goal_state
        open_list = []
        closed_list = set()
        colors_goal_positions = self.calculate_colors_goal_positions(goal_state)
        if heuristic == 'manhattan':
            heapq.heappush(open_list, PuzzleState(start_state,  self.n, None, None, 0, self.manhattan_distance_heuristic(start_state, colors_goal_positions)))
        elif heuristic == 'missplaced':
            heapq.heappush(open_list, PuzzleState(start_state,  self.n, None, None, 0, self.missplaced_tiles_heuristic(start_state, colors_goal_positions)))
        else:
            print("Invalid heuristic")
            return None

        c = 0
        while open_list:
            c += 1
            current_state = heapq.heappop(open_list)
            current_state_goal_positions = [current_state.board[i] for i in current_state.internal_matrix_index]

            if current_state_goal_positions == goal_state:
                return current_state
            
            closed_list.add(tuple(current_state.board))

            blank_pos = current_state.board.index("*")

            for move in current_state.moves:
                if move == 'D' and blank_pos < current_state.n: # Invalid move down
                    continue
                if move == 'U' and blank_pos >= current_state.n * (current_state.n - 1): # Invalid move up
                    continue
                if move == 'R' and blank_pos % current_state.n == 0: # Invalid move right
                    continue
                if move == 'L' and blank_pos % current_state.n == current_state.n - 1: # Invalid move left
                    continue
                new_board = move_tile(current_state.board, move, blank_pos, current_state.moves)

                if tuple(new_board) in closed_list:
                    continue

                if heuristic == 'manhattan':
                    new_state = PuzzleState(new_board,  self.n, current_state, move, current_state.depth + 1, current_state.depth + 1 + self.manhattan_distance_heuristic(new_board, colors_goal_positions))
                elif heuristic == 'missplaced':
                    new_state = PuzzleState(new_board,  self.n, current_state, move, current_state.depth + 1, current_state.depth + 1 + self.missplaced_tiles_heuristic(new_board, colors_goal_positions))
                heapq.heappush(open_list, new_state)

        return None
    

    def IDA_star(self, heuristic):
        start_state = self.initial_state
        goal_state = self.goal_state
        colors_goal_positions = self.calculate_colors_goal_positions(goal_state)

        if heuristic == 'manhattan':
            threshold = self.manhattan_distance_heuristic(start_state, colors_goal_positions)
        elif heuristic == 'missplaced':
            threshold = self.missplaced_tiles_heuristic(start_state, colors_goal_positions)
        else:
            print("Invalid heuristic")
            return

        def search(current_state, threshold):
            if heuristic == 'manhattan':
                f = current_state.depth + self.manhattan_distance_heuristic(current_state.board, colors_goal_positions)
            elif heuristic == 'missplaced':
                f = current_state.depth + self.missplaced_tiles_heuristic(current_state.board, colors_goal_positions)

            current_state_goal_positions = [current_state.board[i] for i in current_state.internal_matrix_index]
            
            if f > threshold:
                return f, None
            
            if current_state_goal_positions == self.goal_state:
                return f, current_state
            
            min_overflow = float('inf')
            blank_pos = current_state.board.index("*")
            
            for move in current_state.moves:
                if move == 'D' and blank_pos < current_state.n: # Invalid move down
                    continue
                if move == 'U' and blank_pos >= current_state.n * (current_state.n - 1): # Invalid move up
                    continue
                if move == 'R' and blank_pos % current_state.n == 0: # Invalid move right
                    continue
                if move == 'L' and blank_pos % current_state.n == current_state.n - 1: # Invalid move left
                    continue
                new_board = move_tile(current_state.board, move, blank_pos, current_state.moves)
                new_state = PuzzleState(new_board, self.n, current_state, move, current_state.depth + 1, 0)  # Guardar bien el padre
                new_threshold, result = search(new_state, threshold)
                if result:
                    return new_threshold, result
                min_overflow = min(min_overflow, new_threshold)

            return min_overflow, None
        
        while True:
            if heuristic == 'manhattan':
                new_threshold, result = search(PuzzleState(start_state, self.n, None, None, 0, self.manhattan_distance_heuristic(start_state, colors_goal_positions)), threshold)
            elif heuristic == 'missplaced':
                new_threshold, result = search(PuzzleState(start_state, self.n, None, None, 0, self.missplaced_tiles_heuristic(start_state, colors_goal_positions)), threshold)

            if result:
                return result, threshold
            if new_threshold == float('inf'):
                return None, None
            threshold = new_threshold