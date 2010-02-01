"""
  This class defines a specific point into a JClic sequence of activities:
  what activity must run at this point, what to do or where to jump when the activity
  finishes, the behavior of the "next" and "prev" buttons, etc. It can also have a "tag",
  used to refer to this point of the sequence with a unique name. <CODE>ActivitySequenceElements</CODE>
  are always stored into {@link edu.xtec.jclic.bags.ActivitySequence} objects.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from xml.dom.minidom import *
from JDomUtility import checkName
from JDomUtility import getIntAttr
from JDomUtility import getStringAttr
from JDomUtility import getParagraphs
from JDomUtility import getStrIndexAttr
from ActivitySequenceJump import *

NAV_BOTH = 3

class ActivitySequenceElement(object):
    
    ELEMENT_NAME="item"
    NAME = "name"
    DELAY = "delay"
    DESCRIPTION="description"
    ID="id"
    NAV_BUTTONS="navButtons"
    NAV_BUTTONS_TAG=["none", "fwd", "back", "both"]
    NAV_BOTH=3
    FORWARD="forward"
    
    activityName = ""
    tag = ""
    description = ""
    delay = 0
    navButtons = 0
    fwdJump=None
    backJump=None
    
    def __init__(self, activityName, delay, navButtons):
        self.setActivityName(activityName)
        self.delay=delay
        self.tag=None
        self.description=None
        
        self.fwdJump=None
        self.backJump=None
        
        self.navButtons=navButtons
    
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        self.setActivityName(e.getAttribute(self.NAME))
        self.delay = getIntAttr(e, self.DELAY, 0)
        self.setTag(getStringAttr(e, self.ID, self.tag, False))
        self.description=getParagraphs(e)
        
        jumps = e.getElementsByTagName(ActivitySequenceJump.ELEMENT_NAME)
        for jump in jumps:
            id = jump.getAttribute(ActivitySequenceJump.ID)
            asj = getActivitySequenceJump(jump)
            if id == self.FORWARD:
                self.fwdJump = asj
            else:
                self.backJump = asj
                
        self.navButtons=getStrIndexAttr(e.getAttribute(self.NAV_BUTTONS), self.NAV_BUTTONS_TAG, self.NAV_BOTH);
    
    def setActivityName(self, sActivityName):
        self.activityName=sActivityName
    
    def getTag(self):
        return self.tag
    
    def setTag(self, newTag):
        self.tag = newTag
    
    def getActivityName(self):
        return self.activityName
    
def getActivitySequenceElement(e):
    ase = ActivitySequenceElement("",0, NAV_BOTH)
    ase.setProperties(e, None)
    return ase