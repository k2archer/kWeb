#!/bin/python
import sys
import MySQLdb

print "脚本名：", sys.argv[0]
for i in range(1, len(sys.argv)):
	print " ", i, sys.argv[i]
# str = "user=pan"
str = sys.argv[1]
print str.split()
# print str.split('=', 1)
user_data = str.split('=', 1)
print user_data[0], user_data[1]

# db = MySQLdb.connect("127.0.0.1", "root", "", "host_db")
# db=MySQLdb.connect(
# 		host='127.0.0.1',
# 		port=3307,user='root',
# 		passwd='usbw',
# 		db='test',
# 		charset='utf8')
# db.close()

db=MySQLdb.connect(
		host='127.0.0.1',
		port=3307,user='root',
		passwd='usbw',
		db='test',
		charset='utf8')
cursor = db.cursor()

cursor.execute("SELECT * FROM users;")
data = cursor.fetchone()
for row in data:
	print row
	# print rwo[1]
	# print rwo[2]
print data[0]

sql_str = "SELECT * FROM users where user_name =\"" + user_data[1] + "\";"
print sql_str
cursor.execute(sql_str)
data = cursor.fetchone()
print data
print data[0]
for row in data:
	print row
db.close()
