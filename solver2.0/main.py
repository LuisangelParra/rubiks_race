from board import generate_initial_state_from_file, generate_goal_state_from_file, get_n_value_from_file
from informed_search import AStarSearchGraph

if __name__ == '__main__':
    file_name_initial = 'inicial.txt'
    file_name_meta = 'meta.txt'

    initial_state = generate_initial_state_from_file(file_name_initial)
    goal_state = generate_goal_state_from_file(file_name_meta)
    n = get_n_value_from_file(file_name_initial)

    heuristic = 'manhattan'

    a_star = AStarSearchGraph(initial_state, goal_state, n)
    #result = a_star.a_star(heuristic)
    result2, limit = a_star.IDA_star(heuristic)


    if result2:
        print("Goal state reached!")
        result2.print_solution()
    else:
        print("No solution found")