""" This abstract class is the base for most graphic components of JClic. It describes
    an {@link java.awt.geom.Area} (a rectangle by default) with some special properties
    that determine how it must be drawn on screen. Some types of boxes can act as
    containers for other boxes, establishing a hierarchy of dependences.
    Box objects are always placed into a {@link javax.swing.JComponent}.
    @author Francesc Busquets (fbusquets@xtec.net)
    @version 1.0 
    
"""

from pygame import Rect
from Point import *
from BoxBase import *

class AbstractBox(Rect):
    
    parent = None
    container = None
    shape = None
    specialShape = None
    boxBase = None
    visible = None
    inactive = None
    border = None
    alternative = None
    temporaryHidden = None
    marked = None
    inverted = None
    
    def __init__(self, parent, container, boxBase):
        self.parent=parent
        self.container=container
        self.shape=self
        self.specialShape=False
        self.boxBase=boxBase
        self.visible=True
        
    def setInactive(self, newVal):
        self.inactive = newVal
        
    def setParent(self, parent):
        self.parent=parent
        
    def getParent(self):
        return self.parent
        
    def setBorder(self, newVal):
        self.border=newVal
        
    def setBounds(self, r):
        if r == self: 
            return
        
        super(AbstractBox, self).__init__(r)
        
    def getContainerX(self):
        return self.container
    
    def getBoxBaseX(self):
        return self.boxBase
    
    def setBoxBase(self, boxBase):
        self.boxBase=boxBase

    def hasBorder(self):
        return self.border
    
    def setAlternative(self, newVal):
        self.alternative=newVal

    def setVisible(self, newVal):
        self.visible=newVal

    def getLocation(self):
        return Point(self.x, self.y)
    
    def setLocation(self, newX, newY):
        self.setBounds(Rect(newX, newY, self.width, self.height))
        
    def setTemporaryHidden(self, newVal):
        self.temporaryHidden = newVal
        
    def repaint(self):
        component = self.getContainerResolve()

    def getContainerResolve(self):
        ab = self
        while ab.container==None and ab.parent!=None:
            ab = ab.parent
        return ab.container
    
    def getBoxBaseResolve(self):
        ab = self
        while ab.boxBase==None and ab.parent!=None:
            ab = ab.parent
        if ab.boxBase==None:
            return BoxBase()
        else:
            return ab.boxBase
    
    def getBounds(self):
        return Rect(self.topleft, (self.width, self.height))
    
    def setInverted(self, newVal):
        self.inverted = newVal
        
    def isInverted(self):
        return self.inverted
    
    def isVisible(self):
        return self.visible
    
    def isTemporaryHidden(self):
        return self.temporaryHidden
    
    def isMarked(self):
        return self.marked
    
    def isAlternative(self):
        return self.alternative
    
    def isInactive(self):
        return self.inactive
    
    def update(self, g2, io):
        if self.isTemporaryHidden() or not self.isVisible() or self.isEmpty():
            return False
        
        bb = self.getBoxBaseResolve()

        if not bb.transparent:
            color = None
            if self.inactive:
                color = bb.inactiveColor       
            elif self.inverted:
                color = bb.textColor
            else:
                color = bb.backColor
            pygame.draw.rect(g2, color, self)
            
        self.updateContent(g2, io)
            
        self.drawBorder(bb, g2)
        
    def drawBorder(self, bb, g2):
        pygame.draw.rect(g2, bb.borderColor, self, 1)
        
    def contains(self, p):
        return self.collidepoint((p[0]),(p[1]))
     
    def isEmpty(self):
        if self.height==0 and self.width==0:
            return True
        else:
            return False
    
    