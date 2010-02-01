"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
from JDomUtility import *
import time
import datetime
import Author
from Author import *

class Revision(object):
    
    date = None
    authors = []
    description = ""
    comments = ""
    
    ELEMENT_NAME = "revision"
    DATE = "date"
    DESCRIPTION = "description"
    COMMENTS = "comments"

    def __init__(self, setDate = None, setDescription = None):
        if (setDate == None and setDescription == None):
            self.date = datetime.date.today()
            self.description = ""
        else:
            self.date = setDate
            self.description = setDescription
        self.authors = None
        self.comments = ""

    def setProperties(self, e, aux):
        
        child = None
        checkName(e, self.ELEMENT_NAME)
        
        self.description = getStringAttr(e, self.DESCRIPTION, self.description, True)
        child = e.getElementsByTagName(self.COMMENTS)
        if child!=[]:
            self.comments = getParagraphs(child[0])
        
        array = []
        child = e.getElementsByTagName(Author.ELEMENT_NAME)
        for x in child:
                array.append(getAuthor(x))
        
        if(array != []):
            self.authors = array
            
def getRevision(e):        
    r = Revision()
    r.setProperties(e, None)
    return r
    