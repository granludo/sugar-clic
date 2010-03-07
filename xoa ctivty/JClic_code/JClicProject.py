"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from ActivityBag import *
from ActivitySequence import *
from ActivitySequenceElement import *
from MediaBag import *
from xml.dom.minidom import *
from JDomUtility import checkName
from JDomUtility import getStringAttr
from ProjectSettings import *

class JClicProject(object):
    
    name = ""
    version = ""
    code = ""
    type = ""
    fileSystem = None
    activityBag = None
    activitySequence = None
    mediaBag = None
    fullPath = ""
    Document = None
    settings = ""
    
    ELEMENT_NAME="JClicProject"
    VERSION="version" 
    NAME="name"
    CODE="code"
    TYPE="type"
    
    def __init__(self, e, fileSystem, fullPath):
        self.Document = e
        self.fileSystem = fileSystem
        self.fullPath = fullPath
        
        self.activityBag = ActivityBag(self);
        self.activitySequence = ActivitySequence(self);
        self.mediaBag = MediaBag(self)
    
    def getFileSystem(self):
        return self.fileSystem
    
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        
        self.name=getStringAttr(e, self.NAME, self.name, False);
        self.version=getStringAttr(e, self.VERSION, self.version, False);
        self.type=getStringAttr(e, self.TYPE, self.type, False);
        self.code=getStringAttr(e, self.CODE, self.code, False);
        
        child = e.getElementsByTagName(ProjectSettings.ELEMENT_NAME)
        if child!=[]:
            self.settings=getProjectSettings(child[0])           
        

        child = e.getElementsByTagName(ActivitySequence.ELEMENT_NAME)
        if(child!=[]):
            self.activitySequence.setProperties(child[0], None)
        child = e.getElementsByTagName(ActivityBag.ELEMENT_NAME)
        if(child!=[]):
            self.activityBag.setProperties(child[0], None)
        child = e.getElementsByTagName(MediaBag.ELEMENT_NAME)
        if(child!=[]):
            self.mediaBag.setProperties(child[0], None)
            
def getJClicProject(e, fs, fullPath):
    jcp= JClicProject(e, fs, fullPath)
    jcp.setProperties(e, None)
    return jcp
    
    