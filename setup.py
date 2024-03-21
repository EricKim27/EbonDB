from getpass4 import getpass

username = input("Username: ")
password = getpass("Password: ")
import db
user = db.User(username, password)
db.Admin.mkuser(user)
print("User created successfully.")
exit()
