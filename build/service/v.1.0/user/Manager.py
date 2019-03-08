# -*- coding: utf-8 -*

import DatabaseOpenHelper
from Config import *
import json


class DataManager:
    db_cursor = None

    def __init__(self):
        db_helper = DatabaseOpenHelper.get_db_helper()
        self.db_cursor = db_helper.db_cursor
        pass

    def get_orders_list(self, user_name):
        user_id_sql = 'SELECT ' + TableConfig.UserInfo.ID \
                      + " FROM " + TableConfig.UserInfo.TABLE_NAME \
                      + " WHERE " + TableConfig.UserInfo.NAME + ' = ' + '\'' + user_name + '\''

        books_id_sql = "SELECT " + TableConfig.BookInfo.ID + '' \
                       + ' FROM ' + TableConfig.Order.TABLE_NAME + ' ' \
                       + ' WHERE ' + TableConfig.UserInfo.ID + ' IN (' + user_id_sql + ')'

        books_name_sql = "SELECT " + TableConfig.BookInfo.NAME \
                         + " FROM " + TableConfig.BookInfo.TABLE_NAME \
                         + " WHERE " + TableConfig.BookInfo.ID + ' IN (' + books_id_sql + ');'

        self.db_cursor.execute(books_name_sql)
        orders_list = self.db_cursor.fetchone()
        # print json.dump(orders_list)
        # print orders_list

        # 构造字典
        json_body = {"code": '200', "message": orders_list, "result": "OK"}
        # 构造 list
        # print json_body
        json_str = json.dumps(json_body)
        # print json_str
        return orders_list


class UserManager:
    db_cursor = None

    def __init__(self):
        db_helper = DatabaseOpenHelper.get_db_helper()
        self.db_cursor = db_helper.db_cursor
        pass

    def login(self, user_name, user_password):
        login_sql = "SELECT * FROM " + TableConfig.UserInfo.TABLE_NAME \
                    + ' WHERE ' + TableConfig.UserInfo.NAME + ' = ' + '\'' + user_name + '\'' \
                    + ' AND ' + TableConfig.UserInfo.PASSWORD + ' = ' + '\'' + user_password + '\''
        # print login_sql
        self.db_cursor.execute(login_sql)
        data = self.db_cursor.fetchone()
        # print data
        return data is not None
        pass


user_manager_instance = UserManager()


def get_user_manager():
    return user_manager_instance


data_manager_instance = DataManager()


def get_data_manager():
    return data_manager_instance


def main():
    user_manager = UserManager()
    user_manager.login("admin", "admin")

    data_manager = DataManager()
    data_manager.get_orders_list('admin')

    pass


if __name__ == '__main__':
    main()
