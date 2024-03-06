import os
import shutil
import security
import request
import requests
import socket
import pickle

#this variable defines the root directory where the db would be located. 
#Edit this if you want it to be placed elsewhere.
rootpath="/usr/local/PyDB"

# - Data class
#Data class defines the data structure and writes it to the db file. 
#The reading process is defined at requests.py.
class Data:
    def __init__(self, typ, cls, value):
        self.typ = typ
        self.cls = cls
        self.value = value
    def writedata(self, dbname, tablename):
        datafile = "{0}/db/{1}/{2}/data".format(rootpath, dbname, tablename)
        with open(datafile, "a") as f:
            f.write("{0}:{1}:{2}\n".format(self.typ, self.cls, self.value))
# - User class
#This is a class that gets the username and password. The password gets hashed.
#The function to write the User's data is defined at the Admin class.
class User:
    def __init__(self, username, pw):
        self.password = security.hash_pw(pw)
        self.username = username
# - Admin class
# This class stores all the functions that are related to administrating the database.
class Admin:
    def getusrdata():
        f = open("{0}/admin/User.data".format(rootpath), "r")
        data = f.readlines()
        f.close()
        return data
    def mkuser(user):
        filename = "{0}/admin/User.data".format(rootpath)
        data = "{0}:{1}\n".format(user.username, user.password)
        with open(filename, "a+") as f:
            f.write(data)
    def modpw(user, pw):
        data = Admin.getusrdata()
        change = []
        for line in data:
            if line.split(":")[0] == user:
                change.append("{0}:{1}\n".format(user, pw))
            else:
                change.append(line)
        with open("{0}/admin/User.data".format(rootpath), "w") as f:
            f.writelines(change)
# - Auth class
# This class is for authenticating user data provided by the client.
# More functions will be added in the future.
class Auth:
    def checkpw(user, pw):
        okay = False
        usrdata = Admin.getusrdata()
        for line in usrdata:
            if line.split(":")[0] == user:
                origin = line.split(":")[1].strip("\n")
                okay = True
                break
        if okay:
            if security.check_pw(pw, origin):
                return 0
            else:
                print("Failed to authenticate")
            return 2
        print("User not found")
        return 1
class DB:
    def __init__(self, name):
        self.name = name
    def mkdb(self):
        with open("{0}/db/dbinfo".format(rootpath), "a+") as f:
            f.write("{0}\n".format(self.name))
        dbdir = "{0}/db/{1}".format(rootpath, self.name)
        os.mkdir(dbdir)
        tableinfo = "{0}/db/{1}/tableinfo".format(rootpath, self.name)
        with open(tableinfo, "w") as f:
            f.write("PyDB:{0}\n".format(self.name))
    def rmdb(self):
        with open("{0}/db/dbinfo".format(rootpath), "r") as f:
            data = f.readlines()
        with open("{0}/db/dbinfo".format(rootpath), "w") as f:
            for line in data:
                if line.strip('\n') != self.name:
                    f.write(line)
        shutil.rmtree('{0}/db/{1}'.format(rootpath, self.name))
class Table:
    def __init__(self, name, dbname):
        self.name = name
        self.dbname = dbname
    def mktable(self):
        with open("{0}/db/{1}/tableinfo".format(rootpath, self.dbname), "a") as f:
            f.write("{0}\n".format(self.name))
        tabledir = "{0}/db/{1}/{2}/".format(rootpath, self.dbname, self.name)
        os.mkdir(tabledir)
        tabledata = "{0}/db/{1}/{2}/data".format(rootpath, self.dbname, self.name)
        tableclass = "{0}/db/{1}/{2}/class".format(rootpath, self.dbname, self.name)
        with open(tabledata, "w") as f:
            f.write("PyDB:{0}\n".format(self.name))
        with open(tableclass, "w") as f:
            f.write("PyDB_class:{0}\n".format(self.name))
    def rmtable(self):
        with open('{0}/db/{1}/tableinfo'.format(rootpath, self.dbname), 'r') as f:
            next(f)
            data = f.readlines()
        with open("{0}/db/{1}/tableinfo".format(rootpath, self.dbname), "w") as f:
            for line in data:
                if line.split('\n') != self.name:
                    f.write(line)
        shutil.rmtree('{0}/db/{1}/{2}'.format(rootpath, self.dbname, self.name))
class Class:
    def __init__(self, name, dbname, tablename, type):
        self.name = name
        self.type = type
        self.dbname = dbname
        self.tablename = tablename
    def writeclass(self):
        classpath = "{0}/db/{1}/{2}/class".format(rootpath, self.dbname, self.tablename)
        with open(classpath, "a") as f:
            f.write("{0}:{1}\n".format(self.name, self.type))
def checkclass(dbname, tablename, classname):
    classpath = "{0}/db/{1}/{2}/class".format(rootpath, dbname, tablename)
    with open(classpath, "r") as f:
        next(f)
        data = f.readlines()
        for line in data:
            if line.split(":")[0] == classname:
                return line.split(":")[1].strip('\n')
        print("Class not found")
        return "error"
class Server:
    def get_selfip(self):
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            return data['origin']
        else:
            return None
    def __init__(self):
        self.userlist = []
        self.ipaddr = self.get_selfip()
    def register_login(self, username, ip):
        userdata = [username, ip]
        self.userlist.append(userdata)
        print(f"{username} logged in from {ip}.")
    def logout(self, username, ip):
        self.userlist.remove([username, ip])
        print(f"{username} logged out")
    def runserver(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', 50075))
        server.listen(5)
        print("Server waiting for request")
        while True:
            c, address = server.accept()
            authinfo = c.recv(1024)
            username = authinfo.split(',')[0]
            pw = authinfo.split(',')[1]
            ret = Auth.checkpw(username, pw)
            if ret > 0:
                c.send("Authentication Failure")
                c.close()
            else:
                self.register_login(username, address)
                while True:
                    request = c.recv(1024)
                    request = pickle.loads(request)
                    #Not completed yet
