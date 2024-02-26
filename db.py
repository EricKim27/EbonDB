import sys
import os

class Data:
    def __init__(self, typ, cls, index, value):
        self.typ = typ
        self.cls = cls
        self.index = index
        self.value = value
    def writedata(self, dbname, tablename):
        datafile = "/usr/local/PyDB/db/{dbname}/{tablename}/data"
        with open(datafile, "a") as f:
            f.write("{0}:{1}:{2}:{3}\n".format(self.typ, self.cls, self.index, self.value))
    def readdata(fd):
        f = open(fd, "r", encoding='utf-8')
        data = f.read()
        f.close()
        return data
class User:
    def __init__(self, username, pw):
        self.password = pw
        self.username = username

class Admin:
    def getusrdata():
        f = open("/usr/local/PyDB/admin/User.data", "r")
        data = f.readlines()
        f.close()
        return data
    def mkuser(user):
        filename = "/usr/local/PyDB/admin/User.data"
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
        with open("/usr/local/PyDB/admin/User.data", "w") as f:
            f.writelines(change)
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
            if str(pw) == origin:
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
        dbdir = "/usr/local/PyDB/db/{}\n".format(self.name)
        os.mkdir(dbdir)
        tableinfo = "/usr/local/PyDB/db/{}/tableinfo\n".format(self.name)
        with open(tableinfo, "w") as f:
            f.write("PyDB:{0}".format(self.name))
class Table:
    def __init__(self, name, dbname):
        self.name = name
        self.dbname = dbname
    def mktable(self):
        with open("/usr/local/PyDB/db/{0}/tableinfo".format(self.dbname), "a") as f:
            f.write("{0}\n".format(self.name))
        tabledir = "/usr/local/PyDB/db/{0}/{1}/".format(self.dbname, self.name)
        os.mkdir(tabledir)
        tabledata = "/usr/local/PyDB/db/{0}/{1}/data".format(self.dbname, self.name)
        tableclass = "/usr/local/PyDB/db/{0}/{1}/class".format(self.dbname, self.name)
        with open(tabledata, "w") as f:
            f.write("PyDB:{0}\n".format(self.name))
        with open(tableclass, "w") as f:
            f.write("PyDB_class:{0}\n".format(self.name))
class Class:
    def __init__(self, name, dbname, tablename, type):
        self.name = name
        self.type = type
        self.dbname = dbname
        self.tablename = tablename
    def mkclass(self):
        classpath = "/usr/local/PyDB/db/{0}/{1}/class".format(self.dbname, self.tablename)
        with open(classpath, "a") as f:
            f.write("{0}:{1}\n".format(self.name, self.type))
    def writeclass(self):
        classpath = "/usr/local/PyDB/db/{0}/{1}/class".format(self.dbname, self.name)
        with open(classpath, "w") as f:
            f.write("{0}:{1}\n".format(self.name, self.type))
    def checkclass(self):
        classpath = "/usr/local/PyDB/db/{0}/{1}/class".format(self.name)
        with open(classpath, "r") as f:
            data = f.read()
            next(data)
            data.readlines()
            for line in data:
                if line.split(":")[0] == self.name:
                    if line.split(":")[1] == self.type:
                        return 0
                    print("Class type mismatch")
                    return 1
            print("Class not found")
            return 1

        
