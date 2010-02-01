"""
  This class stores the complete collection of activities of a {@link edu.xtec.jclic.project.JClicProject}.
  The collection is managed through a private {@link java.util.Vector} of objects
  of type {@link edu.xtec.jclic.bags.ActivityBagElement}.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from Activity import *
from ActivityBagElement import *

class ActivityBag(object):
    
    project = None
    elements = []
    ACTIVITY_ELEMENT_NAME = "activity"
    ELEMENT_NAME="activities"
    
    def __init__(self, project):
        self.project = project
        self.elements = []
    
    def getProject(self):
        return project
    
    def addElement(self, el):
        self.elements.append(el)
    
    def getElement(self, name):
        abe=self.getElementByName(name)
        return abe
    
    def getElementByName(self, name):
        i=self.getElementIndex(name)
        if i>=0:
            return self.elementAt(i)
        else:
            return None 
        
    def getElementIndex(self, name):
        result=-1
        for i in range(self.size()):
            if self.elementAt(i).getName().encode("iso8859-1") == name:
                result=i
                break
        return result
    
    def size(self):
        return len(self.elements)
    
    def elementAt(self, index):
        return self.elements[index]
    
    def addJDomElement(self, e):
        if e!=None:
            abe = self.getElementByName(e.getAttribute(Activity.NAME))
            if abe!=None:
                abe.setData(e)
            else:
                self.addElement(ActivityBagElement(e))
                
    def setProperties(self, e, aux):
        llista = e.getElementsByTagName(Activity.ELEMENT_NAME)
        if len(llista) > len(self.elements):
            elemens = [len(llista)]
        for node in llista:
            self.addJDomElement(node) 

