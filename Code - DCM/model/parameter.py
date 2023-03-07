import json
import os
from config import APP_PATH
from datetime import datetime

class parameter:
    def __init__(self, parameters = None,setTime = None):
        self.parameters = parameters
        self.time = setTime
        self.checkDefaultFile()

    # save in file: mode can be "save" "upload"
    def savereport(self,username,data1,data2):
        filepath = APP_PATH+"/appData/"+username
        if(os.path.exists(filepath) == False):
            os.makedirs(filepath)
        filepath = filepath+"/report"
        if(os.path.exists(filepath) == False):
            os.makedirs(filepath)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filepath = filepath +"/"+time+".xls"
        with open(filepath,mode="w") as f:
            f.write(json.dumps("Parameters: ",indent=4))
            f.write(json.dumps(self.parameters, indent=4)) # insert into file
            f.write(json.dumps("Atrial Signal",indent=4))
            f.write(json.dumps(data1,indent=4))
            f.write(json.dumps("Ventricular Signal",indent=4))
            f.write(json.dumps(data2,indent=4))
        f.close()
        return True

    def save(self, username,mode):
        # check if the value are in the proper range.
        result = self.checkRange()
        if (result != True):
            return result
        # check user folder
        filepath = APP_PATH+"/appData/"+username
        if(os.path.exists(filepath) == False):
            os.makedirs(filepath)
        # check saved folder
        filepath = filepath+"/"+mode
        if(os.path.exists(filepath) == False):
            os.makedirs(filepath)
        # add new file
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filepath = filepath + "/"+time+".json"
        with open(filepath,mode="w") as f:
            f.write(json.dumps(self.parameters, indent=4)) # insert into file
        f.close()
        return True

    def load(self, username):
        filepath = APP_PATH+"/appData/"+username
        if(os.path.exists(filepath) == False):
            return False
        return filepath
    
    def loadcon(self,filepath):
        with open(filepath, 'rb') as f:
            line = f.read();
            self.parameters = json.loads(line);
        f.close()

    # check get the range seeting
    def checkRange(self):
        # get range data
        filepath = APP_PATH+"/appData/rangeSetting.json"
        rangeList = {}
        with open(filepath, 'rb') as f:
            line = f.read();
            rangeList = json.loads(line);
        f.close()
        filepath = APP_PATH+"/appData/incrementSetting.json"
        incList = {}
        with open(filepath, 'rb') as f:
            line = f.read();
            incList = json.loads(line);
        f.close()
        # check range
        errorlist= {}
        for key,value in self.parameters.items():
            if (isinstance(value,int) or isinstance(value,float)):
                range = rangeList[key]
                inc = incList[key]
                # access to all 
                i = -1
                for val in range:
                    # get max and min
                    if isinstance(val,list):
                        min = val[0]
                        max = val[1]
                        i +=1
                        if(max>=value) :
                            break
                if (isinstance(inc,list)):
                    step = inc[i]
                else:
                    step = inc
                # check if it is in the range
                if (min > value or max < value):
                    errorlist[key] = [[min,max],step," not in the range. "]
                # check the inrement step
                remainder = int((value-min)%step)
                if (remainder != 0):
                    errorlist[key] = [[min,max],step," not match the increment, suggest value: "+str(value - remainder)+". "]
        if len(errorlist)!=0:
            return errorlist
        return True

    # get the default value
    def getDefault(self):
        filepath = APP_PATH+"/appData/defaultSetting.json"
        with open(filepath, 'rb') as f:
            line = f.read();
            self.parameters = json.loads(line);
        f.close()
    
    # get disabled field list
    def getDisabled(self,mode):
        filepath = APP_PATH+"/appData/disabledSetting.json"
        with open(filepath, 'rb') as f:
            line = f.read();
            disabled = json.loads(line);
        return disabled[mode]

    # default parameters and ranges for setting
    def checkDefaultFile(self):
        if(os.path.exists(APP_PATH+"/appData") == False):
            os.makedirs(APP_PATH+"/appData")
        filepath = APP_PATH+"/appData/defaultSetting.json"
        #check deault setting
        default = {
            "mode" :"AOO",
            "LRL" : 60,
            "URL" :120,
            "MSR" :120,
            "FAVD":150,
            "DAVD": "Off",
            "MDAVD": 50,
            "SAVDO": "Off",
            "APAR": 5,
            "VPAR": 5,
            "APAU": "3.75",
            "VPAU": "3.75",
            "APW":1,
            "VPW":1,
            "AS": 4,
            "VS": 4,
            "VRP":320,
            "ARP":250,
            "PVARP":250,
            "PVARPE":"Off",
            "HRL":"Off",
            "RS":"Off",
            "ATRM":"Off",
            "ATRD":20,
            "ATRFT":60,
            "VB":40,
            "AT":"Med",
            "ReactionT":30,
            "RF":8,
            "RecoveryT":300
        }
        with open(filepath,mode="w") as f:
            f.write(json.dumps(default, indent=4)) # insert into file
        f.close()
        filepath = APP_PATH+"/appData/disabledSetting.json"
        #check disabled widget list
        default = {
            "OOO":["LRL","URL","MSR","FAVD","DAVD","MDAVD","SAVDO","APAR","VPAR","APAU","VPAU","APW","VPW","AS","VS","VRP","ARP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "DDD":["MSR","VB","AT", "ReactionT", "RF","RecoveryT"],
            "VDD":["MSR","SAVDO","APAR","APAU","APW","AS","ARP","PVARP","HRL","VB","AT", "ReactionT", "RF","RecoveryT"],
            "DDI":["MSR","DAVD","MDAVD","SAVDO","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "DOO":["MSR","DAVD","MDAVD","SAVDO","AS","VS","VRP","ARP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "AOO":["MSR","FAVD","DAVD","MDAVD","SAVDO","VPAR","VPAU","VPW","VS","VRP","AS","ARP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "AAI":["MSR","FAVD","DAVD","MDAVD","SAVDO","VPAR","VPAU","VPW","VS","VRP","PVARPE","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "VOO":["MSR","FAVD","DAVD","MDAVD","SAVDO","APAR","APAU","APW","AS","ARP","VS","VRP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "VVI":["MSR","FAVD","DAVD","MDAVD","SAVDO","APAR","APAU","APW","AS","ARP","PVARP","PVARPE","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "AAT":["MSR","FAVD","DAVD","MDAVD","SAVDO","VPAR","VPAU","VPW","VS","VRP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "VVT":["MSR","FAVD","DAVD","MDAVD","SAVDO","APAR","APAU","APW","AS","ARP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB","AT", "ReactionT", "RF","RecoveryT"],
            "DDDR":[],
            "VDDR":["MDAVD","SAVDO","APAR","APAU","APW","AS","ARP","PVARP","HRL"],
            "DDIR":["DAVD","MDAVD","SAVDO","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB"],
            "DOOR":["DAVD","MDAVD","SAVDO","AS","VS","VRP","ARP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB"],
            "AOOR":["FAVD","DAVD","MDAVD","SAVDO","VPAR","VPAU","VPW","VS","AS","ARP","VRP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB"],
            "AAIR":["FAVD","DAVD","MDAVD","SAVDO","VPAR","VPAU","VPW","VS","VRP","PVARPE","ATRM","ATRD","ATRFT","VB"],
            "VOOR":["FAVD","DAVD","MDAVD","SAVDO","APAR","APAU","APW","VS","AS","ARP","VRP","PVARP","PVARPE","HRL","RS","ATRM","ATRD","ATRFT","VB"],
            "VVIR":["FAVD","DAVD","MDAVD","SAVDO","APAR","APAU","APW","AS","ARP","PVARP","PVARPE","ATRM","ATRD","ATRFT","VB"],
        }
        with open(filepath,mode="w") as f:
            f.write(json.dumps(default,indent=4)) # insert into file
        f.close()
        filepath = APP_PATH+"/appData/rangeSetting.json"
        #check deault setting
        default = {
            "LRL" : [[30,50],[50,90],[90,175]],
            "URL" : [[50,175]],
            "MSR" : [[50,175]],
            "FAVD": [[70,300]],
            "DAVD": ["Off","On"],
            "MDAVD": [[30,100]],
            "SAVDO": [[-100,-10]],
            "APAR": [[0.5,3.2],[3.5,7.0]],
            "VPAR": [[0.5,3.2],[3.5,7.0]],
            "APAU": ["Off",1.25,2.5,3.75,5.0],
            "VPAU": ["Off",1.25,2.5,3.75,5.0],
            "APW": [[1,30]],
            "VPW": [[1,30]],
            "AS": [[0.25,0.25],[0.5,0.5],[0.75,0.75],[1.0,10]],
            "VS": [[0.25,0.25],[0.5,0.5],[0.75,0.75],[1.0,10]],
            "VRP":[[150,500]],
            "ARP":[[150,500]],
            "PVARP":[[150,500]],
            "PVARPE":[[50,400]],
            "HRL":[],
            "RS":["Off",3,6,9,12,15,18,21,25],
            "ATRM":["Off","On"],
            "ATRD":[[10,10],[20,80],[100,2000]],
            "ATRFT":[[1,5]],
            "VB":[[30,60]],
            "AT":["Med","V-Low","Low","Med-Low","Med-High","High","V-High"],
            "ReactionT":[[10,50]],
            "RF":[[1,16]],
            "RecoveryT":[[2,16]]
        }
        with open(filepath,mode="w") as f:
            f.write(json.dumps(default, indent=4)) # insert into file
        f.close()
        filepath = APP_PATH+"/appData/incrementSetting.json"
        #check deault setting
        default = {
            "LRL" : [5,1,5],
            "URL" : 5,
            "MSR" : 5,
            "FAVD": 10,
            "MDAVD": 10,
            "SAVDO": 10,
            "APAR": [0.1,0.5],
            "VPAR": [0.1,0.5],
            "APW": [1],
            "VPW": [1],
            "AS": [1,1,1,0.5],
            "VS": [1,1,1,0.5],
            "VRP":10,
            "ARP":10,
            "PVARP":10,
            "PVARPE":50,
            "ATRD":[1,20,100],
            "ATRFT":1,
            "VB":10,
            "ReactionT":10,
            "RF":1,
            "RecoveryT":1
        }
        with open(filepath,mode="w") as f:
            f.write(json.dumps(default, indent=4)) # insert into file
        f.close()



