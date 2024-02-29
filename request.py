import db
import os
from tabulate import tabulate

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
        elif strip[0] == "insert":
            if self.flag == ' ':
                print("database not selected.")
                result = 1
            else:
                columninfo = strip[2].strip('{').strip('}').split(',')
                datainfo = strip[3].strip('{').strip('}').split(',')
                for i in range(len(columninfo)):
                    type = db.checkclass(self.flag, strip[1], columninfo[i])
                    if type == "error":
                        print('column {} was not found'.format(columninfo[i]))
                        result = 1
                    else:
                        data_for_write = db.Data(type, columninfo[i], datainfo[i])
                        data_for_write.writedata(self.flag, strip[1])
                        result = 0
        elif strip[0] == "get":
            if self.flag == ' ':
                print("database not selected.")
                result = 1
            else:
                if strip[1] == "*":
                    with open("/usr/local/PyDB/db/{0}/{1}/class".format(self.flag, strip[2]), "r") as f:
                        next(f)
                        columnd = f.readlines()
                        columndata = []
                        for line in columnd:
                            columndata.append(line.split(':')[0])
                else:
                    columndata = strip[1].strip('{').strip('}').split(',')
                datapath = "/usr/local/PyDB/db/{0}/{1}/data".format(self.flag, strip[2])
                with open(datapath, "r") as f:
                    next(f)
                    data = f.readlines()
                    primelist = []
                    for i in range(len(columndata)):
                        primelist.append([])
                    for line in data:
                        value = line.split(':')
                        for i in range(len(columndata)):
                            if columndata[i] == value[1]:
                                primelist[i].append(value[2].strip("\n"))
                primelist_aligned = list(zip(*primelist))
                table = tabulate(primelist_aligned, headers=columndata, tablefmt="grid")
                print(table)
                result = 0
        else:
            print("Command not found")
            result = 1
        if result == 200:
            print("error in code. contact developer at github.")
        return result