from time import time
from search import *
from assignment1aux import *
from heapq import *

def read_initial_state_from_file(filename):
    # Task 1
    # Return an initial state constructed using a configuration in a file.

    # Opens the config text file for reading
    config_file = open(filename)
    
    # Gets the height and weight
    height = int(config_file.readline())
    width = int(config_file.readline())

    # Gets all the rocks
    rocks_list = []

    for rock in config_file:
        # Splits the new rock coordinates to a list of coordinates and changes it to integers
        new_rock = [int(value) for value in rock.split(",")]

        # Add the list of rock coordinates to the list of rocks
        rocks_list.append(new_rock)

    # Closing the file
    config_file.close()

    # Map creation
    map_list = []

    for row in range(height):
        # Create the current row we are working in
        current_row = []

        for col in range(width):
            # Checks if a rock was placed
            rockPlaced = False

            # Checks if there is a rock in the current tile (row, col) by looping the rocks list 
            for rock in rocks_list:

                # If there's a rock then append "rock"
                if row == rock[0] and col == rock[1]:
                    current_row.append("rock")
                    rockPlaced = True
            
            # If there wasn't any rock then append ""
            if rockPlaced == False:
                current_row.append("")
                    
        # Change current row list to a tuple and add current row to the map list
        map_list.append(tuple(current_row))
    
    # Create the state tuple and return it
    new_state = (tuple(map_list), None, None)
    return new_state


class ZenPuzzleGarden(Problem):
    def __init__(self, initial):
        if type(initial) is str:
            super().__init__(read_initial_state_from_file(initial))
        else:
            super().__init__(initial)

    def actions(self, state):
        map = state[0]
        position = state[1]
        direction = state[2]
        height = len(map)
        width = len(map[0])
        action_list = []
        if position:
            if direction in ['up', 'down']:
                if position[1] == 0 or not map[position[0]][position[1] - 1]:
                    action_list.append((position, 'left'))
                if position[1] == width - 1 or not map[position[0]][position[1] + 1]:
                    action_list.append((position, 'right'))
            if direction in ['left', 'right']:
                if position[0] == 0 or not map[position[0] - 1][position[1]]:
                    action_list.append((position, 'up'))
                if position[0] == height - 1 or not map[position[0] + 1][position[1]]:
                    action_list.append((position, 'down'))
        else:
            for i in range(height):
                if not map[i][0]:
                    action_list.append(((i, 0), 'right'))
                if not map[i][width - 1]:
                    action_list.append(((i, width - 1), 'left'))
            for i in range(width):
                if not map[0][i]:
                    action_list.append(((0, i), 'down'))
                if not map[height - 1][i]:
                    action_list.append(((height - 1, i), 'up'))
        return action_list

    def result(self, state, action):
        map = [list(row) for row in state[0]]
        position = action[0]
        direction = action[1]
        height = len(map)
        width = len(map[0])
        while True:
            row_i = position[0]
            column_i = position[1]
            if direction == 'left':
                new_position = (row_i, column_i - 1)
            if direction == 'up':
                new_position = (row_i - 1, column_i)
            if direction == 'right':
                new_position = (row_i, column_i + 1)
            if direction == 'down':
                new_position = (row_i + 1, column_i)
            if new_position[0] < 0 or new_position[0] >= height or new_position[1] < 0 or new_position[1] >= width:
                map[row_i][column_i] = direction
                return tuple(tuple(row) for row in map), None, None
            if map[new_position[0]][new_position[1]]:
                return tuple(tuple(row) for row in map), position, direction
            map[row_i][column_i] = direction
            position = new_position

    def goal_test(self, state):
        # Task 2
        # Return a boolean value indicating if a given state is solved.
        
        # List of rows if the goal was met or not
        row_goal_list = []

        # Checks if the agent is out of the perimeter
        if state[1] == None and state[2] == None:
            for row in state[0]:
                row_goal_list.append(all(row))
            
            # Returns true if all rows are true
            return all(row_goal_list)
        
        else:
            return False


# Task 3
# Implement an A* heuristic cost function and assign it to the variable below.
def astar_heuristic_cost(node):
    # Finds the height and width of the map
    map = node.state[0]
    height = len(map)
    width = len(map[0])

    # Counter for rows and column
    row_counter = 0
    column_counter = 0

    # Running a for loop doing the columns first
    for j in range(width):
        for i in range(height):
            # If the value is empty then count the entire column as empty and move on to the next column
            if map[i][j].strip() == "":
                column_counter += 1
                break                

    # Running a for loop doing the columns first
    for i in range(height):
        for j in range(width):
            # If the value is empty then count the entire row as empty and move on to the next row
            if map[i][j].strip() == "":
                row_counter += 1
                break
        
    # Return the smallest count
    if column_counter > row_counter:
        return row_counter
    else:
        return column_counter
    

def beam_search(problem, f, beam_width):
    # Task 4
    # Implement a beam-width version A* search.
    # Return a search node containing a solved state.
    # Experiment with the beam width in the test code to find a solution.

    
    # Initialise the display just as in search.py 
    display = False

    # Copied the best_first_graph_search() function in search.py
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        
        # Only keep the smallest beam_width nodes
        if frontier.heap.__len__() > beam_width:
            frontier.heap = nsmallest(beam_width, frontier.heap)
    return None

if __name__ == "__main__":

    # Task 1 test code
    print('The loaded initial state is visualised below.')
    visualise(read_initial_state_from_file("C:/Users/alexi/Documents/University/2nd Year/COMPX216/Assignment 1/aima-python/aima-python/assignment1config2.txt"))

    # Task 2 test code
    garden = ZenPuzzleGarden('C:/Users/alexi/Documents/University/2nd Year/COMPX216/Assignment 1/aima-python/aima-python/assignment1config2.txt')
    print('Running breadth-first graph search.')
    before_time = time()
    node = breadth_first_graph_search(garden)
    after_time = time()
    print(f'Breadth-first graph search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')

    # Task 3 test code
    
    print('Running A* search.')
    before_time = time()
    node = astar_search(garden, astar_heuristic_cost)
    after_time = time()
    print(f'A* search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    

    # Task 4 test code
    print('Running beam search.')
    before_time = time()
    node = beam_search(garden, lambda n: n.path_cost + astar_heuristic_cost(n), 50)
    after_time = time()
    print(f'Beam search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
