from search import *
from random import randint
from assignment2aux import *

def read_tiles_from_file(filename):
    lines = [line.rstrip('\n') for line in open(filename, 'r').readlines()]
    character_to_tile = {' ': (), 'i': (0,), 'L': (0, 1), 'I': (0, 2), 'T': (0, 1, 2)}
    return tuple(tuple(character_to_tile[character] for character in line) for line in lines)

class KNetWalk(Problem):
    def __init__(self, tiles):
        if type(tiles) is str:
            self.tiles = read_tiles_from_file(tiles)
        else:
            self.tiles = tiles
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])
        self.max_fitness = sum(sum(len(tile) for tile in row) for row in self.tiles)
        super().__init__(self.generate_random_state())

    def generate_random_state(self):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [randint(0, 3) for _ in range(height) for _ in range(width)]

    def actions(self, state):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [(i, j, k) for i in range(height) for j in range(width) for k in [0, 1, 2, 3] if state[i * width + j] != k]

    def result(self, state, action):
        pos = action[0] * len(self.tiles[0]) + action[1]
        return state[:pos] + [action[2]] + state[pos + 1:]

    def goal_test(self, state):
        return self.value(state) == self.max_fitness

    def value(self, state):
        # Task 1
        # Return an integer fitness value of a given state.
        # Replace the line below with your code.

        # Create fitness function
        fitness_function = 0

        # Create a dictionary for the valid connection types
        valid_connections = {0: 2, 1: 3, 2: 0, 3: 1}

        # Loop through the state
        for i in range(self.height):
            for j in range(self.width):
                # (i,j) is the current examining tile and stores what type of tile it is and what connections it has
                current_tile = self.tiles[i][j]

                # Current state stores the orientation of the current tile (how many times its rotated counterclockwise)
                current_rotation = state[i * self.width + j]
                current_tile = tuple((con + current_rotation) % 4 for con in current_tile)

                # Checks if the right neighbouring tile (i, j + 1) exists 
                if (j + 1) < self.width:
                    right_tile = self.tiles[i][j + 1]

                    # Rotate the right tile
                    right_rotation = state[i * self.width + (j + 1)]
                    right_tile = tuple((con + right_rotation) % 4 for con in right_tile)
                else:
                    right_tile = None

                # Checks if the top neighbouring tile (i - 1, j) exists
                if (i - 1) >= 0:
                    top_tile = self.tiles[i - 1][j]

                    # Rotate the top tile
                    top_rotation = state[(i - 1) * self.width + j]
                    top_tile = tuple((con + top_rotation) % 4 for con in top_tile)
                else:
                    top_tile = None

                # Checks if the left neighbouring tile (i, j - 1) exists
                if (j - 1) >= 0:
                    left_tile = self.tiles[i][j - 1]

                    # Rotate the left tile
                    left_rotation = state[i * self.width + (j - 1)]
                    left_tile = tuple((con + left_rotation) % 4 for con in left_tile)
                else:
                    left_tile = None

                # Checks if the bottom neighbouring tile exists (i + 1, j)
                if (i + 1) < self.height:
                    bottom_tile = self.tiles[i + 1][j]

                    # Rotate the bottom tile
                    bottom_rotation = state[(i + 1) * self.width + j]
                    bottom_tile = tuple((con + bottom_rotation) % 4 for con in bottom_tile)
                else:
                    bottom_tile = None
                
                # Loops through the current tile's connections
                for current_connection in current_tile:
                    # If current tile has a right connection
                    if (current_connection == 0 and right_tile is not None):
                        # Check if the right tile has a left connection
                        if 2 in right_tile:
                            fitness_function += 1

                    # If the current tile has a top connection
                    if (current_connection == 1 and top_tile is not None):
                        # Check if the top tile has a bottom connection
                        if 3 in top_tile:
                            fitness_function += 1

                    # If the current tile has a left connection
                    if (current_connection == 2 and left_tile is not None):
                        # Check if the left tile has a right connection
                        if 0 in left_tile:
                            fitness_function += 1

                    # If the current tile has a bottom connection
                    if (current_connection == 3 and bottom_tile is not None):
                        # Check if the bottom tile has a ritopght connection
                        if 1 in bottom_tile:
                            fitness_function += 1       

        # Return the fitness function
        return fitness_function
                


# Task 2
# Configure an exponential schedule for simulated annealing.
sa_schedule = exp_schedule(k=20, lam=0.005, limit=100)

# Task 3
# Configure parameters for the genetic algorithm.
pop_size = None
num_gen = 1000
mutation_prob = 0.1

def local_beam_search(problem, population):
    # Task 4
    # Implement local beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the next population contains no fitter state.
    # Replace the line below with your code.
    raise NotImplementedError

def stochastic_beam_search(problem, population, limit=1000):
    # Task 5
    # Implement stochastic beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the generation limit is reached.
    # Replace the line below with your code.
    raise NotImplementedError

if __name__ == '__main__':

    network = KNetWalk('assignment2config.txt')
    visualise(network.tiles, network.initial)

    # Task 1 test code
    run = 0
    method = 'hill climbing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = hill_climbing(network)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)

    # Task 2 test code
    '''
    run = 0
    method = 'simulated annealing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = simulated_annealing(network, schedule=sa_schedule)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 3 test code
    '''
    run = 0
    method = 'genetic algorithm'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = genetic_algorithm([network.generate_random_state() for _ in range(pop_size)], network.value, [0, 1, 2, 3], network.max_fitness, num_gen, mutation_prob)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 4 test code
    '''
    run = 0
    method = 'local beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = local_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 5 test code
    '''
    run = 0
    method = 'stochastic beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = stochastic_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''
