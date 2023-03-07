# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import  QHBoxLayout, QMessageBox



class Ui_Form(QtWidgets.QWidget):
    # add init function
    def __init__(self,windows):
        super(Ui_Form, self).__init__()
        self.setupUi(self,windows)

    def setupUi(self, Form,windows):
        Form.setObjectName("Form")
        Form.resize(1200,900)

        formbody = QHBoxLayout() #use form layout

        # add component to form
        for window in windows:
            formbody.addWidget(window) # add each child view
        self.setLayout(formbody) #set layout

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PackMaster Controller Monitor"))
    
    def showMsg(self,type,str):
        QMessageBox.about(self, type, str)