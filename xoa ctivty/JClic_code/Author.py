"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
from JDomUtility import *

class Author(object):
    
    name = ""
    mail = ""
    url = ""
    organization = ""
    comments = ""
    rol = ""
    
    ELEMENT_NAME = "author"
    NAME = "name"
    MAIL = "mail"
    URL = "url"
    ORGANIZATION = "organization"
    COMMENTS = "comments"
    ROL = "rol"
    
    def __init__(self):
        self.name = ""
        self.mail = ""
        self.url = ""
        self.organization = ""
        self.comments = ""
        self.rol = ""
    
    def setProperties(self, e, aux):
        
        checkName(e, self.ELEMENT_NAME)
        self.name = getStringAttr(e, self.NAME, self.name, True)
        self.mail = getStringAttr(e, self.MAIL, self.mail, False)
        self.url = getStringAttr(e, self.URL, self.url, False)
        self.rol = getStringAttr(e, self.ROL, self.rol, False)
        self.organization=getStringAttr(e, self.ORGANIZATION, self.organization, False)
        child = e.getElementsByTagName(self.COMMENTS)
        if child!=[]:
            self.comments=getParagraphs(child[0])
        
def getAuthor(e):
    checkName(e, Author.ELEMENT_NAME)

    a = Author()
    a.setProperties(e, None)
    return a