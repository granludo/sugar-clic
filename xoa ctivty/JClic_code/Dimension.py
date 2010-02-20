import unittest
from Point import *

class Dimension(object):
    """Point class with public x and y attributes """
 
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h
        
    def getW(self):
        return self.w
    
    def getH(self):
        return self.h
    
    def setW(self, wi):
        self.w = wi
        
    def setH(self,he):
        self.h = he
        
    def getSize(self):
        size = self.w * self.h
        return size
        
    def reset(self):
        self.w = 0
        self.h = 0

    def __add__(self, d):
        """return a new point found by adding self and p. This method is
        called by e.g. p+q for points p and q"""
        return Point(self.w+d.w, self.h+d.h)
 
    def __repr__(self):
        return 'Dimension(%d,%d)' % (self.w, self.h)