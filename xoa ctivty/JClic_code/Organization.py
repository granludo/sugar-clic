"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

import xml.dom
from xml.dom.minidom import Element
from xml.dom.minidom import Node
from xml.dom.minidom import Document
from JDomUtility import *

class Organization(object):
    
    name = ""
    mail = ""
    url = ""
    address = ""
    pc = ""
    city = ""
    country = ""
    state = ""
    comments = ""
    
    ELEMENT_NAME = "organization"
    NAME = "name"
    MAIL = "mail"
    URL = "url"
    ADDRESS = "address"
    PC = "pc"
    CITY = "city"
    COUNTRY = "country"
    STATE = "state"
    COMMENTS = "comments"

    def __init__(self):
        self.name = ""
        self.mail = ""
        self.url = ""
        self.address = ""
        self.pc = ""
        self.city = ""
        self.country = ""
        self.state = ""
        self.comments = ""
    
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        self.name = getStringAttr(e, self.NAME, self.name, True)
        self.mail = getStringAttr(e, self.MAIL, self.mail, False)
        self.url = getStringAttr(e, self.URL, self.url, False)
        self.address = getStringAttr(e, self.ADDRESS, self.address, False)
        self.pc = getStringAttr(e, self.PC, self.pc, False)
        self.city = getStringAttr(e, self.CITY, self.city, False)
        self.state = getStringAttr(e, self.STATE, self.state, False)
        self.country = getStringAttr(e, self.COUNTRY, self.country, False)
        child = e.getElementsByTagName(self.COMMENTS)
        if child!=[]:
            self.comments = getParagraphs(child[0])
        
def getOrganization(e):
        o = Organization()
        o.setProperties(e, None)
        return o