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
import PanelsExplore


import Constants


from os.path import isdir
import sys, zipfile, os, os.path
from os import mkdir
import xml.dom.minidom
from  ExchangePuzzle  import ExchangePuzzle
from  MemoryGame  import MemoryGame
from  DoublePuzzle import DoublePuzzle 
from  InformationScreen import InformationScreen 
from  HolePuzzle import HolePuzzle
from  IdentifyPanels import IdentifyPanels
from  FinishActivity import FinishActivity
from  PanelsExplore import PanelsExplore

from xml.dom.minidom import parse
 
import os,sys
class DomainController(object):
    #vector of activities
    ActivityList = None
    actualActivity = None
    prevActivity = None
    ################## os.getcwd()##############
   
    def __init__(self):
        print 'executing domain controller'
        
        '''HARDCODED 
        This part will be replaced by the sequencer package
        '''
        
        dom = parse(os.getcwd()+'/../media/orientat.jclic')
        self.ActivityList = dom.getElementsByTagName('activity')

 

    def nextActivity(self):
        
        '''obtaining next actitivy'''
        
        hemPassatLaAnterior = False
        
        if self.actualActivity == None:
            hemPassatLaAnterior = True
            
        for node in self.ActivityList:  
            if hemPassatLaAnterior:
                if self.canExecuteActivity(node):
                    self.actualActivity = node.getAttribute('name')
                    return self.executeActivity(node)
            else:
                if node.getAttribute('name') == self.actualActivity:
                    hemPassatLaAnterior = True
                    self.prevActivity = node

        ''' This  is the end of activities. We dont know more activities
            we load a the empty, FinishActivity
        '''   
       
        self.actualActivity = None
        
        return FinishActivity(node)
            
                
    def canExecuteActivity(self,node):
        ''' at the end this function is not necessary'''
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
        


    def previousActivity(self):
        print 'Not implemented'
        '''This part will be similar to nextActivity'''