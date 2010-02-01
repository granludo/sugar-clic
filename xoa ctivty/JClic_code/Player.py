"""
  <CODE>Player</CODE> is one of the the main classes of the JClic system. It implements the
  {@link edu.xtec.jclic.PlayStation} interface, so it can read and play JClic
  projects from files or streams. In order to allow activities to run,
  <CODE>Player</CODE> provides them of all the necessary resources: media bags
  (to load and realize images and other media contents), sequence control,
  report system management, user interface (loading and management of skins),
  display of system messages, etc.
  Player is also a {@link edu.xtec.jclic.RunnableComponent}, so it can be
  embedded in applets, frames and other containers.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from os import getcwd
from os.path import isdir
from os import mkdir
import pygame
from pygame import *
import xml.dom.minidom
from FileSystem import *
from JClicProject import getJClicProject
from Activity import getActivity
import pygame
from pygame import *
import ActiveBoxContent
from ActiveBox import *
from Point import *
from zipfile import ZipFile
from sugar.activity import activity
from FileChooser import *
from ConfigFile import projectPath
from ConfigFile import nextPath
from ConfigFile import previousPath
from ConfigFile import backgroundColor

class Player(object):
    
    project = None
    actPanel = None
    screen = None
    AC_MARGIN_Y = 30
    AC_MARGIN_X = 6
    ab = None
    messages = False
    next = None
    previous = None
    pointNext = None
    pointPrevious = None
    fileSystem = None
    bgImageOrigin = None
    
    def __init__(self):
        self.project = None 
        self.bgImageOrigin = Point()
 	pygame.init()
	self.screen = pygame.display.set_mode((1025, 693), 0, 32)
	self.load(projectPath, None, None, None)
 
    def read_file(self, filename):
	pygame.init()
	self.screen = pygame.display.set_mode((1200, 850), 0, 32)
        self.load(filename, None, None, None)
           
    def setProject(self, p):
        self.project = p
            
    def load(self, sFullPath, sSequence, sActivity, sAbe):
        
	fullPath = sFullPath
        sequence = sSequence
        act = None
        activityName = sActivity
        abe = sAbe
        thisPlayer = self
        actp = None
        
        #Step 1: load or create project and set a valid value for "sequence"
        if fullPath != None:
            if sequence == None:
                sequence = "0"
            projects = sFullPath.split("/")
            projectName = projects[-1]
            
            if(projectName[-6:] == ".jclic"):
                self.fileSystem = FileSystem(projects[1:-1], fullPath)
                doc = self.fileSystem.getXMLDocument(fullPath)
                self.setProject(getJClicProject((doc.documentElement), self.fileSystem, fullPath))
                
            elif projectName[-4:] == ".zip":
                unziped = ZipFile(fullPath, 'r')
                dir = fullPath[:-4]
                if not isdir(dir):
                    mkdir(dir)
                
                for file_path in unziped.namelist():
                    file_content = unziped.read(file_path)
                    f = open(dir + "/" + file_path, "w")
                    f.write(file_content)
                    f.close()
                    if file_path[-6:] == ".jclic":
                        directory_list = projects[1:-1] + [projects[-1][:-4]]
                        self.fileSystem = FileSystem(directory_list, fullPath[:-4] + "/" + file_path)
                        doc = self.fileSystem.getXMLDocument(f.name)
                        self.setProject(getJClicProject((doc.documentElement), self.fileSystem, fullPath))
                              
                
        #Step 2: load ActivitySequenceElement ase
        if sequence!=None:
            ase=self.project.activitySequence.getElementByTag(sequence, True)
            
            if ase == None:
                i = int(sequence)
                if i >=0:
                    ase=self.project.activitySequence.getElement(i, True)
            
            
            if ase!=None:
                activityName = ase.getActivityName()
        
        #step 3: load ActivityBagElement abe
        if activityName!=None:
            actName = activityName.encode("iso8859-1")
            abe=self.project.activityBag.getElement(actName)
        
        if abe.getClass()!="@puzzles.ExchangePuzzle" and abe.getClass()!="@puzzles.DoublePuzzle" and abe.getClass()!="@puzzles.HolePuzzle":
            self.nextActivity()
        
        #step 4: load Activity act
        if abe!=None:
            act=getActivity(abe.getData(), self.project )
        
        #step 5: Load activity carregar la activitat
        if act!=None:
            actp = act.getActivityPanel(self.screen, self)
            actp.buildVisualComponents()
            self.buildPlayer()
            self.actPanel = actp
            
        self.initActivity()
        
    def initActivity(self):
        self.actPanel.initActivity()
        self.doLayout() 
        self.repaint()
        
    def buildPlayer(self):
        self.ab = ActiveBox(None, None, 0, Rect(55, self.screen.get_height() - 25, self.screen.get_width() - 60, 20), None)
        
        next = pygame.image.load(nextPath).convert_alpha()
        previous = pygame.image.load(previousPath).convert_alpha()
        
        self.next = pygame.transform.scale(next, (20, 20))
        self.previous = pygame.transform.scale(previous, (20, 20))
        
    def doLayout(self):
        if self.actPanel!=None:
            bounds=Rect(0,0,self.screen.get_width(), self.screen.get_height())
            proposedRect=Rect(self.AC_MARGIN_X, self.AC_MARGIN_X, bounds.width-2*self.AC_MARGIN_X, bounds.height-self.AC_MARGIN_Y)
            if self.actPanel.bgImage!=None and self.actPanel.getActivity().tiledBgImg:
                self.bgImageOrigin.setX((self.screen.get_width()-self.actPanel.bgImage.get_width)/2)
                self.bgImageOrigin.setY((self.screen.get_height()-self.actPanel.bgImage.get_height)/2)
                if actPanel.getActivity().absolutePositioned:
                    proposedRect.x=self.bgImageOrigin.getX()
                    proposedRect.y=self.bgImageOrigin.getY()
                    proposedRect.width = proposedRect.width - (bgImageOrigin.getX()-AC_MARGIN)
                    proposedRect.height = proposedRect.height - (bgImageOrigin.getY()-AC_MARGIN)
                    proposedRect.width = min(proposedRect.width, bounds.width)
                    proposedRect.height= min(proposedRect.height, bounds.height)
            self.actPanel.fitTo(proposedRect, bounds)

    def setMsg(self, abc):
        if self.ab!=None:
            self.ab.clear()
            if abc == None:
                self.ab.setContent(ActiveBoxContent.getEmptyContent())
            else:
                self.ab.setContent1(abc)
                self.ab.setBoxBase(abc.bb)
                self.ab.setBorder(True)
            self.messages = True
            
    def paintButtons(self):
        self.pointPrevious = Point(5, self.screen.get_height()-self.previous.get_height()-5)
        self.pointNext = Point(5 + self.previous.get_width() + 5, self.screen.get_height()-self.next.get_height()-5)
        self.screen.blit(self.previous, (self.pointPrevious.getX(), self.pointPrevious.getY()))
        self.screen.blit(self.next, (self.pointNext.getX(), self.pointNext.getY()))
        
    def isOver(self, p, point, button):
        if point.getX() < p[0] < point.getX() + button.get_width() and point.getY() < p[1] < point.getY() + button.get_height(): 
            return True
        else:
            return False

    def repaint(self):
        going = True
        events = None
        while going:
            self.paintBackground()
            if self.messages:
                self.ab.update(self.screen, self)
            self.paintButtons()
            self.actPanel.repaint()
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    exit()
                p = pygame.mouse.get_pos()
                if event.type == MOUSEBUTTONDOWN:
                    if self.isOver(p, self.pointNext, self.next):
                        self.nextActivity()
                    elif self.isOver(p, self.pointPrevious, self.previous):
                        self.previousActivity()
                self.actPanel.processEvent(events)
            pygame.display.update()
            
    def paintBackground(self):
        self.screen.fill(backgroundColor)
            
    def nextActivity(self):
        self.project.activitySequence.currentAct = self.getNextExchangePuzzle()
        if self.project.activitySequence.currentAct == len(self.project.activitySequence.elements):
            self.project.activitySequence.currentAct = 0
        self.load(self.fileSystem.fullPath, self.project.activityBag.elementAt(self.project.activitySequence.currentAct).getName(), None, None)
        
    def previousActivity(self):
        self.project.activitySequence.currentAct = self.getPreviousExchangePuzzle()
        self.load(self.fileSystem.fullPath, self.project.activityBag.elementAt(self.project.activitySequence.currentAct).getName(), None, None)
        
    def getNextExchangePuzzle(self):
        if len(self.project.activityBag.elements)==1:
            return 0
        b = False
        i = self.project.activitySequence.currentAct
        while not b:    
            if i == len(self.project.activitySequence.elements):
                i = 0
                break
            elif (self.project.activityBag.elementAt(i).getClass()=="@puzzles.ExchangePuzzle" or self.project.activityBag.elementAt(i).getClass()=="@puzzles.DoublePuzzle" or self.project.activityBag.elementAt(i).getClass()=="@puzzles.HolePuzzle") and i!=self.project.activitySequence.currentAct:
                b = True
                break
            i = i + 1
        return i
    
    def getPreviousExchangePuzzle(self):
        if len(self.project.activityBag.elements)==1:
            return 0
        b = False
        i = self.project.activitySequence.currentAct
        i2 = i+1
        while not b and i!=i2:
            if i == -1:
                i = len(self.project.activitySequence.elements) - 1
            if (self.project.activityBag.elementAt(i).getClass()=="@puzzles.DoublePuzzle" or self.project.activityBag.elementAt(i).getClass()=="@puzzles.ExchangePuzzle" or self.project.activityBag.elementAt(i).getClass()=="@puzzles.HolePuzzle") and i!=self.project.activitySequence.currentAct:
                b = True
                break
            i = i - 1
        return i

if __name__=="__main__":
    p = Player()
