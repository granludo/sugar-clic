"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from Activity import *
from ActiveBagContent import *
from JDomUtility import *
from BoxConnector import *
from ActiveBoxGrid import createEmptyGrid
from BoxBag import *

class DoublePuzzle(Activity):
    
    def __init__(self, project):
        super(DoublePuzzle, self).__init__(project)
        self.abc = [None] * 1
        self.boxGridPos = self.AB
        self.dragCells = True
        
    def initNew(self):
        super(DoublePuzzle, self).initNew()
        self.abc[0] = ActiveBagContent.initNew(3, 2, 'A')
        
    def setProperties(self, e, aux):
        child = None
        super(DoublePuzzle, self).setProperties(e, aux)
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
        bgA = None
        bgB = None
        posicioAnterior = None
        
        def __init__(self, screen, activity, ps):
            super(DoublePuzzle.Panel, self).__init__(screen, activity, ps)
            self.bc = BoxConnector(self)
            
        def clear(self):
            if self.bgA!=None:
                self.bgA.end()
                self.bgA=None
            if self.bgB!=None:
                self.bgB.end()
                self.bgB=None
                
        def buildVisualComponents(self):
            if self.firstRun:
                super(DoublePuzzle.Panel,self).buildVisualComponents()
                
            self.clear()
            
            if self.abc[0] != None:
                self.bgA = createEmptyGrid(None, self, self.margin, self.margin, self.abc[0])
                self.bgB = createEmptyGrid(None, self, self.margin, self.margin, self.abc[0])
                self.bgA.setContent(self.abc[0])
                self.bgA.setVisible(True)
                self.bgB.setVisible(True)
                
        def initActivity(self):
            super(DoublePuzzle.Panel, self).initActivity()
            
            if self.firstRun == False:
                 self.buildVisualComponents()
            else:
                self.firstRun = False
                
            self.setAndPlayMsg(self.activity.MAIN)
            if self.bgA != None and self.bgB!=None:
                self.shuffle([self.bgA], True, True)
                
                if self.activity.useOrder:
                    self.currentItem = self.bgA.getNextItem(-1)
                
                self.playing = True
                
        def render(self, g2):
            if self.bgA != None:
                self.bgA.update(g2, self)
            if self.bgB != None:
                self.bgB.update(g2, self)
            if self.bc.active == True:
                self.bc.update(g2, self)
                
        def setDimension(self, preferredMaxSize):
            if self.bgA==None or self.bgB==None:
                return preferredMaxSize
            return layoutDouble(preferredMaxSize, self.bgA, self.bgB, self.activity.boxGridPos, self.activity.margin)
        
        def processMouse(self, e):
            bx1 = None
            bx2 = None
            p=pygame.mouse.get_pos()
            if self.bgImage!=None:
                p = (p[0] - (self.panelDim.getW()/2 - self.imageDim.getW()/2 + self.origin.x) ,p[1] - (self.panelDim.getH()/2 - self.imageDim.getH()/2 + self.origin.y))
            else:
                p = (p[0] - self.origin.x,p[1] - self.origin.y)
            m=False
            
            if self.playing:
                botonsApretats = pygame.mouse.get_pressed()
                if botonsApretats[0] == True or botonsApretats[1] == True or botonsApretats[2] == True:
                    if self.bc.active:
                        if self.activity.dragCells:
                            bx1=self.bc.getBox()
                        else:
                            bx1=self.bgA.findActiveBox((self.bc.origin.getX(),self.bc.origin.getY()))
                        self.bc.end() 
                        bx2=self.bgB.findActiveBox(p)
                        if bx1!=None and bx2!=None and bx2.isInactive():
                            ok = False
                            if bx1.getContent().isEquivalent(self.abc[0].getActiveBoxContent(bx2.idOrder), True):
                                ok = True
                                bx1.exchangeContent(bx2)
                                bx1.setVisible(False)
                                if self.activity.useOrder:
                                    self.currentItem=self.bgA.getNextItem(self.currentItem)
                            cellsAtPlace=self.bgA.countInactiveCells()
                            if ok and cellsAtPlace==self.bgA.getNumCells():
                                self.finishActivity(True)
                    else:
                        bx1=self.bgA.findActiveBox(p)
                        if bx1!=None and not bx1.isInactive() and (not self.activity.useOrder or bx1.idOrder==self.currentItem):
                            if self.activity.dragCells:
                                self.bc.begin(p, bx1)
                            else:
                                self.bc.begin(p)
                elif self.posicioAnterior!=p:
                        self.bc.moveTo(p);
            self.posicioAnterior = p    
                    