################################################################################
#
# File: quadtree.py
# Author: Ken Sheedlo
# ASTR 3750 - Fall 2012
#
# A simple QuadTree implementation for collision detection in two dimensions
#
################################################################################

import unittest

def _range_contains_point(x_min, y_min, x_max, y_max, x_p, y_p):
    return (x_min <= x_p) and (x_p <= x_max) and (y_min <= y_p) and (y_p <= y_max)

_QT_NW = 0
_QT_NE = 1
_QT_SW = 2
_QT_SE = 3

class QuadTree:
    '''
    A simple quadtree implementation for collision detection.

    This quadtree implementation stores points as (x, y) pairs in a suitable
    numeric format. It is designed with floating-point in mind, though integers
    will probably also work.

    In a deviation fron the traditional quadtree, interior nodes are not
    permitted to contain point values. This is done to facilitate node removal
    and help the tree prune nodes that are no longer being used. Additionally,
    to simplify the implementation, only one point value is permitted per leaf
    node.

    MEMBER FIELDS

        (x_min, y_min, x_max, y_max)
            
            The bounding coordinates of this QuadTree. These define a rectangle
            in 2D space and are the domain of the tree.

        p
            
            A point value. This is None for empty trees, defined for a tree 
            containing exactly one value, and None for a tree with children.

        child
            
            An array of child nodes. Each child node is a complete QuadTree. 
            This field is None for empty trees and trees with one child. For 
            trees with children, this field is always defined and initialized
            as an array of four child QuadTrees.
    '''
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max
        self.x_max = x_max

        self.p = None
        self.child = None

    def bounds_contain_point(self, x, y):
        '''
        Queries this tree's bounds to determine if they contain the given point.

        Returns True if so, False otherwise.
        '''
        return _range_contains_point(self.x_min, self.y_min, 
                                    self.x_max, self.y_max, 
                                    x, y)

    def bounds_intersect_area(self, x_min, y_min, x_max, y_max):
        '''
        Checks the tree's bounds for intersecting the given area.

        Returns True if the areas intersect, False otherwise.
        '''
        return not (x_max < self.x_min) or (y_max < self.y_min) or \
            (self.x_max < x_min) or (self.y_max < y_min)

    def contains_point(self, x, y):
        '''
        Determines if the tree contains a specific (x, y) point value.

        Returns True if so, False otherwise.
        '''
        if not self.bounds_contain_point(x, y):
            return False

        if self.p is not None:
            return self.p[0] == x and self.p[1] == y
        if self.child is None:
            return False
        for c in self.child:
            if c.contains_point(x, y):
                return True
        return False

    def __contains__(self, p):
        return self.contains_point(p[0], p[1])

    def __len__(self):
        if self.p is not None:
            return 1
        if self.child is None:
            return 0
        return sum([len(c) for c in self.child])

    def _subdivide(self):
        '''

        '''
        x_center = self.x_min + ((self.x_max - self.x_min) / 2.0)
        y_center = self.y_min + ((self.y_max - self.y_min) / 2.0)
        self.child = [
            QuadTree(self.x_min, self.y_min, x_center, y_center),
            QuadTree(x_center, self.y_min, self.x_max, y_center),
            QuadTree(self.x_min, y_center, x_center, self.y_max),
            QuadTree(x_center, y_center, self.x_max, self.y_max)
        ]
        for c in self.child:
            if c.insert(self.p[0], self.p[1]):
                break
        else:
            raise Exception('Failed to insert point in a child node')
        self.p = None

    def empty(self):
        return self.p is None and self.child is None

    def is_leaf_node(self):
        return self.child is None

    def insert(self, x, y):
        if not self.bounds_contain_point(x, y):
            return False

        if self.child is None:
            if self.p is None:
                self.p = (x, y)
                return True
            self._subdivide()
        
        for c in self.child:
            if c.insert(x, y):
                return True

        # This line should never be reached
        return False

    def remove(self, x, y):
        if not self.bounds_contain_point(x, y):
            return False

        if self.child is None:
            if self.p is None:
                return False
            if self.p == (x, y):
                self.p = None
                return True
            return False

        for c in self.child:
            if c.remove(x, y):
                break
        else:
            return False

        # If one or no children have point values, coalesce
        only = None
        for c in self.child:
            if not c.empty():
                if only is None:
                    only = c
                else:
                    break
        else:
            if only is not None and only.is_leaf_node():
                self.p = only.p
                self.child = None
            elif only is None:
                self.child is None
        return True

    def query_range(self, x_min, y_min, x_max, y_max):
        points = []
        if self.p is not None:
            if _range_contains_point(x_min, y_min, x_max, y_max, self.p[0], self.p[1]):
                points.append(self.p)
        if self.child is not None:
            for c in self.child:
                if c.bounds_intersect_area(x_min, y_min, x_max, y_max):
                    points.extend(c.query_range(x_min, y_min, x_max, y_max))
        return points

class TestQuadtree(unittest.TestCase):
    
    def setUp(self):
        pass

    def assert_quadtree_contents(self, tree, expect_list):
        # All points in the expect list must be in the tree
        for p in expect_list:
            self.assertIn(p, tree)

        # And no others.
        self.assertEqual(len(tree), len(expect_list))

    def assert_list_contents_no_ordering(self, test_list, expect_list):
        self.assertEqual(len(test_list), len(expect_list))
        for e in expect_list:
            self.assertIn(e, test_list)

    def test_insert(self):
        tree = QuadTree(0.0, 0.0, 100.0, 100.0)
        self.assertTrue(tree.insert(5.0, 3.0))
        self.assertTrue(tree.insert(42.0, 13.37))
        self.assertTrue(tree.insert(11.11, 99.99))
        self.assertTrue(tree.insert(5.0, 8.0))

        expect = [
            (5.0, 3.0),
            (42.0, 13.37),
            (11.11, 99.99), 
            (5.0, 8.0)
        ]

        self.assert_quadtree_contents(tree, expect)

        # Illegal insert
        self.assertFalse(tree.insert(101.1, 3.3))
        self.assert_quadtree_contents(tree, expect)

    def test_remove(self):
        tree = QuadTree(0.0, 0.0, 100.0, 100.0)
        tree.insert(5.0, 3.0)
        tree.insert(42.0, 13.37)
        tree.insert(11.11, 99.99)
        tree.insert(5.0, 8.0)

        expect = [
            (5.0, 3.0),
            (42.0, 13.37),
            (11.11, 99.99), 
            (5.0, 8.0)
        ]

        self.assert_quadtree_contents(tree, expect)

        self.assertTrue(tree.remove(42.0, 13.37))

        expect = [
            (5.0, 3.0),
            (11.11, 99.99), 
            (5.0, 8.0)
        ]
        
        self.assert_quadtree_contents(tree, expect)
        self.assertFalse(tree.remove(5.0, 4.0))

    def test_query_range(self):
        tree = QuadTree(0.0, 0.0, 100.0, 100.0)
        tree.insert(5.0, 3.0)
        tree.insert(42.0, 13.37)
        tree.insert(11.11, 99.99)
        tree.insert(5.0, 8.0)
        tree.insert(70.0, 30.0)

        expect = [
            (5.0, 8.0),
            (42.0, 13.37)
        ]

        result = tree.query_range(3.0, 5.0, 50.0, 50.0)
        self.assert_list_contents_no_ordering(result, expect)

if __name__ == "__main__":
    unittest.main()
