'''
Created on 09/05/2009

@author: mbenito
'''
from pygame.locals import *

import pygame
import pygame.locals
from  ContentCell import ContentCell
import Constants

class StyleGrid(object):
    transparent = False
    fontFamily = 'Arial'
    fontSize = 30
    fontBold= False
    fontItalic= False
    backgroundColor = Constants.colorBackground
    foregroundColor = Constants.colorWhite
    borderColor = Constants.colorCell
    hasBorder = True
    
     
    
    def __init__(self,xml):

        '''BackGround Color'''
        try:
            bgcolor =xml.getElementsByTagName('color')[0].getAttribute('background')
            self.backgroundColor = pygame.Color(hex(int(bgcolor, 16)))
        except:
            '''Default color'''
            pass
    
        '''foreground Color'''
        try:
            bgcolor =xml.getElementsByTagName('color')[0].getAttribute('foreground')
            self.foregroundColor = pygame.Color(hex(int(bgcolor, 16)))
        except:
            '''Default color'''
            pass
        
        '''borderColor Color'''
        try:
            bgcolor =xml.getElementsByTagName('color')[0].getAttribute('border')
            self.borderColor = pygame.Color(hex(int(bgcolor, 16)))
        except:
            '''Default color'''
            pass
