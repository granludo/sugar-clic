import xml.dom
from xml.dom.minidom import Node
from xml.dom.minidom import Element
from Point import *
from Dimension import *
import pygame
from pygame import font
from pygame import Color
from pygame.color import THECOLORS
   
ID="id"
IMAGE="image"
NAME="name"
TYPE="type"
BGCOLOR="bgcolor"
FORECOLOR="forecolor"
MARGIN="margin"
BORDER="border"
POSITION="position"
X="x"
Y="y"
P="p"
CLASS="class"
HALIGN="hAlign" 
VALIGN="vAlign"
ALIGN_MIDDLE = 1
FONT="font"
BOLD = "bold"
ITALIC= "italic"
FAMILY = "family"
SIZE = "size"
P="p"

rare = -18634527

hAlignName=["left", "middle", "right"]
vAlignName=["top", "middle", "bottom"]

DEFAULT_ALIGNMENT=[ALIGN_MIDDLE, ALIGN_MIDDLE]

HTML_COLOR_NAMES = [
    "Black", "Silver", "Gray", "White",
    "Maroon", "Red", "Purple", "Fuchsia",
    "Green", "Lime", "Olive", "Yellow",
    "Navy", "Blue", "Teal", "Aqua",
    "Pink", "Orange", "DarkGray"
    ]

HTML_COLORS = [
    THECOLORS["black"], THECOLORS["gray"], THECOLORS["gray"], THECOLORS["white"],
    Color("0x800000"), THECOLORS["red"], Color("0x800080"), THECOLORS["magenta"],
    Color("0x008000"), THECOLORS["green"], Color("0x808000"), THECOLORS["yellow"],
    Color("0x000080"), THECOLORS["blue"], Color("0x008080"), THECOLORS["cyan"],
    THECOLORS["pink"], THECOLORS["orange"], THECOLORS["gray"]
    ]

BOOL_STR=["false", "true", "default"]

def checkName(e, expectedName):    
    
    if(e == None):
        raise SyntaxError, "Null element passed as argument, expecting: %d" % expectedName
    if(e._get_localName() != expectedName):
        raise SyntaxError, "Find element %d while expecting %d" % e._get_localName() %expectedName         
        
def getClassName(e):           
    
    className=e.getAttribute(CLASS)
    if(e == ""):
        raise SyntaxError, "Element without class name!"
    return className

def getStringAttr(e, attr, defaultValue, allowEmpty):
    
    s = e.getAttribute(attr)
    result = defaultValue
    s = s.encode("iso8859-1")
    if(s != None and (allowEmpty or len(s))):
        result=s;
    return result

def getIntAttr(e, attr, defaultValue):
    
    s = e.getAttribute(attr)
    result = defaultValue
    if(s != ""):
        result= int(s)
    return result

def getDoubleAttr(e, attr, defaultValue):
    
    s=e.getAttribute(attr)
    result = defaultValue
    if s!="":
        result = float(s)
    return result
    
def getBoolAttr(e, attr, defaultValue):
    
    s = e.getAttribute(attr)
    result=defaultValue
    if(s != ""):
        if(s.lower() == "true"):
            result = True
        elif(s.lower() == "false"):
            result = False
        else:
            raise TypeError, "Invalid boolean"
    return result
  
def stringToColor(s):
    
    color = None
    if s.startswith('0x'): 
        color = Color(s)
    else:
        for i in range(len(HTML_COLOR_NAMES)):
            if(HTML_COLOR_NAMES[i] == s):
                color = HTML_COLORS[i]
                exit
    if(color == None):
        raise TypeError, "Invalid color"
    return color
        
def colorToString(color):
    
    s = color.__str__()
    return "0x"+s 

def getColorAttr(e, attr, defaultValue):
    
    s = e.getAttribute(attr)
    result = defaultValue
    if (s != ""):
        result = stringToColor(s.encode("iso8859-1"))
    return result

def getPointAttr(e, atrX, atrY, defaultValue):
    
    result=defaultValue
    x=getIntAttr(e, atrX, rare)
    y=getIntAttr(e, atrY, rare)
    if(x != rare and y != rare):
        result = Point(x, y)
    return result

def getDimensionAttr(e, atrW, atrH, defaultValue):
    
    result=defaultValue
    w=getIntAttr(e, atrW, rare)
    h=getIntAttr(e, atrH, rare)
    if(w != rare and h != rare):
        result = Dimension(w, h)
    return result

def getParagraphs(e):
    
    sb = ""
    if(e!=None):
        llista_paragrafs = e.getElementsByTagName(P)
        if llista_paragrafs !=[]:
            for Node in llista_paragrafs:
                s = (Node.childNodes[0].nodeValue).encode("iso8859-1")
                if(sb == ""):
                    sb = s
                else:
                    sb.__add__("\n").__add__(s) 
            return sb
        else:
            return ""

def addParagraphs(parent, childName, text):
    
    if(text != None):
        child = Element(childName)
        setParagraphs(child, text)
        parent.appendChild(child)

def setParagraphs(e, text):
    
    if(text != None):
        s = text.split()
        for i in range(len(s)):
            e.addChild(Element(P).setText(s[i]))
            
def boolString(value):
    if(value == True):
        return BOOL_STR[1]
    else: return BOOL_STR[2]
    

def getStrIndexAttr(s, values, defaultValue):
    result = defaultValue
    s = s.encode("iso8859-1")
    if (s!=None and len(s)>0):
        for result in range(len(values)):
            if s.lower() == values[result].lower():
                break
        if result == len(values):
            raise ValueError, "Unknow value: " + s
    return result

def elementToFont(e):
    checkName(e, FONT)
    family = getStringAttr(e, FAMILY, "default", False)
    size = getIntAttr(e, SIZE, 12)
    style = ""
    if getBoolAttr(e, BOLD, False):
        style = style + BOLD
    if getBoolAttr(e,ITALIC, False):
        style = style + ITALIC
    return getValidFont(family, style, size)

def getValidFont(family, style, size):
    f = None
    if(style == BOLD):
        f = font.SysFont(family, size, True)
    elif(style == ITALIC):
        f = font.SysFont(family, size, False, True)
    elif(style == BOLD+ITALIC):
        f = font.SysFont(family, size, True, True)
    else:
        f = font.SysFont(family, size)
    return f

def getHAlign(e, defaultValue):
    if e == None:
        return defaultValue
    return getStrIndexAttr(e.getAttribute(HALIGN), hAlignName, defaultValue)

def getVAlign(e, defaultValue):
    if e == None:
        return defaultValue
    return getStrIndexAttr(e.getAttribute(VALIGN), vAlignName, defaultValue)

def getAlignProp(e, id, defaultValue):
    result = [0] * 2
    if defaultValue == None:
        defaultValue=DEFAULT_ALIGNMENT
    result[0]=defaultValue[0]
    result[1]=defaultValue[1]
    if id!=None:
        s = e.getAttribute(id)
        if s!="" and len(s)>0:
            st = s.split(",")
    return result

def getChildWithId(e, name, id):
    
    result = None
    if e!=None and id!=None and name!=None:
        childs = e.getElementsByTagName(name)
        for child in childs:
            if id == child.getAttribute(ID):
                return result
    return None


