# -*- coding: utf-8 -*
#
import sys
import json
import Manager


def send_message(code, message, result):
    json_body = {"code": code, "message": message, "result": result}
    print json.dumps(json_body)
    pass


def parse_argv():
    try:
        # sys.argv[1] 的格式 "user=XXXX"
        user_argv = sys.argv[1].split('&', 1)
        user_name = user_argv[0].split('=', 1)
        user_name = user_name[1].strip()
        return user_name
    except:
        send_message("500", "parameter error", "result")
        exit()


def get_user_orders(user_name):
    data_manager = Manager.get_data_manager()
    order_list = data_manager.get_orders_list(user_name)
    send_message('200', order_list, 'OK')
    pass


def main():
    user_name = parse_argv()
    get_user_orders(user_name)
    pass


if __name__ == '__main__':
    main()
