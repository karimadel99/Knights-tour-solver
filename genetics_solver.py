import random
import pandas as pd

GENE_SIZE = 150
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.7


class Individual:
    def __init__(self):
        self.gene_pool = [0] * GENE_SIZE

    def generateGenes(self):
        for i in range(GENE_SIZE):
            self.gene_pool[i] = random.randint(0, 1)

    def getFitness(self, fn):
        return fn(self.gene_pool)

    def crossover(self, mate):
        crossover_point = random.randint(0, GENE_SIZE - 1)
        child = Individual()
        child.gene_pool[:crossover_point] = self.gene_pool[:crossover_point]
        child.gene_pool[crossover_point:] = mate.gene_pool[crossover_point:]
        return child

    def mutate(self, mrate):
        for i in range(GENE_SIZE):
            if random.random() < mrate:
                self.gene_pool[i] = 1 if self.gene_pool[i] == 0 else 0


class Population:
    def __init__(self, fn):
        self.pop_size = 0
        self.individuals = []
        self.next_gen = []
        self.fitness_fn = fn

    def initializePop(self, p=10):
        self.pop_size = p
        for _ in range(self.pop_size):
            ind = Individual()
            ind.generateGenes()
            self.individuals.append(ind)

    def addIndividual(self, x):
        self.individuals.append(x)
        self.pop_size += 1

    def removeIndividual(self, i):
        self.individuals.pop(i)
        self.pop_size -= 1

    def getBestFit(self):
        best_val = 0
        best_index = 0
        for i in range(self.pop_size):
            this_val = self.individuals[i].getFitness(self.fitness_fn)
            if this_val > best_val:
                best_val = this_val
                best_index = i
        return self.individuals[best_index], best_index

    def tournamentSelection(self, sample_size=3):
        if sample_size > self.pop_size:
            sample_size = 3
        tour = Population(self.fitness_fn)
        for i in range(sample_size):
            tour.addIndividual(self.individuals[random.randint(0, self.pop_size - 1)])
        par1, i = tour.getBestFit()
        tour.removeIndividual(i)
        par2, i = tour.getBestFit()
        del tour
        return par1, par2

    def breed(self, par1, par2):
        child = par1.crossover(par2)
        child.mutate(MUTATION_RATE)
        return child

    def generateNextGeneration(self, elite=1, target=-1):
        n_size = self.pop_size
        if elite == 1:
            n_size -= 1
            best_fit, _ = self.getBestFit()
            self.next_gen.append(best_fit)
        for _ in range(n_size):
            p1, p2 = self.tournamentSelection()
            if random.random() < CROSSOVER_RATE:
                child = self.breed(p1, p2)
                if not child.getFitness(self.fitness_fn) == target:
                    child.mutate(MUTATION_RATE)
                self.next_gen.append(child)
            else:
                p1.mutate(MUTATION_RATE)
                self.next_gen.append(p1)
        self.individuals = self.next_gen.copy()
        self.next_gen.clear()
        if self.getBestFit()[0].getFitness(self.fitness_fn) == target:
            return True
        return False


class KnightBoard:
    @staticmethod
    def pos2board(pos):
        return [pos[0] - 1, pos[1] - 1]

    def __init__(self, x, y, n):
        self.board_size = n
        self.kn_pos = self.pos2board([x, y])
        self.ori_pos = self.kn_pos.copy()
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.board[self.kn_pos[0]][self.kn_pos[1]] = 1

    def reset(self):
        self.kn_pos = self.ori_pos
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.board[self.kn_pos[0]][self.kn_pos[1]] = 1

    def isVisited(self, pos):
        return 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size and self.board[pos[0]][pos[1]] == 1

    @staticmethod
    def decodeMove(enc_mv):
        return (enc_mv[0] * 4 + enc_mv[1] * 2 + enc_mv[2])

    @staticmethod
    def encodeMove(mv):
        return [int(i) for i in format(mv, '03b')]

    def move(self, enc_mv):
        mv = self.decodeMove(enc_mv)
        new_pos = [self.kn_pos[0], self.kn_pos[1]]

        moves = [
            [-2, 1], [-1, 2], [1, 2], [2, 1],
            [2, -1], [1, -2], [-1, -2], [-2, -1]
        ]

        new_pos[0] += moves[mv][0]
        new_pos[1] += moves[mv][1]

        if 0 <= new_pos[0] < self.board_size and 0 <= new_pos[1] < self.board_size:
            if not self.isVisited(new_pos):
                self.kn_pos = new_pos
                self.board[self.kn_pos[0]][self.kn_pos[1]] = 1
                return True

        return False

    def tryRepair(self, mv_list, index):
        ori_mv = self.decodeMove(mv_list[index * 3:(index + 1) * 3])
        moves = [i for i in range(8) if i != ori_mv]
        random.shuffle(moves)
        for i in moves:
            enc = self.encodeMove(i)
            if self.move(enc):
                mv_list[index * 3] = enc[0]
                mv_list[index * 3 + 1] = enc[1]
                mv_list[index * 3 + 2] = enc[2]
                return True
        return False

    def getValidMoves(self, mv_list):
        self.reset()
        num_mvs = len(mv_list) // 3
        if len(mv_list) % 3 != 0:
            return 0  # Invalid move list length
        count = 0
        for i in range(num_mvs):
            if not self.move(mv_list[i * 3:(i + 1) * 3]):
                if not self.tryRepair(mv_list, i):
                    break
            count += 1
        return count

    def showMoves(self, mv_list):
        self.reset()
        num_mvs = len(mv_list) // 3
        if len(mv_list) % 3 != 0:
            print("Invalid move list length.")
            return
        mv_arr = [[-1] * self.board_size for _ in range(self.board_size)]
        mv_arr[self.kn_pos[0]][self.kn_pos[1]] = 0

        for i in range(num_mvs):
            if not self.move(mv_list[i * 3:(i + 1) * 3]):
                break
            mv_arr[self.kn_pos[0]][self.kn_pos[1]] = i + 1

        move_matrix = [[-1 if val == -1 else val + 1 for val in row] for row in mv_arr]
        df = pd.DataFrame(move_matrix, columns=[f'Col {i + 1}' for i in range(len(move_matrix[0]))])

        # Remove rows and columns with all -1 values
        df = df.loc[:, (df != -1).any(axis=0)]
        df = df.loc[(df != -1).any(axis=1)]
        
        board = df.values.tolist()
        return board



# Get the knight's initial position and board size from the user
def solve_genetics(n,x,y):
 x_coord = x
 y_coord =y
 board_size = n
 knboard = KnightBoard(x_coord, y_coord, board_size)

 chb = Population(knboard.getValidMoves)
 chb.initializePop(50)

 for i in range(7000):
    if i % 500 == 0:
        MUTATION_RATE = 0.05
    if i % 500 == 50:
        MUTATION_RATE = 0.02

    if chb.generateNextGeneration(1, board_size * board_size - 1):
        print("Found at Generation: ", i)
        break

 xx, _ = chb.getBestFit()
 if xx.getFitness(knboard.getValidMoves) != board_size * board_size - 1:
    print(f"Could not find path in 4000 generations for a {board_size}x{board_size} board.")
    print("Final fitness: ", xx.getFitness(knboard.getValidMoves))
 return knboard.showMoves(xx.gene_pool)
