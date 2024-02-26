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
    def __init__(self, req, user, *flags):
        self.request = req
        self.user = user
        self.flag = flags
    def stripcmd(self):
        return self.request.split(' ')
    def commandinterpret(self):
        strip = self.stripcmd()
        if strip[0] == "show":
            if strip[1] == "databases":
                print("-----------------")
                print(" Databases       ")
                print("-----------------")
                for line in os.listdir("/usr/local/PyDB/db"):
                    print(" {}".format(line))
                print("-----------------")
                result = 0
        elif strip[0] == "mkdb":
            database = db.DB(strip[1])
            database.mkdb()
            result = 0
        elif strip[0] == "usedb":
            if os.path.isdir("/usr/local/PyDB/db/{}".format(strip[1])):
                self.flag = strip[1]
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
        if ret == 0:
            print("Authentication successful.")
            while True:
                stin = input("(" + uid + ")>")
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
