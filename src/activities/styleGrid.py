''' 
    This file is part of Sugar-Clic
    
    Sugar-Clic is copyrigth 2009 by Maria Jos� Casany Guerrero and Marc Alier Forment
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
    @copyrigth 2009 Marc Alier, Maria Jos� Casany marc.alier@upc.edu
    @copyrigth 2009 Universitat Politecnica de Catalunya http://www.upc.edu
    
    @autor Marc Alier
    @autor Jordi Piguillem
    
    @license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
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
