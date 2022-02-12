# Libraries
from random import shuffle, choice, randint, random
import pandas as pd
import numpy as np
import constant as const
from operator import itemgetter

# Import Excel file into Python
file_name, sheet = "Dane_TSP_48.xlsx", "Arkusz1"
data = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')

m = np.delete(data.to_numpy(), 0, 1) # The first arrays column removal, because it contains indexes

# Parametres 
p = 40 # Population size
iterations = 100  # The number of generations
const.PC = 0.8 # The probability of using crossover operators
const.PM = 0.20 # The probability of using mutation operators
neighbourhood_type = ""
crossover_type = ""
parent_selection_type = ""

# Population initialization
population = np.empty(shape = (p, len(m)), dtype = 'object') # Empty array for population

for i in range(0, p): # Populating array with random solutions
    chromosome = list(range(1, len(data) + 1)) # Generating numbers which represent jobs
    shuffle(chromosome) # Representation of random solution
    population[i] = chromosome

def count_score(o): # function responsible for counting score
    time_travel, copied_solution = 0, o.copy()
    time_travel = np.double(time_travel)
    for i in range(0, len(m) - 1):
        first_city, second_city = copied_solution[i], copied_solution[i + 1]
        time_travel += m[first_city - 1, second_city - 1]
    time_travel += m[copied_solution[0] - 1, copied_solution[-1] - 1]
    return time_travel

def fitness_value(a, b): # Function responsible for calculating and gathering fitness values for every chromosome in population
    new_fv = [] # List of fitted values
    for i in range(0, b):
        chromosome = a[i].tolist()
        new_score = count_score(chromosome) # Generating new score as one of many scores which would be placed in fitted values list
        new_fv.append(new_score)
    return new_fv

# Parent selection methods
# Parent tournament selection
const.K = 6 # The representation of k chromosomes chosen for tournament selection

def tournament_selection():
    best, copied_fv, used_k, used_win = [], fv.copy(), [], []
    individuals = [] # list for gathered random chromosomes
    for l in range(0, 2):
        for s in range(0, const.K):
            while True: # This loop and condition below control if random chromosome does not already exist in individuals
                k = randint(0, p - 1) # Choosing random integer as representation of chromosome index 
                if k not in used_k and k not in used_win: 
                    individuals.append([k, copied_fv[k]]) # An element of list of lists is created where 0 element is index and 1 element is fitted value
                    used_k.append(k)
                    break
        b = min((x for x in individuals), key = lambda k:k[1]) # Choosing the best chromosome among individuals by the smallest fitted value
        best.append(int(b[0]))
        used_win.append(int(b[0]))
        used_k.clear()
        individuals.clear()
    parent_selection_type = "tournament"
    return int(best[0]), int(best[1]), parent_selection_type # Returning best chromosomes index

def rank_selection():
    rank_list, copied_fv = [], fv.copy()
    i = 0
    while i != 2: # In fact only two parents are needed
        min_fv = min(copied_fv)
        copied_fv = [v for v in copied_fv if v != min_fv] # creating new copied fv list without used min fitted value
        rank_list.append([i + 1, min_fv]) # simulation of rank list
        i += 1
    best1, best2 = rank_list[0], rank_list[1]
    best1, best2 = fv.index(best1[1]), fv.index(best2[1])
    parent_selection_type = "rank"
    return best1, best2, parent_selection_type

# Crossover methods
def partially_matched_crossover(x, y):
    offspring1, offspring2 = [0] * len(m), [0] * len(m)
    exchange_map = []
    for o in range(0, len(m)):
        exchange_map.append([x[o], y[o]])
    offspring1[11:31], offspring2[11:31] = y[11:31].copy(), x[11:31].copy()
    for e in range(0, len(m)):
        if offspring1[e] == 0:
            if int(x[e]) not in offspring1:
                offspring1[e] = int(x[e])
            else:
                for pair in exchange_map:
                    if int(pair[1]) == int(x[e]):
                        offspring1[e] = int(pair[0])               
    for h in range(0, len(m)):
        if offspring2[h] == 0:
            if y[h] not in offspring2:
                offspring2[h] = int(y[h])
            else: 
                for pair in exchange_map:
                    if int(pair[0]) == int(x[h]):
                        offspring2[h] = int(pair[1]) 
    crossover_type = "partially matched crossover"
    return offspring1.copy(), offspring2.copy(), crossover_type

