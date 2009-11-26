import pygame
import random
from clic_activities_handler import ClicActivities
import controller
from sugar.graphics.toolbutton import ToolButton


class Sequencer:
    def __init__(self):
        self.index = 0 #current activity position of the sequence    
        self.activities = [] #name of the activities 
        self.size = 0 #number of activities in the sequence
        
    #load the clic sequence information
    def begin_sequence(self, sequence, mediaBag, settings, clic_path):
        #get all the names of the activities (inside the sequence)
        for item in sequence.getElementsByTagName('item'):
            self.activities.append(item.getAttribute('name'))
            
        self.size = self.activities.__len__()
        self.act_handler = ClicActivities(clic_path, mediaBag, settings)
    
    #play clic
    def play(self):
        self.index = 0
        self.controller = controller.Controller() #gets a controller instance (necessary to have activity tags)
        clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
        self.__start_pygame_view() #initiate pygame view
        self.act_handler.start_activity(clic_activity)#initiate activity view
    
    #function called all the time to refresh the screen and the activity
    #also returns activity information
    def activity_clic_information(self):
        # Pygame updating
        if not self.exit:
            pygame.display.flip()

            for evento in pygame.event.get():
    
                #With resultat we controll what we do next
                resultat = self.act_handler.update_activity(evento)    
    
                #Next activity
                if(resultat == -2 and self.index < self.size-1):
                    self.index = self.index + 1
                    clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                    self.act_handler.start_activity(clic_activity)#initiate activity view
        
                #Previous activity
                if(resultat == -3 and self.index > 0):
                    self.index = self.index - 1
                    clic_activity = self.controller.get_clic_activity(self.activities[self.index]) #gets the first activity(tag) of the sequence
                    self.act_handler.start_activity(clic_activity)#initiate activity view
            
            
                #Return -1 to see available clics, controled in clic_player.py
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
        self.exit= False



