import json
import jsonlines
import os
from config import APP_PATH
from hashlib import md5

class User:
    def __init__(self,username = None,password = None):
        # initialize fields
        self.username = username
        self.password = password

    def addUser(self):
        filepath = APP_PATH+"/appData/Users.jsonl"
        #check if addData folder exist
        if(os.path.exists(APP_PATH+"/appData") == False):
            os.makedirs(APP_PATH+"/appData")
        # check if username already exits, make sure username is the primary key
        haveuser = self.getUser(self.username)
        if(haveuser == True): 
            return "User Already Exist"
        # encode password
        enc = md5()
        enc.update(self.password.encode("utf8"))
        self.password = enc.hexdigest()
        # check is there is already 10 users.
        if(os.path.exists(filepath) == True):
            with open(filepath, 'r') as fp:
                num_lines = sum(1 for line in fp)
                if (num_lines>9):
                    fp.close()
                    return "There are 10 users in system. Cannot register new user"
            fp.close()
        # open file
        with jsonlines.open(filepath,mode="a") as f:
            f.write(json.dumps(self.__dict__,indent = 4)) # insert into file
        f.close()   
        return True

    # get user by username
    def getUser(self,username):
        filepath = APP_PATH+"/appData/Users.jsonl"
        if(os.path.exists(filepath)):
            haveuser = False
            with open(filepath, 'rb') as f:
                # search is any match
                for row in jsonlines.Reader(f):
                    user = json.loads(row)
                    if(user["username"] == username):
                        self.username = user["username"]
                        self.password = user["password"]
                        haveuser = True
                        break
                # if user does not exist
            f.close()
            return haveuser
        else:
            # if file not exist
            return False

    def checkPW(self,tempPassword):
        # encode password from parameter
        enc = md5()
        enc.update(tempPassword.encode("utf8"))
        tempPassword = enc.hexdigest()
        if(self.password == tempPassword):
            return True
        else:
            return False
