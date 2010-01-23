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
from xml.dom import minidom
import os
import re
import threading
import paths

import controller

class Installer:
    def __init__(self):
        self.clics_path = paths.clics_path #folder to install clics
        self.data_path = paths.application_data_path
        if not os.path.exists(self.clics_path):
            t = os.system('mkdir ' + self.clics_path)
            
            
    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc


    #Parse information about the clic (sequence, mediaBag, settings)
    def get_clic_info(self, file):
        t = self.__unzip_xmlclic(file)
        
        clicInfo = minidom.parse(self.data_path + '/' + file)
        urlsC = clicInfo.getElementsByTagName('urlClic')   
        urlsI = clicInfo.getElementsByTagName('urlIcon') 
        
        subjectP = clicInfo.getElementsByTagName('Subject')
        authorP = clicInfo.getElementsByTagName('Author')
        licenseP = clicInfo.getElementsByTagName('License')
        themeP = clicInfo.getElementsByTagName('Theme')
        languageP = clicInfo.getElementsByTagName('Language')
        
       
        self.subject =  subjectP[0].childNodes[0].data
        self.author =  authorP[0].childNodes[0].data
        self.license = licenseP[0].childNodes[0].data
        self.theme = themeP[0].childNodes[0].data
        self.language = languageP[0].childNodes[0].data
                       
        clic = {'Title': self.subject,
                'Author': self.author,
                'Area': self.theme,
                'Language': self.language,
                'File': '',
                'Icon': ''
                }     
        
        
        fileUrls = list()
        iconUrls = list()
        
        for url in  urlsC:
            oneUrl = self.getText(url.childNodes)
            if oneUrl != "" :
                fileUrls.append(url.childNodes[0].data)
                
        for url in  urlsI:
            iconUrls.append(url.childNodes[0].data)
                
        l = list()
        l.append(clic)
        l.append(fileUrls)
        l.append(iconUrls)
            

            

#        ##############thread test########################
        hilo = threading.Thread(target=self.__download_file, args=(l))
        hilo.start()

        self.__delete_file(file)
        
    def __delete_file(self, file):
        t = os.system('rm '+ self.data_path + '/'+ file)                 
        return t       
            
    #Unzips the Jclic to a local folder and removes the file
    def __unzip_xmlclic(self, file):   
        #self.label.set_text('File downloaded')
        t = os.system('unzip -o '+ self.data_path + '/'+ file + ' -d ' + self.data_path)                 
        return t  
    
    def __download_file(self, *urls):
        #enter in the thread
        #gtk.gdk.threads_enter()

#        list = self.__get_urls(urlsClics)
#
#        print 'c: '+ list
        clic = urls[0]
        urls_to_download = urls[1]
        icons_to_download = urls[2]
        print icons_to_download

        
        done = False
                
        i = 0
        
        while ((done == False) and (i < len(urls_to_download))) : 
            
            file =  urls_to_download[i].split("/")[-1]
            folder = file.split('.',1)[0]
            clic['File'] = folder        
                
            t = os.system('wget -q ' + urls_to_download[i] + ' --directory-prefix=' + self.clics_path )    
            if t == 0:
                t = os.system('unzip '+ self.clics_path + '/'+ file + ' -d ' + self.clics_path + '/' + folder)            
                if t == 0:
                    t = os.system('rm '+ self.clics_path + '/' + file)
                    if t == 0:
                        print 'Installed in folder clics/' + folder
                        self.controller = controller.Controller()
                        #calls the controller to add a new clic to the db list
                        done = True
                        
            i = i + 1
        
                        
                        
        if done == True :
            icon =  icons_to_download[0].split("/")[-1]
            t = os.system('wget -q ' + icons_to_download[0] + ' --directory-prefix=' + self.clics_path + '/' + folder )  
            if t == 0:
                clic['Icon'] = icon  
            else :
                clic['Icon'] = ''
                    
            self.controller.add_new_clic(clic)
                    
        
        if done == False:
            print 'NOT INSTALLED'
        
    
    
    
    

