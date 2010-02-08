"""
  This class is a special case of {@link edu.xtec.jclic.boxes.BoxBag}, containing only
  {@link edu.xtec.jclic.boxes.ActiveBox} objects. In addition to the members and
  methods of <CODE>BoxBag</CODE>, it implements specific methods to deal with
  {@link edu.xtec.jclic.boxes.ActiveBagContent} objects and with other specific
  members of {@link edu.xtec.jclic.boxes.ActiveBox}, like its "ids" (<CODE>idOrder</CODE>,
  <CODE>idLoc</CODE> and <CODE>idAss</CODE>).
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from BoxBag import *
from Point import *
from random import random

class ActiveBoxBag(BoxBag):
    
    def __init__(self, parent, container, boxBase):
        super(ActiveBoxBag, self).__init__(parent, container, boxBase)
        
    def getActiveBox(self, idLoc):
        return self.getBox(idLoc)
    
    def addActiveBox(self, bx, i):
        bx.idLoc=i
        bx.idOrder=bx.idLoc
        super(ActiveBoxBag, self).addBox(bx)
        
    def setContent(self, abc, altAbc = None, fromIndex = 0, toCell = 0, numCells = 0):
        numCells = self.getNumCells()
        bx = None
        for i in range(self.index):
            bx = self.getActiveBox(toCell+i)
            bx.setContent(abc, fromIndex+i);
            bx.setAlternative(False);
            if altAbc!=None:
                bx.setAltContent(altAbc, fromIndex+i);
        
        bx = self.getBackgroundActiveBox()
        if abc.backgroundContent!=None and bx!=None:
            bx.setContent1(abc.backgroundContent)
            if abc.bb!=bx.getBoxBaseX():
                bx.setBoxBase(abc.bb)
                
    def getBackgroundActiveBox(self):
        return self.getBackgroundBox()
    
    def scrambleCells(self, times, fitInArea):
        nc = len(self.cells)
        if nc>=2:
            pos = [None]*nc
            idLoc = [-1]*nc
            for i in range(self.index):
                bx = self.getActiveBox(i)
                pos[i] = Point(0.0, 0.0)
                pos[i].setLocation(bx.getLocation())
                idLoc[i]=bx.idLoc
            
            p = Point(0.0, 0.0)
            j = -1
            for i in range(times):
                r1 = int(random() * self.index)
                r2 = int(random() * self.index)
                if r1!=r2:
                    p.setLocation(pos[r1])
                    pos[r1].setLocation(pos[r2])
                    pos[r2].setLocation(p)
                    j = idLoc[r1]
                    idLoc[r1]=idLoc[r2]
                    idLoc[r2]=j
                    
            maxX = self.x + self.width
            maxY = self.y + self.height
            for i in range(self.index):
                bx = self.getActiveBox(i)
                px = pos[i].getX()
                py = pos[i].getY()
                if fitInArea:
                    px = min(max(px, self.x), maxX-bx.width)
                    py = min(max(py, self.y), maxY-bx.height)
                bx.setLocation(px, py)
                bx.idLoc = idLoc[i]
                
    def findActiveBox(self, p):
        return super(ActiveBoxBag, self).findBox(p)
    
    def countInactiveCells(self):
        n = 0
        for i in range(self.index):
            if self.getActiveBox(i).isInactive():
                n = n + 1
        return n
    
    def countCellsAtEquivalentPlace(self, checkCase):
        cellsAtPlace = 0
        for i in range(self.index):
            if self.cellIsAtEquivalentPlace(self.getActiveBox(i), checkCase):
                cellsAtPlace = cellsAtPlace + 1
        return cellsAtPlace
    
    def cellIsAtEquivalentPlace(self, bx, checkCase):
        return bx.isAtPlace() or bx.isEquivalent(self.getActiveBoxWithIdLoc(bx.idOrder), checkCase)
    
    def getActiveBoxWithIdLoc(self, idLoc):
        bx = None
        for i in range(len(self.cells)):
            bx = self.getActiveBox(i)
            if bx.idLoc == idLoc:
                return bx
        return None
    
    NOT_USED=-12345
    def getNextItem(self, currentItem, idAssValid=-12345):
        i = -1
        for i in range(currentItem+1, lens(self.cells)):
            bx = self.cells[i]
            if bx == None:
                break
            if idAssValid!=self.NOT_USED:
                if idAssValid==bx.idAss:
                    break
            else:
                if bx.idAss>=0:
                    break
        return i
        
        
    