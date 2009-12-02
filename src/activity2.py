# Load GTK
import gtk
import os
import gobject
# Load our own source code from clic_player.py
# There you can find the main class clic_player()
from clic_player import clic_player
# Load sugar libraries
from sugar.activity import activity  

class JClicDownloaderActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self._name = handle

        # Set title for our Activity
        self.set_title('Clic Player')

        # Attach sugar toolbox (Share, ...)
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        # Create the main container
        self._main_view = gtk.VBox()
        
        # Import our class clic_player():

        # Step 1: Load class, which creates clic_player.widget
        self.clic_player = clic_player()

        # Step 2: Remove the widget's parent
        if self.clic_player.widget.parent:
            self.clic_player.widget.parent.remove(self.clic_player.widget)
 
        # Step 3: We attach that widget to our window
        self._main_view.pack_start(self.clic_player.widget)

        # Display everything
        self.clic_player.widget.show()
        self._main_view.show()
        self.set_canvas(self._main_view)
        self.show()
        
        # Get the mainloop ready to run (this should come last).
        gobject.timeout_add(20, self.mainloop)
    def mainloop (self):
        # Runs the game loop. Note that this doesn't actually return until the activity ends.
        while True:
            self.clic_player.updating()
            gtk.main_iteration(False)
