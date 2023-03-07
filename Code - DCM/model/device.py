from PyQt5 import QtCore, QtSerialPort
import threading
import struct

class device(QtCore.QObject):

    status = QtCore.pyqtSignal(str)

    errorOccurred = QtCore.pyqtSignal()
    newConnect = QtCore.pyqtSignal(str)
    atrialegram = QtCore.pyqtSignal(float)
    egram = QtCore.pyqtSignal(float)
    #paraemit = QtCore.pyqtSignal()

    availablePort = set()

    def __init__(self):
        super(device, self).__init__()
        self.ser = QtSerialPort.QSerialPort(
            baudRate=QtSerialPort.QSerialPort.Baud115200
        )
        # field
        self.connection = False
        self.currentport = ''

        # for contineous scan
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkNewConnect)
        self.timer.start(500) # scan new every half s

        self.timer2 = QtCore.QTimer(self)

        #error handler
        self.__connectionsList()

    #access pacemaker
    def rqstPara(self,para1):
        # send request to device
        if self.isSerialOpen() == False:
            self.status.emit('Device not open')
            return 

        self.sendRequest(1)
        # read
        #self.readLine();
        para = self.startSerialRead(para1)

        return para
    
    def startEgram(self):
        # send request to device

        if self.isSerialOpen() == False:
            self.status.emit('Device not open')
            return
        self.sendRequest(2)
        self.timer2.timeout.connect(self.startSerialReadegram)
        self.timer2.start(100)
        # read
        #self.readLine();


    def stopEgram(self):
        # send request to device
        self.sendRequest(3)
        # read
        #self.readLine();
    
    def sendParam(self,para):
        # pre process parameter
        for key,value in para.items():
            if isinstance(value,str):
                if value == "Off":
                    para[key] = 0 # choose a value that represent off
                elif value == "On":
                    para[key] = 1
                elif value == "DDD":
                    para[key] =1
                elif value == "VDD":
                    para[key] =2
                elif value == "DDI":
                    para[key] =3
                elif value == "DOO":
                    para[key] =4
                elif value == "AOO":
                    para[key] =5
                elif value == "AAI":
                    para[key] =6
                elif value == "VOO":
                    para[key] =7
                elif value == "VVI":
                    para[key] =8
                elif value == "AAT":
                    para[key] =9
                elif value == "VVT":
                    para[key] =10
                elif value == "DDDR":
                    para[key] =11
                elif value == "VDDR":
                    para[key] =12
                elif value == "DDIR":
                    para[key] =13
                elif value == "DOOR":
                    para[key] =14
                elif value == "AOOR":
                    para[key] =15
                elif value == "AAIR":
                    para[key] =16
                elif value == "VOOR":
                    para[key] =17
                elif value == "VVIR":
                    para[key] =18
                    
                elif value == "V-Low":
                    para[key] =0
                elif value == "Low":
                    para[key] = 1
                elif value == "Med-Low":
                    para[key] = 2
                elif value == "Med":
                    para[key] = 3
                elif value == "Med-High":
                    para[key] = 4
                elif value == "High":
                    para[key] = 5
                elif value == "V-High":
                    para[key] = 6
                else:
                    para[key] = float(value)
        # send request
        self.sendRequest0(0,para)
    
    # access to device data
    def checkNewConnect(self):
        
        for i in self.getSerialPorts():
            if not(i in self.availablePort):
                self.timer.stop()
                self.newConnect.emit(i)
                self.availablePort.add(i)

    def getSerialPorts(self):
        ports = QtSerialPort.QSerialPortInfo.availablePorts()
        for p in range(len(ports)):
            ports[p] = ports[p].portName()
        return ports

    def closeSerial(self):
        if self.ser.isOpen():
            self.ser.close()
            self.status.emit("Port Was Successfully Closed")
            self.connection = False
            self.currentport = ''
        else:
            self.status.emit("Port Already Closed")

    def clearSerial(self):
        self.ser.clear(QtSerialPort.QSerialPort.AllDirections)

    def isSerialOpen(self):
        if (self.ser.isOpen()):
            return True
        else:
            #self.__errorHandler(13)
            return False
    
    # serial slot action
    # Type: 0x02-request egram 0x03-stopegram 0x01-request para 0x00-send para
    def sendRequest0(self,type, para=None):
        print("request data type ",type)

        if(not self.isSerialOpen()):
            self.status.emit("Serial Not Open")
            return 0

        try:
            if (self.ser.error() == 0):
                data=[]
                print("Start Sending")
                data.append(b'\x55')
                data.append(bytes([type]))
                # for j in data:
                #     print(j.hex())

                bytelen = 2

                for key,value in para.items():
                    if key == "APAU" or key =="VPAU" or key == "APAR" or key == "VPAR" or key =="AS" or key =="VS" :
                        byteval = struct.pack('<f', value)
                        lis = byteval
                        newlis = [lis[i:i+1] for i in range (0,len(lis),1)]
                        for i in range(len(newlis)):
                            data.append(newlis[i])
                            # print(newlis[i].hex())
                        bytelen += 4

                    elif key == "FAVD" or key == 'VRP' or key =='ARP' or key == 'PVARP' or key == 'ATRD' or key == 'ATRFT' or key == 'RT':
                            byteval = value.to_bytes(2,"little") # little: most significant last, big: most significant first
                            
                            lis = byteval
                            newlis = [lis[i:i+1] for i in range (0,len(lis),1)]
                            for i in range(len(newlis)):
                                data.append(newlis[i])
                                # print(newlis[i].hex())
                            bytelen += 2
                    elif key == "SAVDO_en" or key == "VPAR_en" or key == 'PVARPE_en' or key == 'APAR_en':
                        continue
                    else:
                        byteval = bytes([value])
                        bytelen += 1
                        data.append(byteval)
                        # print(byteval.hex())

                while bytelen < 58:
                    data.append(b'\x00')
                    bytelen += 1

                result = 0
                for i in data:
                    result ^= int.from_bytes(i,'little')
                    

                data.append(bytes([result]))
                for w in data:
                    self.ser.write(w)
                print(para)
                for j in data:
                    print(j.hex())
                
                print(bytelen)

                self.status.emit("Serial Sent Successfully")
                print("End Sending")

                return 1

        except Exception as e:
            pass    # Serial Error signal will direct error to __errorHandler
            
        return 0

    def sendRequest(self,type):
        print("request data type ",type)

        if(not self.isSerialOpen()):
            self.status.emit("Serial Not Open")
            return 0

        try:
            if (self.ser.error() == 0):
                data=[]
                print("Start Sending")
                data.append(b'\x55')
                data.append(bytes([type]))

                bytelen = 2

                while bytelen < 58:
                    data.append(b'\x00')
                    bytelen += 1

                result = 0
                for i in data:
                    result ^= int.from_bytes(i,'little')
                    

                data.append(bytes([result]))
                for w in data:
                    self.ser.write(w)
                for j in data:
                    print(j.hex())
                if type == 3:
                    self.timer2.stop()

                self.status.emit("Serial Sent Successfully")
                print("End Sending")
                return 1

        except Exception as e:
            pass    # Serial Error signal will direct error to __errorHandler

        return 0

    def openSerial(self, portText):
        currentConnected = portText #self.parentWidget.serialComboBox.currentText()

        if (self.isSerialOpen and portText == self.currentport and self.ser.portName() == currentConnected.split('/')[-1]):
            self.status.emit("Serial Port: " + str(currentConnected) + " - Already Open")

        # trying to connect a new device
        elif (self.ser.portName != currentConnected):

            # close the old port
            if self.isSerialOpen():
                self.closeSerial()

            # define port
            self.ser.setPortName(currentConnected)

            # open the serial port
            serstatus = self.ser.open(QtCore.QIODevice.ReadWrite)
            if (serstatus):
                self.status.emit("Serial Enabled - Connected to " + str(currentConnected))
                self.__connectionsList()    # establish connections
                self.clearSerial()
                self.currentport = portText
                self.connection = True
            else:
                self.__errorHandler()

    #need 
    def startSerialRead(self,para):
    
        print('Serial Thread:\t', threading.get_ident())

        readdata = self.ser.read(2)
        readtime = 2
        print(readdata)
        while readdata != b'\x55\x04':
            if readdata == b'':
                print("empty data please check the connection")
                self.status.emit('Please try again')
                return
            readtime += 2
            if readtime > 5900 :
                self.clearSerial()
                readtime = 0
            readdata = self.ser.read(2)
            print(readdata.hex())
        print("Start reading")
        if readdata == b'\x55\x04':
            print(readdata.hex())
            serdata = []
            serdata.append(b'\x55')
            serdata.append(b'\x04')
            while len(serdata)<59:
                readdata = self.ser.read(1)
                serdata.append(readdata)
                print(readdata.hex())


            dataindex = 2
            while(dataindex<58 ):
                
                # Start of Message
                SOM = serdata[0]

                if (SOM == b'\x55'):
                    try:
                        # if data is large enough
                        fncode = serdata[1]
                        if (fncode == b'\x04'): # echo_s
                            print("Receive Parameters from Pacemaker")
                            for key,value in para.items():
                                if key == "mode":
                                    if serdata[dataindex] == b'\x00':
                                        para[key] = "Off"
                                    elif serdata[dataindex] == b'\x01':
                                        para[key] = "DDD"
                                    elif serdata[dataindex] == b'\x02':
                                        para[key] = "VDD"
                                    elif serdata[dataindex] == b'\x03':
                                        para[key] = "DDI"
                                    elif serdata[dataindex] == b'\x04':
                                        para[key] = "DOO"
                                    elif serdata[dataindex] == b'\x05':
                                        para[key] = "AOO"
                                    elif serdata[dataindex] == b'\x06':
                                        para[key] = "AAI"
                                    elif serdata[dataindex] == b'\x07':
                                        para[key] = "VOO"
                                    elif serdata[dataindex] == b'\x08':
                                        para[key] = "VVI"
                                    elif serdata[dataindex] == b'\x09':
                                        para[key] = "AAT"
                                    elif serdata[dataindex] == b'\x10':
                                        para[key] = "VVT"
                                    elif serdata[dataindex] == b'\x11':
                                        para[key] = "DDDR"
                                    elif serdata[dataindex] == b'\x12':
                                        para[key] = "VDDR"
                                    elif serdata[dataindex] == b'\x13':
                                        para[key] = "DDIR"
                                    elif serdata[dataindex] == b'\x14':
                                        para[key] = "DOOR"
                                    elif serdata[dataindex] == b'\x15':
                                        para[key] = "AOOR"
                                    elif serdata[dataindex] == b'\x16':
                                        para[key] = "AAIR"
                                    elif serdata[dataindex] == b'\x17':
                                        para[key] = "VOOR"
                                    elif serdata[dataindex] == b'\x18':
                                        para[key] = "VVIR"
                                    dataindex += 1
                                elif key == "APAU" or key =="VPAU" or key == "APAR" or key == "VPAR" or key =="AS" or key =="VS" :
                                    for i in range(4):
                                        serdata[dataindex+i] = int.from_bytes(serdata[dataindex+i],'little')
                                    byte_array1 = bytearray(serdata[dataindex:dataindex+4])
                                    paravalue = struct.unpack('<f',byte_array1)
                                    para[key] = paravalue[0]
                                    if key == "APAU" or key == "VPAU":
                                        para[key] = str(para[key])
                                    dataindex += 4
                                elif key == "DAVD" or key == "SAVDO" or key == "HRL" or key == "ATRM":
                                    
                                    if serdata[dataindex] == b'\x00':
                                        para[key] = "Off"
                                    elif serdata[dataindex] == b'\x01':
                                        para[key] = "On"
                                    else :
                                        para[key] = int.from_bytes(serdata[dataindex],'little')
                                    dataindex += 1
                                elif key == "RS":
                                    if serdata[dataindex] == b'\x00':
                                        para[key] = "OFF"
                                    else:
                                        para[key] = int.from_bytes(serdata[dataindex],'little')
                                    dataindex += 1
                                elif key == "AT":
                                    if serdata[dataindex]==b'\x00':
                                        para[key] = "V-Low"
                                    elif serdata[dataindex] ==b'\x01':
                                        para[key] = "Low"
                                    elif serdata[dataindex] ==b'\x02':
                                        para[key] = "Med-Low"
                                    elif serdata[dataindex] ==b'\x03':
                                        para[key] = "Med"
                                    elif serdata[dataindex] ==b'\x04':
                                        para[key] = "Med-High"
                                    elif serdata[dataindex] ==b'\x05':
                                        para[key] = "High"
                                    elif serdata[dataindex] ==b'\x06':
                                        para[key] = "V-High"
                                    dataindex += 1
                                elif key == "FAVD" or key == 'VRP' or key =='ARP' or key == 'PVARP' or key == 'ATRD' or key == 'ATRFT' or key == 'RT':
                                    for j in range(2):
                                        serdata[dataindex+j] = int.from_bytes(serdata[dataindex+j],'little')
                                    byte_array2 = bytearray(serdata[dataindex:dataindex+2])
                                    paravalue = struct.unpack('<h',byte_array2)
                                    para[key] = paravalue[0]
                                    dataindex += 2
                                elif key == "SAVDO_en" or key == "VPAR_en" or key == 'PVARPE_en' or key == 'APAR_en':
                                    if serdata[dataindex] != b'\x00':
                                        para[key] = 1
                                else:
                                    para[key] = int.from_bytes(serdata[dataindex],'little')
                                    dataindex += 1
                                print(key,para[key],dataindex)
                            
                            # self.paraemit.emit(serdata)
                            print(para)
                            self.status.emit('Receive parameter data Success')
                            return para


                    
                    except Exception as e:
                        print("Internal Exception, \t", e)
                        break


            else:
                # not at start of message
                # Forseeable issue losing data points since they are not SOMs
                None

        # except Exception as e:
        #     # TODO handle error: QIODevice::read (QSerialPort): device not open
            
        #     pass 

    def startSerialReadegram(self):
    
        print('Serial Thread:\t', threading.get_ident())


        readdata = self.ser.read(1)
        readtime = 1
        print(readdata)
        while readdata != b'\x55':
            if readdata == b'':
                print("empty data please check the connection")
                return
            readtime += 1
            if readtime > 59*100 :
                self.clearSerial()
                readtime = 0
            readdata = self.ser.read(1)
            print(readdata)
        print("Start reading")
        if readdata == b'\x55':
            print(readdata.hex())
            serdata = []
            serdata.append(b'\x55')
            while len(serdata)<59:
                readdata = self.ser.read(1)
                serdata.append(readdata)
                print(readdata.hex())

        dataindex = 2
        while(dataindex<58):
            
            # Start of Message
            SOM = serdata[0]

            if (SOM == b'\x55'):
                try:
                    # if data is large enough
                    fncode = serdata[1]

                    if(fncode == b'\x05'):
                        print("Receive data from Pacemaker")
                        for i in range(8):
                            serdata[i+2] = int.from_bytes(serdata[i+2],'little')
                        byte_array = bytearray(serdata[2:10])
                        print(byte_array.hex())
                        atrialdata=struct.unpack('d',byte_array)
                        self.atrialegram.emit(atrialdata[0])
                        print(atrialdata[0])
                        for j in range(8):
                            serdata[j+10] = int.from_bytes(serdata[j+10],'little')
                        byte_array2 = bytearray(serdata[10:18])
                        print(byte_array2.hex())
                        ventriculardata = struct.unpack('d',byte_array2)
                        self.egram.emit(ventriculardata[0])
                        print(ventriculardata[0])

                except Exception as e:
                    print("Internal Exception, \t", e)
                    break


            else:
                # not at start of message
                # Forseeable issue losing data points since they are not SOMs
                None

    def __errorHandler(self, *args):
        

        if (self.ser.error() != 0): 
            self.status.emit("Serial Error:\t" + self.ser.errorString())
            if ('ser' in locals()):
                self.ser.close()

        # catch non-signal error
        elif(len(args) != 0):
            if (args[0] == 13):
                self.status.emit("Serial Error:\t" + "Device Not Open")
                
            elif (args[0] == 2):
                self.status.emit("Serial Error:\t" + "Permission Error")

            elif (args[0] == 7):
                self.status.emit("Serial Error:\t" + "Write Error")

            elif (args[0] == 8):
                self.status.emit("Serial Error:\t" + "Read Error")

            if ('ser' in locals()):
                    self.ser.close()

        # clear flag
        self.ser.clearError()
    
    def __connectionsList(self):
        self.errorOccurred.connect(self.__errorHandler)
