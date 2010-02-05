"""
  <CODE>BoxConnector</CODE> allows users to visually connect two {@link edu.xtec.jclic.boxes.ActiveBox}
  objects in a {@link edu.xtec.jclic.Activity.Panel}. There are two modes of operation:
  drwaing a line between an origin point (usually the point where the user clicks on)
  and a destination point, or dragging the box from one location to another. The lines can
  have arrows at its ending.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from Point import *
from pygame import Rect
from ActiveBox import ActiveBox

class BoxConnector(object):
    
    bx = None
    parent = None
    origin = None
    relativePos = None
    arrow = None
    active = False
    linePainted = False
    
    def __init__(self, setParent):
        self.parent = setParent
        self.origin = Point(-1.0, -1.0)
        self.dest = Point(-1.0, -1.0)
        self.arrow=False
        self.active=False
        self.linePainted=False
        self.relativePos = Point(-1.0, -1.0)
        
    def getBox(self):
        return self.bx
    
    def begin(self, p, setBox=None):
        point = p
        if setBox==None:
            if self.active:
                self.end()    
            point2 = Point(p[0], p[1])
            self.origin.setLocation(point2)
            self.dest.setLocation(point2)
            self.linePainted=False
            self.active=True
        else:
            self.begin(point)
            self.bx = setBox
            self.relativePos.setLocation(Point(point[0]-self.bx.x, point[1]-self.bx.y))
            self.bx.setTemporaryHidden(True)
            r = super(ActiveBox, self.bx).getBounds()
            self.linePainted=False

    def end(self):
        if not self.active: 
            return
        if self.bx!=None:
            r = super(ActiveBox, self.bx).getBounds()
            self.bx.setLocation(self.origin.getX()-self.relativePos.getX(), 
                           self.origin.getY()-self.relativePos.getY())
            self.bx.setTemporaryHidden(False)
            r = super(ActiveBox, self.bx).getBounds()
            self.bx=None
            self.relativePos.setLocation(Point(0, 0))
        else:
            self.moveTo(self.dest, True)
        self.active=False
        self.linePainted=False

    def moveTo(self, p, forcePaint=False):
        clipRect = None
        
        if not self.active or (forcePaint and self.dest.getX()==p[0] and self.dest.getY()==p[1]):
            return 
        
        if self.bx!=None:
            clipRect = Rect(
            int(p[0]-self.relativePos.getX()),
            int(p[1]-self.relativePos.getY()),
            int(self.bx.width),
            int(self.bx.height))
            super(ActiveBox, self.bx).union(clipRect)
            self.bx.setLocation(p[0]-self.relativePos.getX(), p[1]-self.relativePos.getY())            
    
    def update(self, g2, io):
        if not self.active:
            return False
        
        if self.bx!=None:
            self.bx.setTemporaryHidden(False)
            self.bx.update(g2, io)
            self.bx.setTemporaryHidden(True)

        return True
    