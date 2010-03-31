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

import paths
import gtk
import gtk.glade
import gobject
from gettext import gettext as _
from browser import Browser

class BrowserView:
    def __init__(self):   
        self.views_path = paths.views_path #path to the icons folder (appIcons)
        self.icons_path = paths.icons_path #path to the views folder (appViews) 
               
        #LOADING BROWSER VIEW
        self.xml = gtk.glade.XML(self.views_path + '/BrowserView.glade') 
        #loading window
        self.windowBrowser = self.xml.get_widget('window')
        
        self.bBM = self.xml.get_widget('buttonHome')
        self.ImageBr = self.xml.get_widget('imageHome') 
        self.ImageBr.set_from_file(self.icons_path + '/home.png')
        
        self.bGo = self.xml.get_widget('buttonFirstPage')
        self.ImageGo = self.xml.get_widget('imageGoBack') 
        self.ImageGo.set_from_file(self.icons_path + '/goBack.png')
        
        self.labelButHome = self.xml.get_widget('labelButHome')
        self.labelButHome.set_text(_('MAIN MENU'))
        self.labelButFirst = self.xml.get_widget('labelButFirst')
        self.labelButFirst.set_text(_('CLICS TO DOWNLOAD'))
        
        self.vboxBrowser = self.xml.get_widget('vboxBrowser')
        self.browser = Browser()
        self.vboxBrowser.add(self.browser)       
        gtk.Container.remove(self.windowBrowser, self.vboxBrowser)