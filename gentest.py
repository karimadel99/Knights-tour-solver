import random
from deap import base, creator, tools, algorithms

def is_valid_move(x, y, n, board):
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1

def knight_moves(x, y, n, board):
    moves = [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
             (1, -2), (2, -1), (1, 2), (2, 1)]
    possible_moves = [(x + dx, y + dy) for dx, dy in moves]
    valid_moves = [(mx, my) for mx, my in possible_moves if is_valid_move(mx, my, n, board)]
    return valid_moves

def generate_individual(n):
    return random.sample(range(n * n), n * n)

def individual_to_board(individual, n):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    for i, pos in enumerate(individual):
        x, y = divmod(pos, n)
        board[x][y] = i
    return board

def knight_tour_fitness(individual, n, start_x, start_y):
    flat_individual = [pos for row in individual for pos in row]
    board = individual_to_board(flat_individual, n)

    x, y = start_x, start_y
    for move in flat_individual:
        x, y = divmod(move, n)
        if board[x][y] == -1:
            board[x][y] = 1
        else:
            return 0,  # Fitness is 0 if there is an invalid move
    return 1,  # Fitness is 1 if the tour is valid

def cxOrdered(ind1, ind2):
    size = min(len(ind1), len(ind2))
    a, b = sorted(random.sample(range(size), 2))
    temp = ind1[a:b + 1] + [item for item in ind2 if item not in ind1[a:b + 1]]
    ind1[a:b + 1], ind2 = ind2[a:b + 1], temp
    return ind1, ind2


def main(start_x, start_y, n, generations=100, population_size=100, crossover_prob=0.7, mutation_prob=0.2):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initRepeat, creator.Individual, lambda: generate_individual(n), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", knight_tour_fitness, n=n, start_x=start_x, start_y=start_y)

    population = toolbox.population(n=population_size)
    offspring = algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size,
                                          cxpb=crossover_prob, mutpb=mutation_prob, ngen=generations, stats=None,
                                          halloffame=None, verbose=True)

    best_solution = tools.selBest(population, k=1)[0]
    best_board = individual_to_board(best_solution, n)
    return best_board


if __name__ == "__main__":
    start_x = 0  # Starting x-coordinate
    start_y = 0  # Starting y-coordinate
    n = 5  # Board size n * n
    best_board = main(start_x, start_y, n)
    print("Best Knight's Tour:")
    for row in best_board:
        print(row)
