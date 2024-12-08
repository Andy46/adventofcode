#!/bin/python3

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Output title
print ("Day 9: All in a Single Night")

# Read data
import re
filedata = []
with open(filename, mode="r") as file:
    filedata = [list(re.findall(r"(.*) to (.*) = (\d*)", line)[0]) for line in file.readlines()]

# Prepare data
cities = set()
travels = {}
for data in filedata:
    cities.add(data[0])
    cities.add(data[1])
    travels[(data[0], data[1])] = int(data[2])
    travels[(data[1], data[0])] = int(data[2])

# Helper functions
def calcRoutes(cities):
    routes = []
    if len(cities) == 1:
        return [cities]
    for city in cities:
        leftCities = cities.copy()
        leftCities.remove(city)
        for innerRoute in calcRoutes(leftCities):
            innerRoute.extend([city])
            routes.append(innerRoute)
    return routes

def calcRouteDistance(route, travels):
    distance = 0
    for i in range(len(route) - 1):
        distance = distance + travels[(route[i], route[i+1])]
    return distance

# Calculate
routes = calcRoutes(list(cities))
routes = [[route, calcRouteDistance(route, travels)] for route in routes]

# Output result (part 1)
print(f"Shortest route: {min(routes, key=lambda x: x[1])}")

# Output result (part 2)
print(f"Longest route: {max(routes, key=lambda x: x[1])}")

