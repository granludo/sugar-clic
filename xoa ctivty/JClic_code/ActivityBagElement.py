"""
  This class stores a XML {@link orj.jdom.Element} that defines an
  {@link edu.xtec.jclic.Activity}. It stores also a {@link java.util.HashMap}
  with references of other objects to this activity, and implements some
  useful methods to directly retrieve some properites of the related Activity,
  like its name. ActivityBagElements are usually stored into
  {@link edu.xtec.jclic.bags.ActivityBag} objects.
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from xml.dom.minidom import *
from Activity import *
from JDomUtility import CLASS

class ActivityBagElement(object):
    
    element = None
    
    def __init__(self, e):
        self.setData(e)
        
    def getName(self):
        return self.element.getAttribute(Activity.NAME)
    
    def getClass(self):
        return self.element.getAttribute(CLASS)
    
    def getData(self):
        return self.element
    
    def setData(self, e):
        self.element = e
    