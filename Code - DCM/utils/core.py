import sys
from PyQt5.QtWidgets import QApplication
# import every controller
import controller.loginController as login
import controller.registerController as register
import controller.mainWinController as mainWin



"""
    Class responsible for opening controllers
"""
class Core(QApplication): 
    windows = {}
    def __init__(self):
        app = QApplication(sys.argv)
        # initialize every controller
        Core.windows= {
            "login":login.loginController(self),
            "register":register.registerController(self),
            "mainWin":mainWin.mainWinController(self),
        }
        #default page is login page
        self.openView("login")
        sys.exit(app.exec_()) 
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    """
        Given a controller name, return an instance of it
    
        @param controller:string Controller to be opened

        this method currently not for use becuase is cause error in pyinstaller
    """
    """ 
    @staticmethod
    def openController(controller):
        response = None

        # Set controller name
        controllerName = controller+"Controller"
        
        # Check if file exists
        if os.path.exists(APP_PATH+"/controller/"+controllerName+".py"):
            module = importlib.import_module("controller."+controllerName)
            class_ = getattr(module, controllerName)
            response = class_()
        
        print("create controller "+controller)
        return response
    """
    @staticmethod
    def openView(viewName):
        # print(viewName)
        Core.windows[viewName].loadView()

    @staticmethod
    def loadUser(viewName,user):
        # print(viewName)
        Core.windows[viewName].loadUser(user)
        
        