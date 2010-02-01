"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
from Activity import *
from JDomUtility import *
from Author import *
from Revision import *
from Organization import *
from StrUtils import *
import time
import datetime

class ProjectSettings(object):
    
    title = ""
    iconFileName = ""
    description = ""
    descriptors = ""
    area = ""
    level = ""
    
    languages = []
    authors = []
    organizations = []
    revisions = []
    
    UNTITLED = "untitled"
    ELEMENT_NAME = "settings"
    TITLE = "title"
    LANGUAGE = "language"
    DESCRIPTION = "description"
    DESCRIPTORS = "descriptors" 
    AREA = "area" 
    LEVEL = "level"
    ICON="icon"
    
    def __init__(self):
        self.title = self.UNTITLED
        self.description = ""
        self.area = ""
        self.level = ""
        self.descriptors = ""
        self.languages = None
        self.authors = None
        self.organizations = None
        self.revisions = [Revision(datetime.date.today(),"created")]
        self.iconFileName = ""
        
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        child = None
        array = []
        s = ""
        
        child = e.getElementsByTagName(self.TITLE)
        if(child != []):
            self.title = child[0]._get_localName()
        
        child = e.getElementsByTagName(Revision.ELEMENT_NAME)
        for x in child:
            array.append(getRevision(x))
        if(array != []):
            self.revisions = array
            
        array = [None]
        
        child = e.getElementsByTagName(Author.ELEMENT_NAME)
        for x in child:
            array.append(getAuthor(x))
        if(array != []):
            self.authors = array
        
        array = [None]
        
        child = e.getElementsByTagName(Organization.ELEMENT_NAME)
        for x in child:
            array.append(getOrganization(x))
        if(array != []):
            self.organizations = array

        
        array = [None]
        
        child = e.getElementsByTagName(self.LANGUAGE)
        for x in child:
            array.append(x._get_localName)
        if(array != []):
            self.languages = array

        child = e.getElementsByTagName(self.DESCRIPTION)
        self.description = getParagraphs(child[0])
        
        child = e.getElementsByTagName(self.DESCRIPTORS)
        if(child !=[]):
            child2 = child[0].getElementsByTagName(P)
            if(child2 != []):
                self.descriptors = getParagraphs(child2[0].getElementsByTagName(self.DESCRIPTORS))
                self.descriptors = StrUtils.replace(self.descriptors, "\n", ", ")

            else:
                self.descriptors = ""
                
            self.area = getStringAttr(child[0], self.AREA, self.area, False)
            self.level = getStringAttr(child[0], self.LEVEL, self.level, False)
        
        child = e.getElementsByTagName(self.ICON)
        if(child != []):
            self.iconFileName = getStringAttr(child[0], self.FILE, self.iconFileName, False)
            
def getProjectSettings(e):
        st = ProjectSettings()
        st.setProperties(e, None)
        return st
      