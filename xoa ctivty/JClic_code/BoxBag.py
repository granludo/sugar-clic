"""
  A BoxBag is a class derived from {@link edu.xtec.jclic.boxes.AbstractBox} that contains
  a collection of "boxes" (objects also derived from AbstractBox). The boxes are stores into
  a protected {@link java.util.ArrayList}. The class implements methods to add, remove and
  retrieve boxes, and to manage some of its properties like visibility, status, location
  and size.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from AbstractBox import *
from Dimension import *
from pygame import *
from Activity import *

class BoxBag(AbstractBox):
    
    preferredBounds = None
    cells = None
    index = 0
    backgroundBox = None
    
    def __init__(self, parent, container, boxBase):
        super(BoxBag, self).__init__(parent, container, boxBase)
        self.cells = [None] * 12
        self.preferredBounds = Rect(self.left, self.top, self.width, self.height)
    
    def ensureCapacity(self, n):
        if n>len(self.cells):
            self.cells = [None]*n
            
    def addBox(self, bx):
        self.cells[self.index] = bx
        self.index = self.index + 1
        bx.setParent(self)
        if self.index==1:
            super(BoxBag, self).setBounds(bx) 
        else:
            super(BoxBag, self).setBounds(self.union(bx))
        self.preferredBounds = Rect(self.left, self.top, self.width, self.height)
        
    def setBorder(self, newVal):
        for i in range(self.index):
            self.getBox(i).setBorder(newVal)
            
    def getBox(self, id):
        if id<0 or id>=self.index:
            return None
        else:
            return self.cells[id]
        
    def getNumCells(self):
        return self.index
    
    def getBackgroundBox(self):
        return self.backgroundBox
    
    def getPreferredSize(self):
        return Dimension(self.preferredBounds.width, self.preferredBounds.height)
    
    def getScaledSize(self, scale):
        d=self.getPreferredSize()
        return Dimension((scale*d.w), (scale*d.h))
    
    def setVisible(self, newVal):
        for i in range(self.index):
            self.getBox(i).setVisible(newVal)
            
    def update(self, g2, io):
        if self.index==0 or not self.isVisible() or self.isTemporaryHidden():
            return False
        
        bx = None
        for i in range(self.index):
            bx = self.getBox(i)
            if not bx.isMarked():
                bx.update(g2, io)
        for i in range(self.index):
            bx = self.getBox(i)
            if bx.isMarked():
                bx.update(g2, io)
        return True
    
    def setBounds(self, r):     
        if  not(r.width<=0 or r.height<=0) and not r==self:
            scaleW = r.width/float(self.width)
            scaleH = r.height/float(self.height)
            dx = float(r.left)-float(self.x)
            dy = float(r.top) -float(self.y)
            for i in range(self.index):
                bx = self.getBox(i)
                p = Point(bx.x-self.x, bx.y-self.y)
                bx.setBounds(Rect(dx+self.x+scaleW*float(p.x), dy+self.y+scaleH*float(p.y), scaleW*float(bx.width), scaleH*float(bx.height) ))
        super(BoxBag, self).setBounds(r)
    
    def findBox(self, p):
        bx = None
        for i in range((self.index)-1, -1, -1):
            bx = self.getBox(i)
            if bx.isVisible() and bx.contains(p):
                return bx
        return None 
    
def layoutSingle(preferredMaxSize, rs, margin):
    d = rs.getPreferredSize()
    minSize = rs.getMinimumSize()
    maxSize = preferredMaxSize
    
    maxSize.w = maxSize.w - 2*margin
    maxSize.h = maxSize.h - 2*margin
    
    if minSize.w>maxSize.w or minSize.h>maxSize.h:
        maxSize = minSize
        
    scale = 1
    if d.w>maxSize.w:
        scale = float(maxSize.w)/float(d.w)
        
    if (scale * d.h) > maxSize.h:
        scale = float(maxSize.h) / float(d.h)
        
    d = rs.getScaledSize(scale)
    rs.setBounds(Rect(margin, margin, d.w, d.h))
    
    d.w= d.w + 2*margin
    d.h = d.h + 2*margin
    
    return d

def layoutDouble(desiredMaxSize, rsA, rsB, boxGridPos, margin):
        
    isHLayout = False
    nbh = 1
    nbv = 1
    
    if boxGridPos==Activity.AB or boxGridPos==Activity.BA:
        nbh=2
        nbv=1
        isHLayout=True
    elif boxGridPos==Activity.AUB or boxGridPos==Activity.BUA:
        nbh=1
        nbv=2
        isHLayout=False
    
    ra = rsA.getBounds()
    rb = rsB.getBounds()
    
    da=rsA.getPreferredSize()
    db=rsB.getPreferredSize()
    
    d = None
    if isHLayout:
        d = Dimension(da.w + db.w, max(da.h, db.h))
    else:
        d = Dimension(max(da.w,db.w), da.h + db.h)
    
    minSizeA=rsA.getMinimumSize()
    minSizeB=rsB.getMinimumSize()
    
    minSize = None
    if isHLayout:
        minSize = Dimension(minSizeA.w+minSizeB.w, max(minSizeA.h, minSizeB.h))
    else:
        minSize = Dimension(max(minSizeA.w, minSizeB.w), minSizeA.h + minSizeB.h)
        
    maxSize = desiredMaxSize
    maxSize.w = maxSize.w - (1+nbh) * margin
    maxSize.h = maxSize.h - (1+nbv) * margin
    
    if minSize.w>maxSize.w or minSize.h>maxSize.h:
        maxSize = Dimension(minSize.w, minSize.h)
       
    scale = 1
    
    if d.w>maxSize.w:
        scale = float(maxSize.w)/float(d.w)
        
    if (scale * d.h) > maxSize.h:
        scale = float(maxSize.h) / float(d.h)
        
    da=rsA.getScaledSize(scale)
    db=rsB.getScaledSize(scale)
    
    dah = -1
    dav = -1
    dbh = -1
    dbv = -1
    
    if db.w>da.w:
        dah = (db.w-da.w)/2
    else:
        dah = 0
    
    if da.w>db.w:
        dbh = (da.w-db.w)/2
    else:
        dbh = 0
        
    if db.h>da.h:
        dav = (db.h-da.h)/2
    else:
        dav = 0
    
    if da.h>db.h:
        dbv = (da.h-db.h)/2
    else:
        dbv = 0
        
    if boxGridPos==Activity.AB:
        rsA.setBounds(Rect(margin, margin+dav, da.w, da.h))
        rsB.setBounds(Rect(2*margin+da.w, margin+dbv, db.w, db.h))
    elif boxGridPos == Activity.BA:
        rsB.setBounds(Rect(margin, margin+dbv, db.w, db.h))
        rsA.setBounds(Rect(2*margin+db.w, margin+dav, da.w, da.h))
    elif boxGridPos == Activity.AUB:
        rsA.setBounds(Rect(margin+dah, margin, da.w, da.h))
        rsB.setBounds(Rect(margin+dbh, 2*margin+da.h, db.w, db.h))
    elif boxGridPos == Activity.BUA:
        rsB.setBounds(Rect(margin+dbh, margin, db.w, db.h))
        rsA.setBounds(Rect(margin+dah, 2*margin+db.h, da.w, da.h))
    else:
        rsA.setBounds(Rect(int(margin+scale*ra.getX()), int(margin+scale*ra.getY()), da.w, da.h))
        rsB.setBounds(Rect(int(margin+scale*rb.getX()), int(margin+scale*rb.getY()), da.w, da.h))  
    
    r = rsA.getBounds()
    r2 = r.union(rsB.getBounds())
    d.w = r2.w+2*margin
    d.h = r2.h+2*margin
    return d
        