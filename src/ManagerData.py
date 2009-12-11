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
(
    COLUMN_TITLE,
    COLUMN_AUTHOR,
    COLUMN_AREA,
    COLUMN_LANGUAGE,
    COLUMN_FILE
) = range(5)

#add web service information in a list
def add_clics_data(data):
    lstore = gtk.ListStore(
        gobject.TYPE_STRING,
        gobject.TYPE_STRING,
        gobject.TYPE_STRING,
        gobject.TYPE_STRING,
        gobject.TYPE_STRING)

    for item in data:
        iter = lstore.append()
        lstore.set(iter,
            COLUMN_TITLE, item['Title'],
            COLUMN_AUTHOR, item['Author'],
            COLUMN_AREA, item['Area'],
            COLUMN_LANGUAGE, item['Language'],
            COLUMN_FILE, item['File'])
    return lstore

#put columns in treeView
def put_columns(tree):
        
    #column for title
    column = gtk.TreeViewColumn('Clic Title', gtk.CellRendererText(), 
                                    text=COLUMN_TITLE)
    column.set_sort_column_id(COLUMN_TITLE)
    tree.append_column(column)


    # column for authors
    column = gtk.TreeViewColumn('Author', gtk.CellRendererText(),text=COLUMN_AUTHOR)
    column.set_sort_column_id(COLUMN_AUTHOR)
    tree.append_column(column)

    # columns for areas
    column = gtk.TreeViewColumn('Area', gtk.CellRendererText(),text=COLUMN_AREA)
    column.set_sort_column_id(COLUMN_AREA)
    tree.append_column(column)

    # column for languages
    column = gtk.TreeViewColumn('Language', gtk.CellRendererText(),text=COLUMN_LANGUAGE)
    column.set_sort_column_id(COLUMN_LANGUAGE)
    tree.append_column(column)
    
def get_clic_data(tree):
    pos =  tree.get_cursor()[0][0]
    iter = tree.get_model().get_iter(pos)
    clic = {'Title': tree.get_model().get_value(iter,0),
            'Author': tree.get_model().get_value(iter,1),
            'Area': tree.get_model().get_value(iter,2),
            'Language': tree.get_model().get_value(iter,3),
            'File': tree.get_model().get_value(iter,4)                   
            }
    return clic