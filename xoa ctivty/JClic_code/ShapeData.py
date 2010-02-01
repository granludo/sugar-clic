"""
 
  @author  Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from copy import deepcopy 
import PathIterator
import pygame
from pygame import *

class ShapeData(object):
    
    points = None
    pointsIndex = None
    CAPACITY_BLOCK=6
    pointsIndex = None
    descriptors = None
    descriptorsIndex = None
    comment = None
    primitiveType = None
    primitivePoint = None
    
    def __init__(self):
        self.points = [-1.0] * self.CAPACITY_BLOCK
        self.pointsIndex = 0
        self.descriptors = [-1] * self.CAPACITY_BLOCK
        self.descriptorsIndex = 0
        self.primitivePoints=None
        self.primitiveType=-1
        self.comment=None
        
    def addDescriptor(self, descriptor):
        if self.descriptorsIndex+1>=len(self.descriptors):
            d2 = [None]*(len(self.descriptors)+self.CAPACITY_BLOCK)
            for i in range(self.descriptorsIndex): 
                d2[i]=self.descriptors[i]
            self.descriptors=deepcopy(d2)
        self.descriptors[self.descriptorsIndex]=descriptor
        self.descriptorsIndex = self.descriptorsIndex + 1
        
    def addData(self, data):
        if data==None:
            return
        if self.pointsIndex+len(data)>=len(self.points):
            d2=[None]*(len(self.points)+2*self.CAPACITY_BLOCK)
            for i in range(self.pointsIndex):
                d2[i]=self.points[i]
            self.points=deepcopy(d2)
        for i in range(len(data)):
            self.points[self.pointsIndex]=data[i]
            self.pointsIndex = self.pointsIndex + 1
            
    
    def add(self, descriptor, data):
        self.addDescriptor(descriptor)
        if data!=None: 
            self.addData(data)
    
    def moveTo(self, x, y):
        self.add(PathIterator.SEG_MOVETO, [x, y])
       
    def lineTo(self, x, y):
        self.add(PathIterator.SEG_LINETO, [x, y])
       
    def quadTo(self, x0, y0, x1, y1):
        self.add(PathIterator.SEG_QUADTO, [x0, y0, x1, y1])
    
    def cubicTo(self, x0, y0, x1, y1, x2, y2):
        self.add(PathIterator.SEG_CUBICTO, [x0, y0, x1, y1, x2, y2])
    
    def closePath(self):
        self.add(PathIterator.SEG_CLOSE, None)
        
    def getShape(self, dx, dy, scaleX, scaleY):
        gp=[None] * (self.pointsIndex+1)
        j=0 
        ox = oy = 0
        for i in range(self.descriptorsIndex):
            if self.descriptors[i] == PathIterator.SEG_MOVETO:
                gp[i] = (PathIterator.SEG_MOVETO, dx+scaleX*self.points[j], dy+scaleY*self.points[j+1])
                ox = dx+scaleX*self.points[j]
                oy = dy+scaleY*self.points[j+1]
                j = j + 2
            elif self.descriptors[i] == PathIterator.SEG_LINETO: 
                gp[i] = (PathIterator.SEG_LINETO, dx+scaleX*self.points[j], dy+scaleY*self.points[j+1])
                j = j + 2
            elif self.descriptors[i] == PathIterator.SEG_QUADTO: 
                gp[i] = (PathIterator.SEG_QUADTO, dx + scaleX*self.points[j], dy + scaleY*self.points[j+1], dx+scaleX*self.points[j+2],dy+scaleY*points[j+3])
                j = j + 4
            elif self.descriptors[i] == PathIterator.SEG_CUBICTO:
                gp[i] = (PathIterator.SEG_CUBICTO, dx+scaleX*self.points[j], dy+scaleY*self.points[j+1], dx+scaleX*self.points[j+2], dy+scaleY*self.points[j+3], dx+scaleX*self.points[j+4], dy+scaleY*self.points[j+5])
                j = j + 6
            elif self.descriptors[i] == PathIterator.SEG_CLOSE:
                gp [i] = (PathIterator.SEG_LINETO, ox, oy)
        return gp
    