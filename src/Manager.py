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
import logging
import gtk
import gtk.glade
import gobject
import threading
#starting module hulahop
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

from sugar.graphics.objectchooser import ObjectChooser
from sugar import mime
#views
from MainView import MainView
from MyClicsView import MyClicsView
from AddClicsView import AddClicsView
from BrowserView import BrowserView
from PlayView import PlayView


class Manager:
    def __init__(self, runaslib = True):           
        #if runaslib is True -> we are in a Xo laptop
        paths.set_environment(runaslib) 
        
        #local variables    
        self.clicked = False #is a clic chosen to download?
        self.selected = False #is a clic chosen to play?
        self.start_clic_view = False #is a clic_activity running?
        self.views_path = paths.views_path #path to the icons folder (appIcons)
        self.icons_path = paths.icons_path #path to the views folder (appViews)
        self.listClicsInstall = False
        self.currentClicsView = 'Clics'
      
        #loading application views
        self.xmlMain = gtk.glade.XML(self.views_path + '/windowApp.glade')
        #loading window (Sugar has it owns window - not this one)
        self.window = self.xmlMain.get_widget('window')
        self.window.connect("destroy", gtk.main_quit)

        # Get Windows child (Vertical Box with the views)
        self.w_child = self.window.get_child()  
        # Needs to remove the parent (we will use the Sugar's window)
        if runaslib:
            gtk.Container.remove(self.window, self.w_child)

        #LOADING MAIN VIEW and connect events
        self.mainView = MainView()
        self.mainView.bMy.connect('clicked', self.__available_clics_view)
        self.mainView.bMy.connect('enter', self.__change_icon, '/clics_2.png', 0) 
        self.mainView.bMy.connect('leave', self.__change_icon, '/clics.png', 0) 
        #Manual button
        self.mainView.bManual.connect('clicked', self.__manual_view)
        self.mainView.bManual.connect('enter', self.__change_icon, '/manual_2.png', 1) 
        self.mainView.bManual.connect('leave', self.__change_icon, '/manual.png', 1) 
        #About button
        self.mainView.bAbout.connect('clicked', self.__about_view)
        self.mainView.bAbout.connect('enter', self.__change_icon, '/about_2.png', 2) 
        self.mainView.bAbout.connect('leave', self.__change_icon, '/about.png', 2) 
        #Search button
        self.mainView.bS.connect('clicked', self.__browser_view) 
        self.mainView.bS.connect('enter', self.__change_icon, '/download_2.png', 3) 
        self.mainView.bS.connect('leave', self.__change_icon, '/download.png', 3) 
        #Install button    
        self.mainView.bIns.connect('clicked', self.__install_view) 
        self.mainView.bIns.connect('enter', self.__change_icon, '/install_2.png', 4) 
        self.mainView.bIns.connect('leave', self.__change_icon, '/install.png', 4) 

        #LOADING MY CLICS VIEW and connect events
        self.myClicsView = MyClicsView()
        self.myClicsView.iconView.connect('selection-changed', self.__clics_view)
        self.myClicsView.bClics.connect('clicked', self.__generate_list)
        self.myClicsView.bPM.connect('clicked', self.__main_view)
        self.myClicsView.buttonSI.connect('clicked', self.__remove_clic)
        self.myClicsView.buttonNO.connect('clicked', self.__dont_remove_clic)
        
        #LOADING INSTALL CLICS VIEW and connect events
        self.addClicsView = AddClicsView()
        self.addClicsView.iconViewIns.connect('selection-changed', self.__installation_info_view) #item-activated 2 clicks //selection-changed 1 click
        self.addClicsView.buttonOK.connect('clicked', self.__hide_installation_info_view)
        self.addClicsView.bInsMain.connect('clicked', self.__main_view)
   
        #LOADING BROWSER VIEW and connect events
        self.browserView = BrowserView()
        self.browserView.bBM.connect('clicked', self.__main_view)        
        self.browserView.bGo.connect('clicked', self.__browser_view_galeria)
      
        #LOADING VIEW FOR CLICS PLAYER
        self.playView = PlayView()
        #translates GTK events into Pygame events 
        t = gtkEvent.Translator(self.playView.area)
        self.playView.area.connect('map-event', self.__callback)
        t.hook_pygame()
         
        # self.widget will be attached to the XO-Activity
        # This can be any GTK widget except a window
        self.widget = self.w_child

        #initiate controller
        self.controller = Controller()

        #current(first) view is the main menu
        self.current_view = self.mainView.Main
        self.w_child.add(self.current_view)
        
        if not runaslib: 
            #called every 250 miliseconds (for communication with pygame module (player))
            gobject.timeout_add(250, self.updating)
            #called every second to refresh some views of the application
            gobject.timeout_add(2000, self.updating_views)
            self.window.show() 
            gtk.main()

            
    #this method calls the clic player (pygame) until the user stops playing a clic 
    def updating(self):        
        if self.start_clic_view:
            nou = self.controller.updating_activity()
            #stops calling, goes to My Clics View
            if (nou == -1):
                nou = 0
                self.__available_clics_view()
            #stops callings, goes to the Main Menu View
            if (nou == -7):
                self.__main_view()  
        return True
    
    #this method refresh the Clics view (My Clics, Add Clics)
    def updating_views(self):
        
        #refresh Add Clics View
        if self.listClicsInstall == True:
            self.__refresh_install_view()
        
        #refresh My Clics View
        if self.currentClicsView == 'Clics':
            self.__refresh_clics_view(True)
            
        return True
    
    #changes the bright of an icon
    def __change_icon(self, *args):
        image = args[2]
        if image == 0:
            self.mainView.ImageMy.set_from_file(self.icons_path + args[1]) 
        elif image == 1 :
            self.mainView.ImageManual.set_from_file(self.icons_path + args[1]) 
        elif image == 2:
            self.mainView.ImageAbout.set_from_file(self.icons_path + args[1])
        elif image == 3 :
            self.mainView.ImageSearch.set_from_file(self.icons_path + args[1])
        elif image == 4 :
            self.mainView.ImageInstall.set_from_file(self.icons_path + args[1])


    #Changes the current view of the application.
    def __change_current_view(self, view):
        self.w_child.remove(self.current_view)
        self.current_view = view
        self.w_child.add(self.current_view)  
        
    #Shows the Main Menu View of the application.
    def __main_view(self,*args):
        self.listClicsInstall = False
        if (self.current_view == self.playView.vboxPlay):
            self.playView.vboxPlay.hide()
            self.current_view = self.mainView.Main
            self.w_child.add(self.current_view)  
        else :
            self.__change_current_view(self.mainView.Main)    
        self.mainView.ImageSearch.set_from_file(self.icons_path + '/download.png')
        self.mainView.ImageMy.set_from_file(self.icons_path + '/clics.png')  
        self.myClicsView.hboxSure.hide() 
        
    #Shows all the clics of the user (default clics, downloaded clics).
    def __available_clics_view(self, *args):
        self.start_clic_view = False
        
        self.currentClicsView = 'Clics'  
        self.myClicsView.labelMy.set_text(_('SELECT A CLIC TO PLAY'))
        self.myClicsView.labelButBorrar.set_text(_('DELETE CLICS'))
        self.myClicsView.imageBorrar.set_from_file(self.icons_path + '/borrar.png')
        
        self.__refresh_clics_view(True)
                            
        if (self.current_view == self.playView.vboxPlay):
            self.playView.vboxPlay.hide()
            self.current_view = self.myClicsView.vboxAvailable
            self.w_child.add(self.current_view)  
        else :
            self.__change_current_view(self.myClicsView.vboxAvailable)   
    
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
        self.myClicsView.labelMy.set_text(_('SELECT A CLIC TO PLAY'))
        self.myClicsView.labelButBorrar.set_text(_('DELETE CLICS'))
        self.myClicsView.imageBorrar.set_from_file(self.icons_path + '/borrar.png')
        self.__refresh_clics_view(True)
        self.myClicsView.hboxSure.hide()

    #List of clics to remove (view)
    def __remove_clics_view(self, *args):
        self.myClicsView.labelMy.set_text(_('SELECT A CLIC TO DELETE'))
        self.myClicsView.labelButBorrar.set_text(_('MY CLICS'))
        c = self.myClicsView.imageBorrar.set_from_file(self.icons_path + '/clics_mini.png')
        self.__refresh_clics_view(False)
      
    
    #Shows the clics to install from Journal or a usb device (view)
    def __install_view (self, *args):

        self.addClicsView.hboxInfoInstall.hide()
        
        #change view to install clics view
        self.__change_current_view(self.addClicsView.vboxInstall)
        
        #get found clics
        found_clics = self.controller.find_clics()
        
        #check if the list is not empty
        if len(found_clics) == 0 :
            self.addClicsView.labelInfoInstall.set_text(_('IT WAS NOT POSSIBLE TO FIND ANY CLIC'))
            self.addClicsView.hboxInfoInstall.show()
        else:
            #reloads the view (shows all the clics available to install)
            self.__refresh_install_view()
        self.listClicsInstall = True
    
        
    #try to install the file (clic) selected by the user 
    def __installation_info_view(self, *args):
        #get data of selected clic
        title, path = ManagerData.get_found_clic_data(self.addClicsView.iconViewIns)
        self.addClicsView.vboxInstall.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        
        #try to install the clic
        self.controller.install_new_clic_from_datastore(title, path)
        self.__refresh_install_view()
        self.addClicsView.vboxInstall.window.set_cursor(None)
    
    #hides the information label in instllation view
    def __hide_installation_info_view(self, *args):
        self.addClicsView.hboxInfoInstall.hide()
        
    #reloads the view to install clics
    def __refresh_install_view(self, *args):
        #get found clics
        found_clics = self.controller.find_clics()
        #add clics in the iconview with a default icon
        lclics = ManagerData.add_found_clics_data(found_clics)
        self.addClicsView.iconViewIns.set_model(lclics)
        ManagerData.put_columns(self.addClicsView.iconViewIns)
    

    # removes a clic from the clics list of the user
    def __remove_clic(self, *args):
        title, folder, default = ManagerData.get_clic_data(self.myClicsView.iconView)
        self.controller.remove_clic(title, folder)
        self.__refresh_clics_view(False)
        self.myClicsView.hboxSure.hide()
        
    #the user doesn't want to remove the clic
    def __dont_remove_clic(self, *args):
        self.myClicsView.hboxSure.hide()


    #View that shows the clics (and its activities)
    #View that delete clics
    def __clics_view(self, *args):
        name, folder, default = ManagerData.get_clic_data(self.myClicsView.iconView)
        if self.currentClicsView == 'Delete':
            text = _('DO YOU REALLY WANT TO DELETE') + ' "' + name +'"?'
            self.myClicsView.labelSure.set_text(text)
            self.myClicsView.hboxSure.show()
        else :
            self.controller.load_clic_information(folder, default)
            self.playView.vboxPlay.show()
            self.__change_current_view(self.playView.vboxPlay)   
            
    #Shows the page with the clics of 'http://www.sbennel.es' (website of PortalClic)
    def __browser_view_galeria(self, *args):        
        self.browserView.browser.load_uri('http://www.sbennel.es/?q=galeria')
            
    #Shows the Browser with the website of PortaClic that allows user to download new clics 
    def __browser_view(self, *args):        
        self.browserView.vboxBrowser.remove(self.browserView.browser)
        self.browserView.browser = Browser()
        self.browserView.browser.show()
        self.browserView.vboxBrowser.add(self.browserView.browser)
        self.__change_current_view(self.browserView.vboxBrowser)
        self.browserView.browser.load_uri('http://www.sbennel.es')
            
    #shows the about view    
    def __about_view(self, *args):
        #check if the user is in the clic view (not in list-clic view)
        self.controller.load_about()
        self.playView.vboxPlay.show()
        self.__change_current_view(self.playView.vboxPlay)      
        
    #shows the manual view    
    def __manual_view(self, *args):
        #check if the user is in the clic view (not in list-clic view)
        self.controller.load_manual()
        self.playView.vboxPlay.show()
        self.__change_current_view(self.playView.vboxPlay)         
    
           
    #Initiates the clic selected by the user to play 
    def __play_clic(self):
        self.controller.play_clic()
        self.start_clic_view = True
        
    #Update clics view      
    def __refresh_clics_view(self, default):
        clics = self.controller.get_installed_clics(default)
        lstore = ManagerData.add_clics_data(clics)
        self.myClicsView.iconView.set_model(lstore)
        ManagerData.put_columns(self.myClicsView.iconView)
        
    #connects the pygtk area with the pygame surface
    def __callback(self, *args):
            handle = self.playView.area.window.xid
            os.environ['SDL_WINDOWID'] = str(handle)
            pygame.init()
            pygame.display.init()
            pygame.display.set_mode(self.playView.area.size_request())
            self.__play_clic()

#To execute outside the Xo laptop
if __name__=="__main__":
    Manager(False)
        
