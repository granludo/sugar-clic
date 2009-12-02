from db_clics import DbClics
from ws_handler import WSHandler
from module_handler import ClicParser 
from sequencer import Sequencer
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
    __ws = WSHandler()
    __mh = ClicParser() 
    
    def __init__(self):
        self.db = self.__db
        self.seq = self.__seq
        self.ws = self.__ws
        self.mh = self.__mh
        
    #downloads and installs a new clic (after that, is ready to play)
    def add_new_clic(self, clic):
        t = self.ws.download_clic(clic['File'])
        if t == 0 :
            t = self.ws.install_clic(clic)
            if t == 0:
                self.db.insert_clic(clic)
        return t
       
    #returns a list of clics available in the web service
    def get_clics_list(self):
        return self.ws.get_clics_from_webservice()
    
    #returns a list of installed clics
    def get_installed_clics(self):
        return self.db.get_clics()

    #initialize all the structure information to play the clic
    def load_clic(self, clic_name):
        clic_path = paths.get_clic_path(clic_name)
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
