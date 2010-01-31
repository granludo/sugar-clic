"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from JDomUtility import checkName
from JDomUtility import getClassName
from JDomUtility import getIntAttr
from ShapeData import *

class Shaper(object):
    
    ELEMENT_NAME="shaper"
    COLS = "cols"
    ROWS = "rows"
    BASE_CLASS_TAG="@"
    nCols = -1.0
    nRows = -1.0
    nCells = -1
    initiated = False
    WIDTH = 1.0
    HEIGHT = 1.0
    shapeData = None
    
    def __init__(self, nx, ny):
        self.reset(nx, ny)
        
    def reset(self, nCols, nRows):
        self.nCols=nCols
        self.nRows=nRows
        self.nCells = nCols * nRows
        self.initiated = False
        self.shapeData = [None] * self.nCells
        for i in range(self.nCells):
            self.shapeData[i]= ShapeData()
    
    def setProperties(self, e, aux):
        return
    
    def getNumColumns(self):
        return self.nCols
    
    def getNumRows(self):
        return self.nRows
    
    def getNumCells(self):
        return self.nCells
    
    def getShape(self, n, rect):
        if not self.initiated:
            self.buildShapes()
        if n>=self.nCells or self.shapeData[n]==None:
            return None
        return self.shapeData[n].getShape(rect.x, rect.y, rect.width, rect.height);

    def getBounds2D(self, shape):
        minx = 400000000
        maxx = -1
        miny = 400000000
        maxy = -1
        for i in range(len(shape)):
            if shape[i]==None:
                break
            if (shape[i])[1]<minx:
                minx = (shape[i])[1]
            if (shape[i])[1]>maxx:
                maxx = (shape[i])[1]
            if (shape[i])[2]<miny:
                miny = (shape[i])[2]
            if (shape[i])[2]>maxy:
                maxy = (shape[i])[2]
        return (minx, miny, maxx-minx, maxy-miny)
    
def createShaper(className, cw, ch):
    if className.startswith(Shaper.BASE_CLASS_TAG):
        className = className[1:]
    if className=="JigSaw" or className=="ClassicJigSaw" or className=="TriangularJigSaw" or "Holes":
        className="Rectangular"
    sh = None
    s = ""
    module = __import__(className)
    shaperClass = getattr(module,className)
    sh = Shaper.__new__(shaperClass)
    sh.__init__(cw, ch)
    return sh
    
def getShaper(e): 
    checkName(e, Shaper.ELEMENT_NAME)
    className = getClassName(e)
    cw = getIntAttr(e, Shaper.COLS, 1)
    ch = getIntAttr(e, Shaper.ROWS, 1)
    sh = createShaper(className, cw, ch)
    sh.setProperties(e, None)
    return sh
    