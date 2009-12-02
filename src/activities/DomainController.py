'''
Created on 09/05/2009

@author: mbenito
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