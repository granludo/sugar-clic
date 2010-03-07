"""
  This class stores the definition of the sequence of activities related to a
  specific {@link edu.xtec.jclic.project.JClicProject}. The sequence are formed by
  an ordered list of objects of type {@link edu.xtec.jclic.bags.ActivitySequenceElement},
  internally stored in a {@link java.util.Vector}. It stores also a transient pointer
  to a current element, and provides several methods useful to deal with sequences.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from xml.dom.minidom import *
from xml.dom import *
from xml.dom.NodeFilter import NodeFilter
from ActivitySequenceElement import *
from JDomUtility import checkName

class ActivitySequence(object):
    
    currentAct = 0
    project = None
    elements = []
    
    ELEMENT_NAME="sequence"
    
    def __init__(self, project):
        self.project = project
        self.elements = []
        self.currentAct = -1
        
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        llista = e.getElementsByTagName(ActivitySequenceElement.ELEMENT_NAME)
        for node in llista:
                ase = getActivitySequenceElement(node)
                if ase.tag ==None:
                    self.add(ase)
            
    def add(self, ase):
        self.elements.append(ase) 
        if len(self.elements) == 1:
            self.currentAct = 1
            if(ase.getTag()==None):
                ase.setTag("start")
    
    def getElement(self, n, updateCurrentAct):
        result=None
        try:
            result = self.elements[n]
        except:
            result = None
        if result!=None and updateCurrentAct:
            self.currentAct=n
        return result
    
    def getElementByTag(self, tag, updateCurrentAct):
        i=0
        k = len(self.elements)
        if k<1 or tag=="":
            return None
        
        b = False
        normalizedTag = tag
        ase = None
        for i in range(k):
            ase = self.getElement(i, False)
            if ase!=None and ase.getActivityName()!="" and ase.getActivityName()==normalizedTag:
                b = True
                break
        if i==k-1 and not b:
            ase=None
        else:
            if updateCurrentAct:
                self.currentAct=i
        return ase
    

