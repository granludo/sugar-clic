"""
  Objects of this class are widely used in JClic activities: cells in puzzles and
  associations, messages and other objects are active boxes. The specific
  content, size and location of <CODE>ActiveBox</CODE> is determined by its
  {@link edu.xtec.jclic.boxes.ActveBoxContent} members. Most ActiveBoxes have only
  one content, but some of them can have a secondary or "alternative" content, indicated
  by the <CODE>altContent</CODE> member. This content is used only when the <CODE>alternative</CODE>
  flag of the <CODE>ActiveBox</CODE> is on.
  Active boxes can host video and interactive media content (specified in the mediaContent member of
  the {@link edu.xtec.jclic.boxes.ActiveBoxContent}) through the <CODE>hostedMediaPlayer</CODE> member.
  @author Francesc Busquets (fbusquets@xtec.net)
"""

from AbstractBox import *
import pygame
from ActiveBoxContent import *

class ActiveBox(AbstractBox):
    
    idLoc = None
    idOrder = None
    idAss = None
    hasHostedComponent = False
    content = None
    altContent = None
    hostedMediaPlayer = None
    
    def __init__(self, parent, container, setIdLoc, r= None, boxBase=None):
        super(ActiveBox, self).__init__(parent, container, boxBase)
        self.clear()
        self.idLoc=setIdLoc
        if r!=None:
            self.setBounds(r)
        
    def copyContent(self, bx):
        self.idOrder=bx.idOrder
        self.idAss=bx.idAss
        self.content=bx.content
        self.altContent=bx.altContent
        
        if self.content!=None:
            if self.content.bb!=None:
                self.setBoxBase(self.content.bb)
            if self.content.border!=None and bx.hasBorder()!=self.content.border:
                setBorder(self.content.border)
                
        self.setInactive(bx.isInactive())
        self.setInverted(bx.isInverted())
        self.setAlternative(bx.isAlternative())
        
    def clear(self):
        self.content = None
        self.altContent = None
        self.idOrder = -1
        self.setInactive(True)

    def setBounds(self, r):
        super(ActiveBox, self).setBounds(r)

    def setContent1(self, abc):
        self.content = abc
        if self.content != None:
            if self.content.bb!=self.getBoxBaseX():
                self.setBoxBase(self.content.bb)
            if self.content.border!=None and self.hasBorder()!=self.content.border:
                self.setBorder(self.content.border)
            self.setInactive(False)
        else:
            self.clear()

    def setContent(self, abc, i):
        if i<0:
            i = self.idOrder
        if abc==None or i>=abc.getNumCells():
            return 
        if abc.bb!=self.getBoxBaseX():
            self.setBoxBase(abc.bb)
        self.setContent1(abc.getActiveBoxContent(i))
        
    def setAltContent(self, abc, i):
        if i<0: 
            i=self.idOrder
        if abc==None or abc.isEmpty() or i>abc.getNumCells(): 
            return
        self.setAltContent1(abc.getActiveBoxContent(i))
        
    def setAltContent1(self, abc):
        self.altContent=abc

    def getCurrentContent(self):
        if self.isAlternative():
            return self.altContent
        else:
            return self.content
        
    def isAtPlace(self):
        return self.idOrder==self.idLoc
    
    def isEquivalent(self, bx, checkCase):
        return bx!=None and self.content!=None and self.content.isEquivalent(bx.content, checkCase)
        
    def exchangeLocation(self, bx):
        pt = Point(self.x, self.y)
        idLoc0 = self.idLoc
        self.setLocation(bx.getLocation().getX(),bx.getLocation().getY())
        bx.setLocation(pt.getX(), pt.getY())
        self.idLoc = bx.idLoc
        bx.idLoc = idLoc0

    def updateContent(self, g2, io):
        
        abc = self.getCurrentContent()
        bb = self.getBoxBaseResolve()
        
        if self.isInactive() or abc==None or self.width<2 or self.height<2:
            return True
        
        if abc.img!=None:
            if abc.imgClip!=None:
                r = Rect(self.getBounds(abc))
                surf1 = abc.img.subsurface(r)
                surf1 = pygame.transform.scale(surf1, (self.width, self.height))
                g2.blit(surf1, (self.x, self.y))
        
        if abc.text!=None:
            text_surface = bb.font.render(abc.text, True, bb.textColor)
            if text_surface.get_width()>=self.width-4:
                text_surface = pygame.transform.scale(text_surface, (self.width-4, text_surface.get_height()))
            g2.blit(text_surface,(self.centerx - text_surface.get_width()/2,self.centery-text_surface.get_height()/2))
            
    def getBounds(self, abc):
        minx = 400000000
        maxx = -1
        miny = 400000000
        maxy = -1
        for i in range(len(abc.imgClip)):
            if abc.imgClip[i]==None:
                break
            if (abc.imgClip[i])[1]<minx:
                minx = (abc.imgClip[i])[1]
            if (abc.imgClip[i])[1]>maxx:
                maxx = (abc.imgClip[i])[1]
            if (abc.imgClip[i])[2]<miny:
                miny = (abc.imgClip[i])[2]
            if (abc.imgClip[i])[2]>maxy:
                maxy = (abc.imgClip[i])[2]
        return (minx, miny, maxx-minx, maxy-miny)
    
    def getContent(self):
        if self.content==None:
            self.setContent1(ActiveBoxContent())
        return self.content
    
    def exchangeContent(self, bx):
        bx0=ActiveBox(self.getParent(), self.getContainerX(), self.getBoxBaseX())
        bx0.copyContent(self)
        self.copyContent(bx)
        bx.copyContent(bx0)
            
        
        