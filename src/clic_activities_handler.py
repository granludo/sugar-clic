''' 
    This file is part of Sugar-Clic
    
    Sugar-Clic is copyrigth 2009 by Maria José Casany Guerrero and Marc Alier Forment
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
    @copyrigth 2009 Marc Alier, Maria José Casany marc.alier@upc.edu
    @copyrigth 2009 Universitat Politecnica de Catalunya http://www.upc.edu
    
    @autor Marc Alier
    @autor Jordi Piguillem
    
    @license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
'''
import pygame
from   GeneralDialog import GeneralDialog
from Point import Point

import xml.dom.minidom
from  ExchangePuzzle  import ExchangePuzzle
from  MemoryGame  import MemoryGame
from  DoublePuzzle import DoublePuzzle 
from  InformationScreen import InformationScreen 
from  HolePuzzle import HolePuzzle
from  IdentifyPanels import IdentifyPanels
from  FinishActivity import FinishActivity
from  PanelsExplore import PanelsExplore
import Constants
import pygame
from pygame.locals import *

class ClicActivities:
    display = None
    
    def __init__(self, path, mediaTag, settingsTag,clic_name):
        print 'clicname = ',clic_name
        print 'path = ',path
        self.path_to_clic = path
        self.mediaBagXML = mediaTag
        self.settingsXML = settingsTag
        
    #starts the activity declared in activityTag
    def start_activity(self, activityTag):
# Inicialize screen and buttons of ClicXO
        self.screen = pygame.display.get_surface()
        self.dialog = GeneralDialog()
        self.dialog.renderDialog(self.screen)
        
        '''HardCodded:creating the subsurface for ACTIVITIES'''
        weidth = Constants.MAX_WIDTH -(Constants.MARGIN_LEFT+Constants.MARGIN_RIGHT)
        height = Constants.MAX_HEIGHT-(Constants.MARGIN_TOP+Constants.MARGIN_BOTTOM)
        rectborder= Rect(30,30,weidth,height)
        self.activity_surf = self.screen.subsurface(rectborder)
        
        '''por si acaso no hay actividad'''
        
       
       
        if self.canExecuteActivity(activityTag):
           
      
            self.activityInUse = self.executeActivity(activityTag)
            self.activityInUse.pathToMedia = self.path_to_clic
            self.activityInUse.Load(self.screen)
        
        else: 
            self.activityInUse = FinishActivity(activityTag)
            
            self.dialog.printMessage(self.screen,'activitat no disponible' )
        
        
	#Prova: mostrem per pantalla el nom de l'activitat actual de la sequencia	
       

        # TODO
	# Recollir parametres i class de clic_activity
	# executar activity_class.main(parametres)


    def update_activity(self, evento):
        
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
                     self.activityInUse.OnEvent((pointMouse.getX()-32,pointMouse.getY()-32))

            
        
        
        self.activityInUse.OnRender( self.activity_surf)
            
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
                
