# this file is currently not in use
"""
# -*- encoding:utf-8 -*-
#from utils.core import Core
from view.deviceSetting import Ui_Form
from model.parameter import parameter as pr


"""
    #setting pannel for device parameter, inlude history
"""

class deviceSettingController:
    # available mood dictionary
    # name: index
    modeIndex = {
        "OOO":-1, # this is off state
        "DDD":0,
        "VDD":1,
        "DDI":2,
        "DOO":3,
        "AOO":4,
        "AAI":5,
        "VOO":6,
        "VVI":7,
        "AAT":8,
        "VVT":9,
        "DDDR":10,
        "VDDR":11,
        "DDIR":12,
        "DOOR":13,
        "AOOR":14,
        "AAIR":15,
        "VOOR":16,
        "VVIR":17
    }
    modeIndex1 = {
        "O":0,
        "A":1,
        "V":2,
        "D":3
    }
    modeIndex3 = {
        "O":0,
        "T":1,
        "I":2,
        "D":3
    }
    checkBox = {
        "SAVDO":"SAVDO_en",
        "VPAR":"VPAR_en",
        "APAR":"APAR_en",
        "PVARPE":"PVARPE_en"
    }


    #-----------------------------------------------------------------------
    #        Constructor (show windows)
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
        print(str(parent)+str(type(parent)))
        self.core = parent; # do not miss this line, core is necessary
        self.view = Ui_Form()
        # field
        self.parameter = pr()
        # add button event
        self.view.B_Logout.clicked.connect(self.logOut)
        self.view.B_Save.clicked.connect(self.save)
        self.view.B_Upload.clicked.connect(self.upload)
        self.view.B_Reset.clicked.connect(self.resetDefault)
        self.view.B_Cur.clicked.connect(self.resetCurrent)
        self.view.B_ConfirmMode.clicked.connect(self.confirmForm)
        # check box state change event
        self.view.SAVDO_en.stateChanged.connect(self.checkBoxEn)
        self.view.VPAR_en.stateChanged.connect(self.checkBoxEn)
        self.view.APAR_en.stateChanged.connect(self.checkBoxEn)
        self.view.PVARPE_en.stateChanged.connect(self.checkBoxEn)
        # when mode index changed
        #self.view.I_Pace.currentIndexChanged.connect(self.refreshForm)
        self.view.I_Rate.currentIndexChanged.connect(self.refreshForm)
        self.view.I_Response.currentIndexChanged.connect(self.refreshForm)
        #self.view.I_Sence.currentIndexChanged.connect(self.refreshForm)
        self.resetDefault()
        self.checkBoxEn()

    
    def loadView(self):
        return self.view
    
    def loadUser(self,user):
        self.username = user.username
        self.view.B_Logout.setText("Logout:" + user.username)

    def loadParameter(self):
        for key, value in self.parameter.parameters.items():
            itemtype = str(type(self.view.__dict__[key]))
            if(itemtype.find("QLineEdit")!=-1):
                self.view.__dict__[key].setText(value)
                self.refreshFormByText(value)
            elif(itemtype.find("QComboBox")!=-1):
                self.view.__dict__[key].setCurrentText(value)
            else:
                self.view.__dict__[key].setProperty("value", value)
        # for special check box case
        temp = self.parameter.parameters
        for key, value in self.checkBox.items():
            if(temp[key] == "Off"):
                self.view.__dict__[value].setChecked(False)
            else:
                self.view.__dict__[value].setChecked(True)
            

    
    def getPara(self):
        para = {}
        for key, value in self.view.__dict__.items():
            if(value.isEnabled()):
                if(key.find("_")==-1):
                    valuetype = str(type(value))
                    if(valuetype.find("QLineEdit")!=-1):
                        value = value.text()
                    elif(valuetype.find("QComboBox")!=-1):
                        value = value.currentText()
                    else:
                        value = value.value()
                    para[key] = value
            else:
                para[key] = "Off"
        return para


    # action method
    def confirmForm(self):
        self.refreshFormByText(self.view.mode.text())

    def refreshFormByText(self,mode):
        try:
            index = self.modeIndex[mode]
            self.view.mode.setText(mode)
        except KeyError as e:
            self.view.showMsg("Mode Error",mode+" is not a proper mode")
        index = [0,0,0,0]
        index[0] = self.modeIndex1[mode[0]]
        index[1] = self.modeIndex1[mode[1]]
        index[2] = self.modeIndex3[mode[2]]
        if(len(mode)>3 and mode[3]=="R"):
            index[3] = 1
        else:
            index[3] = 0
        self.view.I_Pace.setCurrentIndex(index[0])
        self.view.I_Sence.setCurrentIndex(index[1])
        self.view.I_Response.setCurrentIndex(index[2])
        self.view.I_Rate.setCurrentIndex(index[3])
        self.setDisabled(mode)


    def refreshForm(self):
            # get current value
            pace = self.view.I_Pace.currentText().split("-")[0]
            sense = self.view.I_Sence.currentText().split("-")[0]
            response = self.view.I_Response.currentText().split("-")[0]
            if (self.view.I_Rate.currentText()=="None"):
                rate = ""
            else:
                rate = "R"
            mode = pace+sense+response+rate
            print(mode)
            try:
                index = self.modeIndex[mode]
                self.view.mode.setText(mode)
                self.setDisabled(mode)
            except KeyError as e:
                self.view.showMsg("Mode Error",mode+" is not a proper mode")

    def logOut(self):
        self.core.core.openView("login")
        self.core.view.hide()
    
    def save(self):
        self.parameter.parameters = self.getPara()
        result = self.parameter.save(self.username,"save")
        if result == True:
            self.view.showMsg("Success","Save Success")
        else:
            meg = ""
            for key, value in result.items():
                meg += (key+value[2] + "Range: "+ str(value[0])+" Increment: "+str(value[1])+". "+"\n")
            self.view.showMsg("Error", meg)

    def upload(self):
        result = self.view.confirm('Are you sure to upload parameters to pacemaker')
        #if select yes
        if (result == 16384): 
            # check device connection
            if(self.device.connection == False):
                self.view.showMsg("Error", "No device Connected")
                return
            
            self.parameter.parameters = self.getPara()
            # add line where we will upload through device
            result = self.parameter.save(self.username,"upload") # save history
            if result == True:
                 self.view.showMsg("Success","Upload Success")
            else:
                meg = ""
                for key, value in result.items():
                    meg += (key+value[2] + "Range: "+ str(value[0])+" Increment: "+str(value[1])+". "+"\n")
                self.view.showMsg("Error", meg)

            

    def resetDefault(self):
        self.parameter.getDefault()
        self.loadParameter()

    def resetCurrent(self):
        pass

    def setDisabled(self,mode):
        disabledList = self.parameter.getDisabled(mode)
        for key, value in self.view.__dict__.items():
            value.setEnabled(True)
        for key, value in self.checkBox.items():
            self.view.__dict__[value].setChecked(True)
        for key in disabledList:
            self.view.__dict__[key].setEnabled(False)
            if key in self.checkBox.keys():
                checkBoxName = self.checkBox[key]
                self.view.__dict__[checkBoxName].setChecked(False)
                self.view.__dict__[checkBoxName].setEnabled(False)
            
        
        
    
    def checkBoxEn(self):
        for key, value in self.checkBox.items():
            if(self.view.__dict__[value].isChecked()):
                self.view.__dict__[key].setEnabled(True)
            else:
                self.view.__dict__[key].setEnabled(False)
       
"""
        




    