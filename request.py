import db
from db import rootpath
import os
from tabulate import tabulate

# this class is for getting requests and returning results.
# in the future, the commandinterpret function will be divided into multiple functions, as it is getting way too big.
class Request:
    def __init__(self, req, user, flags):
        self.request = req
        self.user = user
        self.flag = flags
        self.out = []
    def stripcmd(self):
        return self.request.split(' ')
    def commandinterpret(self):
        strip = self.stripcmd()
        result = 200
        if strip[0] == "show":
            if len(strip) != 1:
                primelist = []
                if strip[1] == "databases":
                    with open("{0}/db/dbinfo".format(rootpath), "r") as f:
                        data = f.readlines()
                        for line in data:
                            primelist.append([line.strip("\n")])
                            header = ['Databases']
                    table = tabulate(primelist, headers=header, tablefmt="fancy_grid")
                    self.out.append(table)
                    result = 0
                elif strip[1] == "tables":
                    if self.flag == ' ':
                        self.out.append("database not selected")
                        result = 1
                    else:
                        primelist = []
                        header = ['Tables']
                        table_info = "{0}/db/{1}/tableinfo".format(rootpath, self.flag)
                        with open(table_info, "r") as f:
                            next(f)
                            data = f.readlines()
                            for line in data:
                                primelist.append([line.strip('\n')])
                        table = tabulate(primelist, headers=header, tablefmt="fancy_grid")
                        self.out.append(table)
                        result = 0
                else:
                    self.out.append("Syntax error")
                    result = 2
            else:
                self.out.append("Syntax error")
                result = 1
        elif strip[0] == "mkdb":
            database = db.DB(strip[1])
            database.mkdb()
            result = 0
        elif strip[0] == "rmdb":
            # temporarily deprecated because I can't think of a way to make it work.
            # doublecheck = input("Are you sure you want to delete the Database: {0}?(y/n)".format(strip[1]))
            db_to_remove = db.DB(strip[1])
            db_to_remove.rmdb()
            self.out.append("Database removed.")
            result = 0
        elif strip[0] == "rmtable":
            if self.flag == ' ':
                self.out.append("database not selected")
                result = 1
            else:
                # temporarily deprecated because I can't think of a way to make it work.
                # doublecheck = input("Are you sure you want to delete table: {0}?(y/n)".format(strip[1]))
                table_to_remove = db.Table(strip[1], self.flag)
                table_to_remove.rmtable()
                self.out.append("Table removed.")
                result = 0
        elif strip[0] == "mkcolumn":
            if self.flag == ' ':
                self.out.append('database not selected')
                result = 1
            else:
                classdata = strip[2].strip('{').strip('}').split(',')
                for i in range(len(classdata)):
                    towrite = classdata[i].split(':')
                    writedata = db.Class(towrite[0], self.flag, strip[1], towrite[1])
                    writedata.writeclass()
                    result = 0
        elif strip[0] == "usedb":
            if os.path.isdir("{0}/db/{1}".format(rootpath, strip[1])):
                self.flag = str(strip[1])
                self.out.append("Database changed to {}".format(strip[1]))
                result = 0
            else:
                self.out.append("Database not found")
                result = 1
        elif strip[0] == "mktable":
            if self.flag == ' ':
                self.out.append("database not selected.")
                result = 1
            else:
                table = db.Table(strip[1], self.flag)
                table.mktable()
                result = 0
        elif strip[0] == "insert":
            if len(strip) == 4:
                if self.flag == ' ':
                    self.out.append("database not selected.")
                    result = 1
                else:
                    columninfo = strip[2].strip('{').strip('}').split(',')
                    datainfo = strip[3].strip('{').strip('}').split(',')
                    for i in range(len(columninfo)):
                        type = db.checkclass(self.flag, strip[1], columninfo[i])
                        if type == "error":
                            self.out.append('column {} was not found'.format(columninfo[i]))
                            result = 1
                        else:
                            data_for_write = db.Data(type, columninfo[i], datainfo[i])
                            data_for_write.writedata(self.flag, strip[1])
                            result = 0
            else:
                self.out.append("Syntax error")
                result = 2
        # the get function is used for getting data of columns in the table.
        elif strip[0] == "get":
            if self.flag == ' ':
                self.out.append("database not selected.")
                result = 1
            elif not os.path.exists("{0}/db/{1}/{2}".format(rootpath, self.flag, strip[2])):
                self.out.append("table not found.")
                result = 1
            else:
                if strip[1] == "*":
                    with open("{0}/db/{1}/{2}/class".format(rootpath, self.flag, strip[2]), "r") as f:
                        next(f)
                        columnd = f.readlines()
                        columndata = []
                        for line in columnd:
                            columndata.append(line.split(':')[0])
                else:
                    columndata = strip[1].strip('{').strip('}').split(',')
                datapath = "{0}/db/{1}/{2}/data".format(rootpath, self.flag, strip[2])
                with open(datapath, "r") as f:
                    next(f)
                    data = f.readlines()
                    # primelist is for storing lists that contain each column's data. It's in a matrix structure.
                    primelist = []
                    # below is for making lists according to the number of columns requested.
                    for i in range(len(columndata)):
                        primelist.append([])
                    # the bottom function reads line by line, and checks which column does the data belong to.
                    # process:
                    # read line -> check if the data belongs on column (in order) -> finds it ->
                    # goto next line -> repeat until end
                    for line in data:
                        value = line.split(':')
                        for i in range(len(columndata)):
                            if columndata[i] == value[1]:
                                if line.split(':')[0] == "int":
                                    primelist[i].append(int(value[2].strip("\n")))
                                if line.split(':')[0] == "char":
                                    primelist[i].append(str(value[2].strip("\n")))
                primelist_aligned = list(zip(*primelist))
                table = tabulate(primelist_aligned, headers=columndata, tablefmt="fancy_grid")
                self.out.append(table)
                result = 0
        else:
            self.out.append("Command not found")
            result = 1
        if result == 200:
            self.out.append("error in code. contact developer at github.")
        return self.out, str(self.flag), result