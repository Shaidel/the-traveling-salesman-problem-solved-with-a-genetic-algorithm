from math import sqrt
from random import randint, sample

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from genetic_library import GeneticAlgorithm, Element
from genetic_library.selection_models import elite_selection_model


## ODCZYT WSPÓŁRZĘDNYCH

START_POINT = [(13.53, 107.46)]
END_POINT = [(13.53, 107.46)]

tmpCities = [] 
nbCitiesDisplayed = 16

def remove_newlineCharacter( str ) :
    if(str[-1:]=='\n'):
        return str[:-1]
    else:
        return str

fLocations = open('16miast.txt', 'r')

cities_locations = fLocations.readlines()[8:]

for location in cities_locations:
    tmp = remove_newlineCharacter(location).split('\t')
    tmp[0] = float(tmp[0])
    tmp[1] = float(tmp[1])
    tmpCities.append(tmp)

cities_locations = list(tmpCities[:nbCitiesDisplayed])

POINTS = cities_locations

class Route(Element):
    def __init__(self, points):
        self.points = points
        super().__init__()

    def _perform_mutation(self):
        first = randint(1, len(self.points) - 2)
        second = randint(1, len(self.points) - 2)

        self.points[first], self.points[second] = self.points[second], self.points[first]

    def crossover(self, element2: 'Element') -> 'Element':
        child_points = self.points[1:int(len(self.points) / 2)]
        for point in element2.points:
            if point not in child_points and point not in END_POINT + START_POINT:
                child_points.append(point)

            if len(child_points) == len(element2.points):
                break
        return Route(START_POINT + child_points + END_POINT)

    def evaluate_function(self):
        def _calculate_distance(x1, x2, y1, y2):
            return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        sum = 0
        for i, p in enumerate(self.points):
            if i + 1 > len(self.points) - 1:
                break
            next_point = self.points[i + 1]
            sum += _calculate_distance(p[0], next_point[0], p[1], next_point[1])

        return sum

    def __repr__(self):
        return str(self.points)


def first_generation_generator():
    return [Route(START_POINT + sample(POINTS, len(POINTS)) + END_POINT) for _ in range(1000)] #wielkość populacji


plt.ion()
fig = plt.figure(figsize=(7, 7))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ZbX=np.zeros((5,301))


def stop_condition(string, current_fitness, i):
      
    x = i-1
    ZbX[0,i] = x
    y = current_fitness
    ZbX[1,i] = y
	
    ax1.clear()
    ax2.clear()
    ax1.plot(ZbX[0,:],ZbX[1,:],'r')
    
    poland_img=mpimg.imread('poland.png')
    plt.imshow(poland_img, extent=[13, 24, 99, 110], alpha=0.5)
    
    ax2.scatter(*zip(*string.points))
    ax2.plot(*zip(*string.points))
    plt.axis('off')
    fig.canvas.draw()
    fig.canvas.flush_events()

    return i == 300 #liczba pokoleń


ga = GeneticAlgorithm(first_generation_generator, elite_selection_model, stop_condition)
ga.run()
plt.show(block=True)
fLocations.close()