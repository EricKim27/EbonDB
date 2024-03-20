import hashlib
from db import rootpath

def hash_pw(pw):
    hashed = hashlib.sha512(pw.encode()).hexdigest()
    return hashed
def check_pw(pw, hashed):
    return hashed == pw
class Permission:
    def add_new_user_permission(user, db):
        filename = "{0}/admin/Permission.data".format(rootpath)
        data = "{0}:{1}\n".format(user, db)
        with open(filename, 'a+') as f:
            f.write(data)
    def add_existing_user_permission(user, db):
        filename = "{0}/admin/Permission.data".format(rootpath)
        with open(filename, "r") as f:
            data = f.readlines()
            for line in data:
                if line.split(":")[0] == user:
                    changed_line = line.split(":")[0] + ":" + line.split(":")[1].strip("\n") + f",{db}\n"
        with open(filename, "w") as f:
            for line in data:
                if line.split(":")[0] == user:
                    f.write(changed_line)
                else:
                    f.write(line)
    def check_permission(user, db):
        filename = f"{rootpath}/admin/Permission.data"
        with open(filename, "r") as f:
            data = f.readlines()
            for line in data:
                if line.split(":")[0] == user:
                    if db in line.split(":")[1].strip("\n").split(","):
                        return True
                    else:
                        return False
