'''
Created on 09/05/2009

@author: mbenito
'''

import Constants

from Activity import  Activity
from Grid import Grid

class DoublePuzzle(Activity):

    Grid1 = None
  
    activity = None
    PressedCell = None
    FinishGame = False
    xmlActivity = None
    numRows = None
    nomCols = None
    
    
    def __init__(self,xmlActivity):
        
        self.xmlActivity = xmlActivity
        
 
     
    def Load(self, display_surf ):
        self.setBgColor()

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]

        self.Grid1 = Grid(xmlGrid1)
        self.Grid2 = Grid(xmlGrid1)
           
        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols
            
        '''Maximize size'''
        coef = self.calculateCoef(width, height)      
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        try:
            layout =self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')
        except:
            layout = 'AB'
        if layout == 'AB':
            width = width/2 - 5
        else:
            height = height/2 -5

        '''Loading constants for the activity'''
        
        
        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        
       
        ''' 1 Imagen de fondo '''

        self.Grid1.LoadWithImage(self.numRows,self.numCols,width,height,xActual ,yActual, display_surf,self.pathToMedia)
        
        if layout == 'AB':
            xActual = xActual + width + 10
        else:
            yActual = yActual + height + 10
        
        
        self.Grid2.LoadWithImage(self.numRows,self.numCols,width,height,xActual ,yActual, display_surf)
        
        for cell in self.Grid1.Cells:
            cell.contentCell.img.fill(Constants.colorBackground)
           
        self.Grid2.unsort()
    
        ''' A image 1 le quitamos la imagen'''
    

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        
        '''Hay una celda apretada.. anteriormente'''
        if self.PressedCell  != None:
            ''' si click en alguna celda izkierda '''
            for cell in self.Grid1.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    ''' si ids son iguales --> cambiamos celdas.. '''
                    if cell.contentCell.id == self.PressedCell.contentCell.id:
                        
                        tmpImg = self.PressedCell.contentCell.img
                        self.PressedCell.contentCell.img = cell.contentCell.img
                        cell.contentCell.img = tmpImg
                        self.PressedCell.contentCell.id = -1
                    ''' desmarcamos pressedCell'''
                    self.PressedCell.actualColorCell = Constants.colorCell
                    self.PressedCell = None
                   
            
            '''si click en derecha.. '''
            for cell in self.Grid2.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    if cell.contentCell.id != -1:
                        ''' cambiamos el pressedCell '''
                        self.PressedCell.actualColorCell = Constants.colorCell
                        self.PressedCell = None
                        self.PressedCell = cell
                        self.PressedCell.actualColorCell = Constants.colorPressedCell
                       

        else:
            ''' si click en alguna celda izkierda nothing...--> no ponemos nada '''
             
            
            '''si click en derecha.. '''
            for cell in self.Grid2.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    ''' cambiamos el pressedCell a esta celda..-> si no ha sido ya cambiada...'''
                    if cell.contentCell.id != -1:
                    
                        self.PressedCell = cell
                        self.PressedCell.actualColorCell = Constants.colorPressedCell


        
    def OnRender(self,display_surf):
        display_surf.fill(self.containerBg)
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        self.Grid2.OnRender(display_surf)
        
        '''si la celda anterior  se ha apretado, la repintamos para que se vean los margenes bien'''
        if self.PressedCell != None :
            self.PressedCell.OnRender(display_surf)
       


    def isGameFinished(self):
        for cell in self.Grid2.Cells:
            if cell.contentCell.id != -1:
                return False
        return True

        