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
from TextGrid import TextGrid
from TextField import TextField

class WrittenAnswer(Activity):

    Grid1 = None
    PressedCell = None

    color = None


    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        self.desactGrid1 = []
        self.desactGrid2 = []
        self.respostes = []
        self.result = ""
        self.resolts = []
        ''' ----Dos posibilidades en XML----

         orientation   -1 Grid: Hay que doblar el tamano del Grid para duplicar las posibilidades
            -2 Grids: Hay que printar todas las posibilidades
        '''

        '''Loading xml values'''


	orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')

	'''Create 2 Grids'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.Grid1 = Grid(xmlGrid1, self.pathToMedia)

        '''xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid2 = Grid(xmlGrid2, self.pathToMedia)'''

        xmlTextGrid = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid2 = TextField(xmlTextGrid, pygame.font.SysFont('Arial', Constants.minFontSize), (200,200,200))
        #self.Grid2 = TextGrid(xmlTextGrid,self.mediaInformation,self.pathToMedia)

        try:
            xmlGrid3 = self.xmlActivity.getElementsByTagName('cells')[2]
            self.Grid3 = Grid(xmlGrid3, self.pathToMedia)
        except:
            self.Grid3 = Grid()


        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols

        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            height = height + 100
        else:
            '''Sumamos el width al tamano total'''
            width = width + 400


        ''' Calculamos porcentaje...'''

        '''Maximize size'''
        coef = self.calculateCoef(width, height)

        '''Maximize size'''
        #coef = self.calculateCoef(width, height)
	#coefx = self.calculateCoefPart(height)
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef



        '''coef = self.calculateCoef(width2, height2)
	#coefx = self.calculateCoefPart(height2)
        height2 = self.Grid2.cellHeight * self.Grid2.numRows * coef
        width2 = self.Grid2.cellWidth * self.Grid2.numCols * coef'''

	print "paramentres"
	print height
	print self.Grid1.cellHeight
	print self.Grid1.numRows

        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        '''Cargamos grupo de celdas comunes...'''
        cellsPrimary = self.xmlActivity.getElementsByTagName('cells')[0]
        self.styleCell = StyleCell(cellsPrimary)
        xGrid1 = (Constants.ACTIVITY_WIDTH - width) / 2
        yGrid1 = (Constants.ACTIVITY_HEIGHT - height) / 2
        xGrid1 = max(xGrid1,xActual)
        yGrid1 = max(yGrid1,yActual)

        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            newHeight = 100
            #Para centrarlo verticalmente calculamos el heighttotal menos los height de los dos grids unidos
            yGrid1 = (Constants.ACTIVITY_HEIGHT - height - newHeight - 10) / 2
            yGrid1 = max(yGrid1,yActual)
        else:
            '''Sumamos el width al tamano total'''
            newWidth = 200
            newHeight = height
            xGrid1 = (Constants.ACTIVITY_WIDTH - width - newWidth - 10) / 2
            xGrid1 = max(xGrid1,xActual)

        #yGrid1 = 0

        if self.Grid1.imagePath == None:
            self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf)

        try:
            '''if cells 2 not exists, only create an empty Grid'''
            if self.Grid3.imagePath == None:
                self.Grid3.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
                cells = xmlGrid3.getElementsByTagName('cell')
                i = 0
                for i in range(len(cells)):
                    self.printxmlCellinCell(self.Grid3.Cells[i], cells, self.styleCell)
                    #i = i+1
            else:
                self.Grid3.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)
        except:
            pass


        '''Cargamos secondaryCells'''
        cellsSecondary = self.xmlActivity.getElementsByTagName('cells')[1]

        '''Cargamos primer Grid del XML'''
        cells = cellsPrimary.getElementsByTagName('cell')
        '''indexCell  = Numero de Celda que ocupa:'''
        indexCell = 0
        cells = cellsPrimary.getElementsByTagName('cell')
        self.styleCell = StyleCell(cellsPrimary)
        indexCell = self.doBucle2(cells,indexCell)
        #indexCell = self.doBucle(cells, cellsSecondary, indexCell) # a CADA volta del bucle posar fer un ids[]

        '''Cargamos segundo Grid del XML'''
        cells2 = cellsSecondary.getElementsByTagName('cell')
        indexCell = self.doBucle(cells2, indexCell)

        if self.Grid1.imagePath != None:
            ''' 1 Imagen de fondo '''
            self.Grid1.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)

        if orientation == 'AUB' or orientation == 'BUA':
            self.Grid2.Load((xGrid1+(xGrid1 + width))/2 - 150,yGrid1+height + 5, display_surf)
        else:
            self.Grid2.Load(xGrid1+width + 5,(yGrid1+height)/2, display_surf)

        i = 0

        #self.Grid3.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)

        if self.Grid1.imagePath == None:
            self.Grid1.unsort()

        for cell in self.Grid1.Cells:
            self.Grid1.ids.append(cell.contentCell.id)

        self.PressedCell = self.Grid1.Cells[0]
        self.PressedCell.actualColorCell = Constants.colorCell


    def doBucle(self,cells,i):
        id = 0
        print "entraaki???"
        print cells
        for cell in cells:
            #self.printxmlCellinCell(self.Grid1.Cells[i], cell,self.styleCell)
            print cell.toxml()
            resposta = cell.getElementsByTagName('p')[0].firstChild.data
            print resposta
            self.respostes.append(resposta)
            '''Guardamos las imagenes en el Grid'''
            #self.Grid2.Cells[i].contentCell.img2 = self.Grid1.Cells[i].contentCell.img
            #self.Grid2.Cells[i].contentCell.id = id
            id = id+1
            i = i+1
        return i

    def doBucle2(self,cells,i):
        id = 0
        idsAux = []
        for cell in cells:
            self.printxmlCellinCell(self.Grid1.Cells[i], cell,self.styleCell)
            '''Guardamos las imagenes en el Grid'''
            self.Grid1.Cells[i].contentCell.img2 = self.Grid1.Cells[i].contentCell.img

            if (self.Grid1.ids == []):
                id = cell.getAttribute('id')
                #Si los ids ya vienen por defecto los cojemos y sino los generamos incrementado en 1 cada vuelta
                if cell.hasAttribute('id'):
                    self.Grid1.Cells[i].contentCell.id = int(cell.getAttribute('id'))
                    id2 = id
                else:
                    self.Grid1.Cells[i].contentCell.id = int(id2)
            #Cargamos los ids directamente de la matriz en caso que sea una imagen i tenga un vector de ids
            else:
                self.Grid1.Cells[i].contentCell.id = int(self.Grid1.ids[i])

            i = i+1
        return i

    def OnEvent(self,PointOfMouse):
        cont = 0
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]) and self.Grid1.ids[cont]!='-1' and self.resolts.count(cont) == 0:
                self.PressedCell.actualColorCell = Constants.colorCell
                self.PressedCell.contentCell.borders=False
                self.PressedCell = cell
                self.Grid2.writed = ''
                self.Grid2.numCharsAdded = 0
                self.result = ""
            cont+= 1



    def OnKeyEvent(self,key):

        print self.Grid1.ids
        self.result = self.Grid2.processKey(key)
        self.Grid2.printCursor(0, 0)
        print "result= ", self.result
        cont = 0
        contCeles = 0
        if (self.result!="" and len(self.resolts)<len(self.Grid1.Cells) ):
            for cell in self.Grid1.Cells:
                if(self.Grid1.ids[cont]!="-1"):
                    if (self.PressedCell == cell):
                        print "aki peta, cont = ", cont
                        idResposta = self.respostes[int(self.Grid1.ids[cont])].split('|')
                        for resposta in idResposta:
                            print "cont es ", cont
                            print "resposta correcta pot ser: ", resposta
                            if (self.result==resposta.upper()): # comparar_resultat(cell.idCell):
                                print "entra"
                                cell.contentCell.img = self.Grid3.Cells[cell.idCell].contentCell.img
                                self.PressedCell.actualColorCell = Constants.colorCell
				self.PressedCell.contentCell.borders=False
                                self.resolts.append(cont)
                                self.PressedCell.actualColorCell = Constants.colorCell

                                idsNegatius =  self.Grid1.ids.count('-1')
                                if(len(self.resolts) < len(self.Grid1.Cells) - idsNegatius):
                                    cont = self.NextPiece(cont) -1
                                    self.PressedCell = self.Grid1.Cells[cont+1]
                                else:
                                    self.PressedCell = None
                                    
                                self.Grid2.writed = ''
                                self.Grid2.numCharsAdded = 0
                                self.result = ""
                        break

                                #self.PressedCell.OnRender(display_surf)
                    contCeles += 1
                cont += 1
        #self.Grid2.writed = ''
        #self.Grid2.numCharsAdded = 0
        #self.result = ""

      

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
            self.PressedCell.actualColorCell = Constants.colorPressedCell
            self.PressedCell.OnRender(display_surf)


    def isOverActivity(self,PointOfMouse):
        return True

    def isGameFinished(self):
        '''finish = True
        for cell in self.Grid1.Cells:
            if cell.contentCell.img2 != None:
                finish = False'''
        idsNegatius =  self.Grid1.ids.count('-1')
        if(len(self.resolts) == len(self.Grid1.Cells) - idsNegatius ):
            return True
        return False


    def NextPiece(self, cont):
        i = cont+1
        j = 0
        while (j<len(self.Grid1.Cells)):
            if(i==len(self.Grid1.Cells)):
                i = 0
            if(self.Grid1.ids[i]!="-1") and self.resolts.count(i)==0:
                return i
            else:
                i += 1
                j += 1







