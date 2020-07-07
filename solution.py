#! /usr/bin/python3
import math
import random
import copy
from collections import deque

class mySet:
    def __init__(self, data):
        self.min = data[0]
        self.coordinates = []
        for idx in range(len(data[1])):
            self.coordinates.append([int(data[1][idx]), int(data[2][idx])])
        self.best = [int(x) for x in data[3]]

class Path:
    def __init__(self, coordinates, route):
        self.coordinates = coordinates
        self.route = route
        self.fit = 0
        self.length = 0
        for idx in range(len(route) - 1):
            self.length += dist(coordinates[route[idx]], coordinates[route[idx + 1]])
        self.length += dist(coordinates[route[len(route) - 1]], coordinates[route[0]]) #Account for going from the last point back to start
        self.fit = 1.0 / self.length

def csvData(path):
    file = open("points.csv", "r")
    min = 0
    xCoordinates = []
    yCoordinates = []
    best = []
    for line in file:
        if path in line and min == 0:
            min = float(line.split(',')[1])
        elif min != 0 and len(xCoordinates) == 0: #Make sure min != 0 so it reads from the next line
            xCoordinates = line.strip().split(',')
        elif len(xCoordinates) != 0 and len(yCoordinates) == 0: #Make sure xCoordinates isn't empty so it reads from the next line
            yCoordinates = line.strip().split(',')
        elif len(yCoordinates) != 0 and len(best) == 0 : #Make sure yCoordinates isn't empty so it reads from the next line
            best = line.strip().split(',')
    file.close()
    return [min, xCoordinates, yCoordinates, best]

def dist(P1, P2):
    x1 = P1[0]
    y1 = P1[1]
    x2 = P2[0]
    y2 = P2[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def mate(path1, path2):
    part1 = random.randint(0, len(path1.route) - 1)
    part2 = random.randint(1, len(path1.route) - 1)
    newRoute = []
    for idx in range(len(path1.route)):
        newRoute.append(-1)              #Making the new route to be the correct length
    for idx in range(part1, part1 + part2):
        newRoute[idx % len(newRoute)] = path1.route[idx % len(newRoute)]   #Fill in a random portion of the newRoute with parts of path1
    idx1 = (part1 + part2) % len(newRoute)
    idx2 = (part1 + part2) % len(newRoute)
    while -1 in newRoute:  #Don't stop filling in the newRoute from the parent paths until the newRoute is completely filled without repeats
        if path2.route[idx2] not in newRoute:  #Fill in the rest of newRoute with parts of path2 without repeats
            newRoute[idx1] = path2.route[idx2]
            idx1 = ((idx1 + 1) % len(newRoute))
        idx2 = ((idx2 + 1) % len(newRoute))
    return Path(path1.coordinates, newRoute)

def generations(name, gen, pop):
    bestLength = 3984729875298374
    best = []
    myData = mySet(csvData(name))
    paths = []
    for idx in range(pop):
        newRoute = copy.copy(myData.best)
        random.shuffle(newRoute)
        paths.append(Path(myData.coordinates, newRoute))
    idx = 0
    while idx < gen:
        weights = []
        newPaths = []
        for path in paths:
            weights.append(path.fit ** 5) #Make paths with higher fitnesses more likely to be chosen
        i = 0
        while i < len(paths):
            path1 = random.choices(paths, weights)[0]
            path2 = random.choices(paths, weights)[0]
            newPaths.append(mate(path1, path2))
            i += 1
        paths = newPaths
        idx += 1
        paths.sort(reverse = True, key = lambda path: path.fit)
        if paths[0].length < bestLength:
            bestLength = paths[0].length
            best = paths[0].route
    if best[0] != 0:  #To ensure the first point is always 0
        idx = best.index(0)
        newBest = deque(best)
        newBest.rotate(len(best) - idx)
        best = list(newBest)
    best = [str(x) for x in best]
    string = name + "\n" + ",".join(best) + "\n\n"
    print(name + " done\n")
    return string


def main():
    paths = ["A4", "A8", "A9", "A9-2", "A10", "A11", "A12", "A12-2", "A13", "A13-2", "A30", "A50"]
    open("StudentPaths.csv", "w").close() #Clears the output file at first
    file = open("StudentPaths.csv", "a")
    for path in paths:
        str = generations(path, 1000, 150)
        file.write(str)
    file.close()

main()
