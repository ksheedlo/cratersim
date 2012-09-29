################################################################################
#
# File: sim.py
# Author: Ken Sheedlo
# ASTR 3750 - Fall 2012
#
# Main crater simulation program for ASTR 3750 project.
#
################################################################################

import numpy
import quadtree
import random

def crater(tree):
    '''
    Performs one cratering timestep.

    Returns an integer dC representing the change in the number of craters.
    '''
    crater_x = random.uniform(0.0, 500.0)
    crater_y = random.uniform(0.0, 500.0)

    obliterated = tree.query_range(crater_x - 30.0, crater_y - 30.0,
                                    crater_x + 30.0, crater_y + 30.0)

    dC = 1
    for crater in obliterated:
        dist = numpy.sqrt((crater[0] - crater_x) ** 2 + (crater[1] - crater_y) ** 2)
        if dist <= 30.0:
            tree.remove(crater[0], crater[1])
            dC -= 1

    tree.insert(crater_x, crater_y)
    return dC

def main():
    tree = quadtree.QuadTree(0.0, 0.0, 500.0, 500.0)
    counts = [0]
    i = 1
    while True:
        dC = crater(tree)
        counts.append(counts[i-1] + dC)
        if counts[i / 2] * 1.05 > counts[i]:
            break
        i += 1
    print 'Time: %d years\tCrater count: %d' % (i * 1000, counts[i])

if __name__ == "__main__":
    main()
