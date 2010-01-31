"""
  <CODE>MediaBagElements</CODE> are the members of {@link edu.xtec.jclic.bags.MediaBag}
  objects. Media elements have a name, a reference to a file (the <CODE>fileName</CODE>)
  and, when initialized, a <CODE>data</CODE> field containing the raw content of
  the media. They have also a flag indicating if the data must be saved into the
  {@link edu.xtec.jclic.project.JClicProject} file or must be mantained as a single
  reference to a external file.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from JDomUtility import checkName
from JDomUtility import getBoolAttr
from JDomUtility import getStringAttr
from JDomUtility import getIntAttr
import pygame

class MediaBagElement(object):
    
    ELEMENT_NAME="media"
    FILE="file" 
    NAME="name" 
    SAVE="save" 
    USAGE="usage"
    name = ""
    fileName=""
    animated = False
    usageCount=0
    saveFlag=True
    data=None
        
    def __init__(self, fileName, data, name):
        self.setName(name)
        self.setFileName(fileName)
        self.setData(data)
        self.usageCount=0
        self.animated=False
        self.saveFlag=True
        
    def setName(self, name):
        self.name= name
    
    def setFileName(self, fileName):
        self.fileName=fileName
        self.data = None
        self.animated = False
        
    def setData(self, data):
        self.data=data
        self.animated=False
        
    def getName(self):
        return self.name
    
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        self.setName(getStringAttr(e, self.NAME, self.name, False))
        self.setFileName(getStringAttr(e, self.FILE, self.fileName, False))
        self.saveFlag=getBoolAttr(e, self.SAVE, True)
        self.usageCount=getIntAttr(e, self.USAGE, self.usageCount)
        
    def prepareImage(self, fileSystem):
        b = False
        if self.isImage():
            if self.data==None:
                self.data = pygame.image.load(fileSystem.getPath() + self.fileName)
            b = True
        return b
    
    def getImage(self):
        if self.data==None:
            return None
        else:
            return self.data
    
    def isImage(self):
        if self.fileName.lower().endswith("jpg") or self.fileName.lower().endswith("gif") or self.fileName.lower().endswith("png"):
            return True
        else:
            return False
    
def getMediaBagElement(e):
    mb = MediaBagElement("NONAME", None, "NONAME")
    mb.setProperties(e, None)
    return mb