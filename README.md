## PyDB - a DBMS made from python
 PyDB is a DBMS made using python.

Now, since this is just some BS I made to learn more about OOP, please don't expect it to work like MySQL, MariaDB, MongoDB, etc. I really have no idea about databases. I'm just making it based on my understandings of DB after fiddling around with MariaDB. Heck, I don't even know all the sql statements.

Currently, it is not ready for use. It currently can do:
 - creating database
 - creating tables
 - creating columns
 - inserting data to a column
 - printing data in the form of a table

The contents of this repository has to go under /usr/local/PyDB.

I'm planning on making this work like a server. Currently, in order to use the prompt, run:
```
python sh.py
```
Though nothing is ready, so there's nothing to do with it.
## Dependencies
 - getpass4
 - tabulate
## How to use
(most of these are yet to be implemented)
 - commands
    * show (things)
    * mkdb (dbname) - makes a db
    * rmdb (dbname) - deletes a db
    * mktable (tablename) - makes a table in the current database with the corresponding name.
    * mkcolumn (tablename) {(column name):(type),(another column name):(type)} - makes a column in a table.
    * usedb (dbname) - use db
    * get (data) (tablename) - gets data from table (data section can be *, column name. if it's using columns, it shoud be like get {column1, column2} exdb)
      * get (data) (tablename) where (buncha shit) - like the one from sql.
    * insert (table) {column,column} {data1,data2}
