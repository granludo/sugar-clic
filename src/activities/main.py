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
from pygame.locals import *

from GeneralDialog  import GeneralDialog
from Activity import Activity
import Constants
from Point import Point
from DomainController import DomainController



class MainApp:
    display_surf = None
    activity_surf = None
    Activity = None
    GeneralInfo = None
    controller = None
    def __init__(self): 
        self._running = True
        self._surf_display = None
 
    def OnInit(self):
        pygame.init()
        self.controller = DomainController()
        
        self.display_surf = pygame.display.set_mode((Constants.MAX_WIDTH,Constants.MAX_HEIGHT), pygame.HWSURFACE)
        '''Inicialitzem GeneralDialog'''
        self.GeneralInfo = GeneralDialog()
        self.GeneralInfo.__init__()
        self.GeneralInfo.renderDialog(self.display_surf)
        self.GeneralInfo.printMessage(self.display_surf,"")
        self._running = True
        
        '''HardCodded:creating the subsurface for ACTIVITIES'''
        weidth = Constants.MAX_WIDTH -(Constants.MARGIN_LEFT+Constants.MARGIN_RIGHT)
        height = Constants.MAX_HEIGHT-(Constants.MARGIN_TOP+Constants.MARGIN_BOTTOM)
        rectborder= Rect(30,30,weidth,height)
        self.activity_surf = self.display_surf.subsurface(rectborder)
        
        
        '''Loading  the firs activity'''
        self.Activity = self.controller.nextActivity()
        self.Activity.Load(self.activity_surf)
        '''Init_message activity into MESSAGE_DIALOG'''
        self.GeneralInfo.printMessage(self.display_surf, self.Activity.getInitMessage())
               
    def OnEvent(self, event):
        if event.type == QUIT:
            self._running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pointMouse = Point(pygame.mouse.get_pos())
            
            if  self.GeneralInfo.isOverNextButton(pointMouse) :
                '''is over Next Button'''
                self.Activity = self.controller.nextActivity();
                self.Activity.Load(self.activity_surf)
                self.GeneralInfo.renderDialog(self.display_surf)
                '''Init_message activity into MESSAGE_DIALOG'''
                self.GeneralInfo.printMessage(self.display_surf, self.Activity.getInitMessage())
                           
            elif  self.GeneralInfo.isOverPreviousButton(pointMouse):
                '''is over Previous Button''' 
            elif self.isOverActivity(pointMouse):
                
                self.Activity.OnEvent((pointMouse.getX()-32,pointMouse.getY()-32))
            else :
                '''mousebutton down'''
        
    def OnLoop(self):
        if self.Activity.isGameFinished():
            self.GeneralInfo.printMessage(self.display_surf,self.Activity.getFinishMessage())

    def OnRender(self):
        '''Delegate to Activity render'''
        self.Activity.OnRender(self.activity_surf)
        
        '''General dialog isnt modifyed --> no render '''
        pygame.display.flip()
        pass
    
    def OnCleanup(self):
        pygame.quit()
        
    def isOverActivity(self,pointMouse):
        '''TODO, now all surface represents that mouse is over activity'''
        return True
    def OnExecute(self):
       
        if self.OnInit() == False:
            self._running = False
            
        while( self._running ):
            for event in pygame.event.get():
                self.OnEvent(event)
            self.OnLoop() 
            self.OnRender()
        self.OnCleanup()
 

if __name__ == "__main__" :
    theApp = MainApp()
    theApp.OnExecute()


