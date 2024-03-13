# How to setup & use
## Setup

 1. use the following command to clone the repository.
    ```
    git clone https://github.com/EricKim27/EbonDB.git /usr/local/EbonDB
    ```
    you might need sudo.
 2. create a user with the bottom command.
    ```
    python3 sh.py mkuser <username> <password>
    ```
 3. Run the command to start the server.
    ```
    python3 server.py
    ```
 4. Run the client side code to connect to the server. This code can be placed anywhere.
    ```
    python3 client.py <username>@<serveraddress>
    ```
## Using it

you can use the following commands to manipulate the Database.

  * ``` show (things) ```
  * ``` mkdb (dbname) ``` - makes a db
  * ``` rmdb (dbname) ``` - deletes a db
  * ``` rmtable (tablename) ``` - deletes a table from a db
  * ``` mktable (tablename) ``` - makes a table in the current database with the corresponding name.
  * ```mkcolumn (tablename) {(column name):(type),(another column name):(type)}``` - makes a column in a table.
  * ```usedb (dbname)``` - use db
  * ```get (data) (tablename)``` - gets data from table (data section can be *, column name. if it's using columns, it shoud be like get {column1, column2} exdb)
  * ```insert (table) {column,column} {data1,data2}``` - inserts data to a column
