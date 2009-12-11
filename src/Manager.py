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
import paths
hulahop.startup(paths.application_data_path + '/test')
import gtk
import gtk.glade
import gobject
from controller import Controller
import ManagerData
from olpcgames import gtkEvent
import pygame
from browser import Browser



class Manager:
    def __init__(self, runaslib = True):                
        self.clicked = False #is a clic chosen to download?
        self.selected = False #is a clic chosen to play?
        self.start = False #is a clic_activity running?
        self.newclic = False #check when a newclic is installed
        self.isBrowseActivated = False #check if the Browse is activated
        self.iterate = True #execute the app?
        self.firstWs = True #first call to the web service?
        
        
        img_app_path = os.path.join(paths.application_bundle_path, 'img/app') 
        views_path = os.path.join(img_app_path, 'appViews')
        icons_path = os.path.join(img_app_path, 'appIcons')
        
#        self.window.connect('delete_event', gtk.main_quit) 
#        #self.window.set_size_request(800,600)  
#        # Get Windows child (Vertical Box with the views)
#        self.w_child = self.window.get_child()  
#      
        
        #loading application views
        self.xmlMain = gtk.glade.XML(views_path + '/windowApp.glade')
        #loading window (OLPC has it owns window - not this one)
        self.window = self.xmlMain.get_widget('window')
        self.window.connect('delete_event', self.__destroy) 

        # Get Windows child (Vertical Box with the views)
        self.w_child = self.window.get_child()      
        if runaslib:
            gtk.Container.remove(self.window, self.w_child)
        
        
        self.xml = gtk.glade.XML(views_path + '/mainView.glade') 
        self.win = self.xml.get_widget('window')
        self.Main = self.xml.get_widget('Main')
        #remove parent (in glade there is always a parent (window))
        gtk.Container.remove(self.win ,self.Main)
        self.bMy = self.xml.get_widget('buttonMyClics')
        self.bMy = self.bMy.connect('clicked', self.__available_clics_view)
        self.ImageMy = self.xml.get_widget('imageMyClics')
        self.ImageMy.set_from_file(icons_path + '/myclics.png')
        self.bAbout = self.xml.get_widget('buttonAbout')
        self.ImageAbout = self.xml.get_widget('imageAbout')
        self.ImageAbout.set_from_file(icons_path + '/about.png')
        
        if not runaslib:
            self.hboxWS = self.xml.get_widget('hboxWS')
            self.bD = self.xml.get_widget('buttonDownload')
            self.bD = self.bD.connect('clicked', self.__download_clics_view)  
            self.hboxWS.show()
            #loading download_clics widget  
            self.xml = gtk.glade.XML(views_path + '/WSview.glade') 
            self.winDow = self.xml.get_widget('window')

            self.labelInfo = self.xml.get_widget('labelInfo')
            self.labelXo = self.xml.get_widget('labelXo')
            self.bDF = self.xml.get_widget('buttonDownloadFile')
            self.bDF.connect('clicked', self.__clic_selected)
            self.bDM = self.xml.get_widget('buttonDownMain')
            self.bDM.connect('clicked', self.__main_view)
            self.tree = self.xml.get_widget('treeviewClics')
            self.tree.connect('cursor-changed',self.__is_clicked)
            self.vboxDownload = self.xml.get_widget('vboxDownload')
            #remove parent (in glade there is always a parent (window))
            gtk.Container.remove(self.winDow ,self.vboxDownload)
            


#        #loading main widget
#        self.bD = self.xml.get_widget('buttonDownload')
#        self.bD = self.bD.connect('clicked', self.__download_clics_view)   
#        self.ImageD = self.xml.get_widget('imageDownload')
#        img_path = os.path.join(paths.application_bundle_path, 'img') 
#        self.ImageD.set_from_file(img_path + '/download.jpg')
#        self.ImageS = self.xml.get_widget('imageSearch')
#        self.ImageS.set_from_file(img_path + '/lupa.JPG')
#        self.ImageAva = self.xml.get_widget('imageAvailable')
#        self.ImageAva.set_from_file(img_path + '/caja.jpg')
#        self.bAva = self.xml.get_widget('buttonAvailable')                
#        self.bAva = self.bAva.connect('clicked', self.__available_clics_view)
#        self.bSearch = self.xml.get_widget('buttonSearch')                
#        self.bSearch = self.bSearch.connect('clicked', self.__search_clics_view)
#        self.vboxMain = self.xml.get_widget('vboxMain')
#



       
        #loading available_clics widget 
        self.xml = gtk.glade.XML(views_path + '/MyClicsView.glade') 
        #loading window
        self.windowAva = self.xml.get_widget('window')
        self.treeAvailable = self.xml.get_widget('treeviewAvailable')
        self.treeAvailable.connect('cursor-changed',self.__is_selected)
        self.bPM = self.xml.get_widget('buttonAvaMain')
        self.bPM.connect('clicked', self.__main_view)
        self.bGV = self.xml.get_widget('playClic')
        self.bGV.connect('clicked', self.__play_clics_view)
        self.vboxAvailable = self.xml.get_widget('vboxAvailable')
        gtk.Container.remove(self.windowAva, self.vboxAvailable)


     
