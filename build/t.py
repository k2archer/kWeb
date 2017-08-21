#!/bin/python
import sys
import MySQLdb

# str = "user=pan"
# print str.split()
# print str.split('=', 1)

# db = MySQLdb.connect("localhost", "root", "", "host_db")

db = MySQLdb.connect("localhost", "root", "", "test");
cursor = db.cursor()

# cursor.execute("SELECT * FROM users;")
# data = cursor.fetchone()
# for row in data:
# 	print row
# 	# print rwo[1]
# 	# print rwo[2]
# print data[0]

cursor.execute("SELECT * FROM users where user_name =\'pan\';")
data = cursor.fetchone()
print data
print data[1]
for row in data:
	print row
db.close()
