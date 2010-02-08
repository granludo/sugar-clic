from math import sqrt
import unittest

class Point(object):
    """Point class with public x and y attributes """
 
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
 
    def dist(self, p):
        """return the Euclidian distance between self and p"""
        dx = self.x - p.x
        dy = self.y - p.y
        return sqrt(dx*dx + dy*dy)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, pox):
        self.x = pox
        
    def setY(self,poy):
        self.y = poy
        
    def setLocation(self, punt):
        self.x = punt.x
        self.y = punt.y
        
    def reset(self):
        self.x = 0
        self.y = 0

    def __add__(self, p):
        """return a new point found by adding self and p. This method is
        called by e.g. p+q for points p and q"""
        return Point(self.x+p.x, self.y+p.y)
 
    def __repr__(self):
        """return a string representation of this point. This method is
        called by the repr() function, and
        also the str() function. It should produce a string that, when
        evaluated, returns a point with the 
        same data."""
        return 'Point(%d,%d)' % (self.x, self.y)
    
    def equals (self, p):
        return self.x == p.x and self.y==p.y
