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
from TextGrid import TextGrid
from Grid import Grid
from styleCell import StyleCell
from CheckButton import CheckButton


class TextComplete(Activity):

    TextGrid = None
    
    pressedCell = None
    checkButton = None
    finish = False
    
    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        
        '''Loading constants for the activity'''
        xmlTextGrid = self.xmlActivity.getElementsByTagName('document')[0]
        
        self.TextGrid = TextGrid(xmlTextGrid,self.mediaInformation,self.pathToMedia)
        
        self.TextGrid.Load(display_surf,xmlTextGrid,'complete')
        
        try:
            checkText = xmlActivity.getElementsByTagName('checkButton')[0].firstChild.data
        except:
            checkText = 'Comprueba'
            
        self.checkButton = CheckButton(checkText)
        
        self.finish = False
        
        
    def OnEvent(self,PointOfMouse):
        
        if self.checkButton.isOverCheck(PointOfMouse[0],PointOfMouse[1]):
            self.finish = self.isCorrect()
            '''Si no es correcte, reproduim so d'error'''
            if not self.finish:
                self.play_sound(Constants.Sounds.FINISH_ERROR)
        else:
            for cell in self.TextGrid.textCells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    self.pressedCell = cell
            
    def OnKeyEvent(self,key):
        
        if self.pressedCell != None:
            self.pressedCell.contentCell.processKey(key)
                
            

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))

        '''repintamos el grid'''
        self.TextGrid.OnRender(display_surf)
        
        self.checkButton.OnRender(display_surf)

    def isGameFinished(self):
        return self.finish
    
    def isCorrect(self):
        for cell in self.TextGrid.textCells:
            if cell.contentCell.writed.upper() != cell.contentCell.answer:
                return False
        '''Si cap esta malament, tot esta correcre i acaba el joc'''
        return True
    
