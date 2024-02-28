import request
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
while True:
    try:
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
                        req = request.Request(stin, uid, flags)
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
    except Exception as e:
        print("error occured: {0} \ncontact developer at github".format(e))
        continue