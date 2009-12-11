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
import paths

class DbClics:
    def __init__(self):
        self.path_db = self.__get_path_db() #Absolute path of the downloaded.xml (File with information about clics downloaded)          
        self.__load_db()

    def __get_path_db(self):
        cmd = 'echo ' + paths.application_data_path
        fin,fout = os.popen4(cmd)
        result = fout.read()
        result = result.replace ( '\n', '' )
        result = result + '/downloaded.xml'

        return result

    #Creation of the DB
    def __load_db(self):
        if not os.path.exists(self.path_db):
            self.__create_db()   
            
    #Returns a list with all the clics downloaded          
    def get_clics(self):
        doc = minidom.parse(self.path_db)        
        files = doc.childNodes[0]
        l = list()
        clic = {'Title': '',
                    'Author': '',
                    'Area': '',
                    'Language': '',
                    'File': ''              
                }
        for file in files.childNodes: 
            clic = {'Title': file.childNodes[0].childNodes[0].data,
                    'Author': file.childNodes[1].childNodes[0].data,
                    'Area': file.childNodes[2].childNodes[0].data,
                    'Language': file.childNodes[3].childNodes[0].data,
                    'File': file.childNodes[4].childNodes[0].data              
                    }
            l.append(clic)
        return l

    #insert clic to the DB    
    def insert_clic(self, clic):
        doc = minidom.parse(self.path_db)
        wml = doc.childNodes[0]
            
        #Create the main <card> element
        element = doc.createElement('file')
        wml.appendChild(element)
    
        #Add the new file
        title = doc.createElement('title')
        element.appendChild(title)
        nodeTitle = doc.createTextNode(clic['Title'])
        title.appendChild(nodeTitle)
            
        author = doc.createElement('author')
        element.appendChild(author)
        ptext = doc.createTextNode(clic['Author'])
        author.appendChild(ptext)
                    
        area = doc.createElement('area')
        element.appendChild(area)
        ptext = doc.createTextNode(clic['Area'])
        area.appendChild(ptext)
                    
        language = doc.createElement('language')
        element.appendChild(language)
        ptext = doc.createTextNode(clic['Language'])
        language.appendChild(ptext)
                    
        fileName = doc.createElement('file_name')
        element.appendChild(fileName)
        nodeFile = doc.createTextNode(clic['File'])
        fileName.appendChild(nodeFile)
            
        file = doc.toxml()
        f = open(self.path_db, 'w')
        f.write(file)
        f.close()

    #Creates the file downloaded.xml       
    def __create_db(self):
        doc = minidom.Document()
        # Create the <wml> base element
        wml = doc.createElement('files')
        doc.appendChild(wml)
        doc.toxml
        file = doc.toxml()
        global path_db
        f = open(self.path_db, 'w')
        f.write(file)
        f.close()

#def remove_clic():
#        print 'Not yet implemented'        