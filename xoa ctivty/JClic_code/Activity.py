"""
  <CODE>Activity</CODE> is the abstract base class for JClic activities. It
  defines also the inner class {@link edu.xtec.jclic.Activity.Panel}, wich is
  responsible of the user interaction with the activity content.
  Activities should extend both <CODE>Activity</CODE> and
  <CODE>Activity.Panel</CODE> classes in order to become fully operative.
  JClic stores activities in memory as {@link org.JDom.Element} objects. So,
  all non-transient data must be stored to and retrieved from JDom elements.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
import pygame
from pygame import Color
from Point import *
from Dimension import *
from pygame.locals import *
from math import *
from JDomUtility import getClassName
from JDomUtility import checkName
from JDomUtility import getStringAttr
from JDomUtility import getParagraphs
from JDomUtility import getStrIndexAttr
from JDomUtility import getIntAttr
from JDomUtility import getColorAttr
from JDomUtility import getPointAttr
from ActiveBoxContent import *
from time import sleep

BASE_CLASS_TAG="@"

class Activity(object):

    DEFAULT_BG_COLOR=Color("0xBEBEBE")
    DEFAULT_WIDTH=400
    DEFAULT_HEIGHT=300
    MINIMUM_WIDTH=40
    MINIMUM_HEIGHT=40
    DEFAULT_NAME="---"
    DEFAULT_MARGIN=8
    DEFAULT_SHUFFLES=31
    DEFAULT_GRID_ELEMENT_SIZE=20
    ELEMENT_NAME="activity"
    PREVIOUS = 0
    MAIN = 1
    NUM_MSG = 4
    END = 2
    
    project = None  
    name = DEFAULT_NAME
    code = ""
    description = ""
    margin = DEFAULT_MARGIN
    bgColor= None
    origin = None
    d = None
    tiledBgImg = False
    bgImageFile = ""
    border = True
    absolutePositioned = False
    absolutePosition = Point(0, 0)
    includeInReports = True
    reportActions = False
    helpWindow = False
    showSolution = False
    helpMsg = ""
    useOrder = False
    dragCells = False
    skinFileName = ""
    maxTime = 0
    countDownTime = False
    maxActions = 0
    countDownActions = False
    infoUrl = ""
    infoCmd = ""
    
    messages = [""] * NUM_MSG
    bTimeCounter = True
    bScoreCounter = True
    bActionsCounter = True
    windowSize = Dimension(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    transparentBg = False
    activityBgColor = DEFAULT_BG_COLOR
    shuffles = DEFAULT_SHUFFLES
    acp = None
    
    boxGridPos = -1
    
    AB=0
    BA=1
    AUB=2
    BUA=3
   
    NAME="name"
    BASE_CLASS="edu.xtec.jclic.activities."
    ID="id"
    CODE="code"
    DESCRIPTION="description"
    MESSAGES="messages"
    TYPE="type"
    PREVIOUS="previous"
    INITIAL="initial"
    FINAL="final"
    FINAL_ERROR="finalError"
    SETTINGS="settings"
    LAYOUT="layout"
    MARGIN="margin"
    CONTAINER="container"
    BGCOLOR="bgColor"
    IMAGE="image"
    TILED="tiled"
    COUNTERS="counters"
    TIME="time"
    ACTIONS="actions"
    SCORE="score"
    WINDOW="window"
    TRANSPARENT="transparent"
    BORDER="border"
    POSITION="position"
    X="x"
    Y="y"
    SIZE="size"
    WIDTH="width"
    HEIGHT="height"
    PRIMARY="primary"
    SECONDARY="secondary"
    SOLVED_PRIMARY="solvedPrimary"
    SOLVED_SECONDARY="solved_secondary"
    GRID="grid"
    ROW="row"
    CLUES="clues"
    CLUE="clue"
    RANDOM_CHARS="random_chars"
    SCRAMBLE="scramble"
    TIMES="times"
    REPORT="report"
    REPORT_ACTIONS="reportActions"
    HELP_WINDOW="helpWindow"
    HELP_SHOW_SOLUTION="showSolution"
    USE_ORDER="useOrder"
    DRAG_CELLS="dragCells"
    SKIN="skin"
    FILE="file"
    MAX_TIME="maxTime"
    COUNT_DOWN_TIME="countDownTime"
    MAX_ACTIONS="maxActions"
    COUNT_DOWN_ACTIONS="countDownActions"
    INFO_URL="infoUrl"
    INFO_CMD="infoCmd"
    MSG_TYPE=["previous", "initial", "final", "finalError"]
    LAYOUT_NAMES=["AB", "BA", "AUB", "BUA"]
    
    abc = [] 

    def __init__(self, project):
        self.project=project
        
    def initNew(self):
        self.name=self.project.getBridge().getMsg("UNNAMED")
       
    def getPublicName(self):
        return self.name
    
    def getProject(self):
        return self.project
    
    def setProperties(self, e, aux):     
        child = child2 = child3 = None
        
        checkName(e, self.ELEMENT_NAME)
        
        self.name=getStringAttr(e, self.NAME, self.name, False)
        self.code=getStringAttr(e, self.CODE, self.code, False)
        
        child = e.getElementsByTagName(self.DESCRIPTION) 
        if(child != []):
            self.description = getParagraphs(child[0])
        
        child= e.getElementsByTagName(self.MESSAGES)
        if(child != []):
            child2 = child[0].getElementsByTagName(ActiveBoxContent.ELEMENT_NAME)
            for x in child2: 
                i = getStrIndexAttr(x.getAttribute(self.TYPE), self.MSG_TYPE, -1) 
                if(i >= 0):
                    self.messages[i]=getActiveBoxContent(x, self.project.mediaBag)
                         
        child = e.getElementsByTagName(self.SETTINGS)
        if(child != []):
            self.margin = getIntAttr(child[0], self.MARGIN, self.margin)
            self.infoUrl = getStringAttr(child[0], self.INFO_URL, self.infoUrl, False)
            if(self.infoUrl == None):
                self.infoCmd = getStringAttr(child[0], self.INFO_CMD, self.infoCmd, False)
            self.useOrder = getBoolAttr(child[0], self.USE_ORDER, self.useOrder)
            self.dragCells = getBoolAttr(child[0], self.DRAG_CELLS, self.dragCells)
            self.maxTime = getIntAttr(child[0], self.MAX_TIME, self.maxTime)
            if(self.maxTime > 0):
                self.countDownTime = getBoolAttr(child[0], self.COUNT_DOWN_TIME, self.countDownTime)
            self.maxActions = getIntAttr(child[0], self.MAX_ACTIONS, self.maxActions)
            if(self.maxActions>0):
                self.countDownActions = getBoolAttr(child[0], self.COUNT_DOWN_ACTIONS, self.countDownActions)
            self.includeInReports = getBoolAttr(child[0], self.REPORT, self.includeInReports)
            if(self.includeInReports):
                self.reportActions=getBoolAttr(child[0], self.REPORT_ACTIONS, self.reportActions);
            else: 
                self.reportActions = False
                
            child2 = child[0].getElementsByTagName(self.HELP_WINDOW)
            if(child2 != []):
                if(self.helpSolutionAllowed()):
                    self.showSolution = getBoolAttr(child2[0], self.HELP_SHOW_SOLUTION, self.showSolution)
                if(not self.showSolution):
                    self.helpMsg = getParagraphs(child2[0])
                self.helpWindow = self.helpMsg != None or self.showSolution
            
            child2 = child[0].getElementsByTagName(self.CONTAINER)    
            if(child2 != []):
                self.bgColor=getColorAttr(child2[0], self.BGCOLOR, self.bgColor)
                
                child3 = child2[0].getElementsByTagName(self.IMAGE)
                if(child3 != []):
                    self.bgImageFile = child3[0].getAttribute(self.NAME)
                    self.tiledBgImg=getBoolAttr(child3[0], self.TILED, self.tiledBgImg) 
                child3=child2[0].getElementsByTagName(self.COUNTERS)
                if(child3 != []):
                    self.bTimeCounter=getBoolAttr(child3[0], self.TIME, self.bTimeCounter)
                    self.bActionsCounter=getBoolAttr(child3[0], self.ACTIONS, self.bActionsCounter)
                    self.bScoreCounter=getBoolAttr(child3[0], self.SCORE, self.bScoreCounter)
            
            child2 = child[0].getElementsByTagName(self.WINDOW)          
            if(child2 != []):
                self.activityBgColor=getColorAttr(child2[0], self.BGCOLOR, self.activityBgColor)
                self.transparentBg=getBoolAttr(child2[0], self.TRANSPARENT, self.transparentBg)
                self.border=getBoolAttr(child2[0], self.BORDER, self.border)
                
                child3 = child2[0].getElementsByTagName(self.POSITION)    
                if(child3 != []):
                    self.absolutePositioned=True
                    self.absolutePosition=getPointAttr(child3[0], self.X, self.Y, self.absolutePosition)
                child3 = child2[0].getElementsByTagName(self.SIZE)    
                if(child3 != []):
                    self.windowSize=getDimensionAttr(child3[0], self.WIDTH, self.HEIGHT, self.windowSize)
  
    def innerListReferences(self, e, map):    
        child = None
        
        child = e.getElementsByTagName(self, ActiveBoxContent.ELEMENT_NAME)
        for x in child:
            ActiveBoxContent.listReferences(x, map)
        
        x = e._get_ChildNodes()
        for y in x:      
            if(ActiveBoxContent.ELEMENT_NAME != y._get_localName()):
                self.innerListReferences(y, map)
            
    def listReferences(self, e, map):
        child,child2,child3 = None
        
        child = e.getElementsByTagName(self, self.MESSAGES)
        if(child != None):
            child2 = child.getElementsByTagName(self, ActiveBoxContent.ELEMENT_NAME)
            for x in child2:
                ActiveBoxContent.listReferences(x, map)
        
        child = e.getElementsByTagName(self, self.SETTINGS)
        if(child != None):
            child2 = child.getElementsByTagName(self, self.CONTAINER)
            if(child2 != None):
                child3 = child2.getElementsByTagName(self, self.IMAGE)
                if(child3 != None):
                    map[child3.getAttribute(self.NAME)] = Constants.MEDIA_OBJECT
        
        child = e.getElementsByTagName(self, ActiveBoxContent.ELEMENT_NAME)
        for x in child:
            ActiveBagContent.listReferences(x, map)
        
        child = e.getElementsByTagName(self, "document")
        if(child != None):
            self.innerListReferences(child, map)
    
    def getMessages(self):
        return self.messages
    
    def helpSolutionAllowed(self):
        return False
    
    def initAutoContentProvider(self):
        if(self.acp != None):
            self.acp.init(project.getBridge(), project.getFileSystem())
            return
        
    def prepareMedia(self, ps):
        for i in range(self.NUM_MSG):
            if(self.messages[i] != None):
                self.messages[i].prepareMedia(ps)
        if(self.abc != None):
            for i in range(len(self.abc)):
                if(self.abc[i] != None):
                    self.abc[i].prepareMedia(ps)
        return True
    
    def getActivity2(self):
        return self
    
    def helpWindowAllowed(self):
        return self.helpWindow and ((self.helpSolutionAllowed() and self.showSolution) or self.helpMsg != None)
    
    def canReinit(self):
        return True
    
    def hasInfo(self):
        return((self.infoUrl != None and len(self.infoUrl) > 0) or (self.infoCmd != None and len(self.infoCmd) > 0))
    
    def hasRandom(self):
        return False
    
    def shuffleAlways(self):
        return False
    
    def end(self):
        self.clear()
    
    def clear(self):
        return
    
    def finalize(self):
        self.end()
        
    def getWindowSize(self):
        return Dimension(self.windowSize.w, self.windowSize.h)
    
    def setWindowSize(self, windowSizeW, windowSizeH):
        self.windowSize = Dimension(windowSizeW, windowSizeH)
    
    class Panel(object):
        
        solved = False
        bgImage = None
        playing = False
        firstRun = True
        currentItem = 0
        bc = None
        ps = None
        screen = None
        abc = None
        margin = None
        activity = None
        panelDim = None
        imageDim = None
        
        def __init__(self, screen, activity, ps):
            
            self.abc = activity.abc
            self.ps = ps
            self.margin = activity.margin
            self.screen = screen
            self.activity = activity
            
        def getActivity(self):
            return self.activity
       
        def getPs(self):
            return self.ps
        
        def buildVisualComponents(self):
            self.playing = False
            
            self.bgImage = None 
            if self.activity.bgImageFile !="" and len(self.activity.bgImageFile) > 0:
                mbe = self.activity.project.mediaBag.getImageElement(self.activity.bgImageFile)
                self.bgImage = mbe.getImage()
                self.bgImageFile = mbe.getName()
                
        def enableCounters(self):
            self.enableCounters_1(self.bTimeCounter, self.bScoreCounter, self.bActionsCounter)
        
        def enableCounters_1(self, eTime, eScore, eActions):
            self.ps.setCounterEnabled(self.TIME_COUNTER, eTime)
            if(self.countDownTime):
                self.ps.setCountDown(self.TIME_COUNTER, self.maxTime)
            self.ps.setCounterEnabled(self.SCORE_COUNTER, eScore)
            self.ps.setCounterEnabled(self.ACTIONS_COUNTER, eActions)
            if(self.countDownActions):
                self.ps.setCountDown(self.ACTIONS_COUNTER, self.maxActions)    
            
        def initActivity(self):
            if(self.playing):
                self.playing = False
            
        def startActivity(self):
            return
        
        def showHelp(self):
            return
        
        def processMouse(self, e):
            return
        
        def processKey(self, e):
            return
        
        def isPlaying(self):
            return self.playing
        
        def fitTo(self, proposed, bounds):
            self.origin = Point(0,0)
            if self.activity.absolutePositioned == True and self.activity.absolutePosition != None:
                self.origin.x = max(0, self.activity.absolutePosition.x+proposed.x)
                self.origin.y = max(0, self.activity.absolutePosition.y+proposed.y)
                proposed.width = proposed.width - self.activity.absolutePosition.x
                proposed.height = proposed.height - self.activity.absolutePosition.y
            self.d = Dimension(max(2*self.margin+self.activity.MINIMUM_WIDTH,proposed.width),max(2*self.margin+self.activity.MINIMUM_HEIGHT,proposed.height))
            self.d = self.setDimension(self.d)
            
            if not self.activity.absolutePositioned:
                self.origin.setLocation(Point(max(0, proposed.x+(proposed.w-self.d.w)/2), max(0, proposed.y+(proposed.h-self.d.h)/2)))
            if self.origin.x+self.d.w > bounds.width:
                self.origin.x = max(0, bounds.width-self.d.w)
            if self.origin.y+self.d.h > bounds.height:
                self.origin.y = max(0, bounds.height-self.d.h)
           
        def setAndPlayMsg(self, msgCode):
            self.ps.setMsg(self.activity.messages[msgCode])
            
        def forceFinishActivity(self):
            return
                    
        def end(self):
            self.forceFinishActivity()
            if(self.playing == True):
                if(self.bc != None):
                    self.bc.end()
                self.ps.reportEndActivity(Activity.this, self.solved)
                self.playing = False
                self.solved = False
            self.clear()
            
        def finalize(self):
            self.end()
      
        def shuffle(self, bg, visible, fitInArea):
            steps=self.activity.shuffles
            
            i=self.activity.shuffles
            while i>0:
                k = i     
                for j in range(len(bg)):
                    if bg[j]!=None:
                        bg[j].scrambleCells(k, fitInArea);
                i= i-steps
                
        def repaint(self):
            panel = self.screen.subsurface(Rect(self.origin.x, self.origin.y, self.d.w, self.d.h))
            r = Rect(6, 6, self.screen.get_width()-12, self.screen.get_height()-6-30)
            panelSurface = self.screen.subsurface(r)
            panelSurface.fill(self.activity.bgColor)
            if self.bgImage!=None:
                self.panelDim = Dimension(panelSurface.get_width(), panelSurface.get_height())
                self.imageDim = Dimension(self.bgImage.get_width(), self.bgImage.get_height())
                self.screen.blit(self.bgImage, (self.panelDim.getW()/2 - self.imageDim.getW()/2, self.panelDim.getH()/2 - self.imageDim.getH()/2))
                panel = self.bgImage.subsurface(Rect(self.origin.x, self.origin.y, self.d.w, self.d.h))
                panel.fill(self.activity.activityBgColor)
            pygame.draw.rect(self.screen, (0,0,0), r, 1) 
            self.render(panel)
            
        def processEvent(self, events):
            for e in events:
                if self.playing and (e.type == MOUSEMOTION or e.type==MOUSEBUTTONDOWN):
   
                    if self.playing:
                        self.processMouse(e)
    
        def finishActivity(self, result):
            self.playing=False
            self.solved=result
            
            if self.bc!=None:
                self.bc.end()
            
            if result:
                self.setAndPlayMsg(self.activity.END)
                
            else:
                mostrar_missatge_error = ""
                self.setAndPlayMsg(END_ERROR)
          
def getActivity(o, project):
    act = None
    e = None
    className = ""
    
    if isinstance(o, Element):
        e = o 
        checkName(e, Activity.ELEMENT_NAME)
        className=getClassName(e)
    elif isinstance(o, str):
        className = o
    else:
        raise SyntaxError, "Unknown data!"
    
    activityClass = None
    con = None
    cparams = [] 
    initArgs = project
    if(className.startswith(BASE_CLASS_TAG)):
        className = className[1:].encode("iso8859-1")
        nom = className.split(".")
        className = nom[1]
    module = __import__(className)
    activityClass = getattr(module,className)
    act = Activity.__new__(activityClass)
    act.__init__(initArgs)
    if(e != None):
        act.setProperties(e, None)
    else:
        act.initNew()
    return act
