# Author: Bartłomiej Jamiołkowski
# Libraries
from random import choice
import pandas as pd
import numpy as np

# Import an Excel file into Python
file_name, sheet = "Dane_TSP_127.xlsx", "Arkusz1"
data = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')

# Setting of the stop criterion
iterations = 4000 # Parameter 1
tabu_len = 30 # Parameter 2
neighbourhood = 400 # Parameter 3
neighbourhood_type = ""

# Current solution initialization
solution = list(range(1, len(data) + 1)) # List of all job indexes from the file

# Creating array in order to conduct goal function calculations
m = np.delete(data.to_numpy(), 0, 1) # The first arrays column removal, because it contains indexes

def count_score(o): # Functuion responsible for counting score
    time_travel, copied_solution = 0, o.copy()
    time_travel = np.double(time_travel)
    for i in range(0, len(m) - 1):
        first_city, second_city = copied_solution[i], copied_solution[i + 1]
        time_travel += m[first_city - 1, second_city - 1]
    time_travel += m[copied_solution[0] - 1, copied_solution[-1] - 1]
    return time_travel

score = count_score(solution)

# Tabu list initialization
tabu = [] # Tabu list

# Creation of a candidate list of neighbors to the current solution
candidates = [] # A list of all candidates

def candidates_generator(n): # The function generating all candidates
    k, x, y = 0, 0, 0
    for k in range(0, neighbourhood):
        while True:
            while True:
                x, y = choice(n), choice(n)
                if x != y:
                    break
            if [x, y] not in candidates:
                candidates.append([x, y]) # Populating list with small lists of two numbers
                break
    k += 1

def swap_method(t1, y): # The first type of neighbourhood
    x = solution.index(t1)
    copied_solution = new_solution.copy() # Copied solution which is used for experiments
    copied_solution[x], copied_solution[y] = copied_solution[y], copied_solution[x] # Swapping positions of these jobs in list
    neighbourhood_type = "swap"
    return copied_solution, neighbourhood_type

def insertion_method(t1, y): # The second part of neighbourhood
    copied_solution = new_solution.copy() # Copied solution which is used for experiments
    for i in range(1, len(solution) + 1):
        if i == t1:
            copied_solution.remove(t1)
    copied_solution.insert(y, t1) # Inserting experimental solution with job 1 on the place of job 2
    neighbourhood_type = "insertion"
    return copied_solution, neighbourhood_type

i = 0
while i != iterations:
    z = candidates_generator(solution) # Generating candidates
    min_solution, min_score = solution.copy(), score
    tabu_pair = [] #If the move is considered it is held in this list untill it move is done and a new socre is set
    j = 0
    while j != neighbourhood: # checking neighbourhood
        pair, new_solution, new_score = candidates[j].copy(), solution.copy(), 0 #candidates_score[j]
        if pair not in tabu: 
            t1 = pair[0]
            y = new_solution.index(pair[1])
            new_solution, neighbourhood_type = insertion_method(t1, y) # swap method can be also used
            new_score = count_score(new_solution)
            if new_score < min_score: # Checking if a new socre is better than local socre
                min_solution, min_score, tabu_pair = new_solution.copy(), new_score, pair.copy()
        j += 1
    if min_score < score: # Checking if local score can replace previous score
        solution, score = min_solution.copy(), min_score
        tabu.append(tabu_pair)
    if len(tabu) == tabu_len: # Controlling the tabu list lenght
        del tabu[0]
    candidates.clear() # Preparing candidates list for the next iteration
    i += 1

print(f"The results of Tabu Search algorithm for {file_name} file")
print(f"Solution: {solution}")
print(f"Score: {round(score, 4)}")
print(f"Neighbourhood type: {neighbourhood_type}")
print(f"Neighbourhood size: {neighbourhood}")
print(f"Iterations: {iterations}")
print(f"Tabu length: {tabu_len}")