'''
Created on 09/05/2009

@author: mbenito
'''
from pygame.locals import *

import pygame
import pygame.locals
from  ContentCell import ContentCell
import Constants

class Cell(object):
    '''
    classdocs
    '''
    Rect = None
    Points = None
    idCell = None
    contentCell= None
    borderSize = Constants.DEFAULT_BORDER_SIZE
    #id =  None
    actualColorCell = Constants.colorCell
   
    
    def __init__(self,points,display_surf,id):

        self.Rect =[]
        self.Point=[]
        self.idCell = id
        self.Points = points
       
        self.Rect = pygame.draw.lines(display_surf,Constants.colorCell,True,points,self.borderSize)

    def isOverCell(self,x,y):
        #print 'x=',x,' y=',y,' Rect=',self.Rect
        
        if self.Rect.collidepoint(x,y):
                return True
        else:
            return False
    def OnRender(self,display_surf):
        
        #display_surf.fill(Constants.colorBackground,self.Rect)
        display_surf.blit(self.contentCell.img,self.Rect)
        
        ''' Draw borders'''
        if self.contentCell.border == True:
            pygame.draw.lines(display_surf,self.actualColorCell ,True,self.Points,self.borderSize)
        
    def OnRenderPressedCell(self,display_surf):
        if self.contentCell.border == True:
            pygame.draw.lines(display_surf,self.actualColorCell ,True,self.Points,self.borderSize)
