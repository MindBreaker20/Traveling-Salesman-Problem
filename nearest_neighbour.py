# Libraries
import pandas as pd
import numpy as np
from operator import itemgetter

# Import Excel file into Python
file_name, sheet = "TSP.xlsx", "Arkusz1"
data = pd.read_excel(file_name, sheet_name = sheet, engine = 'openpyxl')

m = np.delete(data.to_numpy(), 0, 1) # The first arrays column removal, because it contains indexes

start_city = 117 # Setting start city
copied_start_city = start_city # Start city is copied in order to be presented in results
visited_cities = [] # List of visited cities
visited_cities.append(start_city) # Setting start city as visited 

score = 0 # Variable where distances between cities are summarised

i = 0
while i != len(m) - 1: 
    distances = [] # List which is responsible for gathering all possible movements from the current start city
    for j in range(1, len(m) + 1): # Checking all cities 
        if j not in visited_cities: # If the city has not been visited yet
            dist = m[start_city - 1, j - 1] # Obatining distance to the next city from the array
            distances.append([dist, j]) # Adding possible move to the list of all possible moves
    distances = sorted(distances, key = itemgetter(0), reverse = False) # Sorting list in order to find the shortest distance
    pair = distances[0] # Exctracting the shortest distance with the cities number
    score += pair[0] # Adding the smallest distance between cities to the whole distance
    visited_cities.append(pair[1]) # Adding chosen city to the list of visited cities
    start_city = pair[1] # Setting chosen city as start city
    distances.clear() # Clearing list of cities with distances in order to prepare it for the next iteration
    i += 1

score += m[visited_cities[0] - 1, visited_cities[-1] - 1] # Adding distance between the fist city and the last visited city
solution = visited_cities.copy() # Setting solution

print(f"The results of Nearest Neighbour algorithm for {file_name} file")
print(f"Solution: {solution}")
print(f"Score: {round(score, 4)}")
print(f"Start city: {copied_start_city}")
