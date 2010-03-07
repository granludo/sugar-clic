"""
  This class contains information about what the sequence manager of JClic must do
  in specific circumstances: when an activity finishes, when the user clicks on the
  "next" and "prev" buttons, or when a special active content is activated. Different
  kinds of actions are possible: to go back to a previous point in the sequence, to exit
  the program, to stop (do nothing), to jump to a specific point in the sequence of activities
  or to jump to another JClic project.
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
from JDomUtility import *

class JumpInfo(object):
    
    JUMP = 0
    STOP = 1
    RETURN = 2
    EXIT = 3
    action = 0
    projectPath = ""
    sequence = ""
    actNum = -1
    
    actions = ["JUMP", "STOP", "RETURN", "EXIT"]
    ELEMENT_NAME = "jump"
    ACTION = "action"
    TAG = "tag" 
    PROJECT = "project"
    EXTERNAL_OBJECT = "external"
    SEQUENCE_OBJECT = "sequence"
    
    def __init__(self, action, sequence = None, actNum = -1):
        self.action = action
        self.projectPath = None
        if ( self.actNum == -1 and self.sequence != None):
            self.sequence = sequence
        elif (self.sequence == None and self.actNum != -1):
            self.actNum = actNum
            
    def setProperties(self, e, aux):
        
        checkName(e, self.ELEMENT_NAME)
        
        self.action = getStrIndexAttr(e.getAttribute(self.ACTION), self.actions, self.JUMP)
        if(self.action == self.JUMP):
            self.sequence = getStringAttr(e, self.TAG, self.sequence, False)
            self.projectPath = getStringAttr(e, self.PROJECT, self.projectPath, False)
    
    def listReferences(self, type, map) :
        if(self.action == self.JUMP):
            if(self.projectPath !=  None):
                if(self.type == None or type.equals(self.EXTERNAL_OBJECT)):
                    map.put(self.projectPath, self.EXTERNAL_OBJECT);
            elif(self.sequence != None):
                if(type == None or type.equals(self.SEQUENCE_OBJECT)):
                    map.put(self.sequence, self.SEQUENCE_OBJECT)