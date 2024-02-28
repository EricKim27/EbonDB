import db
import fcntl
import os
import subprocess
import sys
from getpass4 import getpass

def if_sudo():
    try:
        subprocess.check_call(['sudo', '-S', 'echo', 'authenticated'])
        return True
    except subprocess.CalledProcessError:
        return False
class Request:
    def __init__(self, req, user, flags):
        self.request = req
        self.user = user
        self.flag = flags
    def stripcmd(self):
        return self.request.split(' ')
    def commandinterpret(self):
        strip = self.stripcmd()
        result = 200
        if strip[0] == "show":
            if strip[1] == "databases":
                print("-----------------")
                print(" Databases       ")
                print("-----------------")
                with open("/usr/local/PyDB/db/dbinfo", "r") as f:
                    data = f.readlines()
                    for line in data:
                        print(" {}".format(line).strip("\n"))
                print("-----------------")
                result = 0
            elif strip[1] == "tables":
                if self.flag == ' ':
                    print("database not selected")
                    result = 1
                else:
                    table_info = "/usr/local/PyDB/db/{}/tableinfo".format(self.flag)
                    print("-----------------")
                    print("Tables")
                    print("-----------------")
                    with open(table_info, "r") as f:
                        next(f)
                        data = f.readlines()
                        for line in data:
                            print(line.strip('\n'))
                        print("-----------------")
                        result = 0
        elif strip[0] == "mkdb":
            database = db.DB(strip[1])
            database.mkdb()
            result = 0
        elif strip[0] == "mkcolumn":
            if self.flag == ' ':
                print('database not selected')
                result = 1
            else:
                classdata = strip[2].strip('{').strip('}').split(',')
                for i in range(len(classdata)):
                    towrite = classdata[i].split(':')
                    writedata = db.Class(towrite[0], self.flag, strip[1], towrite[1])
                    writedata.writeclass()
                    result = 0
        elif strip[0] == "usedb":
            if os.path.isdir("/usr/local/PyDB/db/{}".format(strip[1])):
                self.flag = str(strip[1])
                print(self.flag)
                print("Database changed to {}".format(strip[1]))
                result = 0
            else:
                print("Database not found")
                result = 1
        elif strip[0] == "mktable":
            if self.flag == ' ':
                print("database not selected.")
                result = 1
            else:
                table = db.Table(strip[1], self.flag)
                table.mktable()
                result = 0
        else:
            print("Command not found")
            result = 1
        if result == 200:
            print("error in code. contact developer at github.")
        return result
if len(sys.argv) >= 3:
    if sys.argv[1] == "mkuser":
        if if_sudo():
            user = db.User(sys.argv[2], sys.argv[3])
            db.Admin.mkuser(user)
            print("mkuser successful.")
            exit()
else:
    print("PyDB test Prompt")
    print(" ")
    print("This software comes with ABSOLUTELY NO WARRANTY, \nto the extent permitted by applicable law.")
    print(" ")
    flags = ' '
    while True:
        uid = input("DB login: ")
        upw = getpass("Password: ")
        ret = db.Auth.checkpw(uid, upw)
        res = 0
        if ret == 0:
            print("Authentication successful.")
            while True:
                stin = input("(" + uid + ")[" + str(res) + "]>")
                if stin == "exit":
                    print("bye")
                    exit()
                if stin == "err":
                    execfail = 1
                req = Request(stin, uid, flags)
                res = req.commandinterpret()
                flags = req.flag
                if res == 0:
                    print("command completed with no errors")
                    continue
                else:
                    print("command failed with error code: " + str(res))
        elif ret == 1:
            continue
        elif ret == 2:
            continue
