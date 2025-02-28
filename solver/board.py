import copy
import matplotlib.pyplot as plt
import numpy as np
import heapq
from collections import Counter
from reader import read_input_file
from reader import path

""" Board game class to manage the game """

color_abbreviation = {
        'V': 'green',
        'B': 'white',
        'R': 'red',
        'A': 'yellow',
        'N': 'orange',
        'Z': 'blue',
        '*': 'black'
}

def flatten(lst):
    return [item for sublist in lst for item in sublist]

def validate_file_state(file_state, goal, min_size=3):
    # Check it has at least 3 rows and 3 columns
        if len(file_state) < min_size or any(len(row) < min_size for row in file_state):
             raise ValueError(f'The board must have at least {min_size}x{min_size} dimensions')
        
    # Check it has only valid colors
        colors = set(flatten(file_state))
        invalid_colors = colors - set(color_abbreviation.keys())
        if invalid_colors:
            raise ValueError(f'Invalid colors found: {invalid_colors}, must be one of {color_abbreviation.keys()}')
    
        if goal == False:
            # Check color count, each color must have (n*n)-1/6 pieces
            n = len(file_state)
            total_blocks = n*n
            colors = ['V', 'B', 'R', 'A', 'N', 'Z']
            blocks_per_color = (total_blocks - 1) // 6 # Expected quantity of each color

            expected_counts = {color: blocks_per_color for color in colors}
            expected_counts['*'] = 1 #  There is only one black block

            # Count the actual number of blocks of each color
            actual_counts = Counter(color for row in file_state for color in row)

            # Validate the difference between the expected and actual counts
            invalid_counts = {color: actual_counts.get(color, 0) - expected_counts.get(color, 0) 
                            for color in expected_counts if actual_counts.get(color, 0) != expected_counts.get(color, 0)}

            if invalid_counts:
                raise ValueError(f'Invalid color count. Must have {blocks_per_color} blocks per color, and 1 black block.')


def generate_state_from_file(file_name, goal=False):
    colors = ['green', 'white', 'red', 'yellow', 'orange', 'blue']
    file_state = read_input_file(file_name)
    
    try:
        validate_file_state(file_state, goal)
    except ValueError as e:
        print(e)
        exit(1)

    n = len(file_state)
    total_blocks = n*n

    grid = [[color_abbreviation[color] for color in row] for row in file_state]
    return grid


def display_grid(grid):
    n = len(grid)
    block_size = 50
    border_size = 1

    image = np.ones(((n + 1) * border_size + n * block_size, (n + 1) * border_size + n * block_size, 3),
                    dtype=np.uint8) * 0

    color_mapping = {
        'green': (0, 255, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0)
    }

    for i in range(n):
        for j in range(n):
            color = color_mapping[grid[i][j]]
            start_row = i * (block_size + border_size) + border_size
            end_row = start_row + block_size
            start_col = j * (block_size + border_size) + border_size
            end_col = start_col + block_size

            image[start_row:end_row, start_col:end_col] = color

    plt.imshow(image)
    plt.axis('off')
    plt.savefig(path+'/data/images/board_image.png')  # Save the image to a file
    plt.close()

def display_goal_state(goal_state):
    n = len(goal_state)
    block_size = 50
    border_size = 1

    image = np.ones(((n + 1) * border_size + n * block_size, (n + 1) * border_size + n * block_size, 3),
                    dtype=np.uint8) * 0
    
    color_mapping = {'green': (0, 255, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'yellow': (255, 255, 0),
                     'orange': (255, 165, 0), 'blue': (0, 0, 255), '': (0, 0, 0)}

    for i in range(n):
        for j in range(n):
            color = color_mapping[goal_state[i][j]]
            start_row = i * (block_size + border_size) + border_size
            end_row = start_row + block_size
            start_col = j * (block_size + border_size) + border_size
            end_col = start_col + block_size

            image[start_row:end_row, start_col:end_col] = color

    plt.imshow(image)
    plt.axis('off')
    plt.savefig(path+'/data/images/goal_image.png')  # Save the image to a file

class Puzzle:
    def __init__(self, n, goal, puzzle):
        self.size = n
        self.goal_state = goal
        self.puzzle = puzzle
        self.black_row, self.black_col = self.find_black_block()
        self.path_cost = 0

    def __hash__(self):
        return hash(tuple(map(tuple, self.puzzle)))
    def __eq__(self, other):
        return isinstance(other, Puzzle) and self.puzzle == other.puzzle
    def find_black_block(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i][j] == 'black':
                    return i, j
                
    def applyMove(self, m):
        if m == 'right' and self.black_col > 0:
            self.puzzle[self.black_row][self.black_col], self.puzzle[self.black_row][self.black_col - 1] = \
            self.puzzle[self.black_row][self.black_col - 1], self.puzzle[self.black_row][self.black_col]
            self.black_col -= 1
        elif m == 'left' and self.black_col < self.size - 1:
            self.puzzle[self.black_row][self.black_col], self.puzzle[self.black_row][self.black_col + 1] = \
            self.puzzle[self.black_row][self.black_col + 1], self.puzzle[self.black_row][self.black_col]
            self.black_col += 1
        elif m == 'down' and self.black_row > 0:
            self.puzzle[self.black_row][self.black_col], self.puzzle[self.black_row - 1][self.black_col] = \
            self.puzzle[self.black_row - 1][self.black_col], self.puzzle[self.black_row][self.black_col]
            self.black_row -= 1
        elif m == 'up' and self.black_row < self.size - 1:
            self.puzzle[self.black_row][self.black_col], self.puzzle[self.black_row + 1][self.black_col] = \
            self.puzzle[self.black_row + 1][self.black_col], self.puzzle[self.black_row][self.black_col]
            self.black_row += 1
        self.path_cost += 1

    def is_goal_state(self):
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.puzzle[i][j] != self.goal_state[i - 1][j - 1]:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)
    
    def get_possible_moves(self):
        possible_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i][j] == 'black':
                    if i > 0:
                        possible_moves.append("up")
                    if i < self.size - 1:
                        possible_moves.append("down")
                    if j > 0:
                        possible_moves.append("left")
                    if j < self.size - 1:
                        possible_moves.append("right")
        return possible_moves
    
    def __lt__(self, other):
        return (self.path_cost + self.numberOfMisplacedHeuristic()) < (other.path_cost + other.numberOfMisplacedHeuristic())
    
    def numberOfMisplacedHeuristic(self):
        heuristic_value = (self.size - 2) * (self.size - 2)

        current_positions = {color: [] for color in set(flatten(self.puzzle))}
        goal_positions = {color: [] for color in set(flatten(self.goal_state))}

        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):

                current_color = self.puzzle[i][j]

                if current_color == "black":
                    continue
                goal_color = self.goal_state[i - 1][j - 1]

                if current_color != '' and goal_color != '':
                    goal_positions[goal_color].append((i, j))

        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                current_color = self.puzzle[i][j]
                if current_color == "black":
                    continue
                current_positions[current_color].append((i, j))

        for color in current_positions:
            if color == "black":
                continue

            elif color not in goal_positions:
                continue

            current_color_positions = current_positions[color]
            goal_color_positions = goal_positions[color]

            for current_pos in current_color_positions:
                if current_pos in goal_color_positions:
                    heuristic_value -= 1

        return heuristic_value
