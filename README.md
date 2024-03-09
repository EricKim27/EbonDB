# EbonDB - Pure Python DBMS
<img src="images/logo.png" width="350">

 EbonDB is a DBMS made using python.

It currently can do:
 - creating database
 - removing database
 - creating tables
 - creating columns
 - inserting data to a column
 - printing data in the form of a table

I'm planning on making this work like a server.
# Dependencies
 - getpass4
 - tabulate
# How to use
put the contents of this repo to the /usr/local/EbonDB. Or you could edit the rootpath defined on db.py.

first, you need to set the user. so you have to do:
```
python sh.py mkuser {username} {password}
```
and then run:
```
python sh.py
```
 - commands
    * show (things)
    * mkdb (dbname) - makes a db
    * rmdb (dbname) - deletes a db
    * rmtable (tablename) - deletes a table from a db
    * mktable (tablename) - makes a table in the current database with the corresponding name.
    * mkcolumn (tablename) {(column name):(type),(another column name):(type)} - makes a column in a table.
    * usedb (dbname) - use db
    * get (data) (tablename) - gets data from table (data section can be *, column name. if it's using columns, it shoud be like get {column1, column2} exdb)
      * get (data) (tablename) where (buncha shit) - like the one from sql.(soon to be implemented)
    * insert (table) {column,column} {data1,data2}
