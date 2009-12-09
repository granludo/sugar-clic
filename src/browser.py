from hulahop.webview import WebView
import gtk
import xpcom

from xpcom.nsError import *
from xpcom import components
from xpcom.components import interfaces
from xpcom.server.factory import Factory

from progresslistener import ProgressListener
from downloadmanager import Download
from downloadmanager import HelperAppLauncherDialog

class ContentInvoker:
    _com_interfaces_ = interfaces.nsIDOMEventListener

    def __init__(self, browser):
        self._browser = browser

    def handleEvent(self, event):
        print event

        if event.button != 2:
            return

        target = event.target
        print target.tagName.lower()

class Browser(WebView):
    def __init__(self):
        WebView.__init__(self)
        self.progress = ProgressListener()

        io_service_class = components.classes[ \
        "@mozilla.org/network/io-service;1"]
        io_service = io_service_class.getService(interfaces.nsIIOService)

        # Use xpcom to turn off "offline mode" detection, which disables
        # access to localhost for no good reason.  (Trac #6250.)
        io_service2 = io_service_class.getService(interfaces.nsIIOService2)
        io_service2.manageOfflineStatus = False

        self.progress.connect('loading-stop', self._loaded)
        self.progress.connect('loading-progress', self._loading)

    def do_setup(self):
        print "do_setup"
        WebView.do_setup(self)
        self.progress.setup(self)
        
        listener = xpcom.server.WrapObject(ContentInvoker(self),
                                            interfaces.nsIDOMEventListener)
        self.window_root.addEventListener('click', listener, False)

    def _loaded(self, progress_listener):

        print "loaded"
        
    def _loading(self, progress_listener, progress):

        print "loading", progress
        
class PopupDialog(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

        border = 1 #style.GRID_CELL_SIZE
        self.set_default_size(gtk.gdk.screen_width() - border * 2,
                              gtk.gdk.screen_height() - border * 2)

        self.view = WebView()
        self.add(self.view)
        self.view.realize()
        self.show()

class WindowCreator:
    _com_interfaces_ = interfaces.nsIWindowCreator

    def createChromeWindow(self, parent, flags):
        dialog = PopupDialog()

        #modify if i want the same window 
        browser = dialog.view.browser

        if flags & interfaces.nsIWebBrowserChrome.CHROME_OPENAS_CHROME:
            dialog.view.is_chrome = True

            item = browser.queryInterface(interfaces.nsIDocShellTreeItem)
            item.itemType = interfaces.nsIDocShellTreeItem.typeChromeWrapper

        return browser.containerWindow
    
components.registrar.registerFactory('{64355793-988d-40a5-ba8e-fcde78cac631}',
                                     'Kumu Download Test Manager',
                                     '@mozilla.org/helperapplauncherdialog;1',
                                     Factory(HelperAppLauncherDialog))

components.registrar.registerFactory('{23c51569-e9a1-4a92-adeb-3723db82ef7c}',
                                     'KumuTest Download',
                                     '@mozilla.org/transfer;1',
                                     Factory(Download))