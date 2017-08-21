#!/bin/python
import sys
import MySQLdb

print "脚本名：", sys.argv[0]
for i in range(1, len(sys.argv)):
    print "参数", i, sys.argv[i]

test = sys.argv[1].replace('=',' ');
print test.replace('&',' ');

db = MySQLdb.connect("localhost", "root", "", "host_db")
#db = MySQLdb.connect("192.168.0.105", "root", "asdfasdf", "host_db")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version: %s " % data
db.close()
