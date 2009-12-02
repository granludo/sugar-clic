'''
Created on 09/05/2009

@author: mbenito
'''

import Constants
import pygame
import pygame.font
import pygame.locals

from Activity import  Activity
from Grid import Grid

class IdentifyPanels(Activity):

    Grid1 = None


    def Load(self, display_surf ):
        self.setBgColor()

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid1 = Grid(xmlGrid1)
        self.Grid2 = Grid(xmlGrid2)
       
        ''' Calculate Real size'''
        
        width = self.Grid1.cellWidth * self.Grid1.numCols
        height = self.Grid1.cellHeight * self.Grid1.numRows


        ''' Calculamos porcentaje...'''
        
        '''Maximize size'''
        coef = self.calculateCoef(width, height)
      
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        '''Cargamos grupo de celdas comunes...'''
        
        ''' 1 Imagen por cada celda ( tipo texto)''' 
        self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
        
        cells = xmlGrid1.getElementsByTagName('cell')
                
        i = 0
        for cell in cells: 
            self.printxmlCellinCell(self.Grid1.Cells[i], cell)
            
            id  = int(cell.getAttribute('id') )
            self.Grid1.Cells[i].contentCell.id = id 
            i = i+1
        
        self.Grid2.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
        
        try:
            '''if cells 2 not exists, only create an empty Grid'''
           
            cells = xmlGrid2.getElementsByTagName('cell')    
            i = 0
            for cell in cells: 
                self.printxmlCellinCell(self.Grid2.Cells[i], cell)
    
                i = i+1
        except:
            pass
        
        

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
        '''
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                if cell.contentCell.id != 0:
                    print cell.contentCell.id
                    if cell.contentCell.id == 1:
                        cell.contentCell.img = self.Grid2.Cells[cell.idCell].contentCell.img
                        cell.contentCell.id = -1
               

    def OnRender(self,display_surf):
        display_surf.fill(self.containerBg)
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
           

    def isGameFinished(self):
        for cell in self.Grid1.Cells:
            if cell.contentCell.id == 1:
                return False
        return True

        