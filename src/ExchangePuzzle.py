'''
Created on 09/05/2009

@author: mbenito
'''

import Constants


from Activity import  Activity
from Grid import Grid

class ExchangePuzzle(Activity):

    Grid1 = None
  
    PressedCell = None
    numRows = None
    nomCols = None
    
    
    def Load(self, display_surf ):
        self.setBgColor()

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.Grid1 = Grid(xmlGrid1)
        

        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        

        
        if self.Grid1.imagePath != None:
            
            '''Loading constants for the activity'''
            width= Constants.ACTIVITY_WIDTH 
            height =Constants.ACTIVITY_HEIGHT
        
            ''' 1 Imagen de fondo '''
            
            self.Grid1.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf,self.pathToMedia)
            
        else:
                
            ''' Calculate Real size'''
            height = self.Grid1.cellHeight * self.Grid1.numRows
            width = self.Grid1.cellWidth * self.Grid1.numCols
            
            '''Maximize size'''
            coef = self.calculateCoef(width, height)      
            height = self.Grid1.cellHeight * self.Grid1.numRows * coef
            width = self.Grid1.cellWidth * self.Grid1.numCols * coef
            
            
            ''' 1 Imagen por cada celda ''' 
            self.Grid1.Load(self.numRows,self.numCols,width,height,xActual ,yActual, display_surf)
            cells = xmlGrid1.getElementsByTagName('cell')
            
            i = 0
            for cell in cells: 
                '''Recuperamos el texto de la celda y lo  bliteamos en imagen actual de celda.. ''' 
                self.printxmlCellinCell(self.Grid1.Cells[i], cell )
                i = i+1
        self.Grid1.unsort()

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                '''celda anterior apretada ''' 
                if self.PressedCell != None:
                    '''celda anterior = celda actual ''' 
                    if self.PressedCell.contentCell.id == cell.idCell:
                        idCell1 = self.PressedCell.idCell
                        idCell2 = cell.idCell
                        self.Grid1.changeImages(idCell1,idCell2 )
                    
                    ''' else: no cambiamos -> no hacemos nada... '''

                    ''' borramos margenes.. '''
                    self.PressedCell.actualColorCell = Constants.colorCell
                    self.PressedCell = None
                     
                else:
                    '''no hay ninguna anterior apretada'''
                    self.PressedCell = cell
                    self.PressedCell.actualColorCell = Constants.colorPressedCell
           

    def OnRender(self,display_surf):
        display_surf.fill(self.containerBg)
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        
        '''si la celda anterior  se ha apretado, la repintamos para que se vean los margenes bien'''
        if self.PressedCell != None :
            self.PressedCell.OnRender(display_surf)
       

    def isGameFinished(self):
        for cell in self.Grid1.Cells:
            if cell.idCell != cell.contentCell.id:
                return False
        return True
    
   
        
        