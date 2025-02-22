from board import display_grid, display_goal_state, generate_state_from_file, Puzzle
from search import IDA, AStarSearchGraph

if __name__ == '__main__':
    file_name_initial = 'inicial.txt'
    file_name_meta = 'meta.txt'

    initial_state = generate_state_from_file(file_name_initial)
    display_grid(initial_state)

    goal_state = generate_state_from_file(file_name_meta, goal=True)
    display_goal_state(goal_state)

    n = len(initial_state)
    puzzle = Puzzle(n=n, goal=goal_state, puzzle=initial_state)
    
    #result = IDA(initial_state=puzzle, n=puzzle.size).searchManhattanDist()

    result = AStarSearchGraph(initial_state=puzzle, n=puzzle.size).searchManhattan()