#        #loading search_clics widget
#        self.vboxBrowser = self.xml.get_widget('vboxBrowser')
#        self.browser = Browser()
#        self.bBM = self.xml.get_widget('buttonHome')
#        self.bBM.connect('clicked', self.__main_view)
#        self.ImageBr = self.xml.get_widget('imageHome') 
#        self.ImageBr.set_from_file(img_path + '/home.png')
        

      
        #loading play_clics widget
        self.xml = gtk.glade.XML(views_path + '/PlayView.glade') 
        #loading window
        self.windowPlay = self.xml.get_widget('window')
        self.vboxPlay = self.xml.get_widget('vboxPlay')
        #initialize play_clics area
        self.area = self.xml.get_widget('playArea')
        self.area.set_size_request(1024,768)
        #translates GTK events into Pygame events 
        t = gtkEvent.Translator(self.area)
        self.area.connect('map-event', self.__callback)
        t.hook_pygame()
        gtk.Container.remove(self.windowPlay, self.vboxPlay)
        
                
        # self.widget will be attached to the XO-Activity
        # This can be any GTK widget except a window
        self.widget = self.w_child
        

        #initiate controller
        self.controller = Controller()
 
        clics = self.controller.get_installed_clics()
        lstore = ManagerData.add_clics_data(clics)
        self.treeAvailable.set_model(lstore)
        ManagerData.put_columns(self.treeAvailable)

        self.current_view = self.Main
        self.w_child.add(self.current_view)
        
        if not runaslib: 
            self.window.show() 
            while self.iterate == True:
                gtk.main_iteration(block=False)
                self.updating()
                self.area.grab_focus()

    def __destroy(self, *args):
        self.iterate = False

    #calls the clic infinite times (until the clic ends) 
    def updating(self):        
        if self.start:
            nou = self.controller.updating_activity()    
	    if nou==-1:
                nou = 0
                self.__available_clics_view()
    
    #main view
    def __main_view(self,*args):
        self.w_child.remove(self.current_view)
        self.current_view = self.Main
        self.w_child.add(self.current_view)
#        self.vboxDownload.hide()
#        self.vboxAvailable.hide()
#        if self.isBrowseActivated:
#            self.vboxBrowser.remove(self.browser)
#        self.vboxBrowser.hide()
#        self.vboxMain.show()
 
    #view to download clics
    def __download_clics_view(self, *args):  
        if self.firstWs == True:
            self.firstWs = False
            #loading data of the treeview (download_clic)
            clics_list = self.controller.get_clics_list()
            lstore = ManagerData.add_clics_data(clics_list)
            self.tree.set_model(lstore)
            #adding columns to treeviews
            ManagerData.put_columns(self.tree)
        self.w_child.remove(self.current_view)
        self.current_view = self.vboxDownload
        self.w_child.add(self.current_view)   
#        self.vboxMain.hide()           
#        self.vboxAvailable.hide()
#        self.vboxPlay.hide()
#        if self.isBrowseActivated:
#            self.vboxBrowser.remove(self.browser)
#        self.vboxBrowser.hide()
#        self.vboxDownload.show()
       
    #View to see the available clics in the computer and select one to play
    def __available_clics_view(self, *args):
        if self.start:
            self.start = False
        else:
            if self.newclic:
                clics = self.controller.get_installed_clics()
                lstore = ManagerData.add_clics_data(clics)
                self.treeAvailable.set_model(lstore)
                self.newclic = False
#        if self.isBrowseActivated:
#            self.vboxBrowser.remove(self.browser)
        if (self.current_view == self.vboxPlay):
            self.vboxPlay.hide()
            self.current_view = self.vboxAvailable
            self.w_child.add(self.current_view)  
        else :
            self.w_child.remove(self.current_view)
            self.current_view = self.vboxAvailable
            self.w_child.add(self.current_view)        
#        self.vboxBrowser.hide()
#        self.vboxMain.hide()           
#        self.vboxDownload.hide()
#        self.vboxPlay.hide()
#        self.vboxAvailable.show()
        
    #View that shows the clics (and its activities)
    def __play_clics_view(self, *args):
        if self.selected:
            clic = ManagerData.get_clic_data(self.treeAvailable)
            self.controller.load_clic(clic['File'].split('.',1)[0])
#            if self.isBrowseActivated: 
#                self.vboxBrowser.remove(self.browser)

            self.w_child.remove(self.current_view)
            self.vboxPlay.show()
            self.current_view = self.vboxPlay
            self.w_child.add(self.current_view)    
#            self.vboxBrowser.hide()
#            self.vboxMain.hide()           
#            self.vboxAvailable.hide()
#            self.vboxDownload.hide()
#            self.vboxPlay.show()
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
        self.isBrowseActivated = True

    #a clic is chosen to download    
    def __is_clicked(self, *args):
        self.clicked = True
     
    #a clic is chosen to play       
    def __is_selected(self, *args):
        self.selected = True
        
    #calls the controller to download and install a clic
    def __clic_selected(self, *args):
        if self.clicked:
            self.labelInfo.set_text('Clics')
            clic = ManagerData.get_clic_data(self.tree)
            t = self.controller.add_new_clic(clic)
            if t == 0 :
                print 'File downloaded (Manger)'
                self.labelInfo.set_text(clic['Title'] + ' downloaded')
                self.newclic = True
            else:
                self.labelInfo.set_text(clic['Title'] + ' not downloaded')
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
    Manager(False)
        
