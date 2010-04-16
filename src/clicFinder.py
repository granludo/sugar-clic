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
import os
import paths
from sugar.datastore import datastore

#look the file activty.info in folder activity
_ACTIVITY_BUNDLE_ID = 'net.netii.kumuolpc.ClicPlayer'
_MEDIA_PATH = '/media/'



class Finder:
    def __init__(self):
        self.clics = list()
        self.path_to_device = ''
    
    #find files that contains real clics (extension = .jclic.zip or .jclic_.zip)
    def find_clics(self):
        
        #clear the list of found clics
        self.clics = list()
        
        devices = datastore.mounts()
        
        #for every mounted device, find all the zips
        for device in devices:
            try:
                (ds_objects, count) = datastore.find({'mime_type':'application/zip', 'mountpoints':[device['id']], 'activity':_ACTIVITY_BUNDLE_ID})
                #usb device
                if device['title'].find('/media/') != -1 :
                    for d in ds_objects:
                        if d.get_file_path() != '' :
                            path = os.path.join(device['title'], d.metadata['title'])
                            path = path + '.zip'
                            title = d.metadata['title']
                            self.clics.append({'title':title, 'path':path})
                        d.destroy()
#                #datastore (this moment is not possible)
#                else:
#                    for d in data:
#                        if d.get_file_path() != '' :                 
#                            path = os.path.join(paths.new_clics_path, d.metadata['title'])
#                            path = path + '.zip'
#                            title = d.metadata['title']
#                            self.clics.append({'title':title, 'path':d.get_file_path()})
#                        d.destroy()     
            except Exception:
                return self.clics      
        return self.clics



    
                
    
