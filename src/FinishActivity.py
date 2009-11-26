'''
Created on 09/05/2009

@author: mbenito
'''


from Activity import  Activity


class FinishActivity(Activity):
    

    def Load(self, display_surf ):
        pass


    def OnEvent(self,PointOfMouse):
        pass
           

    def OnRender(self,display_surf):
        pass
           
    def isGameFinished(self):
        return False

        