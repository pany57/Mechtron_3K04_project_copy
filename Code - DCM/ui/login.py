# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 283)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 0, 531, 281))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.I_UserName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.I_UserName.setObjectName("I_UserName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.I_UserName)
        self.L_password = QtWidgets.QLabel(self.formLayoutWidget)
        self.L_password.setObjectName("L_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.L_password)
        self.I_Password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.I_Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.I_Password.setObjectName("I_Password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.I_Password)
        self.L_UserName = QtWidgets.QLabel(self.formLayoutWidget)
        self.L_UserName.setObjectName("L_UserName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.L_UserName)
        self.B_Forgot = QtWidgets.QPushButton(self.formLayoutWidget)
        self.B_Forgot.setObjectName("B_Forgot")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.B_Forgot)
        self.B_Login = QtWidgets.QPushButton(self.formLayoutWidget)
        self.B_Login.setObjectName("B_Login")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.B_Login)
        self.B_Register = QtWidgets.QPushButton(self.formLayoutWidget)
        self.B_Register.setObjectName("B_Register")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.B_Register)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.L_password.setText(_translate("Form", "PassWord"))
        self.L_UserName.setText(_translate("Form", "User Name"))
        self.B_Forgot.setText(_translate("Form", "Forgot Password"))
        self.B_Login.setText(_translate("Form", "Login"))
        self.B_Register.setText(_translate("Form", "Register New User"))
