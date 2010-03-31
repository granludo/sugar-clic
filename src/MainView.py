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
import os
from gettext import gettext as _

class MainView:
    def __init__(self):   
        self.views_path = paths.views_path #path to the icons folder (appIcons)
        self.icons_path = paths.icons_path #path to the views folder (appViews)        
        #LOADING MAIN VIEW
        self.xml = gtk.glade.XML(self.views_path + '/mainView.glade') 
        self.win = self.xml.get_widget('window')
        self.Main = self.xml.get_widget('Main')
        #remove parent (in glade there is always a parent (window))
        gtk.Container.remove(self.win ,self.Main)
        
        #loading the image of the title (SugarClic)
        self.ImageSearch = self.xml.get_widget('imageTitle')
        self.ImageSearch.set_from_file(self.icons_path + '/title.png')  
        
        #MyClics button
        self.bMy = self.xml.get_widget('buttonMyClics')
        self.ImageMy = self.xml.get_widget('imageMyClics')
        self.ImageMy.set_from_file(self.icons_path + '/clics.png')

        #Manual button
        self.bManual = self.xml.get_widget('buttonManual')
        self.ImageManual = self.xml.get_widget('imageManual')
        self.ImageManual.set_from_file(self.icons_path + '/manual.png')
        
        #About button
        self.bAbout = self.xml.get_widget('buttonAbout')
        self.ImageAbout = self.xml.get_widget('imageAbout')
        self.ImageAbout.set_from_file(self.icons_path + '/about.png')
        
        #Search button
        self.bS = self.xml.get_widget('buttonSearch')
        self.ImageSearch = self.xml.get_widget('imageSearch')
        self.ImageSearch.set_from_file(self.icons_path + '/download.png')
        
        #Install button    
        self.bIns = self.xml.get_widget('buttonInstall')
        self.ImageInstall = self.xml.get_widget('imageInstall')
        self.ImageInstall.set_from_file(self.icons_path + '/install.png')
              
        #set the labels to translate
        self.labelMan = self.xml.get_widget('labelManual')
        self.labelMan.set_text(_('MANUAL'))
        self.labelAbout = self.xml.get_widget('labelAbout')
        self.labelAbout.set_text(_('ABOUT SUGARCLIC'))    
        self.labelSearch = self.xml.get_widget('labelSearch')
        self.labelSearch.set_text(_('DOWNLOAD CLICS'))
        self.labelMYCLICS = self.xml.get_widget('labelMyClics')
        self.labelMYCLICS.set_text(_('MY CLICS'))
        self.labelIns = self.xml.get_widget('labelInstall')
        self.labelIns.set_text(_('ADD CLICS'))
        
        #load the test that appears in the centre of the main menu
        path_to_texto = os.path.join(paths.application_bundle_path, 'data/textoInicio.txt')
        file = open(path_to_texto, 'r')
        self.labelTextoInicial = self.xml.get_widget('labelInitText')
        self.labelTextoInicial.set_text(file.read())
        file.close()
        