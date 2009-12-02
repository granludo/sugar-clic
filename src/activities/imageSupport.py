'''
Created on 09/05/2009

@author: sbennel
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
