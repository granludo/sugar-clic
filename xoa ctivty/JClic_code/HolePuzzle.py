"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from Activity import *
from ActiveBagContent import *
from JDomUtility import *
from BoxConnector import *
from BoxBag import *
from random import random
from ActiveBoxGrid import *

class HolePuzzle(Activity):
    
    def __init__(self, project):
        super(HolePuzzle, self).__init__(project)
        self.abc = [None] * 1
        self.boxGridPos = self.AB
        
    def initNew(self):
        super(HolePuzzle, self).initNew()
        self.abc[0] = ActiveBagContent.initNew(3, 2, 'A')
        
    def setProperties(self, e, aux):
        child = None
        super(HolePuzzle, self).setProperties(e, aux)
        child= e.getElementsByTagName(ActiveBagContent.ELEMENT_NAME)
        if child != []:
            self.abc[0] = getActiveBagContent(child[0], self.project.mediaBag)
        if self.abc[0] == None:
            raise SyntaxError, "Puzzle without content!"
        child= e.getElementsByTagName(self.SCRAMBLE)
        if child != []:
            self.shuffles=getIntAttr(child[0], self.TIMES, self.shuffles)
        
        child= e.getElementsByTagName(self.LAYOUT)
        if child != []:
            self.boxGridPos=getStrIndexAttr(child[0].getAttribute(self.POSITION), self.LAYOUT_NAMES , self.boxGridPos)
            
    def getMinNumActions(self):
        if(self.abc[0] == None):
            return 0
        else:
            return self.abc[0].getNumCells()
        
    def helpSolutionAllowed(self):
        return True
    
    def hasRandom(self): 
        return True
    
    def shuffleAlways(self):
        return True
    
    def getActivityPanel(self, screen, ps):
        p = self.Panel(screen, self, ps)
        return p
    
    class Panel(Activity.Panel):
        bg = None
        parkBg = None
        hiddenBoxIndex = -1
        hiddenBox = None
        
        def __init__(self, screen, activity, ps):
            super(HolePuzzle.Panel, self).__init__(screen, activity, ps)
            self.bg = None
            self.parkBg = None
            self.hiddenBoxIndex = 0
            self.hiddenBox = None
            
        def clear(self):
            if self.bg!=None:
                self.bg.end()
                self.bg = None
            if self.parkBg!=None:
                self.parkBg.end()
                self.parkBg = None
                
        def buildVisualComponents(self):
            if self.firstRun:
                super(HolePuzzle.Panel,self).buildVisualComponents()
                
            self.clear()
            
            if self.abc[0] != None:
                self.bg = createEmptyGrid(None, self, self.margin, self.margin, self.abc[0])
                self.bg.setContent(self.abc[0])
                self.bg.setVisible(True)
                
                self.hiddenBoxIndex=int(random()*self.bg.getNumCells())
                self.hiddenBox=self.bg.getActiveBox(self.hiddenBoxIndex)
                self.hiddenBox.setVisible(False)
                
                self.parkBg=ActiveBoxGrid(None, self, self.margin, self.margin, self.hiddenBox.w, self.hiddenBox.h, Rectangular(1,1) , self.abc[0].bb)
                self.parkBg.setContent(self.abc[0], None, self.hiddenBoxIndex, 0, 1)
                self.parkBg.setBorder(self.bg.hasBorder())
                self.parkBg.setVisible(True)
                
        def initActivity(self):
            super(HolePuzzle.Panel, self).initActivity()
            
            if self.firstRun == False:
                 self.buildVisualComponents()
            self.firstRun = False
            
            self.setAndPlayMsg(self.activity.MAIN)
            if self.bg!=None:
                if self.activity.shuffles % 2 != 1:
                    self.activity.shuffles = self.activity.shuffles + 1
                for i in range(self.activity.shuffles):
                    pth = self.bg.getCoord(self.hiddenBox)
                    v = random()
                    if v>= 0.5:
                        v = 1
                    else:
                        v = -1
                    if random()>=0.5:
                        pth.x = pth.x + v
                        if pth.x<0 or pth.x>=self.bg.nCols:
                            pth.x = pth.x - 2*v
                    else:
                        pth.y = pth.y + v
                        if pth.y<0 or pth.y>=self.bg.nRows:
                            pth.y = pth.y - 2*v
                    dstBx = self.bg.getActiveBoxWithIdLoc(pth.y*self.bg.nCols+pth.x)
                    if dstBx!=None:
                        self.hiddenBox.exchangeLocation(dstBx)
                self.playing = True
                
        def render(self, g2):
            if self.bg != None:
                self.bg.update(g2, self)
            if self.parkBg != None:
                self.parkBg.update(g2, self)
                
        def setDimension(self, preferredMaxSize):
            if self.bg==None or self.parkBg==None:
                return preferredMaxSize
            return layoutDouble(preferredMaxSize, self.bg, self.parkBg, self.activity.boxGridPos, self.activity.margin)
        
        def processMouse(self, e):
            bx = None
            p=pygame.mouse.get_pos()
            if self.bgImage!=None:
                p = (p[0] - (self.panelDim.getW()/2 - self.imageDim.getW()/2 + self.origin.x) ,p[1] - (self.panelDim.getH()/2 - self.imageDim.getH()/2 + self.origin.y))
            else:
                p = (p[0] - self.origin.x,p[1] - self.origin.y)
            m=False
            
            if self.playing:
                botonsApretats = pygame.mouse.get_pressed()
                if botonsApretats[0] == True or botonsApretats[1] == True or botonsApretats[2] == True:
                    bx=self.bg.findActiveBox(p)
                    if bx!=None:
                        if bx.isVisible():
                            pt = self.bg.getCoordDist(bx, self.hiddenBox)
                            if abs(pt.x) + abs(pt.y) ==1:
                                bx.exchangeLocation(self.hiddenBox)
                                ok = (bx.idOrder==bx.idLoc)
                                cellsAtPlace=self.bg.countCellsAtEquivalentPlace(True)
                                if ok and cellsAtPlace==self.bg.getNumCells():
                                    self.hiddenBox.setVisible(True)
                                    self.parkBg.setVisible(False)
                                    self.finishActivity(True)