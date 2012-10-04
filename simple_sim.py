################################################################################
#
# File: simple_sim.py
# Author: Ken Sheedlo
# ASTR 3750 - Fall 2012
#
# Simplified crater simulation program for ASTR 3750 project, intended to 
# validate the more complicated program in sim.py.
#
################################################################################

import matplotlib
matplotlib.use("Agg")

import numpy
import random
import matplotlib.figure
import matplotlib.pyplot

def distance(p1, p2):
    '''
    Computes the distance between two points.

    '''
    return numpy.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def crater(craterset):
    '''
    Performs one cratering timestep.

    Returns a new crater set.
    '''
    crater_x = random.uniform(0.0, 500.0)
    crater_y = random.uniform(0.0, 500.0)
    
    obliterated = set([
        c for c in craterset if distance(c, (crater_x, crater_y)) <= 30.0
    ])

    result = craterset - obliterated
    result.add((crater_x, crater_y))
    return result

def render(craterset, filename):
    '''
    Draws the current crater state and outputs to the named file.

    '''
    fig = matplotlib.pyplot.figure()
    axes = fig.gca()
    circles = [
        matplotlib.pyplot.Circle(point, 25.0, color='#656565') 
        for point in craterset
    ]
    for circle in circles:
        axes.add_artist(circle)
    fig.savefig(filename, dpi=220)

def main():
    craterset = set()
    counts = [0]
    i = 1
    while True:
        craterset = crater(craterset)
        counts.append(len(craterset))
        if counts[i / 2] * 1.05 > counts[i]:
            break
        if i % 100 == 0:
            render(craterset, 'step{0}.png'.format(i))
        i += 1
    print 'Time: %d years\tCrater count: %d' % (i * 1000, counts[i])
    render(craterset, 'final.png')

if __name__ == "__main__":
    main()
