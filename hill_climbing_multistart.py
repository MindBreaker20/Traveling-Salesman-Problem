# Author: Bartłomiej Jamiołkowski
# Libraries
from random import shuffle, choice
import pandas as pd
import numpy as np

# Import Excel file into Python
file_name, sheet = "Dane_TSP_127.xlsx", "Arkusz1"
data = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')

m = np.delete(data.to_numpy(), 0, 1) # The first arrays column removal, because it contains indexes

multistarts = 40 # Parameter 1
iterations1 = 1000 # Parameter 2
iterations2 = 750 # Parameter 3
neighbourhood_type = ""

solution = list(range(1, len(data) + 1)) # List for future job indexes from the file

def count_score(z): # Function responsible for counting distance
    time_travel, copied_solution = 0, z.copy()
    time_travel = np.double(time_travel)
    for n in range(0, len(solution) - 1):
        first_city, second_city = copied_solution[n], copied_solution[n + 1]
        time_travel += m[first_city - 1, second_city - 1]
    time_travel += m[copied_solution[0] - 1, copied_solution[-1] - 1]
    return time_travel
        
def pick_two_towns(): # Function responsible for picking two random jobs
    while True:
        t1, t2 = choice(solution), choice(solution) # Picking two random jobs
        if t1 != t2: # Checking if these jobs are not same
            break
    return t1, t2

def swap_method(x, y): # One of the neighbourhood types
    copied_solution = new_solution.copy() # Copied solution which is used for experiments
    copied_solution[x], copied_solution[y] = copied_solution[y], copied_solution[x] # Swapping positions of these jobs in list
    neighbourhood_type = "swap"
    return copied_solution, neighbourhood_type

def insertion_method(t1, y): # Second type of neighbourhood
    copied_solution = new_solution.copy() # Copied solution which is used for experiments
    copied_solution.remove(t1)
    copied_solution.insert(y, t1) # Inserting experimental solution with job 1 on the place of job 2
    neighbourhood_type = "insertion"
    return copied_solution, neighbourhood_type

score2 = 1000000000
solution2 = []
i = 0
while i != multistarts: # Multistart mechanism 
    shuffle(solution) # Creating new solution (changing point) by shuffling jobs
    j = 0
    score = count_score(solution)
    while j != iterations1:
        min_solution = solution.copy() # Unchanged solution
        min_score, k = count_score(min_solution), 0
        while k != iterations2: # Testing neighbourhood
            new_solution = solution.copy()
            t1, t2 = pick_two_towns()
            x, y = solution.index(t1), solution.index(t2)  # Obtaining index of each job
            new_solution, neighbourhood_type = insertion_method(t1, y) # There can be also used swap method
            new_score = count_score(new_solution) # Calculating score of experimental solution
            if new_score < min_score: 
                min_solution, min_score = new_solution.copy(), new_score # Prescribing new already changed solution
            k += 1
        if min_score < score: # Checking if the local solution is better than min_solution
            solution = min_solution # Applying changes to the solution
            score = min_score
        elif solution == min_solution: # Moment when local maximum is achieved
            break
        j += 1
    if score < score2: # Checking if proposed solution is better than previous one
        score2 = score
        solution2 = solution.copy()
    i += 1

print(f"The results of Hill Climbing algorithm with multistart mechanism for {file_name} file")
print(f"Solution: {solution2}")
print(f"Score: {round(score2,3)}")
print(f"Neighbourhood type: {neighbourhood_type}")
print(f"Multistarts: {multistarts}")
print(f"Iterations 1: {iterations1}")
print(f"Iterations 2: {iterations2}")