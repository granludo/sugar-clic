'''
Created on 09/05/2009

@author: mbenito
'''


import Constants


from Activity import  Activity
from Grid import Grid


class InformationScreen(Activity):

    Grid1 = None
    
    
 
    def Load(self, display_surf ):
        self.setBgColor()

        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        
        self.Grid1 = Grid(xmlGrid1)
        
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols
        
        '''Maximize size'''
        
        coef = self.calculateCoef(width, height)
                 
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
            

        if self.Grid1.imagePath != None:
            width= Constants.ACTIVITY_WIDTH 
            height =Constants.ACTIVITY_HEIGHT
            self.Grid1.LoadWithImage(1,1,width,height,xActual ,yActual, display_surf,self.pathToMedia)
        else:
            self.Grid1.Load(self.Grid1.numRows, self.Grid1.numCols, width, height, xActual, yActual, display_surf)
            i = 0
            cells = xmlGrid1.getElementsByTagName('cell')
            for cell in cells: 
                self.printxmlCellinCell(self.Grid1.Cells[i], cell)
                
                i = i+1 
      

    def OnEvent(self,PointOfMouse):
        '''
           Pantalla informativa, no hacemos nada...
        '''

    def OnRender(self,display_surf):
        display_surf.fill(self.containerBg)
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        

    def isGameFinished(self):
        '''Never will finish. This is a Information Activity '''
        return False

        