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
from TextGrid import TextGrid
from Grid import Grid
from styleCell import StyleCell


class Identify(Activity):

    TextGrid = None
    targets = {} #Diccionari amb parells (idCell,encert) util quan hi ha optionLists
    pressedCells = []
    checkButton = None
    checkRect = None
    checkText = None
    finish = False

    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        
        '''Loading constants for the activity'''
        xmlTextGrid = self.xmlActivity.getElementsByTagName('document')[0]
        
        self.TextGrid = TextGrid(xmlTextGrid,self.mediaInformation,self.pathToMedia)

        self.targets = self.TextGrid.Load(display_surf,xmlTextGrid,True)

        try:
            self.checkText = self.xmlActivity.getElementsByTagName('checkButton')[0].firstChild.data
        except:
            self.checkText = 'Comprueba'
        
        self.checkButton = pygame.surface.Surface((self.TextGrid.Rect.width,40))
        self.checkButton.fill(Constants.colorCelestial)
        self.font = pygame.font.Font(None,30)
        self.checkRect = pygame.Rect((self.TextGrid.Rect.left,self.TextGrid.Rect.bottom - 40),(self.checkButton.get_size()))
        
        self.pressedCells = []
        
    def OnEvent(self,PointOfMouse):
        if self.checkRect.collidepoint(PointOfMouse[0],PointOfMouse[1]):
            self.finish = self.isCorrect()
            print self.finish
        else:
            for cell in self.TextGrid.textCells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    if cell.idCell in self.pressedCells:
                        self.pressedCells.remove(cell.idCell)
                    else:
                        self.pressedCells.append(cell.idCell)
        

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))

        '''repintamos el grid'''
        self.TextGrid.OnRender(display_surf)
        
        for i in self.pressedCells:
            pygame.draw.rect(display_surf,Constants.colorPressedCell,self.TextGrid.textCells[i].Rect,2)
        
        self.renderText(self.checkText,self.checkRect,self.font,self.checkButton,Constants.colorBlack)
        display_surf.blit(self.checkButton,self.checkRect)
        pygame.draw.rect(display_surf,Constants.colorBlack,self.checkRect,2)

    def isGameFinished(self):
        
        return self.finish
    
    def isCorrect(self):

        targetKeys = self.targets.keys()
        if len(self.pressedCells) == len(self.targets.keys()):
            for pressed in self.pressedCells:
                print pressed
                if pressed not in targetKeys:
                    return False
            return True
        else:
            return False
    