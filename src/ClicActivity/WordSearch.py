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
import Constants

from Activity import  Activity
from Grid import Grid
import random

class WordSearch(Activity):

    choiceChar = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    textGrid = None
    cellsGrid = None
    auxGrid = None
    clues = []
    cols = 0
    pressedCellIni = None
    pressedCellFi = None
    encerts = 0
    xmlCells = None
    xmlText = None
    render = False
    textHasBorder = False
    
    
    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading xml values'''
        
        '''xml amb la sopa de lletres'''
        self.xmlText = self.xmlActivity.getElementsByTagName('textGrid')[0]
        '''xml amb els ids que correspon a cada paraula'''
        xmlClues = self.xmlActivity.getElementsByTagName('clues')[0]
        '''xml amb les imatges a mostrar per cada paraula'''
        self.xmlCells = self.xmlActivity.getElementsByTagName('cells')[0]
        
        '''Crea el grid de la sopa'''
        self.textGrid = Grid(self.xmlText)
        '''Crea el grid de les imatges'''
        self.cellsGrid = Grid(self.xmlCells)
        '''Grid auxiliar per anar mostrant les imatges'''
        self.auxGrid = Grid(self.xmlCells)

        '''Loading clues'''
        self.clues = []
        tmpClues = xmlClues.getElementsByTagName('clue')
        for i in range(0,len(tmpClues)):
            self.clues.append(tmpClues[i].firstChild.data)
            
        orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')   
        
        ''' Calculate Real size'''
        heightText = self.textGrid.cellHeight * self.textGrid.numRows
        widthText = self.textGrid.cellWidth * self.textGrid.numCols
        
        heightCells = self.cellsGrid.cellHeight * self.cellsGrid.numRows
        widthCells = self.cellsGrid.cellWidth * self.cellsGrid.numCols
        
        if heightCells < heightText:
            relation = heightText/heightCells
            heightCells = heightText
            widthCells = widthCells * relation
               
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        if self.cellsGrid.imagePath != None:
            self.cellsGrid.LoadWithImage(self.cellsGrid.numRows,self.cellsGrid.numCols,widthCells,heightCells,1,1, display_surf,self.pathToMedia)
        else:
            self.cellsGrid.Load(self.cellsGrid.numRows,self.cellsGrid.numCols,widthCells,heightCells,1,1, display_surf)
        
        
        if orientation == 'AB':
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xActual,yActual, display_surf)
            self.auxGrid.Load(self.cellsGrid.numRows,self.cellsGrid.numCols,widthCells,heightCells,xActual+widthText+10,yActual, display_surf)
        elif orientation == 'BA':
            self.auxGrid.Load(self.cellsGrid.numRows,self.cellsGrid.numCols,widthCells,heightCells,xActual,yActual, display_surf)
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xActual+widthCells+10,yActual, display_surf)
        elif orientation == 'AUB':
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xActual,yActual, display_surf)
            self.auxGrid.Load(self.cellsGrid.numRows,self.cellsGrid.numCols,widthCells,heightCells,xActual,yActual+heightText+10, display_surf)
        elif orientation == 'BUA':
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xActual,yActual+heightCells +10, display_surf)
            self.auxGrid.Load(self.cellsGrid.numRows,self.cellsGrid.numCols,widthCells,heightCells,xActual,yActual, display_surf)
                
        self.textHasBorder = self.textGrid.hasBorder
        
        text = []
        rows = self.xmlText.getElementsByTagName('row')
        for row in rows:
            row = row.firstChild.data
            self.cols = len(row)
            for i in range(0,self.cols):
                letter = row[i]
                if letter == '*':
                    letter = random.choice(self.choiceChar)
                text.append(letter)
                
        for i in range(0,len(text)):
            self.textGrid.Cells[i].contentCell.letter = text[i]
            self.printLetterinCell(self.textGrid.Cells[i],self.xmlText)

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        if self.pressedCellIni == None:
            for cell in self.textGrid.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    print cell.contentCell.id
                    self.pressedCellIni = cell
                    self.pressedCellIni.actualColorCell = Constants.colorPressedCell
        else:
            select = []
            for cell in self.textGrid.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    print cell.contentCell.id
                    self.pressedCellFi = cell
            
            '''Agafa la paraula seleccionada'''
            if self.pressedCellFi != None and self.pressedCellIni != None:
                d = self.pressedCellFi.contentCell.id - self.pressedCellIni.contentCell.id
                if d > -self.cols and d < self.cols:
                    '''Paraula en horitzontal'''
                    if self.pressedCellFi.contentCell.id > self.pressedCellIni.contentCell.id:
                        for i in range(self.pressedCellIni.contentCell.id, self.pressedCellFi.contentCell.id+1):
                            select.append(self.textGrid.Cells[i].contentCell.letter)
                    else:
                        for i in range(self.pressedCellFi.contentCell.id, self.pressedCellIni.contentCell.id+1):
                                select.append(self.textGrid.Cells[i].contentCell.letter)
                else:
                    '''Paraula en vertical'''
                    if self.pressedCellFi.contentCell.id > self.pressedCellIni.contentCell.id:
                        for i in range(self.pressedCellIni.contentCell.id, self.pressedCellFi.contentCell.id+1, self.cols):
                            select.append(self.textGrid.Cells[i].contentCell.letter)
                    else:
                        for i in range(self.pressedCellFi.contentCell.id, self.pressedCellIni.contentCell.id+1, self.cols):
                            select.append(self.textGrid.Cells[i].contentCell.letter)
            
                self.pressedCellIni.actualColorCell = Constants.colorCell
                
                '''Comproba si es una paraula correcta'''
                parfw = '' #Agafa la paraula de principi a fi (forward)
                parbw = '' #Agafa la paraula al reves (backward)
                for l in select:
                    parfw = parfw + l
                    parbw = l + parbw
                print parfw
                clueID = self.isWordCorrect(parfw,parbw)
                if clueID >= 0 and self.clues[clueID] != None:
                    self.encerts += 1
                    self.clues[clueID] = None
                    if self.cellsGrid.imagePath != None:
                        '''Una sola imatge dividida a les cells'''
                        self.auxGrid.Cells[clueID].contentCell.img = self.cellsGrid.Cells[clueID].contentCell.img                        
                    else:
                        '''Una imatge per cada cell'''
                        xmlCell = self.xmlCells.getElementsByTagName('cell')[clueID]
                        self.printxmlCellinCell(self.auxGrid.Cells[clueID],xmlCell)
                    print 'paraula trobada'
                    if d > -self.cols and d < self.cols:
                        if self.pressedCellFi.contentCell.id > self.pressedCellIni.contentCell.id:
                            for i in range(self.pressedCellIni.contentCell.id, self.pressedCellFi.contentCell.id+1):
                                self.printLetterinCell(self.textGrid.Cells[i],self.xmlText,Constants.colorWhite,Constants.colorBlack)
                        else:
                            for i in range(self.pressedCellFi.contentCell.id, self.pressedCellIni.contentCell.id+1):
                                self.printLetterinCell(self.textGrid.Cells[i],self.xmlText,Constants.colorWhite,Constants.colorBlack)
                    else:
                        if self.pressedCellFi.contentCell.id > self.pressedCellIni.contentCell.id:
                            for i in range(self.pressedCellIni.contentCell.id, self.pressedCellFi.contentCell.id+1, self.cols):
                                self.printLetterinCell(self.textGrid.Cells[i],self.xmlText,Constants.colorWhite,Constants.colorBlack)
                        else:
                            for i in range(self.pressedCellFi.contentCell.id, self.pressedCellIni.contentCell.id+1, self.cols):
                                self.printLetterinCell(self.textGrid.Cells[i],self.xmlText,Constants.colorWhite,Constants.colorBlack)
                            
                '''Reset pressedCells'''
                self.pressedCellIni.contentCell.border = self.textHasBorder
                self.pressedCellIni = None
                self.pressedCellFi = None
    
    
    def isWordCorrect(self,parfw,parbw):
        result = -1
        for i in range(0,len(self.clues)):
            if self.clues[i] == parfw or self.clues[i] == parbw:
                result = i
        return result
    
    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        '''repintamos el grid...'''
        self.textGrid.OnRender(display_surf)
        self.auxGrid.OnRender(display_surf)
        if self.pressedCellIni != None:
            self.pressedCellIni.contentCell.border = True
            self.pressedCellIni.OnRenderPressedCell(display_surf)
            
        #self.cellsGrid.OnRender(display_surf)
        

    def isGameFinished(self):
        return self.encerts == len(self.clues)
 
   
        
        