#Module that interacts with the Jclic
from xml.dom import minidom

class ClicParser:
    def __init__(self):
        self.clic_activities = '' #list of activities that contains the jclic

    #Parse information about the clic (sequence, mediaBag, settings)
    def get_clic_info(self, clic_path, clic_name):
        JClicProject = minidom.parse(clic_path + '/' + clic_name + '.jclic')
        set = JClicProject.getElementsByTagName('settings')
        seq = JClicProject.getElementsByTagName('sequence')
        act = JClicProject.getElementsByTagName('activities')
        med = JClicProject.getElementsByTagName('mediaBag')
        settings = set[0]    
        sequence = seq[0]    
        self.clic_activities = act[0]    
        mediaBag = med[0] 
        return sequence, mediaBag, settings

    #Returns the xml code related with the activity_name
    def get_clic_activity(self, activity_name):
        for clic_activity in self.clic_activities.getElementsByTagName('activity'):
            if clic_activity.getAttribute('name') == activity_name:
                return clic_activity        
        raise SyntaxError, "No activities with this name"  

    
    
    
    
    
    

