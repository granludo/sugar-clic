''' 
    This file is part of Sugar-Clic
    
    Sugar-Clic is copyrigth 2009 by Maria José Casany Guerrero and Marc Alier Forment
    of the Universitat Politecnica de Catalunya http://www.upc.edu
    Contact info: Marc Alier Forment granludo @ gmail.com or marc.alier
    @ upc.edu
    
    Sugar-Clic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Sugar-Clic is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with Sugar-Clic. If not, see <http://www.gnu.org/licenses/>.
    


    @package sugarclic
    @copyrigth 2009 Marc Alier, Maria José Casany marc.alier@upc.edu
    @copyrigth 2009 Universitat Politecnica de Catalunya http://www.upc.edu
    
    @autor Marc Alier
    @autor Jordi Piguillem
    
    @license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
'''
import Constants
import pygame
from pygame.locals import *
from Point import *
import pygame.font
class GeneralDialog(object):
    '''
    classdocs
    '''
    pointPrevious = None
    pointNext = None
    
    ImgNext = None
    ImgPrevious = None
    ImgBackground = None
    rectNext = None
    rectPrev = None
    changeClic = None
    def __init__(self):

        self.ImgNext     =  pygame.image.load(Constants.Images.NEXT).convert_alpha()
        self.ImgPrevious =  pygame.image.load(Constants.Images.PREV).convert_alpha()
        self.ImgChangeClic =  pygame.image.load(Constants.Images.PREV).convert_alpha()
    
        self.pointPrevious = Point((10, Constants.MAX_HEIGHT-50))
        self.pointNext =  Point((60, Constants.MAX_HEIGHT-50))
        self.pointChangeClic = Point((Constants.MAX_WIDTH-60, Constants.MAX_HEIGHT-50))

    def renderDialog(self, display_surf): 
        ''' Print all rectancles form the General Dialog'''
       
        ''' THIS PART CAN BE IMPROOVED!!!'''
        rectExt = Rect(0,0,Constants.MAX_WIDTH,Constants.MAX_HEIGHT)
        weidth = Constants.MAX_WIDTH -(32+30)
        height = Constants.MAX_HEIGHT-(32+75)
        rectborder= Rect(30,30,weidth,height)
        weidth = Constants.MAX_WIDTH-(28+30)
        height= Constants.MAX_HEIGHT-(28+75)
        rectInt=    Rect(28,28,weidth,height)
        display_surf.fill(Constants.colorBorder,rectExt)
        display_surf.fill(Constants.colorBorderDark,rectInt)
        display_surf.fill(Constants.colorBackground,rectborder)
        
        ''' TEXT Dialog'''
        rectTextExt= Rect(150,Constants.MAX_HEIGHT-(50),700,40)
        rectTextInt= Rect(152,Constants.MAX_HEIGHT-(48),696,36)
        display_surf.fill(Constants.colorBorderDark,rectTextExt)
        display_surf.fill(Constants.colorBackground,rectTextInt)
        
        ''' Buttons'''
        self.rectPrev = display_surf.blit(self.ImgPrevious, (self.pointPrevious.getX(), self.pointPrevious.getY()) )
        self.rectNext = display_surf.blit(self.ImgNext,     (self.pointNext.getX(), self.pointNext.getY()) )
        self.rectChangeClic = display_surf.blit(self.ImgChangeClic,     (self.pointChangeClic.getX(), self.pointChangeClic.getY()) )
        
        
    def isOverNextButton(self, PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectNext.collidepoint(x,y):
            return True
        else:
            return False
    def printMessage(self,display_surf,message):
        
        rectTextExt= Rect(150,Constants.MAX_HEIGHT-(50),700,40)
        rectTextInt= Rect(152,Constants.MAX_HEIGHT-(48),696,36)
        rectText= Rect(157,Constants.MAX_HEIGHT-(40),696,36)
        font = pygame.font.Font(None,int(25) )
        text  = font.render(message, True, (0,0,0),Constants.colorMessage)    
        
        display_surf.fill(Constants.colorBorderDark,rectTextExt)
        display_surf.fill(Constants.colorBackground,rectTextInt)
       
        display_surf.blit(text,rectText)
    def isOverPreviousButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectPrev.collidepoint(x,y):
            return True
        else:
            return False
    def isOverChangeClicButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectChangeClic.collidepoint(x,y):
            return True
        else:
            return False
    def isOverActivity(self,PointOfMouse):
            return True
       