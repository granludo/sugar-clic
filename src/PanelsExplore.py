'''
Created on 09/05/2009

@author: mbenito
'''

import Constants
from styleGrid import StyleGrid

from Activity import  Activity
from Grid import Grid

class PanelsExplore(Activity):

    Grid1 = None
  
    PressedCell = None

    
    
    def Load(self, display_surf ):
        self.setBgColor()

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid1 = Grid(xmlGrid1)
        self.Grid2 = Grid(xmlGrid2)
        self.Grid3 = Grid(xmlGrid2)

         
        orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')

        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols
        
        
        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            height = height + self.Grid2.cellHeight
        else:
            '''Sumamos el width al tamano total'''
            width = width + self.Grid2.cellWidth
        
        ''' Calculamos porcentaje...'''
        
        

        
        '''Maximize size'''
        coef = self.calculateCoef(width, height)
              
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        

        
        self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
        '''Grid auxiliar...'''
        self.Grid3.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            newHeight = self.Grid2.cellHeight * coef
            self.Grid2.Load(1,1,width,newHeight,xActual ,yActual+ height, display_surf)

        else:
            '''Sumamos el width al tamano total'''
            newWidth = self.Grid2.cellWidth * coef
            self.Grid2.Load(1,1,newWidth,height,xActual + width ,yActual, display_surf)
            
        self.Grid2.Cells[0].contentCell.img2 = self.Grid2.Cells[0].contentCell.img.copy()
        cells = xmlGrid1.getElementsByTagName('cell')
        i = 0
        for cell in cells: 
            self.printxmlCellinCell(self.Grid1.Cells[i], cell)
            idCell = cell.getAttribute('id')
            if len(idCell)>0:
                self.Grid1.Cells[i].contentCell.id = int(idCell)
            else :
                self.Grid1.Cells[i].contentCell.id = -1
            i = i+1
        cells = xmlGrid2.getElementsByTagName('cell')
        i = 0 
        copia = self.Grid2.Cells[0].contentCell.img.copy()
        for cell in cells: 
            copia = self.Grid2.Cells[0].contentCell.img.copy()
            self.Grid3.Cells[i].contentCell.img = copia
            self.printxmlCellinCell(self.Grid3.Cells[i], cell)
            
            i = i+1
        

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                print cell.contentCell.id
                if cell.contentCell.id != -1:
                    self.Grid2.Cells[0].contentCell.img  = self.Grid3.Cells[cell.contentCell.id].contentCell.img
                else:
                    self.Grid2.Cells[0].contentCell.img = self.Grid2.Cells[0].contentCell.img2

    def OnRender(self,display_surf):
        display_surf.fill(self.containerBg)
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        self.Grid2.OnRender(display_surf)
        

    def isGameFinished(self):
        return False

    
   
        
        