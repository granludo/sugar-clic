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
    