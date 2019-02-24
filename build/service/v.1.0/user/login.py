#!/bin/python
import sys
import MySQLdb

# print "Content-type:text/html\r\n\r\n"
print '<html>'
print "<head><meta charset=\"utf-8\"><title>Login</title></head>"
print "<body>"


def sendMessage(code, message, result):
	endl = '\r'
	message_json = '{'  + endl + \
	'"code":' + code       + endl + \
	'"message":' + message  + endl + \
	'"result":'+ result     + endl +'}'
	print message_json

try:
	# sys.argv[1] 的格式 "user=XXXX&pass=XXXX"
	user_argv = sys.argv[1].split('&', 1)
	user_name = user_argv[0].split('=', 1)
	user_pass = user_argv[1].split('=', 1)
except :
	sendMessage("000","parameter error", "result")
	exit()
	
# database info
db_host = '127.0.0.1' 
db_port = 3307
db_user = 'root'
db_passwd = 'usbw'
db_name = 'test'

# connect database
db = MySQLdb.connect(
		host = db_host, port = db_port, 
		user = db_user, passwd = db_passwd,
		db = db_name,  charset='utf8')
		
# 		
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
data = cursor.fetchone()

request = "SELECT * FROM users where user_name =\'"+ user_name[1] + "\';"
cursor.execute(request)
data = cursor.fetchone()

try:
	user_name[1] = user_name[1].strip()
	user_pass[1] = user_pass[1].strip()
except:
	sendMessage("000", "login analytic ", "result")
	exit()
	
if data is not None and data[1] == user_name[1] and data[2] == user_pass[1]:
	sendMessage("000", "login successed", "result")
else:
	sendMessage("000", "login failed", "result")

db.close()

print "</body>"
print "</html>"
