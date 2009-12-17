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
import pygame
import xml.dom.minidom
from pygame.locals import *
from ClicActivity.Point import Point
from ClicActivity.ExchangePuzzle  import ExchangePuzzle
from ClicActivity.MemoryGame  import MemoryGame
from ClicActivity.DoublePuzzle import DoublePuzzle 
from ClicActivity.InformationScreen import InformationScreen 
from ClicActivity.HolePuzzle import HolePuzzle
from ClicActivity.IdentifyPanels import IdentifyPanels
from ClicActivity.FinishActivity import FinishActivity
from ClicActivity.PanelsExplore import PanelsExplore
from ClicActivity.GeneralDialog import GeneralDialog
from ClicActivity.SimpleAssociation import SimpleAssociation
from ClicActivity.ComplexAssociation import ComplexAssociation
from ClicActivity import Constants


class ClicActivities:
    display = None
    path_to_clic = None
    mediaBagXML = None
    settingsXML = None
    
    def __init__(self, path, mediaTag, settingsTag,clic_name):
        print 'clicname = ',clic_name
        print 'path = ',path
        self.path_to_clic = path
        self.mediaBagXML = mediaTag
        self.settingsXML = settingsTag
        
    #starts the activity declared in activityTag
    def start_activity(self, activityTag):
        
        self.screen = pygame.display.get_surface()
        self.dialog = GeneralDialog()
        self.dialog.renderDialog(self.screen)
        
        '''HardCodded:creating the subsurface for ACTIVITIES'''
        weidth = Constants.MAX_WIDTH
        height = Constants.MAX_HEIGHT-(60)
        rectborder= Rect(0,0,weidth,height)
        self.activity_surf = self.screen.subsurface(rectborder)
       
        '''por si acaso no hay actividad'''
        
       
       
        if self.canExecuteActivity(activityTag):
           

                
            self.activityInUse = self.executeActivity(activityTag)
            self.activityInUse.pathToMedia = self.path_to_clic
            self.activityInUse.Load(self.activity_surf)
            self.dialog.printMessage(self.screen,self.activityInUse.getInitMessage())
        
        else: 
            ''' this case never ocurss.. teorically... heheheh'''
            self.activityInUse = FinishActivity(activityTag)
            
            self.dialog.printMessage(self.screen,'activitat no disponible' )
        
        '''Initial rendering'''
        self.activityInUse.OnRender( self.activity_surf)
	
       



    def update_activity(self, evento,isFirstActivity=False,isLastActivity=False):
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pointMouse = Point(pygame.mouse.get_pos())
            
            
            #Retornem -2 tractant la seguent activitat
            if self.dialog.isOverNextButton(pointMouse):                
                return -2

	        #Retornem -3 tractant l'activitat anterior
            if self.dialog.isOverPreviousButton(pointMouse):
                return -3

            #Retornem -1 perque es tracti al clic_player per tornar a comensar
            if self.dialog.isOverChangeClicButton(pointMouse):
                return -1
            
            if self.dialog.isOverActivity(pointMouse):
                self.activityInUse.OnEvent((pointMouse.getX(),pointMouse.getY()))
        
            self.activityInUse.OnRender( self.activity_surf)
            
            
            '''EXTRA:  if activity end, then print the end message '''
            if self.activityInUse.isGameFinished():
                 self.dialog.printMessage(self.screen,self.activityInUse.getFinishMessage())
                
            
        return 0
        #self.activityInUse.onRender(self.screen)
        # TODO
        # activity_class.update()
	# return resultats, temps, ...
    
    def canExecuteActivity(self,node):
        ''' at the end this function is not necessary'''
        print 'classtype=',node.getAttribute('class')
        if  node.getAttribute('class') =='@puzzles.ExchangePuzzle':
                        return True
        elif  node.getAttribute('class') =='@memory.MemoryGame':
                        return True
        elif  node.getAttribute('class') =='@puzzles.DoublePuzzle':
                        return True
        elif  node.getAttribute('class') =='@panels.InformationScreen':
                        return True
        elif  node.getAttribute('class') =='@puzzles.HolePuzzle':
                        return True
        elif  node.getAttribute('class') =='@panels.Identify':
                        return True
        elif  node.getAttribute('class') =='@panels.Explore':
                        return True
        elif  node.getAttribute('class') =='@associations.SimpleAssociation':
                        return True
        elif  node.getAttribute('class') =='@associations.ComplexAssociation':
                        return True
        else:
             return False
    def executeActivity(self,node):
        if node.getAttribute('class') =='@puzzles.ExchangePuzzle':
                        return ExchangePuzzle(node)
        elif  node.getAttribute('class') =='@memory.MemoryGame':
                        return MemoryGame(node)
        elif  node.getAttribute('class') =='@puzzles.DoublePuzzle':
                        return DoublePuzzle(node)
        elif  node.getAttribute('class') =='@panels.InformationScreen':
                        return InformationScreen(node)
        elif  node.getAttribute('class') =='@puzzles.HolePuzzle':
                        return HolePuzzle(node)
        elif  node.getAttribute('class') =='@panels.Identify':
                        return IdentifyPanels(node)
        elif  node.getAttribute('class') =='@panels.Explore':
                        return PanelsExplore(node)
        elif  node.getAttribute('class') =='@associations.SimpleAssociation':
                        return SimpleAssociation(node)
        elif  node.getAttribute('class') =='@associations.ComplexAssociation':
                        return ComplexAssociation(node)
                
