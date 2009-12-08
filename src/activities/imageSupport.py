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
from pygame.locals import *

import pygame
import pygame.locals
from  ContentCell import *
import Constants
from Constants import *
class ImageSupport(object):

    def printTextInSurface(self,surface,text,font=None):
        if font == None:
            font = pygame.font.Font(None, 90)
        else:
            font = pygame.font.Font(None, int(font))
            
        text = font.render(text, True, (0,0,0))
        '''falta centrar  el texto...'''
        surface.blit(text,(20,20))
        return surface
    def isOverCell(self,x,y):
        if self.Rect.collidepoint(x,y):
                print 'hemos apretado un rectangulo.... YUHUUUUUUUUUUUUUUUu'
               
                
                return True
        else:
            return False
    def OnRender(self,display_surf):
        
        display_surf.fill(Constants.colorBackground,self.Rect)
        display_surf.blit(self.contentCell.img,self.Rect)
        self.Rect = pygame.draw.lines(display_surf,self.actualColorCell ,True,self.Points,5)
        
    def getIdCell(self):
        print 'entrando a la funcion getIdCell, id vale', self.idCell   
        return self.idCell    
            #pygame.draw.rect(self.RectImage)
            #display_surf.blit(self.RectImage,(400,100))
            
        #self.Rect = pygame.draw.lines(display_surf,(124,234,211),True,self.Points,5)
        
        #self.Rect.Move(500,100)
