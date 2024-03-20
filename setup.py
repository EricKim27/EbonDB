from getpass4 import getpass
import db

username = input("Username: ")
password = getpass("Password: ")
user = db.User(username, password)
db.Admin.mkuser(user)
print("User created successfully.")
exit()
