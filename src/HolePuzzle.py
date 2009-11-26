'''
Created on 09/05/2009

@author: mbenito
'''


import Constants
from styleGrid import StyleGrid
from Activity import  Activity
from Grid import Grid

class HolePuzzle(Activity):

    Grid1 = None
  
    PressedCell = None
    FinishGame = False

     
    def Load(self, display_surf ):
        self.setBgColor()

        '''Loading xml values'''
        xmlGrid = self.xmlActivity.getElementsByTagName('cells')[0]
       
        
        self.Grid1 = Grid(xmlGrid)
        self.Grid2 = Grid(xmlGrid)
         

        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols
        

        '''Sumamos el width al tamano total'''
        ''' 30 -> Margin over Grids'''
        width = width + self.Grid1.cellWidth + 30
        
        ''' Calculamos porcentaje...'''
        
        '''Maximize size'''
        
        coef = self.calculateCoef(width, height)
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        
        
        '''calculamos espacio para 1 celda mas...'''

       
        if self.Grid1.imagePath!=None:
            ''' 1 Imagen de fondo '''
            width= Constants.ACTIVITY_WIDTH 
            height =Constants.ACTIVITY_HEIGHT
            
            self.Grid1.LoadWithImage(self.numRows,self.numCols,width,height,xActual ,yActual, display_surf)
            
           
        else:
            ''' 1 Imagen por cada celda ( tipo texto)''' 
            self.Grid1.Load(self.numRows,self.numCols,width,height,xActual ,yActual, display_surf)
            cells = xmlGrid.getElementsByTagName('cell')
            i = 0
           
            for cell in cells: 
                '''Recuperamos el texto de la celda y lo  bliteamos en imagen actual de celda.. ''' 
                
                self.printxmlCellinCell(self.Grid1.Cells[i], cell)
                i = i+1
        
        self.Grid1.unsort()
        
        '''Load second Grid only with 1 cell..'''
        print self.Grid1.cellHeight , self.Grid1.cellWidth
        self.Grid2.Load(1,1,self.Grid1.cellHeight,self.Grid1.cellWidth,xActual+  width + 20,(height/2)-(self.Grid1.cellWidth/2), display_surf)
        self.Grid2.Cells[0].contentCell.img = self.Grid1.Cells[0].contentCell.img.copy()
        self.Grid1.Cells[0].contentCell.img.fill(Constants.colorBackground)
        self.Grid1.Cells[0].contentCell.id = -1

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                '''celda anterior apretada ''' 
                if cell.contentCell.id != -1:
                    idCelda = cell.idCell
                    try:
                        ''' celda gris esta a al izkierda'''
                        if self.Grid1.Cells[idCelda -1].contentCell.id == -1:
                            print 'idcelda =',idCelda,'mod=',((idCelda)% self.numCols)
                            if ((idCelda-1)% self.numCols) !=(self.numCols-1) :
                                self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[idCelda -1].idCell )
                        ''' celda gris esta a la derecha'''
                        if self.Grid1.Cells[idCelda +1].contentCell.id == -1:
                            '''evitem laterals'''
                            if ((idCelda+1)% self.numCols) !=0:
                                self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[idCelda + 1].idCell )
                        ''' celda gris esta arriba '''
                        print 'idcelda',idCelda
                        print 'calculo=',(idCelda - self.numCols)
                        
                        if self.Grid1.Cells[int(idCelda - self.numCols)].contentCell.id == -1:
                            self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[int(idCelda - self.numCols)].idCell )
                        ''' celda gris esta abajo '''
                        print 'calculo=',(idCelda + self.numCols)
                        if self.Grid1.Cells[int(idCelda + self.numCols)].contentCell.id == -1:
                            self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[int(idCelda + self.numCols)].idCell )
                    except:
                        
                        '''Estamos fuera de tablero....'''
                        
                    

    def OnRender(self,display_surf):
        display_surf.fill(self.containerBg)
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        self.Grid2.OnRender(display_surf)
  
    def isGameFinished(self):
        for cell in self.Grid1.Cells:
            if cell.idCell != cell.contentCell.id:
                return False
        return True

        