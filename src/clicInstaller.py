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
from sugar.graphics.alert import NotifyAlert
from sugar.datastore import datastore
from xml.dom import minidom
import os
import re
import threading
import shutil
import gtk
from gettext import gettext as _
import controller
import paths


#look the file activty.info in folder activity
_ACTIVITY_BUNDLE_ID = 'net.netii.kumuolpc.ClicPlayer'

class Installer:
    def __init__(self):
        self.clics_path = ""
        self.data_path = ""
        self.hasPaths = False
        
    def get_activity(self, activity):
        self._activity = activity
        

            
    def __getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    #Parse information about the clic (sequence, mediaBag, settings)
    def get_clic_info(self, file):
        
        if (self.hasPaths == False) :
            self.__load_paths()
        
        #unzip the file with metadata
        from_path = os.path.join(self.data_path, file)
        t = self.__unzip_file(from_path, self.data_path)
        
        #parse XML to get all the information about the Clic
        clicInfo = minidom.parse(self.data_path + '/' + file)
        
        #information to download the clic and icon
        urlsC = clicInfo.getElementsByTagName('urlClic')   
        urlsI = clicInfo.getElementsByTagName('urlIcon') 
        
        #information about the clic (subject, author, license, ...)
        subjectElem = clicInfo.getElementsByTagName('Subject')
        authorElem = clicInfo.getElementsByTagName('Author')
        licenseElem = clicInfo.getElementsByTagName('License')
        themeElem = clicInfo.getElementsByTagName('Theme')
        languageElem = clicInfo.getElementsByTagName('Language')
        
        self.subject = ''
        self.author = ''
        self.license = ''
        self.theme = ''
        self.language = ''
       
        #check if all the fields are informed
        if (subjectElem.length != 0 ) : self.subject =  self.__getText(subjectElem[0].childNodes)
        if (authorElem.length != 0) : self.author = self.__getText(authorElem[0].childNodes)
        if (licenseElem.length != 0) : self.license = self.__getText(licenseElem[0].childNodes)
        if (themeElem.length != 0) : self.theme = self.__getText(themeElem[0].childNodes)
        if (languageElem.length != 0) : self.language = self.__getText(languageElem[0].childNodes)
                       
        clic = {'Title': self.subject,
                'Author': self.author,
                'Area': self.theme,
                'Language': self.language,
                'Folder': '',
                'Icon': ''
                }     
        
        
        fileUrls = list()
        iconUrls = list()
        
        #get all the urls (to download clic and to download icon
        for url in  urlsC:
            oneUrl = self.__getText(url.childNodes)
            if oneUrl != "" :
                fileUrls.append(url.childNodes[0].data)
                
        for url in  urlsI:
            iconUrls.append(url.childNodes[0].data)
         
        #put all the information in a list to send it to the thread that downloads the files       
        l = list()
        l.append(clic)
        l.append(fileUrls)
        l.append(iconUrls)
            
        #downloads the new clic file in background (every download has its own thread)
        hilo = threading.Thread(target=self.__download_file, args=(l))
        hilo.start()
        self.__delete_file(self.data_path, file)
        
        
        
    #downloads the new clic file in background (every download has its own thread)
    def __download_file(self, *urls):

        
        clic = urls[0]
        file_urls_to_download = urls[1]
        icons_url_to_download = urls[2]
        
        #notify that it is starting to download the clic
        title = _('Downloading Clic') + ' (' + clic['Title'] + ')'
        msg = _('Once downloaded, you will have the Clic on your list')
        self._alert_notify(title, msg)

        done = False                
        i = 0
        
        #Find a valid url and download the clic.
        while ((done == False) and (i < len(file_urls_to_download))) : 
            
            file =  file_urls_to_download[i].split("/")[-1]
            folder = file.split('.',1)[0]
            clic['Folder'] = folder
            
            t = self.__wget_file(file_urls_to_download[i], self.clics_path)  
            if t == 0:
                from_path = os.path.join(self.clics_path, file)
                to_path = os.path.join(self.clics_path, folder)
                t = self.__unzip_file(from_path, to_path)   
                if t == 0:
                    print 'Installed in folder clics/' + folder
                    
                    #add new file to Journal (datastore)
                    title = clic['Title']
                    self.__write_file_to_datastore(title, from_path)
                    self.__delete_file(self.clics_path, file)
                        
                    self.controller = controller.Controller()
                    done = True
                        
            i = i + 1
        
        #If it was possible to download the clic, download its icon.         
        if done == True :
            to_path = os.path.join(self.clics_path, folder)
            t = self.__wget_file(icons_url_to_download[0], to_path)
            if t == 0:
                icon =  icons_url_to_download[0].split("/")[-1]
                clic['Icon'] = icon  
            else :
                clic['Icon'] = ''
            #calls the controller to add a new clic to the db list     
            self.controller.add_new_clic(clic)
                           
        if done == False:
            title = _('Download failed') + ' (' + clic['Title'] + ')'
            msg = _('It was not possible to download the Clic')
            self._alert_notify(title, msg)
            
            
    #installs a clic from datastore (Journal + devices) to the new clics folder (checking if it's a real clic.)
    def install_clic_from_datastore(self, title, path):
        if (self.hasPaths == False) :
            self.__load_paths()

        l = list()
        l.append(title)
        l.append(path)
        hilo = threading.Thread(target=self.__installing_clic_thread, args=(l))
        hilo.start()     
        
        
        
    def __installing_clic_thread(self, *params):
        
        #get params of the thread
        title = params[0]
        path = params[1]
        
        
        #notify that it is starting to add the Clic
        title_alert = _('Adding Clic') + ' (' + title + ')'
        msg_alert = _('Once added, you will have the Clic on your list')
        self._alert_notify(title_alert, msg_alert)
        

        #get path of clic to install
        from_path = path
        #get destination folder
        folder = title
        to_path = paths.get_clic_path(folder, '0')
        
        #unzip file into the new clic folder
        t = self.__unzip_file(from_path, to_path)
        
        #if everything was OK, check if the file has a JClic document
        #(info about how to show the clic)
        if t == 0 :
            try:
                #find a jclic document in the new clic folder
                for fl in os.listdir(to_path):
                    if not fl[0] == '.': 
                        if not os.path.isdir(os.path.join(to_path, fl)):
                            if fl.find('.jclic') != -1: 
                                #check if the folder of the clic has a .JClic document and is parseable
                                jclic_doc = fl #JClic document has the same name as the zip
                                minidom.parse(os.path.join(to_path, jclic_doc))
                
            except Exception :
                
                #if not, delete the folder created in new clics directory
                self.delete_clic_folder(folder)
                title_alert = _('Clic not added') + '(' + title + ')'
                msg_alert = _('It was not possible to add the Clic')
                self._alert_notify(title_alert, msg_alert)
        else:
                title_alert = _('Clic not added') + '(' + title + ')'
                msg_alert = _('It was not possible to add the Clic')
                self._alert_notify(title_alert, msg_alert)
            
        #everything was correctly done
        #add clic information to database
        self.controller = controller.Controller()
        clic = {'Title': title,
                'Author': '',
                'Area': '',
                'Language': '',
                'Folder': folder,
                'Icon': ''
                }    
        self.controller.add_new_clic(clic)
        
         
        
    
    #removes all the data of a clic's folder. and the entry in Journal
    def delete_clic_folder(self, title, folder):
        shutil.rmtree(paths.get_clic_path(folder, '0'))
        self.__remove_datastore_file(title)
        

    
    #removes zip file.
    def __delete_file(self, path, file):
        file_to_remove = os.path.join(path, file)
        t = os.remove(file_to_remove)      
            
    #Unzips a file to a new path (it will overwrite content if exists).
    def __unzip_file(self, from_path, to_path):  
        from_path = from_path.replace(' ' , '\ ')
        to_path = to_path.replace(' ' , '\ ')
        t = os.system('unzip -o '+ from_path + ' -d ' + to_path)                 
        return t  
    
    #Wget downloads a file from a url and stores it in a path
    def __wget_file(self, url, to_path):
        t = os.system('wget -q ' + url + ' --directory-prefix=' + to_path)  
        return t
    
    #creates a datastore file and puts in Journal
    def __write_file_to_datastore(self, title, path):
        
        #creates a datastore file
        file_dsobject = datastore.create()
        
        # Write metadata info (here we specifically set the title of the file and
        # specify that this is a zip file). 
        file_dsobject.metadata['title'] = title
        file_dsobject.metadata['mime_type'] = 'application/zip'
        file_dsobject.metadata['activity'] = _ACTIVITY_BUNDLE_ID

        
        #Set the file_path in the datastore.
        file_dsobject.file_path = path

        try:
            datastore.write(file_dsobject)
        except Exception:
            print 'not stored in datastore'
        #destroy object
        file_dsobject.destroy()
        
    #deletes the datastore entry related with the clic (only in Journal)
    def __remove_datastore_file(self, title):
    
        devices =  datastore.mounts()
        #remove only datastore entries related with Journal
        for device in devices:
            try:
                #find datastore object related with the query
                (ds_objects, count) = datastore.find({'title':title, 
                                                      'mime_type':'application/zip',
                                                      'activity' : _ACTIVITY_BUNDLE_ID, 
                                                      'mountpoints':[device['id']]})
                #usb device
                if device['title'].find('/media/') == -1 :
                    for d in ds_objects:
                        d.destroy()
                        datastore.delete(d.object_id)
            except Exception:
                print 'not removed in datastore'
        
    #### Method: _alert_notify, create a Notify alert (with only an 'OK' button)
    # and add it to the UI. 
    def _alert_notify(self, title, msg):
        #Notice that for a NotifyAlert, you pass the number of seconds in which to notify. By
        #default, this is 5. 
        alert = NotifyAlert(5)
        alert.props.title = title
        alert.props.msg = msg
        alert.connect('response', self._alert_response_cb)
        self._activity.add_alert(alert)
        
    def _alert_response_cb(self, alert, response_id):
        if response_id is gtk.RESPONSE_OK:
            self._activity.remove_alert(alert)
            
    def __load_paths(self):
        self.clics_path = paths.new_clics_path
        self.data_path = paths.application_data_path
    

