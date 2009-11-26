'''
Created on 09/05/2009

@author: mbenito
'''
from Cell import *
from Constants import *
from pygame import surface
from pygame.locals import *
import os
import pygame
import random

from styleGrid import StyleGrid



class Grid(object):

    Cells = None
    rows = None
    cols = None
    cellHeight = None
    cellWidth  = None
    transparent = False
    fontFamily = 'Arial'
    fontSize = 30
    fontBold= False
    fontItalic= False
    backgroundColor = Constants.colorBackground
    foregroundColor = Constants.colorWhite
    borderColor = Constants.colorCell
    hasBorder = True
    imagePath = None
    
    def __init__(self,xml=None):

        '''We can change the try/except by hasAttribute'''
        '''Grid is a vector of cells'''
        self.Cells = []
        '''BackGround Color'''
        if xml != None:
            try:
                bgcolor =xml.getElementsByTagName('color')[0].getAttribute('background')
                self.backgroundColor = pygame.Color(hex(int(bgcolor, 16)))
            except:
                '''Default color'''
                pass
        
            '''foreground Color'''
            try:
                bgcolor =xml.getElementsByTagName('color')[0].getAttribute('foreground')
                self.foregroundColor = pygame.Color(hex(int(bgcolor, 16)))
            except:
                '''Default color'''
                pass
            
            '''borderColor Color'''
            try:
                bgcolor =xml.getElementsByTagName('color')[0].getAttribute('border')
                self.borderColor = pygame.Color(hex(int(bgcolor, 16)))
            except:
                '''Default color'''
                pass
            try:
                self.cellHeight =  float(xml.getAttribute('cellHeight'))
                self.cellWidth =   float(xml.getAttribute('cellWidth'))
            except:
                self.cellHeight =  float(30)
                self.cellWidth =   float(30)
            
            self.numRows = float(xml.getAttribute('rows'))
            self.numCols = float(xml.getAttribute('cols'))
        
            if xml.hasAttribute('image'):
            
                self.imagePath = xml.getAttribute('image')


    def LoadWithImage (self,rows,cols,width,height,xInicial, yInicial,display_surf,):  
        ''' Load 1 image for the full Grid'''
        self.rows = int(rows)
        self.cols = int(cols)
        
        widthPart = width / self.cols
        heightPart  = height / self.rows
        self.cellHeight = heightPart
        self.cellWidth  = widthPart
        
        img = pygame.image.load(os.getcwd()+'/../media/'+self.imagePath).convert_alpha()

        img2 = pygame.transform.scale(img, (width, height))
        
        surfaceEmpty = surface.Surface((width, height))

        if self.transparent == False: 
            surfaceEmpty.fill(self.backgroundColor)
 
        surfaceEmpty.blit(img2,(0, 0)) 
        img2 = surfaceEmpty
        
        i = 0;
        actualRow = 0
        actualCol = 0
        xActual=xInicial
        yActual=yInicial
        xNext= xActual+widthPart
        yNext= yActual+heightPart
        ''' Calculate the size and the position of Rects'''

        
        while (i < self.rows*self.cols):

            points = ((xActual,yActual),
                      (xNext,yActual),
                      (xNext,yNext),
                      (xActual,yNext))
            
            
            '''Initializing the cell'''
            
            cell = Cell(points,display_surf,i)
           
            '''Calculating the rect size and position'''
            rect  = Rect (xActual-xInicial,yActual-yInicial,widthPart,heightPart)
            '''cut the part of the image that goes in this cell'''
            img3 = img2.subsurface(rect)
            contentCell = ContentCell()
            contentCell.img  = img3
            contentCell.id = i
            cell.contentCell = contentCell
            
            '''adding cell to grid..'''
            self.Cells.append(cell)
            
            
            actualCol = actualCol +1
            xActual = xActual+widthPart
            xNext= xNext+widthPart
            
            
            ''' Counters increment for the loop'''
            if actualCol == self.cols:
                actualCol = 0
                actualRow +=1

                yActual = yActual+heightPart
                yNext= yNext+heightPart
                xActual = xInicial
                xNext= xActual+widthPart
                
            i= i+1
            

    def Load (self,rows,cols,width,height,xInicial, yInicial,display_surf,styleGrid=None):  

        
        self.rows = int(rows)
        self.cols = int(cols)
        
        widthPart = width / self.cols
        heightPart  = height / self.rows
       
        
        surfaceEmpty = surface.Surface((widthPart,heightPart),0)
                
        if styleGrid != None:
            if styleGrid.transparent == False: 
                surfaceEmpty.fill(styleGrid.backgroundColor)


        self.cellHeight = heightPart
        self.cellWidth  = widthPart    



        i = 0;
        actualRow = 0
        actualCol = 0
        xActual=xInicial
        yActual=yInicial
        xNext= xActual+widthPart
        yNext= yActual+heightPart
        while (i < self.rows*self.cols):

            points = ((xActual,yActual),
                      (xNext,yActual),
                      (xNext,yNext),
                      (xActual,yNext))
            
            
            ##Ahora pasamos la imagen...
            
            cell = Cell(points,display_surf,i)

            contentCell = ContentCell()
            

            contentCell.id = i
            contentCell.img = surfaceEmpty.copy()
            
            cell.contentCell = contentCell
            self.Cells.append(cell)
            
            actualCol = actualCol +1
            xActual = xActual+widthPart
            xNext= xNext+widthPart
            
            
            
            if actualCol == self.cols:
                actualCol = 0
                actualRow +=1

                yActual = yActual+heightPart
                yNext= yNext+heightPart
                xActual = xInicial
                xNext= xActual+widthPart
                
            i= i+1
            
      

    def OnRender(self,display_surf):
        
        for cell in self.Cells:
            cell.OnRender(display_surf)
        for cell in self.Cells:
            cell.OnRenderPressedCell(display_surf)
        

    def changeImages(self,idCell1, idCell2):
        
        ''' Change the 2 cell images from a Grid '''
        contentCell1   = self.Cells[idCell1].contentCell
        contentCell2  = self.Cells[idCell2].contentCell
        
        self.Cells[idCell1].contentCell = contentCell2
        self.Cells[idCell2].contentCell = contentCell1

    def unsort(self):
        i = 0
        ''' We do 50 times!!! maby only 10 loops necessary'''
        while (i< 50):
            self.changeImages(random.randint(0, (self.rows*self.cols)-1),random.randint(0, (self.rows*self.cols)-1))
            i = i+1