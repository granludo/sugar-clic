"""
  This class stores a collection of {@link edu.xtec.jclic.boxes.ActiveBoxContent}
  objects, currently in a {@link java.util.ArrayList}, and provides methods to
  manage it. The two main members of <CODE>ActiveBagContent</CODE> are the
  {@link edu.xtec.jclic.shapers.Shaper}, responsible of determining the position and shape of each
  {@link edu.xtec.jclic.boxes.ActiveBox} based on it, and the
  {@link edu.xtec.jclic.boxes.BoxBase}, that provides a common visual style.
  author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import Activity
import BoxBase
from BoxBase import *
from Shaper import *
from JDomUtility import checkName
from JDomUtility import getIntAttr
from JDomUtility import getDoubleAttr
from JDomUtility import getBoolAttr
from ActiveBoxContent import *
from Rectangular import *
from pygame import *

class ActiveBagContent(object):
    print 'demo' 
    ncw = 0
    nch = 0
    w = 0.0
    h = 0.0
    activeBoxContentArray = [None] * 12
    posicioArray = 0
    border = True
    img = None
    imgName=""
    bb=None
    shaper=None
    backgroundContent=None
    
    ELEMENT_NAME = "cells"
    COLS = "cols"
    ROWS = "rows"
    COLUMNS = "columns"
    CELL_WIDTH="cellWidth"
    CELL_HEIGHT="cellHeight"
    BORDER="border"
    IMAGE="image"
    
    def __init__(self, ncw=0, nch=0):
        self.ncw = max(1,ncw)
        self.nch = max(1,nch)
        self.w = Activity.Activity.DEFAULT_GRID_ELEMENT_SIZE
        self.h = Activity.Activity.DEFAULT_GRID_ELEMENT_SIZE
        
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        mediaBag = aux
        
        child = None
        
        k = getIntAttr(e, self.COLS, -1)
        if k>=0:
            self.ncw=k
            self.nch=getIntAttr(e, self.ROWS, self.nch)
        else:
            self.ncw=getIntAttr(e, self.ROWS, self.ncw)
            self.nch=getIntAttr(e, self.COLUMNS, self.nch)
        
        if self.nch * self.ncw > 12:
            self.activeBoxContentArray = [None] * self.nch * self.ncw
        
        self.w=getDoubleAttr(e, self.CELL_WIDTH, self.w)
        self.h=getDoubleAttr(e, self.CELL_HEIGHT, self.h)
        self.border=getBoolAttr(e, self.BORDER, self.border)
        self.imgName=e.getAttribute(self.IMAGE)
        
        child = e.getElementsByTagName(BoxBase.BoxBase.ELEMENT_NAME)
        if child!=[]:
            self.setBoxBase(getBoxBase(child[0]))
        
        child = e.getElementsByTagName(Shaper.ELEMENT_NAME)
        if child!=[]:
            self.setShaper(getShaper(child[0]))
        
        llista_cells = e.getElementsByTagName(ActiveBoxContent.ELEMENT_NAME)
        if llista_cells!=[]:
            for celda in llista_cells:
                self.addActiveBoxContent(getActiveBoxContent(celda, mediaBag))

        if self.imgName!="":
            if mediaBag!=None and mediaBag.getProject()!=None:
                self.setImgContent(mediaBag.getImageElement(self.imgName), self.getShaper(), True)
        
        n = len(self.activeBoxContentArray)
        if n>0 and self.activeBoxContentArray[0]!=None:
            empty = True
            for i in range(n):
                bxc = self.getActiveBoxContent(i)
                if bxc.id!=-1 or bxc.item!=-1 or bxc.isEmpty():
                    empty=False
                    break
            if empty:
                for j in range(n):
                    self.getActiveBoxContent(j).id=j
                    
    def setImgContent(self, mbe, sh, roundSizes):
        self.setShaper(sh)
        self.ncw = self.shaper.getNumColumns()
        self.nch = self.shaper.getNumRows()
        if mbe!=None:
            self.img = mbe.getImage()
            self.imgName=mbe.getName()
            self.w=-1 
            self.h=-1
            while True:
                self.w = float(self.img.get_width())/self.ncw
                self.h = float(self.img.get_height())/self.nch
                if self.w>=0 and self.h>=0:
                    break
            if roundSizes:
                self.w=float(int(self.w))
                self.h=float(int(self.h))
                          
            if self.w<1 or self.h<1:
                raise Error, "Invalid image"
        else:
            self.img=None
            self.imgName=None
            self.w=max(self.w, 10)
            self.h=max(self.h, 10)
      
        r=Rect(0.0, 0.0, self.w*self.ncw, self.h*self.nch)
        if len(self.activeBoxContentArray)<self.shaper.getNumCells():
            self.activeBoxContentArray = [None] * self.shaper.getNumCells()
        for i in range(self.shaper.getNumCells()):
            self.getActiveBoxContent(i).setImgContent(self.img, self.shaper.getShape(i, r))
    
    def getActiveBoxContent(self, i):
        if i >= self.posicioArray:
            for j in range(self.posicioArray, i+1):
                self.activeBoxContentArray[self.posicioArray]=ActiveBoxContent()
                self.posicioArray = self.posicioArray + 1
        return self.activeBoxContentArray[i]
    
    def addActiveBoxContent(self, ab):
        self.activeBoxContentArray[self.posicioArray]=ab
        self.posicioArray = self.posicioArray + 1
        if self.nch==0 or self.ncw==0:
            self.nch = self.ncw = 1
    
    def setBoxBase(self, boxBase):
        self.bb=boxBase
        
    def setShaper(self, sh):
        self.shaper=sh
        
    def getTotalWidth(self):
        return self.w*self.ncw
    
    def getTotalHeight(self):
        return self.h*self.nch
    
    def getShaper(self):
        if self.shaper==None:
            self.setShaper(Rectangular(self.ncw, self.nch))
        return self.shaper
    
    def getNumCells(self):
        return len(self.activeBoxContentArray)
        
def getActiveBagContent(e, mediaBag):
    
    abc = ActiveBagContent()
    abc.setProperties(e, mediaBag)
    return abc
        
        