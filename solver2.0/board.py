import copy
import matplotlib.pyplot as plt
import numpy as np
import random
from termcolor import colored
from reader import read_input_file
from collections import Counter


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

def get_internal_matrix_index(n):
    if n < 3:
        return []  # No internal matrix for n < 3

    indexs = []
    for row in range(1, n - 1):
        for column in range(1, n - 1):
            index = get_index_from_coordinates(row, column, n)
            indexs.append(index)
    return indexs

def get_n_value_from_file(file_name):
    file_state = read_input_file(file_name)
    return len(file_state)

def get_coordinates_from_index(index, n):
    row = index // n
    column = index % n
    return row, column

def get_index_from_coordinates(row, column, n):
    return row * n + column

def generate_random_state(n):
    total_blocks = n * n
    colors = ['V', 'B', 'R', 'A', 'N', 'Z']
    blocks_per_color = (total_blocks - 1) // 6 

    color_counts = {color: blocks_per_color for color in colors}
    color_counts['*'] = 1

    grid = ['' for _ in range(total_blocks)]

    internal_index = get_internal_matrix_index(n)

    for i in internal_index:
        color = random.choice(colors)
        grid[i] = color
        color_counts[color] -= 1
        if color_counts[color] == 0:
            colors.remove(color)

    available_indexes = [i for i in range(total_blocks) if grid[i] == '']
    random.shuffle(available_indexes)

    for color, count in color_counts.items():
        for _ in range(count):
            i = available_indexes.pop()
            grid[i] = color
    return grid

def display_grid_in_chart(grid, n):
    block_size = 50
    border_size = 1

    image = np.ones(((n + 1) * border_size + n * block_size, (n + 1) * border_size + n * block_size, 3),
                    dtype=np.uint8) * 0

    color_mapping = {
        'V': (0, 255, 0),
        'B': (255, 255, 255),
        'R': (255, 0, 0),
        'A': (255, 255, 0),
        'N': (255, 165, 0),
        'Z': (0, 0, 255),
        '*': (0, 0, 0)
    }

    for i in range(n * n):
        row, column = get_coordinates_from_index(i, n)
        color = color_mapping[grid[i]]
        start_row = row * (block_size + border_size) + border_size
        end_row = start_row + block_size
        start_column = column * (block_size + border_size) + border_size
        end_column = start_column + block_size

    plt.imshow(image)
    plt.axis('off')
    plt.savefig('./data/images/board_image.png')
    plt.close()

def getGoalState(grid, n):
        internal_matrix_index = get_internal_matrix_index(n)
        goal_state = []
        for i in internal_matrix_index:
            goal_state.append(grid[i])
        return goal_state
    
def apply_moves_to_black_block(grid, n, moves):
        for i in range(n * n):
            if grid[i] == 'black':
                black_tile = get_coordinates_from_index(i, n)
                break

        if black_tile is None:
            raise ValueError("Black tile not found in grid")
        
        for move in moves:
            if move == 'Left' and black_tile[1] > 0:
                tile_to_move = get_index_from_coordinates(black_tile[0], black_tile[1] - 1, n)
                grid[i], grid[tile_to_move] = grid[tile_to_move], grid[i]
                black_tile = (black_tile[0], black_tile[1] - 1)
            elif move == 'Right' and black_tile[1] < n - 1:
                tile_to_move = get_index_from_coordinates(black_tile[0], black_tile[1] + 1, n)
                grid[i], grid[tile_to_move] = grid[tile_to_move], grid[i]
                black_tile = (black_tile[0], black_tile[1] + 1)
            elif move == 'Up' and black_tile[0] > 0:
                tile_to_move = get_index_from_coordinates(black_tile[0] - 1, black_tile[1], n)
                grid[i], grid[tile_to_move] = grid[tile_to_move], grid[i]
                black_tile = (black_tile[0] - 1, black_tile[1])
            elif move == 'Down' and black_tile[0] < n - 1:
                tile_to_move = get_index_from_coordinates(black_tile[0] + 1, black_tile[1], n)
                grid[i], grid[tile_to_move] = grid[tile_to_move], grid[i]
                black_tile = (black_tile[0] + 1, black_tile[1])

def move_away(grid, n, num_steps):
        while num_steps > 0:
            up = 0
            right = 0

            while abs(up) + abs(right) != 1:
                up = random.randint(0, 1)
                right = random.randint(0, 1)

                if random.random() < 0.5:
                    up *= -1
                if random.random() < 0.5:
                    right *= -1

            for i in range(n * n):
                if grid[i] == 'black':
                    black_tile_coords= get_coordinates_from_index(i, n)
                    break
            
            if (black_tile_coords[0]-up < n and black_tile_coords[0] - up > 0) and (black_tile_coords[1] + right < n and black_tile_coords[1] + right > 0):
                moves = []

                if up == 1:
                    moves.append('Up')
                elif up == -1:
                    moves.append('Down')
                if right == 1:
                    moves.append('Right')
                elif right == -1:
                    moves.append('Left')
                apply_moves_to_black_block(grid, n, moves)
                num_steps -= 1

def validate_file_state(file_state, goal, min_size=3):
    # Check it has at least 4 rows and 4 columns
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

def generate_initial_state_from_file(file_name, goal=False):
    file_state = read_input_file(file_name)
    try:
        validate_file_state(file_state, goal)
    except ValueError as e:
        print(e)
        exit(1)

    n = len(file_state)

    grid = [[[color for color in row] for row in file_state]]
    initial_state = flatten(flatten(grid))
    return initial_state

def generate_goal_state_from_file(file_name, goal=True):
    file_state = read_input_file(file_name)
    try:
        validate_file_state(file_state, goal)
    except ValueError as e:
        print(e)
        exit(1)

    n = len(file_state)

    grid = [[[color for color in row] for row in file_state]]
    goal_state = flatten(flatten(grid))
    return goal_state

# Function to get the new state after a move
def move_tile(board, move, blank_pos, moves):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board

class PuzzleState:
    def __init__(self, board, n, parent, move, depth, cost):
        self.board = board  # The puzzle board configuration
        self.parent = parent  # Parent state
        self.move = move  # Move to reach this state
        self.depth = depth  # Depth in the search tree
        self.cost = cost  # Cost (depth + heuristic)
        if parent is not None:
            self.n = parent.n
            self.internal_matrix_index = parent.internal_matrix_index
        else:
            self.n = n
            self.internal_matrix_index =  get_internal_matrix_index(n)

            
        # Possible moves for the blank tile (up, down, left, right)
        self.moves = {
                        'D': -self.n,  # Move up
                        'U': self.n,   # Move down
                        'R': -1,  # Move left
                        'L': 1    # Move right
                    }

    def __lt__(self, other):
        return self.cost < other.cost
    
    # Function to display the board in a visually appealing format
    def print_board(self):
        print("+" + "---+" * self.n)
        for row in range(0, self.n * self.n,self.n):
            row_visual = "|"
            for tile in self.board[row:row + self.n]:
                if tile == "*":  # Blank tile
                    row_visual += f" {colored(' ', 'cyan')} |"
                else:
                    row_visual += f" {colored(tile, 'yellow')} |"
            print(row_visual)
            print("+" + "---+" * self.n)

    # Function to print the solution path
    def print_solution(self):
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        path.reverse()  # Para mostrar desde el inicio hasta la meta

        for step in path:
            print(f"Move: {step.move}")  # Imprime el movimiento que llevó a este estado
            step.print_board()  # Asegura que se imprime el estado correcto