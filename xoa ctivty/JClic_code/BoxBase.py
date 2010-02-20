"""
  This class contains all the main visual attributes needed to draw
  {@link edu.xtec.jclic.boxes.AbstractBox} objects: background and foreground color
  and gradient, colors for special states (inactive, alternative, disabled...),
  mrgins, fonts, strokes for borders, etc. Objects derived from <CODE>AbstractBox</CODE>
  can have inheritance: boxes that act as "containers" of other boxes
  (like {@link edu.xtec.jclic.boxes.BoxBag}). Most of the attributes of <CODE>BoxBase</CODE>
  can be <I>null</I>, meaning that the value of the ancestor, or a default value
  if the box has no ancestors, must be taken.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import pygame
from pygame import display
from pygame.color import *
from pygame.font import *
from JDomUtility import checkName
from JDomUtility import elementToFont
from JDomUtility import FONT
from JDomUtility import getColorAttr
from JDomUtility import getBoolAttr
from JDomUtility import getIntAttr

class BoxBase (object):
    
    font = None
    originalFont = None
    dynFontSize = -1.0
    backColor = None
    bgGradient = None
    textColor = None
    shadowColor = None
    inactiveColor = None
    alternativeColor = None
    borderColor = None
    shadow = False
    transparent = False
    textMargin = -1
    resetFontCounter=-1
    resetAllFontsCounter=0
    borderStroke = None
    markerStroke = None
    flagFontReduced=False
    
    REDUCE_FONT_STEP=1
    MIN_FONT_SIZE=8
    DEFAULT_BACK_COLOR=THECOLORS["lightgray"]
    DEFAULT_TEXT_COLOR=THECOLORS["black"]
    DEFAULT_SHADOW_COLOR=THECOLORS["gray"]
    DEFAULT_INACTIVE_COLOR=THECOLORS["gray"]
    DEFAULT_ALTERNATIVE_COLOR=THECOLORS["gray"]
    DEFAULT_BORDER_COLOR=THECOLORS["black"]
    DEFAULT_BORDER_STROKE_WIDTH=0.75
    DEFAULT_MARKER_STROKE_WIDTH=2.75
    DEFAULT_FONT=None
    
    AC_MARGIN=6
    
    COLOR = "color"
    FOREGROUND="foreground"
    BACKGROUND="background"
    SHADOW="shadow"
    INACTIVE="inactive"
    ALTERNATIVE="alternative"
    BORDER="border"
    TRANSPARENT = "transparent"
    MARGIN="margin"
    BORDER_STROKE="borderStroke"
    MARKER_STROKE="markerStroke"
    ELEMENT_NAME = "style"
    
    def __init__(self):
        self.setFont(self.getDefaultFont());
        self.dynFontSize=self.font.get_height()
        self.backColor=self.DEFAULT_BACK_COLOR
        self.bgGradient=None
        self.textColor=self.DEFAULT_TEXT_COLOR
        self.shadowColor=self.DEFAULT_SHADOW_COLOR
        self.inactiveColor=self.DEFAULT_INACTIVE_COLOR
        self.alternativeColor=self.DEFAULT_ALTERNATIVE_COLOR
        self.borderColor=self.DEFAULT_BORDER_COLOR
        self.shadow=False
        self.transparent=False
        self.textMargin=self.AC_MARGIN
        self.resetFontCounter=self.resetAllFontsCounter
        self.borderStroke=self.DEFAULT_BORDER_STROKE_WIDTH
        self.markerStroke=self.DEFAULT_MARKER_STROKE_WIDTH
        
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        child = None
        s = ""
        
        child = e.getElementsByTagName(FONT)
        if child!=[]:
            self.setFont(elementToFont(child[0]))
        child = e.getElementsByTagName(self.COLOR)
        if child!=[]:
            self.textColor=getColorAttr(child[0], self.FOREGROUND, self.textColor)
            self.backColor=getColorAttr(child[0], self.BACKGROUND, self.backColor)
            self.shadowColor=getColorAttr(child[0], self.SHADOW, self.shadowColor)
            self.inactiveColor=getColorAttr(child[0], self.INACTIVE, self.inactiveColor)
            self.alternativeColor=getColorAttr(child[0], self.ALTERNATIVE, self.alternativeColor)
            self.borderColor=getColorAttr(child[0], self.BORDER, self.borderColor)
        self.shadow=getBoolAttr(e, self.SHADOW, self.shadow);
        self.transparent=getBoolAttr(e, self.TRANSPARENT, self.transparent);
        self.textMargin=getIntAttr(e, self.MARGIN, self.textMargin);
        
        s = e.getAttribute(self.BORDER_STROKE)
        if s!="":
            self.setBorderWidth(float(s))
            
        s = e.getAttribute(self.MARKER_STROKE)
        if s!="":
            self.setMarkerWidth(float(s))
           
    def setMarkerWidth(self, w):
        self.markerStroke = w
            
    def setBorderWidth(self, w):
        self.borderStroke = w
    
    def setFont(self, newFont):
        if newFont!=None:
            self.font = newFont
            self.dynFontSize=self.font.get_height()
            self.originalFont=self.font
    
    def getDefaultFont(self):
        if self.DEFAULT_FONT==None:
            self.DEFAULT_FONT= pygame.font.SysFont("arial",17)
        return self.DEFAULT_FONT
               
def getBoxBase(e):
    bb = BoxBase()
    bb.setProperties(e, None)
    return bb