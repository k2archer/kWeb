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
print "<h1>图书管理系统</h1></td></tr>"
# Top面板结束 #
print "<tr>"
print "<td style=\"background-color:#FFD700;height:500px;width:100px;\">"
## 侧面板 ##

## 侧面板结束 ##
print "</td>"

print "<td style=\"background-color:#EEEEEE;width:400px;\">"
print "<body>"
### 主面板 ###

# db = MySQLdb.connect("127.0.0.1", "root", "", "host_db")
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print "Database version: %s " % data
# db.close()

db = MySQLdb.connect(
		host='127.0.0.1',
		port=3307,user='root',
		passwd='usbw',
		db='test',
		charset='utf8')
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
data = cursor.fetchone()

# sys.argv[1] 的格式 "user=XXXX&pass=XXXX"
user_argv = sys.argv[1].split('&', 1)
user_name = user_argv[0].split('=', 1)
user_pass = user_argv[1].split('=', 1)

request = "SELECT * FROM users where user_name =\'"+ user_name[1] + "\';"
cursor.execute(request)
data = cursor.fetchone()
user_name[1] = user_name[1].strip()
user_pass[1] = user_pass[1].strip()

if data is not None and data[1] == user_name[1] and data[2] == user_pass[1]:
	print data[1]
	print "，你好，欢迎登录。"
else:
	print '用户名或密码无效'
	print '<a href="/index.html">返回</a>'

db.close()



### 主面板结束 ###
print "</body>"
print "</td>"

print "</tr>"

print "<tr><td colspan=\"2\" style=\"background-color:#FFA500;text-align:center;\">"
print "Copyright 2019&#60;Copyright k2archer&#62;</td></tr>"
print "</table>"
print "</body>"
print "</html>"
