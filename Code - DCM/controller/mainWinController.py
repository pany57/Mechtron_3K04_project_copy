# -*- encoding:utf-8 -*-
#from utils.core import Core
from view.mainWin import Ui_Form
from view.deviceSetting import Ui_Form as deviceSetting
from view.info import Ui_Form as info
from model.parameter import parameter as pr
from model.device import device
from config import APP_PATH
from PyQt5 import QtCore, QtWidgets


"""
    Main Windows
"""
class mainWinController:
    #-----------------------------------------------------------------------
    #        Constructor (show windows)
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
        print(str(parent)+str(type(parent)))
        self.parameter = pr()
        self.device = device() 
        self.setWin = deviceSetting()
        self.infoWin = info()
        self.__connectionList()
        self.data_list=[]
        self.data_list2=[]
        self.start_data = -1
        self.start_data2 = -1
        #-----------------------------------------------------------------------
        #        device setting part
        #-----------------------------------------------------------------------
        self.resetDefault()
        self.checkBoxEn()

        #-----------------------------------------------------------------------
        #        info
        #-----------------------------------------------------------------------

        #store all windows 
        self.core = parent; # do not miss this line, core is necessary
        
        self.view = Ui_Form([self.setWin,self.infoWin])
        ## add button event

    def loadView(self):
        self.view.show()
     
    def loadUser(self,user):
        self.user = user
        self.user_info()

#-----------------------------------------------------------------------
#        info
#-----------------------------------------------------------------------
    def lost_connnect(self):
        self.infoWin.connect.setText("Connection: "+"False")
        self.infoWin.battery.setText("Battery: "+"No infomation")
        self.device.connection = False
        self.infoWin.showMsg("Note","Connection Lost")

    '''
    for test only
    '''

    def message(self,str):
        self.infoWin.showMsg("Serial Output",str)

    # graph action
    def start_graph(self):
        if(self.device.connection):
            self.infoWin.timer.start(self.samplingperiod)
        else:
            self.infoWin.showMsg("Error", "No device Connected")

    def stop_graph(self):
        self.infoWin.timer.stop()

    def get_info(self,data):

        self.data_list.append(5-data*5)
        print(5-data*5)
        xrange = 20
        if len(self.data_list) > 20:
            self.start_data += 1
            self.infoWin.graph.setXRange(self.start_data,self.start_data+xrange)
        else:
            self.infoWin.graph.setXRange(0,xrange)
        if len(self.data_list) > 100:
            self.start_data -= 1
            self.data_list.pop(0)
        self.infoWin.graph.clear()
        # self.infoWin.graph.title('Ventricle Signals')
        self.infoWin.graph.plot().setData(self.data_list,pen = 'g')

    def get_info2(self,data):

        self.data_list2.append(5-data*5)
        print(5-data*5)
        xrange = 20
        if len(self.data_list2) > 20:
            self.start_data2 += 1
            self.infoWin.atrialgraph.setXRange(self.start_data2,self.start_data2+xrange)
        else:
            self.infoWin.atrialgraph.setXRange(0,xrange)
        if len(self.data_list2) > 100:
            self.start_data2 -= 1
            self.data_list2.pop(0)
        self.infoWin.atrialgraph.clear()
        # self.infoWin.atrialgraph.title('Atrium Signals')
        self.infoWin.atrialgraph.plot().setData(self.data_list2,pen = 'g')
    # button action
    
    # device action
    def newConnection(self,port):
        result = self.infoWin.confirm("New Device approch at port " +port+". Connect to new device?")
        if (result == 16384):
            self.device.openSerial(port)
        # add new item to port
        self.infoWin.port.clear()
        self.infoWin.port.addItems(self.device.getSerialPorts())
        self.device.timer.start(500)
        self.infoWin.connect.setText("Device: Connected at "+port)
    
    def manualConnection(self):
        port = self.infoWin.port.currentText()
        if port!= "":
            self.device.openSerial(port)
            self.infoWin.connect.setText("Device: Connected at "+port)
        else:
            self.infoWin.showMsg("Error","Port Not selected. Please select the connection port first.")
    
    def manualUnconnect(self):
        self.device.closeSerial()
        self.infoWin.connect.setText("No Device Connected")
    
    def check_battery(self):
        self.infoWin.battery.setText("Battery: "+str(self.device.getbatterydata()))

    def user_info(self):
        self.infoWin.username.setText("User name is: "+self.user.username)
        self.infoWin.B_Logout.setText("Logout: "+self.user.username)


