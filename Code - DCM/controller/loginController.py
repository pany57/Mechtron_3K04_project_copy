# -*- encoding:utf-8 -*-
#from utils.core import Core
from view.login import Ui_Form
from model.user import User

"""
    Login
"""
class loginController:
    #-----------------------------------------------------------------------
    #        Constructor (show windows)
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
        print(str(parent)+str(type(parent)))
        self.core = parent; # do not miss this line, core is necessary
        self.view = Ui_Form()
        ## add button event
        self.view.B_Login.clicked.connect(self.login)
        self.view.B_Register.clicked.connect(self.register)

    def loadView(self):
        self.view.show()

    def login(self):
        username = self.view.I_UserName.text()
        password = self.view.I_Password.text()
        # validate info
        if(username == ""):
            self.view.showMsg("Please Input User Name")
            return
        if(password == ""):
            self.view.showMsg("Please Input Password")
            return
        # check users information
        try:
            #get infor of user
            user = User()
            user.getUser(username)
            result = user.checkPW(password) #check pw
            if(result):
                # clear password
                self.view.I_Password.setText('');
                # open new win
                self.core.openView("mainWin")
                self.core.loadUser("mainWin",user)
                self.view.hide()
            else:
                self.view.showMsg("User not exist or password not match")
        except Exception as e:
            self.view.showMsg(str(e))

    def register(self):
        #loginController.exit();
        self.core.openView("register") # open new windows

    