def random_operator_with_complement(x, y):
    offspring1, offspring2 = [0] * len(m), [0] * len(m)
    for i in range(0, len(m)):
        if (round(random(),3)) < 0.4:
            offspring1[i] = x[i]
            offspring2[i] = y[i]
    for j in range(0, len(m)):
        if offspring1[j] == 0:
            for k in y:
                if k not in offspring1:
                    offspring1[j] = k
        if offspring2[j] == 0:
            for l in x:
                if l not in offspring2:
                    offspring2[j] = l
    crossover_type = "random operator with complement"
    return offspring1, offspring2, crossover_type

def pick_two_towns(x): # Function responsible for picking two random towns
    t1, t2 = 0, 0
    while True:
        t1, t2 = choice(x), choice(x) # Picking two random towns
        if t1 != t2: # Checking if these jobs are not same
            break
    t1, t2 = x.index(t1), x.index(t2)
    return t1, t2

# Neighbourhood types
def swap_method(x): # the first neighbourhood type
    t1, t2 = pick_two_towns(x)
    x[t1], x[t2] = x[t2], x[t1] # Swapping positions of these towns in list
    neighbourhood_type = "swap"
    return x, neighbourhood_type

def insertion_method(x): # The second neighbourhood type
    t1, t2 = pick_two_towns(x)
    t1 = int(x[t1])
    copied_solution = x.copy() # Copied solution which is used for experiments
    copied_solution.remove(t1)
    copied_solution.insert(t2, t1) # Inserting experimental solution with job 1 on the place of job 2
    neighbourhood_type = "insertion"
    return x, neighbourhood_type

final_population = np.full([p, len(m)], None) 

i = 0
while i != iterations: # Breaking condition, iterations rpresent a number of epoques
    fv = fitness_value(population, int(p)) # calculating fitness values for population
    fv2, fv3, fv4, children = [], [], [], np.full([2*p, len(m)], None)
    j, k = 0, 0
    while j != int(p): 
        idx1, idx2, parent_selection_type = tournament_selection() # rank selection can be also used
        offspring1, offspring2 = [0] * len(m), [0] * len(m)
        parent1, parent2 = population[idx1].tolist(), population[idx2].tolist() # Setting two chromosomes as parents
        if (round(random(),3) < const.PC and round(random(),3)) < const.PC: # The probability of using crossover operators
            offspring1, offspring2, crossover_type = random_operator_with_complement(parent1, parent2) # Other crossover methods can be also used
        else:
            offspring1, offspring2 = parent1.copy(), parent2.copy() # If conditions are not met then there is no crossover
        children[k], children[k + 1] = offspring1.copy(), offspring2.copy()
        k += 2
        j += 1 
    fv2 = fitness_value(children, 2*p) # Calculating fitness values for children
    for n in range(0, 2*p):
        if (round(random(),3)) < const.PM: # The probability of using mutation operators for the first offspring
            y = children[n].tolist()
            child, neighbourhood_type = insertion_method(y) # Mutation of chromosome
            children[n] = child.copy()
            fv2[n] = count_score(child) # Replacing old fitness value with newly counted value
    for n in range(0, 2*p): # It is needed, because of sorting children chromosomes by fitness values
        fv3.append([n, fv2[n]]) # n is an index, while fv2[n] is fitness value
    fv3 = sorted(fv3, key = itemgetter(1), reverse = False) # Sorting list of children indexes and fitness values
    for n in range(0, 2*p): # Extrating indexes and placing them in new list
        x = fv3[n]
        fv4.append(x[0])
    children = np.array([children[c] for c in fv4]) # sorting children population by index in list
    population = children[0:p] # Only part e.g. 50% of the best children are set as new population
    final_population = population.copy() # copy of current population
    fv.clear() # Clearing list of fitted values before next move
    fv2.clear()
    fv3.clear()
    fv4.clear()
    i += 1

solution = final_population[0].tolist() # Setting solution
score = count_score(solution) # Counting score

print(f"The results of Genetic Algorithm for {file_name} file")
print(f"Solution: {solution}")
print(f"Score: {round(score, 3)}")
print(f"Iterations: {iterations}")
print(f"Population: {p}")
print(f"Neighbourhood type: {neighbourhood_type}")
print(f"Crossover type: {crossover_type}")
print(f"Parent selection type: {parent_selection_type}")
print(f"The probability of using crossover operators: {const.PC}")
print(f"The probability of using mutation operators: {const.PM}")
