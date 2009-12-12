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
#paths used in the application

###########################USE ONLY IN YOUR UNIX SESSION##################
__UNIX_data = './data'
__UNIX_bundle = '.'
##########################################################################

####################USE ONLY IN OLPC LAPTOP###############################
##Comment it when you are not in OLPC!!!!
###activity folder to store data ($SUGAR_ACTIVITY_ROOT)
#__XO_data =  os.path.join(activity.get_activity_root(), 'data') 
###activity path (in /home/olpc/Activities folder) ($SUGAR_ACTIVITY_BUNDLE)
#__XO_bundle = activity.get_bundle_path()
##########################################################################

web_service = 'http://potato.lsi.upc.edu/jclicrepository/index.php?wsdl'

#root folder of the application
application_bundle_path = __UNIX_bundle

#folder to store clics files
application_data_path = __UNIX_data

##############ONLY FOR ALPHA TEST###############################       
clics_path = application_bundle_path + '/data/clics' 
################################################################ 
 
#clics_path = application_data_path + '/clics' #path to the folder that contains the clics


#Returns the absolute path of the clic folder
def get_clic_path(clic_name):
        fin,fout = os.popen4('echo ' + clics_path)
        result = fout.read()
        result = result.replace ( '\n', '' )
        return result + '/' + clic_name
    
    