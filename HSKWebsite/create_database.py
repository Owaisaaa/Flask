import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="pwd123",)

#my_cursor = mydb.cursor() # comment is to prevent creating database again

my_cursor.execute("CREATE DATABASE StudyMaterial")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)

# This file is only run once to create a database and since we have created the file once
# so we no longer need to run this file again. In fact we can delete it but lets keep it for future reference
# Also note there are other ways to cdreate a database as well