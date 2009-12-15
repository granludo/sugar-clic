''' 
    This file is part of Sugar-Clic
    
    Sugar-Clic is copyrigth 2009 by Maria Jose Casany Guerrero and Marc Alier Forment
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
    @copyrigth 2009 Marc Alier, Maria Jose Casany marc.alier@upc.edu
    @copyrigth 2009 Universitat Politecnica de Catalunya http://www.upc.edu
    
    @autor Marc Alier
    @autor Jordi Piguillem
    
    @license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
'''
from Cell import *
from Constants import *
from pygame import surface
from pygame.locals import *
import os
import pygame
import random





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
                color =xml.getElementsByTagName('color')[0].getAttribute('background')
                print 'el color k trae de background es:',bgcolor
                self.backgroundColor = pygame.Color(hex(int(bgcolor, 16)))
                print 'he informado bgcolor',bgcolor
            except:
                '''Default color'''
                pass
        
            '''foreground Color'''
            try:
                color =xml.getElementsByTagName('color')[0].getAttribute('foreground')
                self.foregroundColor = pygame.Color(hex(int(bgcolor, 16)))
            except:
                '''Default color'''
                pass
            
            '''borderColor Color'''
            try:
                color =xml.getElementsByTagName('color')[0].getAttribute('border')
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


    def LoadWithImage (self,rows,cols,width,height,xInicial, yInicial,display_surf,pathToMedia):  
        ''' Load 1 image for the full Grid'''
        self.rows = int(rows)
        self.cols = int(cols)
        
        widthPart = width / self.cols
        heightPart  = height / self.rows
        self.cellHeight = heightPart
        self.cellWidth  = widthPart
        
        img = pygame.image.load(pathToMedia+'/'+self.imagePath).convert_alpha()

        img2 = pygame.transform.scale(img, (int(width), int(height)))
        
        surfaceEmpty = surface.Surface((int(width), int(height)))

        if self.transparent == False: 
            print 'surface no transparent bgcolor =',self.backgroundColor
            surfaceEmpty.fill(self.backgroundColor)
        else:
            print 'surface transparent'
 
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
            

    def Load (self,rows,cols,width,height,xInicial, yInicial,display_surf):  

        
        self.rows = int(rows)
        self.cols = int(cols)
        
        widthPart = width / self.cols
        heightPart  = height / self.rows
       
        
        surfaceEmpty = surface.Surface((int(widthPart),int(heightPart)),0)
                 
        
        '''IF INCORRECTE'''
        if self.transparent == False: 
            print 'grid-> color fondo = ',self.backgroundColor
            surfaceEmpty.fill(self.backgroundColor)
        else:
            
            print 'surface transparent'

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