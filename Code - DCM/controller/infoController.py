# this file is currently not in use
'''
# -*- encoding:utf-8 -*-
#from utils.core import Core
from view.info import Ui_Form
from PyQt5 import QtCore
from model.device import device


"""
    Information panel, include graph, device status and information, user information
"""
class infoController:
    #-----------------------------------------------------------------------
    #        Constructor (show windows)
    #-----------------------------------------------------------------------
    def __init__(self, parent=None):
        print(str(parent)+str(type(parent)))
        self.core = parent; # do not miss this line, core is necessary
        self.view = Ui_Form()
        self.device = device() 
        ## add button event

        # controller parameter
        self.data_list = []
        self.data_list2 = []
        self.start_data = -1

        # timer event
        self.view.timer.timeout.connect(self.get_info)
        self.samplingperiod = 500
        #self.check_connection()    

        #monitor signal send from device
        self.device.newConnect.connect(self.newConnection)
        self.device.status.connect(self.message)
        """
        Test button, will be removed after formal deployment
        """
        self.view.testConnect.clicked.connect(self.check_connection)
        self.view.testUnconnect.clicked.connect(self.lost_connnect)
        self.view.showEgram.clicked.connect(self.start_graph)
        self.view.stopEgram.clicked.connect(self.stop_graph)
        """
        Test button end, will be removed after formal deployment
        """
    
    def lost_connnect(self):
        self.view.connect.setText("Connection: "+"False")
        self.view.battery.setText("Battery: "+"No infomation")
        self.device.connection = False
        self.view.showMsg("Note","Connection Lost")

    '''
    #for test only
    '''


    def loadView(self):
        return self.view
    
    def loadUser(self,user):
        self.user = user # access user information
        self.user_info()

    @QtCore.pyqtSlot(str)
    def message(self,str):
        self.view.showMsg(str)

    # graph action
    def start_graph(self):
        if(self.device.connection):
            self.view.timer.start(self.samplingperiod)
        else:
            self.view.showMsg("Error", "No device Connected")

    def stop_graph(self):
        self.view.timer.stop()

    def get_info(self):
        data = self.device.getEgram()
        self.data_list.append(float(data))
        xrange = 10

        if len(self.data_list) > 10:
            self.start_data += 1
            self.view.graph.setXRange(self.start_data,self.start_data+xrange)
        else:
            self.view.graph.setXRange(0,xrange)

        self.view.graph.plot().setData(self.data_list,pen = 'g')

    # button action
    
    # device action
    @QtCore.pyqtSlot(str)
    def newConnection(self,port):
        result = self.view.confirm("New Device Approch at " +port+". Connect to new device?")
        if (result == 16384):
            self.device.openSerial(port)
        # add new item to port
        self.view.port.addItems(self.device.getSerialPorts())
        self.device.timer.start(500)
    
    
    def check_battery(self):
        self.view.battery.setText("Battery: "+str(self.device.getbatterydata()))

    def user_info(self):
        self.view.username.setText("User name is: "+self.user.username)
'''
    