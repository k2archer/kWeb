#!/bin/python
import sys
import MySQLdb

sys.path.append("./service/v.1.0/user")
import Config
import Manager

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

def send_message(code, message, result):
    json_body = {"code": code, "message": message, "result": result}
    print json.dumps(json_body)
    pass


def parse_argv():
    user_name = None
    user_pass = None
    print
    try:
        # sys.argv[1] 的格式 "user=XXXX&pass=XXXX"
        user_argv = sys.argv[1].split('&', 1)
        user_name = user_argv[0].split('=', 1)
        user_pass = user_argv[1].split('=', 1)
    except:
        send_message("500", "parameter error", "result")
        exit()

    try:
        user_name = user_name[1].strip()
        user_pass = user_pass[1].strip()
    except:
        send_message("000", "login analytic ", "result")
        exit()

    return user_name, user_pass
    pass


def main():
    user_argv = parse_argv()
    # print user_argv
    user_manager = Manager.get_user_manager()
    login = user_manager.login(user_argv[0], user_argv[1])
    if login:
        print user_argv[0]
        print "，你好，欢迎登录。"
    else:
        print '用户名或密码无效'
    print '<a href="/index.html">返回</a>'

if __name__ == '__main__':
    main()

### 主面板结束 ###
print "</body>"
print "</td>"

print "</tr>"

print "<tr><td colspan=\"2\" style=\"background-color:#FFA500;text-align:center;\">"
print "Copyright 2019&#60;Copyright k2archer&#62;</td></tr>"
print "</table>"
print "</body>"
print "</html>"
