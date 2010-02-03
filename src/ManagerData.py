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

def __get_icon(name):
    theme = gtk.icon_theme_get_default()
    return theme.load_icon(name, 100, 0)

#generate order lists
def list_clics():
    img_app_path = os.path.join(paths.application_bundle_path, 'img/app') 
    icons_path = os.path.join(img_app_path, 'appIcons')
    
    lstore = gtk.ListStore(str, gtk.gdk.Pixbuf)
    lstore.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
    lstore.clear()

    areaIcon = gtk.gdk.pixbuf_new_from_file_at_size(icons_path + '/area.jpg', 100, 100)
    lstore.append(['Area', areaIcon])
    authorIcon = gtk.gdk.pixbuf_new_from_file_at_size(icons_path + '/author.jpg', 100, 100)
    lstore.append(['Author', authorIcon])
    langIcon = gtk.gdk.pixbuf_new_from_file_at_size(icons_path + '/language.jpg', 100, 100)
    lstore.append(['Language', langIcon])
    return lstore

#add web service information in a list
def add_clics_data(data):

    lstore = gtk.ListStore(str, gtk.gdk.Pixbuf,str, str, str, str, str)
    lstore.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
    lstore.clear()

    defaultIcon = __get_icon(gtk.STOCK_OPEN)
    for item in data:
        icon = item['Icon']
        default = item['Default']
        if default == 0:
            path = paths.new_clics_path
        else:
            path = paths.clics_path
            
        if  icon != '':
            Icon = gtk.gdk.pixbuf_new_from_file_at_size(path + '/' + item['Folder'] + '/' + item['Icon'] , 100, 100)
        else :
            Icon = defaultIcon

        lstore.append([item['Title'], Icon , item['Folder'], item['Default'], item['Area'], item['Language'], item['Author']])
    return lstore

#put columns in treeView
def put_columns(iconView):
    iconView.set_text_column(COL_PATH)
    iconView.set_pixbuf_column(COL_PIXBUF)
        
#    #column for title
#    column = gtk.TreeViewColumn(_('Title'), gtk.CellRendererText(), 
#                                    text=COLUMN_TITLE)
#    column.set_sort_column_id(COLUMN_TITLE)
#    tree.append_column(column)
#
#
#    # column for authors
#    column = gtk.TreeViewColumn(_('Author'), gtk.CellRendererText(),text=COLUMN_AUTHOR)
#    column.set_sort_column_id(COLUMN_AUTHOR)
#    tree.append_column(column)
#
#    # columns for areas
#    column = gtk.TreeViewColumn(_('Area'), gtk.CellRendererText(),text=COLUMN_AREA)
#    column.set_sort_column_id(COLUMN_AREA)
#    tree.append_column(column)
#
#    # column for languages
#    column = gtk.TreeViewColumn(_('Language'), gtk.CellRendererText(),text=COLUMN_LANGUAGE)
#    column.set_sort_column_id(COLUMN_LANGUAGE)
#    tree.append_column(column)
    
def get_clic_data(iconview):
    pos =  iconview.get_cursor()[0][0]
    iter = iconview.get_model().get_iter(pos)
    name = iconview.get_model().get_value(iter, 0)
    folder = iconview.get_model().get_value(iter, 2)
    is_default = iconview.get_model().get_value(iter, 3)
    return name, folder, is_default
