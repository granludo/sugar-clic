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
import os
import hulahop
##from sugar import env
##hulahop.startup(os.path.join(env.get_profile_path(), 'gecko'))
hulahop.startup('data/test')
import gtk
import gtk.glade
import gobject
from controller import Controller
import clic_player_data
from olpcgames import gtkEvent
import pygame
from browser import Browser


class clic_player:
    def __init__(self, runaslib = True):                
        self.clicked = False #is a clic chosen to download?
        self.selected = False #is a clic chosen to play?
        self.start = False #is a clic_activity running?
        self.newclic = False #check when a newclic is installed
        
        #loading application views
        self.xml = gtk.glade.XML('views.glade') 
        #loading window
        self.window = self.xml.get_widget('window')
        self.window.connect('delete_event', gtk.main_quit) 
        self.window.set_size_request(500,300)  
        # Get Windows child (Vertical Box with the views)
        self.w_child = self.window.get_child()  
        
        #loading main widget
        self.bD = self.xml.get_widget('buttonDownload')
        self.bD = self.bD.connect('clicked', self.__download_clics_view)   
        self.bAva = self.xml.get_widget('buttonAvailable')                
        self.bAva = self.bAva.connect('clicked', self.__available_clics_view)
        self.bSearch = self.xml.get_widget('buttonSearch')                
        self.bSearch = self.bSearch.connect('clicked', self.__search_clics_view)
        self.vboxMain = self.xml.get_widget('vboxMain')

        #loading download_clics widget   
        self.labelInfo = self.xml.get_widget('labelInfo')
        self.labelXo = self.xml.get_widget('labelXo')
        self.bDF = self.xml.get_widget('buttonDownloadFile')
        self.bDF.connect('clicked', self.__clic_selected)
        self.bDM = self.xml.get_widget('buttonDownMain')
        self.bDM.connect('clicked', self.__main_view)
        self.tree = self.xml.get_widget('treeviewClics')
        self.tree.connect('cursor-changed',self.__is_clicked)
        self.vboxDownload = self.xml.get_widget('vboxDownload')
        
        #loading available_clics widget 
        self.treeAvailable = self.xml.get_widget('treeviewAvailable')
        self.treeAvailable.connect('cursor-changed',self.__is_selected)
        self.bPM = self.xml.get_widget('buttonAvaMain')
        self.bPM.connect('clicked', self.__main_view)
        self.bGV = self.xml.get_widget('playClic')
        self.bGV.connect('clicked', self.__play_clics_view)
        self.vboxAvailable = self.xml.get_widget('vboxAvailable')
        
        #loading search_clics widget
        self.vboxBrowser = self.xml.get_widget('vboxBrowser')
        self.browser = Browser()
        self.bBM = self.xml.get_widget('button1')
        self.bBM.connect('clicked', self.__main_view)
        
        
        #loading play_clics widget
        self.vboxPlay = self.xml.get_widget('vboxPlay')
        #initialize play_clics area
        self.area = self.xml.get_widget('playArea')
        self.area.set_size_request(1024,768)
        #translates GTK events into Pygame events 
        t = gtkEvent.Translator(self.area)
        self.area.connect('map-event', self.__callback)
        t.hook_pygame()
        
        # self.widget will be attached to the Activity
        # This can be any GTK widget except a window
        self.widget = self.w_child
        
        #initiate controller
        self.controller = Controller()
        
        #loading data of the treeview (download_clic)
        clics_list = self.controller.get_clics_list()
        lstore = clic_player_data.add_clics_data(clics_list)
        self.tree.set_model(lstore)
        #adding columns to treeviews
        clic_player_data.put_columns(self.tree)
        clics = self.controller.get_installed_clics()
        lstore = clic_player_data.add_clics_data(clics)
        self.treeAvailable.set_model(lstore)
        clic_player_data.put_columns(self.treeAvailable)
        
        #runs the first view (main view)
        self.__main_view()
        
        if not runaslib: 
            self.window.show() 
            while True:
                self.updating()
                self.area.grab_focus()
                gtk.main_iteration(block=False)

    #calls the clic infinite times (until the clic ends) 
    def updating(self):        
        if self.start:
            nou = self.controller.updating_activity()
	    
	    if nou==-1:
		nou = 0
	    	self.__available_clics_view()
    
    #main view
    def __main_view(self,*args):
        self.vboxDownload.hide()
        self.vboxAvailable.hide()
        self.vboxPlay.hide()
        self.vboxBrowser.remove(self.browser)
        self.vboxBrowser.hide()
        self.vboxMain.show()
 
    #view to download clics
    def __download_clics_view(self, *args):     
        self.vboxMain.hide()           
        self.vboxAvailable.hide()
        self.vboxPlay.hide()
        self.vboxBrowser.remove(self.browser)
        self.browser.hide()
        self.vboxBrowser.hide()
        self.vboxDownload.show()
       
    #View to see the available clics in the computer and select one to play
    def __available_clics_view(self, *args):
        if self.start:
            #pygame.quit()
            self.start = False
        else:
            if self.newclic:
                clics = self.controller.get_installed_clics()
                lstore = clic_player_data.add_clics_data(clics)
                self.treeAvailable.set_model(lstore)
                self.newclic = False
        self.vboxBrowser.remove(self.browser)
        self.vboxBrowser.hide()
        self.vboxMain.hide()           
        self.vboxDownload.hide()
        self.vboxPlay.hide()
        self.vboxAvailable.show()
        
    #View that shows the clics (and its activities)
    def __play_clics_view(self, *args):
        if self.selected:
            clic = clic_player_data.get_clic_data(self.treeAvailable)
            self.controller.load_clic(clic['File'].split('.',1)[0]) 
            self.vboxBrowser.remove(self.browser)
            self.vboxBrowser.hide()
            self.vboxMain.hide()           
            self.vboxAvailable.hide()
            self.vboxDownload.hide()
            self.vboxPlay.show()
            self.selected = False
            
    #Browser -> find new clics
    def __search_clics_view(self, *args):
        self.vboxMain.hide()           
        self.vboxDownload.hide()
        self.vboxPlay.hide()
        self.vboxAvailable.hide()
        self.browser = Browser()
        self.browser.show()
        self.vboxBrowser.add(self.browser)
        self.vboxBrowser.show()
        self.browser.load_uri('http://wiki.laptop.org/go/Activities')

    #a clic is chosen to download    
    def __is_clicked(self, *args):
        self.clicked = True
     
    #a clic is chosen to play       
    def __is_selected(self, *args):
        self.selected = True
        
    #calls the controller to download and install a clic
    def __clic_selected(self, *args):
        if self.clicked:
            clic = clic_player_data.get_clic_data(self.tree)
            t = self.controller.add_new_clic(clic)
            if t == 0 :
                print 'File downloaded (clic_player)'
                self.newclic = True
            else:
               raise RuntimeError, 'File not downloaded' 
            self.clicked = False
    
    #connects the pygtk area with the pygame surface
    def __callback(self, *args):
            handle = self.area.window.xid
            os.environ['SDL_WINDOWID'] = str(handle)
            pygame.init()
            pygame.display.init()
            pygame.display.set_mode(self.area.size_request())
            self.__play_clic()
               
    #Initiates the clic 
    def __play_clic(self):
        self.controller.play_clic()
        self.start = True

#To execute outside the Xo laptop
if __name__=="__main__":
    clic_player(False)
        