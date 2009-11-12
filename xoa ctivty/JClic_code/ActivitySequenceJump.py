"""
  This is a special case of {@link edu.xtec.jclic.bags.JumpInfo}, used only in
  {@link edu.xtec.jclic.bags.ActivitySequenceElement} objects. Sequence elements contain
  two ActivitySequenceJump objects: one to be processed when the user clicks on the
  "next" button (or when the activity finishes, if in automatic mode), and the
  other one related to the "prev" button. ActivitySequenceJump objects define a default
  jump or action, but can have up to two {@link edu.xtec.jclic.bags.ConditionalJumpInfo} objects,
  used to define alternative jumps when the obtained score or the time used to solve the
  activities are below or over specific values.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import xml.dom
from xml.dom.minidom import Node
from xml.dom.minidom import Element
from JDomUtility import checkName
from JDomUtility import getChildWithId
from ConditionalJumpInfo import getConditionalJumpInfo
from JumpInfo import *

class ActivitySequenceJump(JumpInfo):
    
    upperJump = None
    lowerJump = None
    
    ID = "id"
    NAME = "name"
    UPPER = "upper"
    LOWER = "lower"
    
    def __init__(self, action, sequence = None):
        super(ActivitySequenceJump, self).__init__(action, sequence)
        self.upperJump=None
        self.lowerJump=None
        
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        child = None
        
        s = e.getAttribute(self.NAME)
        if s == "":
            super(ActivitySequenceJump, self).setProperties(e, aux)
            child = getChildWithId(e, self.ELEMENT_NAME, self.UPPER)
            if child!=None:
                self.upperJump=getConditionalJumpInfo(child)
            child = getChildWithId(e, self.ELEMENT_NAME, self.LOWER)
            if child!=None:
                self.lowerJump=getConditionalJumpInfo(child)
        
def getActivitySequenceJump(e):
    asj = ActivitySequenceJump(ActivitySequenceJump.STOP)
    asj.setProperties(e, None)
    return asj