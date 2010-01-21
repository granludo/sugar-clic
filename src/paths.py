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
from sugar.activity import activity
import os
# paths used in the application

# old web_service
web_service = 'http://potato.lsi.upc.edu/jclicrepository/index.php?wsdl'

#paths to use outside the Xo laptop
bundle = '.'
data = './data'
clics = './data/clics'

# root path of the activity (in a Xo laptop is /home/olpc/Activities/activity/)
application_bundle_path = bundle

# Where the activity stores its data (clics, hulahop settings, ...)
application_data_path = data

# folder where the clics are stored
clics_path = clics


def get_db_path():
    global application_bundle_path
##############ONLY FOR ALPHA TEST###############################       
    cmd = 'echo ' + application_bundle_path + '/data'
################################################################        
#    cmd = 'echo ' + application_data_path
    fin,fout = os.popen4(cmd)
    result = fout.read()
    result = result.replace ( '\n', '' )
    result = os.path.join(result , 'downloaded.xml')
    return result

#Returns the absolute path of the clic folder
def get_clic_path(clic_name):
    fin,fout = os.popen4('echo ' + clics_path)
    result = fout.read()
    result = result.replace ( '\n', '' )
    return os.path.join(result , clic_name)
    
def set_environment(is_Xo):
    global application_bundle_path, application_data_path, clics_path
    if is_Xo :
        application_data_path = os.path.join(activity.get_activity_root(), 'data') 
        application_bundle_path = activity.get_bundle_path()
        ##############ONLY FOR ALPHA TEST###########################################
        clics_path = os.path.join(application_bundle_path , 'data/clics')          
        ############################################################################ 
        #clics_path = os.path.join(application_data_path , 'clics') #path to the folder that contains the clics
    
    
    