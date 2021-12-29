# Author: Bartłomiej Jamiołkowski
# Libraries
from random import choice, random, shuffle
import pandas as pd
import numpy as np
from math import exp, sqrt

# Import an Excel file into Python
file_name, sheet = "Dane_TSP_48.xlsx", "Arkusz1"
data = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')

# Getting initial solution
solution = list(range(1, len(data) + 1)) # List of all job indexes
shuffle(solution)
m = np.delete(data.to_numpy(), 0, 1) # Delete the first array's column, because it contains indexes

def count_score(z): # Function responsible for counting score
    time_travel, copied_solution = 0, z.copy()
    time_travel = np.double(time_travel)
    for i in range(0, len(m) - 1):
        first_city, second_city = copied_solution[i], copied_solution[i + 1]
        time_travel += m[first_city - 1, second_city - 1]
    time_travel += m[copied_solution[0] - 1, copied_solution[-1] - 1]
    return time_travel

score = count_score(solution)

temperature = 1000 # Parameter 1 - setting annealing temperature
format(temperature, ".3f")
iterations = 1000 # Parameter 2
temperature_start = temperature # Copy of temperature in order to present initial value of this parameter
cooling_method = "" # Parameter 3
neighbourhood_type = ""

def pick_two_towns(): # Function responsible for picking two random jobs
    while True:
        t1, t2 = choice(solution), choice(solution) # Picking two random jobs
        if t1 != t2: # Checking if these jobs are not same
            break
    return t1, t2

def swap_method(x, y): # The first type of neighbourhood
    copied_solution = new_solution.copy() # Copied solution which is used for experiments
    copied_solution[x], copied_solution[y] = copied_solution[y], copied_solution[x] # Swapping positions of these jobs in list
    neighbourhood_type = "swap"
    return copied_solution, neighbourhood_type

def insertion_method(t1, y): # The second type of neighbourhood
    copied_solution = new_solution.copy() # Copied solution which is used for experiments
    copied_solution.remove(t1)
    copied_solution.insert(y - 1, t1) # Inserting experimental solution with job 1 on the place of job 2
    neighbourhood_type = "insertion"
    return copied_solution, neighbourhood_type

# Temperature cooling methods
def arithmetic_cooling(x):
    x = x - 1
    cooling_method = "arithmetic"
    return x, cooling_method

def geometric_cooling(x):
    x = 0.999 * x
    cooling_method = "geometric"
    return x, cooling_method

def quadratic_multiplicative_cooling(x):
    x = x/(1 + 0.0001*sqrt(iterations))
    cooling_method = "quadratic multiplicative"
    return x, cooling_method

def linear_multiplicative_cooling(x):
    x = x/(1 + 0.0001*iterations)
    cooling_method = "linear multiplicative"
    return x, cooling_method

while round(temperature, 3) != 0.000: # Termination criteria
    i = 0
    while i != iterations: # Testing neighborhood - the number of generated possible solutions
        new_solution = solution.copy()
        t1, t2 = pick_two_towns() # Insertion mechanism - picking two random jobs
        x, y = solution.index(t1), solution.index(t2) # Obtaining index of each job
        new_solution, neighbourhood_type = insertion_method(t1, y) # swap method can be also used
        new_score = count_score(new_solution) # Calculating new score
        change_cost = new_score - score # Probability of accteptance difference betwieen energy and new energy = dE
        np.double(change_cost)
        if change_cost < 0: # Acceptance criterion
            solution, score = new_solution.copy(), new_score
        else: 
            if random() < exp(-change_cost/temperature): # Generating random number from interval [0, 1]
                solution, score = new_solution.copy(), new_score # Accepting worse solution
        i += 1
    temperature, cooling_method = arithmetic_cooling(temperature) # Reducing temperature - arithmetic approach

print(f"The results of Simulated Annealing algorithm for {file_name} file")
print(f"Solution: {solution}")
print(f"Score: {round(score, 3)}")
print(f"Start temperature: {temperature_start}")
print(f"Neighbourhood type: {neighbourhood_type}")
print(f"Temperature reduction method: {cooling_method}")
print(f"End temperature: {round(temperature, 3)}")
print(f"Neighbourhood size: {iterations}")