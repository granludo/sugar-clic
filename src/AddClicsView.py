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

class AddClicsView:
    def __init__(self):   
        self.views_path = paths.views_path #path to the icons folder (appIcons)
        self.icons_path = paths.icons_path #path to the views folder (appViews) 
               
        #LOADING ADD CLICS VIEW
        self.xml = gtk.glade.XML(self.views_path + '/AddClicsView.glade') 
        #loading window
        self.windowIns = self.xml.get_widget('window')
        self.vboxInstall = self.xml.get_widget('vboxInstall')
        
        self.iconViewIns = self.xml.get_widget('iconviewAvailable')
                         
        self.labelInstallClics = self.xml.get_widget('labelInstall')
        self.labelInstallClics.set_text(_('SELECT A CLIC TO ADD'))
        self.labelButInsMain = self.xml.get_widget('labelButInstallMain')
        self.labelButInsMain.set_text(_('MAIN MENU'))    
        
        #informs the installation process
        self.hboxInfoInstall = self.xml.get_widget('hboxInstallation')
        self.labelInfoInstall = self.xml.get_widget('labelInstallation')
        self.imageOK = self.xml.get_widget('imageOK')
        self.imageOK.set_from_file(self.icons_path + '/si.png')
        self.buttonOK = self.xml.get_widget('buttonOK')
        
        self.bInsMain = self.xml.get_widget('buttonInstallMain')
        self.ImageHomeIns = self.xml.get_widget('imageHome')
        self.ImageHomeIns.set_from_file(self.icons_path + '/home.png')    
        
        gtk.Container.remove(self.windowIns, self.vboxInstall)