#---------------------------------------------------------------------
#    Device Setting page
#---------------------------------------------------------------------
    def loadParameter(self):
        for key, value in self.parameter.parameters.items():
            itemtype = str(type(self.setWin.__dict__[key]))
            if(itemtype.find("QLineEdit")!=-1):
                self.setWin.__dict__[key].setText(value)
                self.refreshFormByText(value)
            elif(itemtype.find("QComboBox")!=-1):
                self.setWin.__dict__[key].setCurrentText(value)
            else:
                self.setWin.__dict__[key].setProperty("value", value)
        # for special check box case
        temp = self.parameter.parameters
        for key, value in self.checkBox.items():
            if(temp[key] == "Off"):
                self.setWin.__dict__[value].setChecked(False)
            else:
                self.setWin.__dict__[value].setChecked(True)
            

    
    def getPara(self):
        para = {}
        for key, value in self.setWin.__dict__.items():
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
        self.refreshFormByText(self.setWin.mode.text())

    def refreshFormByText(self,mode):
        try:
            index = self.modeIndex[mode]
            self.setWin.mode.setText(mode)
        except KeyError as e:
            self.setWin.showMsg("Mode Error",mode+" is not a proper mode")
        index = [0,0,0,0]
        index[0] = self.modeIndex1[mode[0]]
        index[1] = self.modeIndex1[mode[1]]
        index[2] = self.modeIndex3[mode[2]]
        if(len(mode)>3 and mode[3]=="R"):
            index[3] = 1
        else:
            index[3] = 0
        self.setWin.I_Pace.setCurrentIndex(index[0])
        self.setWin.I_Sence.setCurrentIndex(index[1])
        self.setWin.I_Response.setCurrentIndex(index[2])
        self.setWin.I_Rate.setCurrentIndex(index[3])
        self.setDisabled(mode)


    def refreshForm(self):
            # get current value
            pace = self.setWin.I_Pace.currentText().split("-")[0]
            sense = self.setWin.I_Sence.currentText().split("-")[0]
            response = self.setWin.I_Response.currentText().split("-")[0]
            if (self.setWin.I_Rate.currentText()=="None"):
                rate = ""
            else:
                rate = "R"
            mode = pace+sense+response+rate
            print(mode)
            try:
                index = self.modeIndex[mode]
                self.setWin.mode.setText(mode)
                self.setDisabled(mode)
            except KeyError as e:
                self.setWin.showMsg("Mode Error",mode+" is not a proper mode")

    def logOut(self):
        self.core.openView("login")
        self.view.hide()
    
    def save(self):
        self.parameter.parameters = self.getPara()
        result = self.parameter.save(self.user.username,"save")
        if result == True:
            self.setWin.showMsg("Success","Save Success")
        else:
            meg = ""
            for key, value in result.items():
                meg += (key+value[2] + "Range: "+ str(value[0])+" Increment: "+str(value[1])+". "+"\n")
            self.setWin.showMsg("Error", meg)

    def load(self):
        test = self.parameter.load(self.user.username)
        if test == False:
            self.setWin.showMsg("Load Failed","Load Failed, user folder not exist!")
        else:
            directory = QtWidgets.QFileDialog.getOpenFileName(None,"Choose file",self.parameter.load(self.user.username))
            if directory[0] == '':
                self.setWin.showMsg("Load Failed","User must choose one json file to load!")
            else:
                self.setWin.showMsg("File Path",directory[0])
                self.parameter.loadcon(directory[0])
                self.loadParameter()
                self.setWin.showMsg("Success","Load Success!")


    def upload(self):
        result = self.setWin.confirm('Comfirm to upload parameters to pacemaker')
        #if select yes
        if (result == 16384): 
            # check device connection
            if(self.device.connection == False):
                self.setWin.showMsg("Error", "No device Connected")
                return
            
            self.parameter.parameters = self.getPara()
            # add line where we will upload through device
            result = self.parameter.save(self.user.username,"upload") # save history also check if parameter are valid
            if result == True:
                # do the actual serial send
                self.parameter.parameters['mode'] = self.modeIndex[self.parameter.parameters['mode']] # store index
                self.device.sendParam(self.parameter.parameters)
            else:
                meg = ""
                for key, value in result.items():
                    meg += (key+value[2] + "Range: "+ str(value[0])+" Increment: "+str(value[1])+". "+"\n")
                self.setWin.showMsg("Error", meg)


    def resetDefault(self):
        self.parameter.getDefault()
        self.loadParameter()

    def resetCurrent(self):
        self.parameter.getDefault()
        self.parameter.parameters = self.device.rqstPara(self.parameter.parameters)
        # result = self.parameter.savecurrent(self.user.username)
        # if result == True:
        #     filepath = self.parameter.load(self.user.username)
        #     self.parameter.loadcon(filepath+'/currentpara/from_device.json')
        #     self.loadParameter()
        self.loadParameter()
        self.setWin.showMsg("Success","Reset Success!")
        
    def export(self):
        atrial = self.data_list2
        ven = self.data_list
        result = self.parameter.savereport(self.user.username,atrial,ven)
        if result == True:
            self.setWin.showMsg("Success","Report saved in"+" "+APP_PATH+"/"+self.user.username+" folder")
        else:
            self.setWin.showMsg("Failed","Export failed, please try again")

    def setDisabled(self,mode):
        disabledList = self.parameter.getDisabled(mode)
        for key, value in self.setWin.__dict__.items():
            value.setEnabled(True)
        for key, value in self.checkBox.items():
            self.setWin.__dict__[value].setChecked(True)
        for key in disabledList:
            self.setWin.__dict__[key].setEnabled(False)
            if key in self.checkBox.keys():
                checkBoxName = self.checkBox[key]
                self.setWin.__dict__[checkBoxName].setChecked(False)
                self.setWin.__dict__[checkBoxName].setEnabled(False)
            
        
        
    
    def checkBoxEn(self):
        for key, value in self.checkBox.items():
            if(self.setWin.__dict__[value].isChecked()):
                self.setWin.__dict__[key].setEnabled(True)
            else:
                self.setWin.__dict__[key].setEnabled(False)
       
    # mode list
    modeIndex = {
        "OOO":0, # this is off state
        "DDD":1,
        "VDD":2,
        "DDI":3,
        "DOO":4,
        "AOO":5,
        "AAI":6,
        "VOO":7,
        "VVI":8,
        "AAT":8,
        "VVT":10,
        "DDDR":11,
        "VDDR":12,
        "DDIR":13,
        "DOOR":14,
        "AOOR":15,
        "AAIR":16,
        "VOOR":17,
        "VVIR":18
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

#-------------------------
# Conection List
    def __connectionList(self):
        #-----------------------------------------------------------------------
        #        device setting part
        #-----------------------------------------------------------------------
        # add button event
        
        self.setWin.B_Save.clicked.connect(self.save)
        self.setWin.B_Load.clicked.connect(self.load)
        self.setWin.B_Upload.clicked.connect(self.upload)
        self.setWin.B_Reset.clicked.connect(self.resetDefault)
        self.setWin.B_Cur.clicked.connect(self.resetCurrent)
        self.setWin.B_ConfirmMode.clicked.connect(self.confirmForm)
        # check box state change event
        self.setWin.SAVDO_en.stateChanged.connect(self.checkBoxEn)
        self.setWin.VPAR_en.stateChanged.connect(self.checkBoxEn)
        self.setWin.APAR_en.stateChanged.connect(self.checkBoxEn)
        self.setWin.PVARPE_en.stateChanged.connect(self.checkBoxEn)
        # when mode index changed
        self.setWin.I_Rate.currentIndexChanged.connect(self.refreshForm)
        self.setWin.I_Response.currentIndexChanged.connect(self.refreshForm)

        #-----------------------------------------------------------------------
        #        info
        #-----------------------------------------------------------------------
        # timer event
        self.infoWin.timer.timeout.connect(self.get_info)
        self.infoWin.timer.timeout.connect(self.get_info2)
        self.samplingperiod = 500
        #self.check_connection()    
        #button
        self.infoWin.showEgram.clicked.connect(self.device.startEgram)
        self.infoWin.stopEgram.clicked.connect(self.device.stopEgram)
        self.infoWin.testConnect.clicked.connect(self.manualConnection)
        self.infoWin.testUnconnect.clicked.connect(self.manualUnconnect)
        self.infoWin.B_Logout.clicked.connect(self.logOut)
        self.infoWin.export.clicked.connect(self.export)
        #monitor signal send from device
        self.device.newConnect.connect(self.newConnection)
        self.device.status.connect(self.message)
        self.device.egram.connect(self.get_info)
        self.device.atrialegram.connect(self.get_info2)
        #self.device.paraemit.connect(self.updatepara)

