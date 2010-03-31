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
import gtk
import gobject
import paths
import os
from gettext import gettext as _

COL_PATH = 0
COL_PIXBUF = 1

#creates an icon to show it with the clic
def __get_alternative_icon():
    img_app_path = os.path.join(paths.application_bundle_path, 'img/app') 
    alternative_icon_path = os.path.join(img_app_path, 'appIcons/defaultIcon.png')
    return gtk.gdk.pixbuf_new_from_file_at_size(alternative_icon_path , 100, 100)


#add clics information in a list (available clics to play)
def add_clics_data(data):

    lstore = gtk.ListStore(str, gtk.gdk.Pixbuf,str, str, str, str, str)
    lstore.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
    lstore.clear()
    
    alternative_icon = __get_alternative_icon()

    for item in data:
        icon = item['Icon']
        default = item['Default']
        if default == 0:
            path = paths.new_clics_path
        else:
            path = paths.clics_path
        #gets the icon of the clic
        if  icon != '':
            Icon = gtk.gdk.pixbuf_new_from_file_at_size(path + '/' + item['Folder'] + '/' + item['Icon'] , 100, 100)
        else :
            #if the clic doesn't have an icon, take an alternative icon to show in the list 
            Icon = alternative_icon

        lstore.append([item['Title'], Icon , item['Folder'], item['Default'], item['Area'], item['Language'], item['Author']])
    return lstore

#create a list of clics found in datastore (Journal + devices)
def add_found_clics_data(found_clics):
    lstore = gtk.ListStore(str, gtk.gdk.Pixbuf, str)
    lstore.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
    
    #get an icon for the clic
    Icon = __get_alternative_icon()
    
    for clic in found_clics:
        #store title, Icon, and path
        lstore.append([clic['title'], Icon, clic['path']])
    return lstore

#get clic data of selected clic in the view (ADD CLICS)
def get_found_clic_data(iconviewAdd):
    pos =  iconviewAdd.get_cursor()[0][0]
    iter = iconviewAdd.get_model().get_iter(pos)
    title = iconviewAdd.get_model().get_value(iter, 0)
    path = iconviewAdd.get_model().get_value(iter, 2)
    return title, path



#put columns in the iconView
def put_columns(iconView):
    iconView.set_text_column(COL_PATH)
    iconView.set_pixbuf_column(COL_PIXBUF)
        

#get clic data of selected clic in the view (MY CLICS)
def get_clic_data(iconviewMyClics):
    pos =  iconviewMyClics.get_cursor()[0][0]
    iter = iconviewMyClics.get_model().get_iter(pos)
    name = iconviewMyClics.get_model().get_value(iter, 0)
    folder = iconviewMyClics.get_model().get_value(iter, 2)
    is_default = iconviewMyClics.get_model().get_value(iter, 3)
    return name, folder, is_default
