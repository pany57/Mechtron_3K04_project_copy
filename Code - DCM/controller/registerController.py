# -*- encoding:utf-8 -*-

from os import error
from view.register import Ui_Register
from model.user import User
"""
    Register 
"""
class registerController:
    #-----------------------------------------------------------------------
    #        Constructor (show windows)
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
        self.core = parent; # do not miss this line, core is necessary
        self.view = Ui_Register()
        ## add button event
        self.view.B_Register.clicked.connect(self.register)
        

    def loadView(self):
        self.view.show()

    def register(self):
        username = self.view.I_UserName.text();
        password = self.view.I_Password.text();
        rePassword = self.view.I_PasswordRe.text();
        # validate info
        if(username == ""):
            self.view.showMsg("Error","Please Input User Name")
            return
        if(password == ""):
            self.view.showMsg("Error","Please Input Password")
            return
        if (password != rePassword):
            self.view.showMsg("Error","Passwords not match")
            return
        # add to database
        try:
            user = User(username,password)
            result = user.addUser()
            if(result == True):
                # clear all input
                self.view.I_UserName.setText('');
                self.view.I_Password.setText('');
                self.view.I_PasswordRe.setText('');
                self.view.showMsg("Success","Register Success! Click OK and go to login")
                self.view.hide()
            else:
                self.view.showMsg("Error",result)
        except Exception as e:
            self.view.showMsg("Error",str(e))


    