"""
  This class defines a content that can be displayed by {@link edu.xtec.jclic.boxes.ActiveBox}
  objects. This content can be a text, an image, a fragment of an image or a
  combination of text and images. The style (colours, font and size, etc.) can be specified
  in a {@link edu.xtec.jclic.boxes.BoxBase} object. It stores also information about
  the optimal size and location of the <CODE>ActiveBox</CODE>.
  @author Francesc Busquets (fbusquets@xtec.net)
"""

from JDomUtility import checkName
from JDomUtility import getIntAttr
from JDomUtility import HALIGN
from JDomUtility import VALIGN
from JDomUtility import ALIGN_MIDDLE
from JDomUtility import getHAlign
from JDomUtility import getVAlign
from JDomUtility import getAlignProp
from JDomUtility import getBoolAttr
from JDomUtility import getParagraphs
from JDomUtility import getDimensionAttr
import BoxBase
from BoxBase import getBoxBase

class ActiveBoxContent(object):
    
    bb = None
    ELEMENT_NAME="cell"
    ID = "id"
    ITEM = "item"
    id = -1
    item = -1
    dimension = None
    border = None
    imgName = None
    imgAlign=[ALIGN_MIDDLE, ALIGN_MIDDLE]
    txtAlign=[ALIGN_MIDDLE, ALIGN_MIDDLE]
    TXTALIGN = "txtAlign"
    IMGALIGN = "imgAlign"
    WIDTH = "width"
    HEIGHT = "height"
    IMAGE = "image"
    BORDER = "border"
    AVOIDOVERLAPPING = "avoidOverlapping"
    avoidOverlapping = False
    rawText = ""
    text = ""
    htmlText=""
    innerHtmlText=""
    img = None
    imgClip = None
    EMPTY_CONTENT=None
    
    def setProperties(self, e, aux):
        checkName(e, self.ELEMENT_NAME)
        mediaBag = aux
        child = None
        
        self.id = getIntAttr(e, self.ID, self.id)
        self.item = getIntAttr(e, self.ITEM, self.item)
        if e.getAttribute(HALIGN)!="" or e.getAttribute(VALIGN)!="":
            self.txtAlign[0] = getHAlign(e, self.txtAlign[0])
            self.txtAlign[1] = getVAlign(e, self.txtAlign[1]) 
            self.imgAlign[0]=self.txtAlign[0]
            self.imgAlign[1]=self.txtAlign[1]
        else:
            self.txtAlign=getAlignProp(e, self.TXTALIGN, self.txtAlign)
            self.imgAlign=getAlignProp(e, self.IMGALIGN, self.imgAlign)
            
        self.avoidOverlapping = getBoolAttr(e, self.AVOIDOVERLAPPING, self.avoidOverlapping)
        self.dimension = getDimensionAttr(e, self.WIDTH, self.HEIGHT, self.dimension)
        self.border = getBoolAttr(e, self.BORDER, self.border)
        
        child=e.getElementsByTagName(BoxBase.BoxBase.ELEMENT_NAME)
        if child != []:
            self.setBoxBase(getBoxBase(child[0]))
        
        self.setTextContent(getParagraphs(e))
        
    def setBoxBase(self, boxBase):
        self.bb = boxBase
        
    def setTextContent(self, tx):
        if tx!=None:
            self.rawText = str(tx)
            self.text = str(tx)
        else:
            self.rawText=None
            self.text=None
            self.htmlText=None
            self.innerHtmlText=None
            
    def getEmptyContent(self):
        if self.EMPTY_CONTENT==None:
            self.EMPTY_CONTENT=ActiveBoxContent()
        return self.EMPTY_CONTENT
            
    def isEmpty(self):
        return self.text=="" and self.img==None
    
    def isEquivalent(self, abc, checkCase):
        if abc==self:
            return True
        result = False
        if abc!=None:
            if self.isEmpty() and abc.isEmpty():
                result = (self.id == abc.id)
            else:
                if self.text==None:
                    result = abc.text==None
                else:
                    if checkCase:
                        result = self.text == abc.text
                    else:
                        result = self.text.lower() == abc.text.lower()
                result = result and (self.img == abc.img)
                if self.imgClip==None:
                    result = result and (abc.imgClip==None)
                else:
                    result = result and (self.imgClip==abc.imgClip)
        return result
    
    def setImgContent(self, setImg, setImgClip):
        self.img=setImg
        self.imgName=None
        self.imgClip=setImgClip
        
    
def getActiveBoxContent(e, mediaBag):
    
    abc = ActiveBoxContent()
    abc.setProperties(e, mediaBag)
    return abc
    