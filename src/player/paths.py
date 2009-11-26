import os
#paths used in the application
__Fedora = '$HOME/Desktop/data'
__XO = '$SUGAR_ACTIVITY_ROOT/data' #an activity can only store in a specific folder
web_service = 'http://potato.lsi.upc.edu/jclicrepository/index.php?wsdl'
application_data_path = __Fedora
clics_path = application_data_path + '/clics' #path to the folder that contains the clics


#Returns the absolute path of the clic folder
def get_clic_path(clic_name):
        fin,fout = os.popen4('echo ' + clics_path)
        result = fout.read()
        result = result.replace ( '\n', '' )
        return result + '/' + clic_name