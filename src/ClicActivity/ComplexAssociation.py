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

import pygame

from Activity import  Activity
from Grid import Grid
from styleCell import StyleCell

class ComplexAssociation(Activity):

    Grid1 = None
    PressedCell = None

    color = None


    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        self.desactGrid1 = []
        self.desactGrid2 = []

        #Loading xml attributes
        #The attribute inverse is how are oriented the grids in the activity (which is the left or top grid)
        self.inverse = False
        try:
            if (self.xmlActivity.getAttribute('inverse') == 'true'):
                self.inverse = True
        except:
            self.inverse = False


        #The attribute orientation is how are oriented the grids in the activity (vertical or horitzontal)
	orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')

        #Load 2 Grids
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.Grid1 = Grid(xmlGrid1, self.pathToMedia)

        xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid2 = Grid(xmlGrid2, self.pathToMedia)

        #Loading a third possible grid
        try:
            xmlGrid3 = self.xmlActivity.getElementsByTagName('cells')[2]
            self.Grid3 = Grid(xmlGrid3, self.pathToMedia)
        except:
            self.Grid3 = Grid()


        #Calculate the size of grids
        width = self.Grid1.cellWidth * self.Grid1.numCols
        height = self.Grid1.cellHeight * self.Grid1.numRows

        width2 = self.Grid2.cellWidth * self.Grid2.numCols
        height2 = self.Grid2.cellHeight * self.Grid2.numRows

        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            height = height + self.Grid2.cellHeight
        else:
            '''Sumamos el width al tamano total'''
            width = width + self.Grid2.cellWidth


        '''Maximize size'''
        coef = self.calculateCoef(width, height)
	#coefx = self.calculateCoefPart(height + height2 + 10)
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef

        #coef = self.calculateCoef(width2, height2)
	#coefx = self.calculateCoefPart(height2)
        height2 = self.Grid2.cellHeight * self.Grid2.numRows * coef
        width2 = self.Grid2.cellWidth * self.Grid2.numCols * coef


        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        '''Cargamos grupo de celdas comunes...'''
        cellsPrimary = self.xmlActivity.getElementsByTagName('cells')[0]


        xGrid1 = (Constants.ACTIVITY_WIDTH - width) / 2
        yGrid1 = (Constants.ACTIVITY_HEIGHT - height) / 2
        xGrid1 = max(xGrid1,xActual)
        yGrid1 = max(yGrid1,yActual)

        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            newWidth = width
            newHeight = self.Grid2.cellHeight * coef
            #Para centrarlo verticalmente calculamos el heighttotal menos los height de los dos grids unidos
            yGrid1 = (Constants.ACTIVITY_HEIGHT - height - newHeight - 10) / 2
            yGrid1 = max(yGrid1,yActual)
            #Cargamos el Grid2 si tiene imagen o no (nos lo indica imagePath)
            if(self.Grid2.imagePath == None):
                self.Grid2.Load(self.Grid2.numRows,self.Grid2.numCols,width,newHeight,xGrid1 ,yGrid1 + height +10, display_surf)
            else:
                self.Grid2.LoadWithImage(self.Grid2.numRows,self.Grid2.numCols,width,newHeight,xGrid1 ,yGrid1 + height +10, display_surf, self.pathToMedia)
        else:
            '''Sumamos el width al tamano total'''
            newWidth = self.Grid2.cellWidth * coef
            newHeight = height
            #Para centrarlo horizontalmente calculamos el widthtotal menos los width de los dos grids unidos
            xGrid1 = (Constants.ACTIVITY_WIDTH - width - newWidth - 10) / 2
            xGrid1 = max(xGrid1,xActual)
            #Cargamos el Grid2 si tiene imagen o no
            if(self.Grid2.imagePath == None):
                self.Grid2.Load(self.Grid2.numRows,self.Grid2.numCols,newWidth,height,xGrid1 + width +10 ,yGrid1, display_surf)
            else:
                self.Grid2.LoadWithImage(self.Grid2.numRows,self.Grid2.numCols,newWidth,height,xGrid1 + width +10 ,yGrid1, display_surf, self.pathToMedia)


        if self.Grid1.imagePath == None:
            self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf)

        try:
            '''if cells 3 not exists, only create an empty Grid, '''
            if self.Grid3.imagePath == None:
                if self.inverse == False:
                    self.Grid3.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
                else:
                    self.Grid3.Load(self.Grid2.numRows,self.Grid2.numCols,newWidth,newHeight,xActual ,yActual, display_surf)
                cellsSolved = self.xmlActivity.getElementsByTagName('cells')[2]
                self.styleCell3 = StyleCell(cellsSolved)
                cells = cellsSolved.getElementsByTagName('cell')
                #self.styleCell3 = StyleCell(self.xmlGrid3)

                i = 0
                for cell in cells:
                    self.printxmlCellinCell(self.Grid3.Cells[i], cell, self.styleCell3)
                    i = i+1
            else:
                self.Grid3.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)
        except:
            pass

        if self.xmlActivity.getElementsByTagName('cells').length >= 2:

            '''Cargamos secondaryCells'''
            cellsSecondary = self.xmlActivity.getElementsByTagName('cells')[1]
            self.styleCell2 = StyleCell(cellsSecondary)

            '''Cargamos primer Grid del XML'''
            cells = cellsPrimary.getElementsByTagName('cell')
            self.styleCell = StyleCell(cellsPrimary)
            '''indexCell  = Numero de Celda que ocupa:'''

            if self.Grid1.imagePath != None:
                # 1 Imagen de fondo
                self.Grid1.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)

            indexCell = 0
            indexCell = self.doBucle(cells,indexCell)
            '''Cargamos segundo Grid del XML'''
            cells2 = cellsSecondary.getElementsByTagName('cell')

    	    i = 0
    	    id = 0

            if self.Grid2.imagePath == None:
                self.styleCell2 = StyleCell(cellsSecondary)
    	    
                for cell in cells2:
                        self.printxmlCellinCell(self.Grid2.Cells[i], cell, self.styleCell2)
                        '''Guardamos las imagenes en el Grid'''
                        self.Grid2.Cells[i].contentCell.img2 = self.Grid2.Cells[i].contentCell.img
                        self.Grid2.Cells[i].contentCell.id = id
                        id = id+1
                        i = i+1


        else:
            '''indexCell  = Numero de Celda que ocupa:'''
            indexCell = 0

            '''Cargamos primer Grid del XML'''
            cells = cellsPrimary.getElementsByTagName('cell')
            self.styleCell = StyleCell(cellsPrimary)
            indexCell = self.doBucle(cells,indexCell)


            '''Recargamos el primer Grid del XML'''
            indexCell = self.doBucle(cells,indexCell)

        #Unsort the Grids
        if self.Grid1.imagePath == None:
            #If Grid3 is not an empty grid, we have to unsort like the grid1
            if(len(self.Grid1.Cells) == len(self.Grid3.Cells)):
                self.Grid1.unsort(self.Grid3)
            else:
                self.Grid1.unsort()

        if self.Grid2.imagePath == None:
            self.Grid2.unsort()

        '''Play start sound'''
        self.play_sound(Constants.Sounds.START)
        
    #Cargamos el primer Grid
    def doBucle(self,cells,i):
        id = 0
        for cell in cells:
            print "i", i
            #self.printxmlCellinCell(self.Grid1.Cells[i], cell,self.styleCell)
            '''Guardamos las imagenes en el Grid'''
            #self.Grid1.Cells[i].contentCell.img2 = self.Grid1.Cells[i].contentCell.img
           
            if (self.Grid1.imagePath == None):
                self.printxmlCellinCell(self.Grid1.Cells[i], cell,self.styleCell)
                id = cell.getAttribute('id')
                id2 = i
                #Si los ids ya vienen por defecto los cojemos y sino los generamos incrementado en 1 cada vuelta
                if cell.hasAttribute('id'):
                    self.Grid1.Cells[i].contentCell.id = int(cell.getAttribute('id'))
                    id2 = id
                else:
                    self.Grid1.Cells[i].contentCell.id = int(id2)
            #Cargamos los ids directamente de la matriz en caso que sea una imagen i tenga un vector de ids
            else:
                if (self.Grid1.ids != []):
                    self.Grid1.Cells[i].contentCell.id = int(self.Grid1.ids[i])
                else:
                    print "ideeeeeeeeee", cell.getAttribute('id')
                    if (cell.hasAttribute('id')):
                        print "acceptat"
                        self.Grid1.Cells[i].contentCell.id = int(cell.getAttribute('id'))
                    else:
                         self.Grid1.Cells[i].contentCell.id = -1

            i = i+1

        j = 0
        if(self.Grid1.ids == []):
            while j< len(self.Grid1.Cells):
                print "j::",j
                print "lenGrid1", len(self.Grid1.Cells)
                print "lenIds", len(self.Grid1.ids)
                self.Grid1.ids.append(self.Grid1.Cells[j].contentCell.id)
                j += 1

        return i

    def OnEvent(self,PointOfMouse):
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                #si la celda no ha sido solucionada o su id es diferente de -1 (valor predeterminado)
                if self.desactGrid1.count(cell)==0 and cell.contentCell.id != -1:
                    # celda anterior apretada...
                    if self.PressedCell != None:
                        #los dos son iguales
                        if self.PressedCell.contentCell.id == cell.contentCell.id:
                            #si el Grid2 es el que esta apretado
			    if self.PressedGrid ==2:
                                #Depende de la orientacion cargamos en un grid u otro
                                if self.inverse == False:
                                    #COINCIDEN LAS CELDAS!!
                                    self.PressedCell.actualColorCell = Constants.colorCell
                                    cell.contentCell.img.fill(Constants.colorBackground)
                                    cell.contentCell.img = self.Grid3.Cells[cell.idCell].contentCell.img
                                    cell.contentCell.img2 = None
                                    self.PressedCell = None
                                    self.desactGrid1.append(cell)
                                else:
                                    self.desactGrid2.append(self.PressedCell)
                                    self.PressedCell.actualColorCell = Constants.colorCell
                                    self.PressedCell.contentCell.img.fill(Constants.colorBackground)
                                    self.PressedCell.contentCell.img = self.Grid3.Cells[0].contentCell.img
                                    self.PressedCell.contentCell.img2 = None
                                    self.PressedCell = None
                                self.play_sound(Constants.Sounds.OK)
                        #los dos son diferentes..
                        else:

                            self.PressedCell.actualColorCell = Constants.colorCell
                            self.PressedCell = None
                            self.play_sound(Constants.Sounds.ERROR)
			    self.PressedGrid = 1

                    #celda anterior no apretada
                    else:
                        self.PressedCell = cell
			self.PressedGrid = 1
                    	self.PressedCell.actualColorCell = Constants.colorPressedCell
                        self.play_sound(Constants.Sounds.CLICK)

        for cell in self.Grid2.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                #si la celda ya ha sido
                if self.desactGrid2.count(cell) == 0:
                    # celda anterior apretada...
                    if self.PressedCell != None:
                        #los dos son iguales
                        if self.PressedCell.contentCell.id == cell.contentCell.id:
			    if self.PressedGrid == 1:
                                if self.inverse == False:
                                    #'COINCIDEN LAS CELDAS!!'
                                    self.desactGrid1.append(self.PressedCell)
                                    self.PressedCell.actualColorCell = Constants.colorCell
                                    self.PressedCell.contentCell.img.fill(Constants.colorBackground)
                                    self.PressedCell.contentCell.img = self.Grid3.Cells[self.PressedCell.idCell].contentCell.img
                                    self.PressedCell.contentCell.borders=False
                                    #anulamos valor de img2 para indicar k ta ok
                                    self.PressedCell.contentCell.img2 = None
                                    self.PressedCell = None
                                else:
                                    self.desactGrid2.append(self.PressedCell)
                                    self.PressedCell.actualColorCell = Constants.colorCell
                                    cell.contentCell.img.fill(Constants.colorBackground)
                                    cell.contentCell.img = self.Grid3.Cells[0].contentCell.img
                                    cell.contentCell.img2 = None
                                    self.PressedCell = None
                                self.play_sound(Constants.Sounds.OK)
                            #los dos son diferentes..
                        else:

                            self.PressedCell.actualColorCell = Constants.colorCell
                            self.PressedCell = None
                            self.play_sound(Constants.Sounds.ERROR)
			    self.PressedGrid = 2

                    #celda anterior no apretada
                    else:
                        self.PressedCell = cell
			self.PressedGrid = 2
                    	self.PressedCell.actualColorCell = Constants.colorPressedCell
                        self.play_sound(Constants.Sounds.CLICK)


    def changeSecondImage(self,cell):
        tmpImg  = cell.contentCell.img
        cell.contentCell.img = cell.contentCell.img2
        cell.contentCell.img2= tmpImg


    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        #repintamos el grid...
        self.Grid1.OnRender(display_surf)
	self.Grid2.OnRender(display_surf)
        #si la celda se ha apretado, la pintamos ( por los bordes)
        if self.PressedCell != None :
            self.PressedCell.OnRender(display_surf)


    def isOverActivity(self,PointOfMouse):
        return True

    def isGameFinished(self):
        finish = False
        desact = len(self.desactGrid1)
        i = 0
        for id in self.Grid1.ids:
            if id != "-1":
                i += 1
                
        if i == 0:
            i = len(self.Grid1.Cells)

        if desact == i:
            finish = True

        return finish





