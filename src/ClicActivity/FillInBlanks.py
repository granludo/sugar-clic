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


class FillInBlanks(Activity):

    TextGrid = None
    
    '''Diccionari amb parells (idCell,encert)'''
    targets = {}
    options = True
    
    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading constants for the activity'''
        xmlTextGrid = self.xmlActivity.getElementsByTagName('document')[0]
        
        self.TextGrid = TextGrid(xmlTextGrid,self.mediaInformation,self.pathToMedia)
        
        self.targets = self.TextGrid.Load(display_surf,xmlTextGrid)


    def OnEvent(self,PointOfMouse):
        
        id = 0
        for cell in self.TextGrid.textCells:
            encert = cell.isOverCell(PointOfMouse[0],PointOfMouse[1])
            id += 1
            if encert:
                break
        
        if id in self.targets:
            self.targets[id] = encert

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        
        '''repintamos el grid...'''
        self.TextGrid.OnRender(display_surf)
        

    def isGameFinished(self):
        i = 0
        status = self.targets.values()
        '''Mira si els targets estan correctes o no'''
        for st in status:
            if not st:
                return False
        '''Si no ha retornat abans, tot esta correcte, acaba la activitat'''
        return True
    
