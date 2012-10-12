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

def render(craterset, filename, t):
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
    axes.set_ylim((0, 500))
    axes.set_xlim((0, 500))
    axes.set_aspect(1.0)
    axes.set_title('Cratering over study area at t = {0}'.format(t))
    axes.set_xlabel('X (km)')
    axes.set_ylabel('Y (km)')
    fig.savefig(filename, dpi=220)

def main():
    craterset = set()
    counts = [0]
    i = 1
    print 'Time (y) | Craters'
    print '---------|--------'
    while True:
        craterset = crater(craterset)
        counts.append(len(craterset))
        if counts[i / 2] * 1.05 > counts[i]:
            break
        if i % 100 == 0:
            render(craterset, 'step{0}.png'.format(i), i * 1000)
        if i % 10 == 0:
            print '%5d000 | %7d' % (i, len(craterset))
        i += 1
    print 'Time: %d years\tCrater count: %d' % (i * 1000, counts[i])
    render(craterset, 'final.png', i * 1000)
    counts_array = numpy.array(counts, numpy.int32)
    ts_array = numpy.array(range(len(counts)), numpy.int32)

    fig = matplotlib.pyplot.figure()
    axes = fig.gca()
    axes.plot(ts_array, counts_array)
    axes.set_xlabel('Time (10^3 years)')
    axes.set_ylabel('Crater count')
    axes.set_title('Crater count to saturation')
    fig.savefig('density.png', dpi=220)

if __name__ == "__main__":
    main()
