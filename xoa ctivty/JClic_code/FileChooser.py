"""
  Small class to create a FileChoosher, to test the program
"""

from os import getcwd
import wx

class FileChooser(object):
            
    def chooseFile(self):
	app = myChoosingApp(0)
        app.MainLoop()
        return app.filePath

class myChoosingApp(wx.App):

    filePath = ""

    frame = None   
 
    def OnInit(self):
        self.frame = ChoosingFrame(None, -1, "Obrir Fitxers", (300,150), (200,200), self)
        self.frame.Show(True)
        return True

class ChoosingFrame(wx.Frame):
    
    app = None
        
    def __init__(self, parent, id, title, position, size, app):
        wx.Frame.__init__(self, parent, id, title, position, size)
        
        self.app = app
        
        b = wx.Button(self, -1, "Open a file",(43,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        cancel = wx.Button(self, -1, "Exit",(65,100))
        self.Bind(wx.EVT_BUTTON, self.OnButton1, cancel)
    
    def OnButton(self, evt):
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=getcwd(), defaultFile="", style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
             #This returns a Python list of files that were selected.
            path = dlg.GetPath()
            if (path[-5:] == "jclic" or path[-5:] == "JCLIC" or path[-9:] == "jclic.zip" or path[-5:]=="JCLIC.ZIP"):
                self.app.filePath = path
		self.app.ExitMainLoop()
                        
            else:
                
                dlg.Close()
                print("You haven't picked the right type of file, it should be a .jclic!!")
         
    def OnButton1(self, evt):
        self.Close()
