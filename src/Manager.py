# -*- coding: utf-8 -*-
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
from sugar.activity import activity
import os
import hulahop
import paths

import gtk
import gtk.glade
import gobject

try:
    hula_path = os.path.join(activity.get_activity_root(), 'data/test')
    hulahop.startup(hula_path)
except RuntimeError:
    hula_path = os.path.join(os.getcwd(), 'data/test')
    hulahop.startup(hula_path)

from gettext import gettext as _
from controller import Controller
import ManagerData
from olpcgames import gtkEvent
import pygame
from browser import Browser
from ClicActivity import Constants



class Manager:
    def __init__(self, runaslib = True):                
        self.clicked = False #is a clic chosen to download?
        self.selected = False #is a clic chosen to play?
        self.start_clic_view = False #is a clic_activity running?
        
        #if runaslib = True -> we are in a Xo laptop
        paths.set_environment(runaslib)
        
        img_app_path = os.path.join(paths.application_bundle_path, 'img/app') 
        views_path = os.path.join(img_app_path, 'appViews')
        icons_path = os.path.join(img_app_path, 'appIcons')
        self.icons_path = icons_path

#              
        #loading application views
        self.xmlMain = gtk.glade.XML(views_path + '/windowApp.glade')
        #loading window (OLPC has it owns window - not this one)
        self.window = self.xmlMain.get_widget('window')
        self.window.connect("destroy", gtk.main_quit)

        # Get Windows child (Vertical Box with the views)
        self.w_child = self.window.get_child()  

        if runaslib:
            gtk.Container.remove(self.window, self.w_child)
        else :
            state = gtk.STATE_NORMAL    
            color = gtk.gdk.Color("orange")
            self.window.modify_bg(state, color)
        
        #loading main view
        self.xml = gtk.glade.XML(views_path + '/mainView.glade') 
        self.win = self.xml.get_widget('window')
        self.Main = self.xml.get_widget('Main')
        #remove parent (in glade there is always a parent (window))
        gtk.Container.remove(self.win ,self.Main)
        
        self.ImageSearch = self.xml.get_widget('imageTitle')
        self.ImageSearch.set_from_file(icons_path + '/title.png')  
        
        #MyClics button
        self.bMy = self.xml.get_widget('buttonMyClics')
        self.bMy.connect('clicked', self.__available_clics_view)
        self.bMy.connect('enter', self.__change_icon, '/clics_2.png', 0) 
        self.bMy.connect('leave', self.__change_icon, '/clics.png', 0) 
        self.ImageMy = self.xml.get_widget('imageMyClics')
        self.ImageMy.set_from_file(icons_path + '/clics.png')

        #Manual button
        self.bManual = self.xml.get_widget('buttonManual')
        self.bManual.connect('clicked', self.__about_view)
        self.bManual.connect('enter', self.__change_icon, '/manual_2.png', 1) 
        self.bManual.connect('leave', self.__change_icon, '/manual.png', 1) 
        self.ImageManual = self.xml.get_widget('imageManual')
        self.ImageManual.set_from_file(icons_path + '/manual.png')
        
        #About button
        self.bAbout = self.xml.get_widget('buttonAbout')
        self.bAbout.connect('clicked', self.__about_view)
        self.bAbout.connect('enter', self.__change_icon, '/about_2.png', 2) 
        self.bAbout.connect('leave', self.__change_icon, '/about.png', 2) 
        self.ImageAbout = self.xml.get_widget('imageAbout')
        self.ImageAbout.set_from_file(icons_path + '/about.png')
        
        #Search button
        self.bS = self.xml.get_widget('buttonSearch')
        self.bS.connect('clicked', self.__search_clics_view) 
        self.bS.connect('enter', self.__change_icon, '/download_2.png', 3) 
        self.bS.connect('leave', self.__change_icon, '/download.png', 3) 
        self.ImageSearch = self.xml.get_widget('imageSearch')
        self.ImageSearch.set_from_file(icons_path + '/download.png')    
        
        #set the labels to translate
        self.labelMan = self.xml.get_widget('labelManual')
        self.labelMan.set_text(_('MANUAL'))
        self.labelAbout = self.xml.get_widget('labelAbout')
        self.labelAbout.set_text(_('ABOUT SUGARCLIC'))    
        self.labelSearch = self.xml.get_widget('labelSearch')
        self.labelSearch.set_text(_('DOWNLOAD CLICS'))
        self.labelMYCLICS = self.xml.get_widget('labelMyClics')
        self.labelMYCLICS.set_text(_('MY CLICS'))
  
  
  
  
        #loading My Clics View
        self.xml = gtk.glade.XML(views_path + '/MyClicsView.glade') 
        #loading window
        self.windowAva = self.xml.get_widget('window')
        
        self.iconView = self.xml.get_widget('iconviewAvailable')
        self.iconView.connect('selection-changed', self.__clics_view) #item-activated 2 clicks //selection-changed 1 click
        
        self.bClics = self.xml.get_widget('buttonClics')
        self.bClics.connect('clicked', self.__generate_list)
        self.currentClicsView = 'Clics'
                         
        self.bPM = self.xml.get_widget('buttonAvaMain')
        self.bPM.connect('clicked', self.__main_view)
                        
        self.labelMy = self.xml.get_widget('labelMyClics')
        self.vboxAvailable = self.xml.get_widget('vboxAvailable')
        
        self.imageBorrar = self.xml.get_widget('imageClics')
        self.imageSI = self.xml.get_widget('imageSI')
        self.imageSI.set_from_file(icons_path + '/si.png')
        self.imageNO = self.xml.get_widget('imageNO')
        self.imageNO.set_from_file(icons_path + '/no.png')
        
        self.ImageHome = self.xml.get_widget('imageHome')
        self.ImageHome.set_from_file(icons_path + '/home.png')
        
        self.hboxSure = self.xml.get_widget('hboxSure')
        self.buttonSI = self.xml.get_widget('buttonSI')
        self.buttonSI.connect('clicked', self.__remove_clic)
        self.buttonNO = self.xml.get_widget('buttonNO')
        self.buttonNO.connect('clicked', self.__dont_remove_clic)
        self.labelSure = self.xml.get_widget('labelSure')
        
        
        gtk.Container.remove(self.windowAva, self.vboxAvailable)


   
        #loading search_clics widget (Browser)
        self.xml = gtk.glade.XML(views_path + '/BrowserView.glade') 
        #loading window
        self.windowBrowser = self.xml.get_widget('window')
        
        self.bFirstPage = self.xml.get_widget('buttonFirstPage')
        self.bFirstPage.connect('clicked', self.__search_clics_view_home)
        
        self.bBM = self.xml.get_widget('buttonHome')
        self.bBM.connect('clicked', self.__main_view)
        self.ImageBr = self.xml.get_widget('imageHome') 
        self.ImageBr.set_from_file(icons_path + '/home.png')
        
        self.vboxBrowser = self.xml.get_widget('vboxBrowser')
        self.browser = Browser()
        self.vboxBrowser.add(self.browser)       
        gtk.Container.remove(self.windowBrowser, self.vboxBrowser)
        
      
        #loading play_clics widget
        self.xml = gtk.glade.XML(views_path + '/PlayView.glade') 
        #loading window
        self.windowPlay = self.xml.get_widget('window')
        self.vboxPlay = self.xml.get_widget('vboxPlay')
        #initialize play_clics area
        self.area = self.xml.get_widget('playArea')
        self.area.set_size_request(Constants.MAX_WIDTH,Constants.MAX_HEIGHT)
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

        self.current_view = self.Main
        self.w_child.add(self.current_view)
        
        if not runaslib: 
            #called every 20 miliseconds (for pygame)
            gobject.timeout_add(20, self.updating)
            self.window.show() 
            gtk.main()

            
    #calls the clic infinite times (until the clic ends) 
    def updating(self):        
        if self.start_clic_view:
            nou = self.controller.updating_activity()
            if (nou == -1):
                nou = 0
                self.__available_clics_view()
            if (nou == -7):
                nou = 0
                self.__main_view()    
        return True
    
    def __change_icon(self, *args):
        image = args[2]
        if image == 0:
            self.ImageMy.set_from_file(self.icons_path + args[1]) 
        elif image == 1 :
            self.ImageManual.set_from_file(self.icons_path + args[1]) 
        elif image == 2:
            self.ImageAbout.set_from_file(self.icons_path + args[1])
        elif image == 3 :
            self.ImageSearch.set_from_file(self.icons_path + args[1]) 


    #Changes the view of the application
    def __change_current_view(self, view):
        self.w_child.remove(self.current_view)
        self.current_view = view
        self.w_child.add(self.current_view)  
        
    #main view
    def __main_view(self,*args):
        self.__change_current_view(self.Main)   
        self.ImageSearch.set_from_file(self.icons_path + '/download.png')
        self.ImageMy.set_from_file(self.icons_path + '/clics.png')  
        self.hboxSure.hide() 
        
    #View to see the available clics in the computer and select one to play
    def __available_clics_view(self, *args):
        self.start_clic_view = False
        self.currentClicsView = 'Clics'  
        self.labelMy.set_text(_('SELECT A CLIC TO PLAY'))
        self.imageBorrar.set_from_file(self.icons_path + '/borrar.png')
        
        self.__refresh_clics_view(True)
                            
        if (self.current_view == self.vboxPlay):
            self.vboxPlay.hide()
            self.current_view = self.vboxAvailable
            self.w_child.add(self.current_view)  
        else :
            self.__change_current_view(self.vboxAvailable)   
    
    #Show the list of clics to play or delete     
    def __generate_list(self, *args):
        if self.currentClicsView == 'Clics':
            self.__remove_clics_view()
            self.currentClicsView = 'Delete'
        else:
            self.__list_clics_view()
            self.currentClicsView = 'Clics'        
            
    #List of clics to play (view)
    def __list_clics_view(self):
        self.labelMy.set_text(_('SELECT A CLIC TO PLAY'))
        self.imageBorrar.set_from_file(self.icons_path + '/borrar.png')
        self.__refresh_clics_view(True)
        self.hboxSure.hide()

    #RList of clics to remove (view)
    def __remove_clics_view(self, *args):
        self.labelMy.set_text(_('SELECT A CLIC TO DELETE'))
        c = self.imageBorrar.set_from_file(self.icons_path + '/clics_mini.png')
        self.__refresh_clics_view(False)
        
    def __remove_clic(self, *args):
        name, clic, default = ManagerData.get_clic_data(self.iconView)
        self.controller.remove_clic(clic)
        self.__refresh_clics_view(False)
        self.hboxSure.hide()
        
    def __dont_remove_clic(self, *args):
        self.hboxSure.hide()

        
    #View that shows the clics (and its activities)
    #View that delete clics
    def __clics_view(self, *args):
        name, clic, default = ManagerData.get_clic_data(self.iconView)
        if self.currentClicsView == 'Delete':
            text = _('DO YOU REALLY WANT TO DELETE') + ' "' + name +'"?'
            self.labelSure.set_text(text)
            self.hboxSure.show()
        else :
            self.controller.load_clic(clic, default)
            self.vboxPlay.show()
            self.__change_current_view(self.vboxPlay)   
     
    def __search_clics_view_home(self, *args):        
        self.browser.load_uri('http://www.sbennel.es')
            
    #Browser -> find new clics
    def __search_clics_view(self, *args):        
        self.vboxBrowser.remove(self.browser)
        self.browser = Browser()
        self.browser.show()
        self.vboxBrowser.add(self.browser)
        self.__change_current_view(self.vboxBrowser)
        self.browser.load_uri('http://www.sbennel.es')
            
    #shows the about view    
    def __about_view(self, *args):
        #check if the user is in the clic view (not in list-clic view)
        self.controller.load_about()
        self.vboxPlay.show()
        self.__change_current_view(self.vboxPlay)           
    
           
    #Initiates the clic 
    def __play_clic(self):
        self.controller.play_clic()
        self.start_clic_view = True
        
    #Update clics view      
    def __refresh_clics_view(self, default):
        clics = self.controller.get_installed_clics(default)
        lstore = ManagerData.add_clics_data(clics)
        self.iconView.set_model(lstore)
        ManagerData.put_columns(self.iconView)
        
    #connects the pygtk area with the pygame surface
    def __callback(self, *args):
            handle = self.area.window.xid
            os.environ['SDL_WINDOWID'] = str(handle)
            pygame.init()
            pygame.display.init()
            pygame.display.set_mode(self.area.size_request())
            self.__play_clic()

#To execute outside the Xo laptop
if __name__=="__main__":
    Manager(False)
        
