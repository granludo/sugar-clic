"""
  This class is a {@link edu.xtec.jclic.boxes.ActiveBoxBag} with constructors that
  take an argument of type {@link edu.xtec.jclic.shapers.Shaper} to build
  all its {@link edu.xtec.jclic.boxes.ActiveBox} elements. It also mantains info about
  the number of "rows" and "columns", useful to compute appropiate (integer) values when
  resizing the <CODE>ActiveBoxBag</CODE> and its <CODE>ActiveBox</CODE> children.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from ActiveBoxBag import *
from pygame import Rect
from ActiveBox import *
from Dimension import *
from Point import *

class ActiveBoxGrid(ActiveBoxBag):
    
    MIN_CELL_SIZE = 10
    nCols = None
    nRows = None
    
    def __init__(self, parent, container, px, py, setWidth, setHeight, sh, boxBase): 
        super(ActiveBoxGrid, self).__init__(parent, container, boxBase)
        self.nCols = sh.getNumColumns()
        self.nRows = sh.getNumRows()
        r = Rect(px, py, (setWidth/self.nCols)*self.nCols, (setHeight/self.nRows)*self.nRows)
        self.ensureCapacity(sh.getNumCells())
        
        for i in range(sh.getNumCells()):
            shape = sh.getShape(i, r)
            bx = ActiveBox(self, None, i, sh.getBounds2D(shape), None)
            if not sh.rectangularShapes():
                bx.setShape(shape) 
            self.addActiveBox(bx, i)

    def getMinimumSize(self):
        return Dimension(self.MIN_CELL_SIZE * self.nCols, self.MIN_CELL_SIZE * self.nRows)
    
    def getCoord(self, bx):
        y=bx.idLoc/self.nCols
        x=bx.idLoc % self.nCols
        return Point(x, y)
    
    def getCoordDist(self, src, dest):
        ptSrc=self.getCoord(src)
        ptDest=self.getCoord(dest)
        return Point(ptDest.x-ptSrc.x, ptDest.y-ptSrc.y)
    
    
def createEmptyGrid(parent, container, px, py, abc, sh=None, boxBase=None):
    result = None
    if(abc!=None):
        if (sh==None and boxBase==None):
            result = ActiveBoxGrid(parent, container, px, py, abc.getTotalWidth(), abc.getTotalHeight(), abc.getShaper(), abc.bb)
        elif (sh==None):
            result = ActiveBoxGrid(parent, container, px, py, abc.getTotalWidth(), abc.getTotalHeight(), abc.getShaper(), boxBase)
        elif(boxBase==None):
            result = ActiveBoxGrid(parent, container, px, py, abc.getTotalWidth(), abc.getTotalHeight(), sh, abc.bb)
        else:
            result = ActiveBoxGrid(parent, container, px, py, abc.getTotalWidth(), abc.getTotalHeight(), abc.getShaper(), abc.bb)
        
        result.setBorder(abc.border)
    return result
        