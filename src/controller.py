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
from db_clics import DbClics
from module_handler import ClicParser 
from sequencer import Sequencer
from clicInstaller import Installer
import paths


class Controller:
    #The Borg pattern allows multiple class instances, but shares state between instances 
    #so the end user cannot tell them apart. Here is the Borg example from the Python Cookbook:
    #class Borg:
        #__shared_state = {}
        #def __init__(self):
            #self.__dict__ = self.__shared_state
    # and whatever else you want in your class -- that's all!
    
    #initiates all the services used in the application (only one time)
    #after the first call, do:
    #import controller
    #c = controller.Controller()
    __seq = Sequencer()
    __db = DbClics()
    __mh = ClicParser() 
    __ins = Installer()
    
    def __init__(self):
        self.db = self.__db
        self.seq = self.__seq
        self.mh = self.__mh
        self.ins = self.__ins
        
    #adds new clic to db list
    def add_new_clic(self, clic):
        self.db.insert_clic(clic)
    
    #returns a list of installed clics
    def get_installed_clics(self, default):
        return self.db.get_clics(default)
    
    def load_about(self):
        sequence, media, settings = self.mh.get_clic_info(paths.about_path, 'sugar_clic_help')
        self.seq.begin_sequence(sequence, media, settings, paths.about_path, 'sugar_clic_help')       

    #initialize all the structure information to play the clic
    def load_clic(self, clic_name, is_default):
        clic_path = paths.get_clic_path(clic_name, is_default)
        sequence, media, settings = self.mh.get_clic_info(clic_path, clic_name)
        self.seq.begin_sequence(sequence, media, settings, clic_path,clic_name)
    
    #returns all the xml code related with this clic_activity
    def get_clic_activity(self, activity_name):
        return self.mh.get_clic_activity(activity_name)
    
    #calls the activity_clic and returns new information about it
    def updating_activity(self):
        return self.seq.activity_clic_information()
    
    #plays the clic and starts the first activity of the clic
    def play_clic(self):
        self.seq.play()
        
    #remove clic
    def remove_clic(self, clic):
        self.db.remove_clic_from_db(clic)
        self.ins.delete_clic_folder(clic)

