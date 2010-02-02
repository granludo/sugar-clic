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
import random

import controller
from clicActivitiesHandler import ClicActivities


class Sequencer:
    def __init__(self):
        self.index = 0 #current activity position of the sequence    
        self.activities = [] #name of the activities 
        self.size = 0 #number of activities in the sequence
        
    #load the clic sequence information
    def begin_sequence(self, sequence, mediaBag, settings, clic_path,clic_name):
        #get all the names of the activities (inside the sequence)
        self.activities = []
        for item in sequence.getElementsByTagName('item'):
            self.activities.append(item.getAttribute('name'))            
        self.size = self.activities.__len__()
        self.act_handler = ClicActivities(clic_path, mediaBag, settings,clic_name)
    
    #play clic
    def play(self):
        self.index = 0
        self.controller = controller.Controller() #gets a controller instance (necessary to have activity tags)
        clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
        self.__start_pygame_view() #initiate pygame view
        self.act_handler.start_activity(clic_activity, self.screen, True, False)#initiate activity view
    
    #function called all the time to refresh the screen and the activity
    #also returns activity information
    #return values:
    # -1 : go back to MyClics View of the application
    # -2 : go to the next Activity
    # -3 : go to the previous Activity
    # -4 : go to the first Activity
    # -5 : go to the last Activity
    # -6 : restart the current Activity
    # -7 : go back to the Main View of the application
    def activity_clic_information(self):
        # Pygame updating
        if not self.exit:
            pygame.display.flip()

            for evento in pygame.event.get():
                #With resultat we controll what we do next
                resultat = self.act_handler.update_activity(evento)    

                first = False
                last = False

                #Next activity
                if(resultat == -2 and self.index < self.size-1):
                    #searching for a new and valid clic activity
                    while (self.index < self.size-1):
                        self.index = self.index + 1
                        if(self.index == self.size-1):
                            last = True
                        clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                        if self.act_handler.canExecuteActivity(clic_activity):
                            self.act_handler.start_activity(clic_activity, self.screen, first, last)#initiate activity view
                            break
        
                #Previous activity
                if(resultat == -3 and self.index > 0):
                    #searching for a new and valid clic activity
                    while (self.index > 0):
                        self.index = self.index - 1
                        if (self.index == 0):
                            first = True
                        clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                        if self.act_handler.canExecuteActivity(clic_activity):
                            self.act_handler.start_activity(clic_activity, self.screen, first, last)#initiate activity view
                            break
                        
                #First activity of the sequence
                if (resultat == -4) :
                    self.index = 0
                    first = True
                    clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                    if self.act_handler.canExecuteActivity(clic_activity):
                        self.act_handler.start_activity(clic_activity, self.screen, first, last)#initiate activity view
                        break
                      
                #Last activity of the sequence  
                if (resultat == -5) :
                    last = True
                    self.index = self.size - 1
                    clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                    if self.act_handler.canExecuteActivity(clic_activity):
                        self.act_handler.start_activity(clic_activity, self.screen, first, last)#initiate activity view
                        break         
                    
                #Restart the current activitytrue
                if (resultat == -6) :
                    clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                    self.act_handler.start_activity(clic_activity, self.screen)#initiate activity view
                    break   
                    
                #Return -7 to go to the main view of the application
                if (resultat == -7) :           
                    return -7
            
                #Return -1 to see available clics
                if(resultat == -1):
                    return -1            
    
                if evento.type == pygame.QUIT:
                    self.exit = True
        
        if self.exit:
            exit()
        pygame.event.clear()
        return 0 #should returns activity_clic information
    
    #this function is to init all the pygame variables (screen, mouse,...)
    def __start_pygame_view(self):
        #Pygame initiation
        self.screen = pygame.display.get_surface()
        self.exit= False
        
    



