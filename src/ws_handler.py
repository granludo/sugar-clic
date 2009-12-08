''' 
    This file is part of Sugar-Clic
    
    Sugar-Clic is copyrigth 2009 by Maria José Casany Guerrero and Marc Alier Forment
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
    @copyrigth 2009 Marc Alier, Maria José Casany marc.alier@upc.edu
    @copyrigth 2009 Universitat Politecnica de Catalunya http://www.upc.edu
    
    @autor Marc Alier
    @autor Jordi Piguillem
    
    @license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
'''
#Module that interacts with the web service, downloads clics and install clics
from SOAPpy import WSDL
import os
import paths

class WSHandler:
    def __init__(self):
        self.clics_path = paths.clics_path
        self.namespace = ''

#    Returns all the clics information from the web service
    def get_clics_from_webservice(self):
        server = WSDL.Proxy(paths.web_service)
        self.namespace = server.methods['GetAllProjects'].namespace
        projects = server.GetAllProjects()
        return projects
#{'SubscriptionId':'Description':'Language':'Author':'Screenshot':'Area':'SubscriptionName': 'Title':'File':'Date': 'Level': 'Id': 'Icon'}

#Downloads a Jclic to the computer
    def download_clic(self, clic_file):
        t = os.system('mkdir ' + self.clics_path)
        t = os.system('wget -q '+ self.namespace +'/'+ clic_file +' --directory-prefix='+ self.clics_path)
        return t

#Unzips the Jclic to a local folder and removes the file
    def install_clic(self, clic):   
        #self.label.set_text('File downloaded')
        t = os.system('unzip '+ self.clics_path + '/'+clic['File'] + ' -d ' + self.clics_path + '/' + clic['File'].split('.',1)[0])            
        if t == 0:
            os.system('rm '+ self.clics_path + '/' + clic['File'])
        else :
            print 'Not installed (ws_handler)'        
        return t     
    