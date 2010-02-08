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

class ExchangePuzzle(Activity):
    
    def __init__(self, project):
        super(ExchangePuzzle, self).__init__(project)
        self.abc = [None] * 1
        self.dragCells = True
        
    def initNew(self):
        super(ExchangePuzzle,self).initNew()
        self.abc[0] = ActiveBagContent.initNew(3, 2, 'A')
        
    def setProperties(self, e, aux):
        child = None
        super(ExchangePuzzle, self).setProperties(e, aux)
        child= e.getElementsByTagName(ActiveBagContent.ELEMENT_NAME)
        if child != []:
            self.abc[0] = getActiveBagContent(child[0], self.project.mediaBag)
        if self.abc[0] == None:
            raise SyntaxError, "Puzzle without content!"
        child= e.getElementsByTagName(self.SCRAMBLE)
        if child != []:
            self.shuffles=getIntAttr(child[0], self.TIMES, self.shuffles)
            
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
        posicioAnterior = None
        
        def __init__(self, screen, activity, ps):
            super(ExchangePuzzle.Panel, self).__init__(screen, activity, ps)
            self.bc = BoxConnector(self)
            
        def clear(self):
            if(self.bg != None):
                self.bg.end()
                self.bg = None
                
        def buildVisualComponents(self):
                
            if self.firstRun:
                super(ExchangePuzzle.Panel,self).buildVisualComponents()
                
            self.clear()
            
            if self.abc[0] != None:  
                self.bg=createEmptyGrid(None, self, self.margin, self.margin, self.abc[0])
                self.bg.setContent(self.abc[0])
                self.bg.setVisible(True)
        
        def initActivity(self):
            super(ExchangePuzzle.Panel, self).initActivity()
            
            if self.firstRun == False:
                 self.buildVisualComponents()
            self.firstRun = False
            
            self.setAndPlayMsg(self.activity.MAIN)
            if self.bg != None:
                self.shuffle([self.bg], True, False)
                self.playing = True
        
        def repaint(self):
            super(ExchangePuzzle.Panel, self).repaint()
        
        def render(self, g2):
            if self.bg != None:
                self.bg.update(g2, self)
            if self.bc.active == True:
                self.bc.update(g2, self)
        
        def setDimension(self, preferredMaxSize):
            if self.bg == None: 
                return preferredMaxSize
            return layoutSingle(preferredMaxSize, self.bg, self.margin)
        
        def processMouse(self, e):
            bx1 = bx2 = None
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
                            bx1=self.bg.findActiveBox((self.bc.origin.getX(),self.bc.origin.getY()))
                        self.bc.end() 
                        bx2=self.bg.findActiveBox(p)
                        if bx1!=None and bx2!=None:
                            ok = (bx1.idOrder==bx2.idLoc)
                            bx1.exchangeLocation(bx2)
                            cellsAtPlace=self.bg.countCellsAtEquivalentPlace(True)
                            if ok and cellsAtPlace==self.bg.getNumCells():
                                self.finishActivity(True)
                
                        self.repaint()
                    else:
                        bx1=self.bg.findActiveBox(p)
                        if bx1!=None:
                            if self.activity.dragCells:
                                self.bc.begin(p, bx1)
                            else:
                                self.bc.begin(p)
                            
                elif self.posicioAnterior!=p:
                        self.bc.moveTo(p);
            self.posicioAnterior = p
        