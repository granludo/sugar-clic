"""
  Base class for Clic filesystems.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 0.1
"""

import sys
import xml.dom.minidom
from xml.dom.minidom import parse

class FileSystem(object):
    
    path = None
    fullPath = None
    
    def __init__(self, fullPathParsed, fullPath):
        self.path = "/"
        self.fullPath = fullPath
        for i in range(len(fullPathParsed)):
            self.path = self.path + fullPathParsed[i] + "/"
    
    def getXMLDocument(self, fname):
        doc = parse(fname)
        return doc 
    
    def getPath(self):
        return self.path
        