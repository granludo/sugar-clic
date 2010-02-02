"""
  This class stores and manages all the media components (images, sounds, animations,
  video, MIDI files, etc.) needed to run the activities of a
  {@link edu.xtec.jclic.project.JClicProject}. The main member of the class is a
  {@link java.util.Vector} that stores {@link edu.xtec.jclic.bags.MediaBagElement}
  objects. It defines also a {@link edu.xtec.jclic.bags.MediaBag.Listener} interface
  to allow other objects to be informed about changes in the media collection.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from copy import deepcopy
from MediaBagElement import *

class MediaBag(object):
    
    project = None
    elements = []
    
    ELEMENT_NAME="mediaBag"
    
    def __init__(self, project):
        self.project = project
        self.elements = []
        
    def getProject(self):
        return self.project 
    
    def getElements(self):
        v = deepcopy(self.elements)
        return v
    
    def setProperties(self, e, aux):        
        llista = e.getElementsByTagName(MediaBagElement.ELEMENT_NAME)
        for node in llista:
                self.elements.append(getMediaBagElement(node))
                
    def getImageElement(self, name):
        result = None
        result = self.registerElement(name, None)
        if result!=None:
            result.prepareImage(self.project.getFileSystem())
            return result
        
    def registerElement(self, name, fileName):
        result= self.getElement(name)
        if result==None:
            if fileName==None:
                result = MediaBagElement(name, None, name)
            else:
                result = MediaBagElement(fileName, None, fileName)
            self.elements.append(result)
        return result
    
    def getElement(self, name):
        result=None
        if name!=None:
            for i in range(len(self.elements)):
                mbe=self.elements[i]
                if name == mbe.getName():
                    result=mbe
                    break
        return result
        
        
    