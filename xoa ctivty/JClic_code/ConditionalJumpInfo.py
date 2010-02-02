"""
 * This special case of {@link edu.xtec.jclic.bags.JumpInfo} is used in
 * {@link edu.xtec.jclic.bags.ActivitySequenceJump} objects to decide the jump to be
 * taked (or the action to be performed) based on the results obtained by the user when
 * playing JClic activities. In addition to the standard JumpInfo fields and methods, this
 * class have two public members where to store a score and time thresholds. The exact
 * meaning of this members will depend on the type of this <CODE>ConditionalJumpInfo</CODE>
 * ({@link edu.xtec.jclic.bags.ActivitySequenceJump.upperJump} or {@link edu.xtec.jclic.bags.ActivitySequenceJump.lowerJump}).
 * @author Francesc Busquets (fbusquets@xtec.net)
 * @version 1.0
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
from JDomUtility import *
from JumpInfo import *


class ConditionalJumpInfo(JumpInfo):
    
    threshold = 0
    time = 0
    
    TIME="time"
    THRESHOLD="threshold"
    
    def ConditionalJumpInfo(self, action, sequence, threshold, time = -1):
        super(ConditionalJumpInfo,self).__init__(action, sequence)
        self.threshold = threshold
        self.time = time
    
    def setProperties(self, e, aux):
        super(ConditionalJumpInfo, self).setProperties(e, aux)
        self.threshold = getIntAttr(e, self.THRESHOLD, self.threshold)
        self.time = getIntAttr(e, self.TIME, self.time)
        
def getConditionalJumpInfo(e):
        cji = ConditionalJumpInfo()
        cji.setProperties(e, None)
        return cji