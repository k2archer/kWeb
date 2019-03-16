# -*- coding: utf-8 -*

import sys
import json
import Manager


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
    if login is None:
        send_message("300", "login failed", "result")
        return
    elif login is True:
        send_message("200", "login succeed", "result")
    else:
        send_message("500", "login error", "result")
    pass


if __name__ == '__main__':
    main()
