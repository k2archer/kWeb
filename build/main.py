#!/bin/python
import sys
import MySQLdb

# print "Content-type:text/html\r\n\r\n"
print '<html>'

head = "<head><meta charset=\"utf-8\"><title>Login</title></head>"
print head

css = "<head><style type=\"text/css\">body {background-color: white}table.center{margin:auto;width:50%;}</style></head>"
print css

print "<body>"

print "<table class=\"center\" width=\"800\" border=\"0\">"
print "<tr><td colspan=\"2\" style=\"background-color:#FFA500;text-align:center\">"
# Top面板 #
print "<h1>Login of Web Page</h1></td></tr>"
# Top面板结束 #
print "<tr>"
print "<td style=\"background-color:#FFD700;height:500px;width:100px;\">"
## 侧面板 ##

## 侧面板结束 ##
print "</td>"

print "<td style=\"background-color:#EEEEEE;width:400px;\">"
print "<body>"
### 主面板 ###
#print "脚本名：", sys.argv[0]
#for i in range(1, len(sys.argv)):
#    print "参数", i, sys.argv[i]
test = sys.argv[1].replace('=',' ');
# print test.replace('&',' ');
# print "<br>"

# db = MySQLdb.connect("localhost", "root", "", "host_db")
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print "Database version: %s " % data
# db.close()
db = MySQLdb.connect("localhost", "root", "", "test");
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
data = cursor.fetchone()
# print data

str = sys.argv[1].split('=', 1)
# print str[0] + " " + str[1]
# print "<br>"
request = "SELECT * FROM users where user_name =\'"+ str[1] + "\';"
# print request
# print "<br>"
cursor.execute(request)
data = cursor.fetchone()
# print data
if data:
	print data[1] + "，你好，欢迎登录。"
else:
	print '用户名无效'

db.close()



### 主面板结束 ###
print "</body>"
print "</td>"

print "</tr>"

print "<tr><td colspan=\"2\" style=\"background-color:#FFA500;text-align:center;\">"
print "Copyright 2016&#60;Copyright Pwei&#62;</td></tr>"
print "</table>"
print "</body>"
print "</html>"
