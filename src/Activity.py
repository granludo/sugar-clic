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

# Load GTK
import Constants
import pygame
from styleCell import StyleCell
import os
class Activity(object):
    xmlActivity = None
    containerBg = None
    pathToMedia = None
    
    def __init__(self,xmlActivity):
        
        self.xmlActivity = xmlActivity
        
    def OnEvent(self,PointOfMouse):
        print 'MOTHER CLASS'
    def OnLoop(self):
        print 'MOTHER CLASS'
    def OnRender(self,display_surf):
        print 'MOTHER CLASS'
    def setBgColor(self):
        '''Background Activity'''
        ''' this function runs so wrong, the bgcolor is in Container-> bgColor not in  gradient'''
        try: 
            bgColor = self.xmlActivity.getElementsByTagName('gradient')[0].getAttribute('source')
            intcolor =  int(bgColor, 16)
            self.containerBg = pygame.Color(hex(intcolor))
        except:
            try:
                bgColor = self.xmlActivity.getElementsByTagName('container')[0].getAttribute('bgColor')
                intcolor =  int(bgColor, 16)
                self.containerBg = pygame.Color(hex(intcolor))
            except:
                '''No bgColor'''
                self.containerBg = Constants.colorBackground
        ''' Background Grid'''

    def Load(self,display_surf):
        print 'MOTHER CLASS'
    def isOverActivity(self,PointOfMouse):
        return True
    def isGameFinished(self):
        print 'MOTHER CLASS'
        
    def getFinishMessage(self):
        '''Recuperamos mensaje de  fin partida'''
        try: 
            cells = self.xmlActivity.getElementsByTagName('messages')[0]
            cells = cells.getElementsByTagName('cell')
            for cell in cells:
                if cell.getAttribute('type')  == 'final':
                    text = cell.getElementsByTagName('p')[0].firstChild.nodeValue
            return text
        except:
            return ""
    def getInitMessage(self):
        '''Recuperamos mensaje de  fin partida'''
        try:
            cells = self.xmlActivity.getElementsByTagName('messages')[0]
            cells = cells.getElementsByTagName('cell')
            for cell in cells:
                if cell.getAttribute('type')  == 'initial':
                    text = cell.getElementsByTagName('p')[0].firstChild.nodeValue
                    return text
        except:
            return ""
        
    def printxmlCellinCell(self,cell,xmlcell2):    
       
        styleCell  = StyleCell(xmlcell2)
        
        
        if styleCell.transparent == False:
            cell.contentCell.img.fill(styleCell.backgroundColor)
    
    
        ''' Image in cell'''
        try:
            pathImage =xmlcell2.getAttribute('image')  
            imagePath = self.pathToMedia+'/'+pathImage
    
            newImg = pygame.image.load(imagePath).convert_alpha()
    
            newImg = pygame.transform.scale(newImg, ( cell.contentCell.img.get_width(),  cell.contentCell.img.get_height()))
            cell.contentCell.img.blit(newImg,(0,0))
        except:
            pass
        '''Text in cell'''
        elementP = xmlcell2.getElementsByTagName('p')
        if elementP.length !=0:
            texto = elementP[0].firstChild.nodeValue
            font = pygame.font.Font(None, styleCell.fontSize)
            text = font.render(texto, True, styleCell.foregroundColor)
            
            '''Center text  -- horitzontal/vertical'''
            try:
                '''TODO'''
                '''Center cell...'''
                centerPosition = (20,20)
            except:
                '''Not centered'''
                centerPosition = (0,0)
        
            '''Blit text'''
            cell.contentCell.img.blit(text,centerPosition)
        
        ''' Border in cell'''
        cell.contentCell.border = styleCell.hasBorder
    def calculateCoef(self,width,height):
        coefWidth =  Constants.ACTIVITY_WIDTH /width
        coefHeight = Constants.ACTIVITY_HEIGHT / height
            
        if coefWidth < coefHeight:
            coef = coefWidth
        else:
            coef = coefHeight
        return coef
    
 