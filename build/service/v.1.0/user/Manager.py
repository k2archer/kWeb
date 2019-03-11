# -*- coding: utf-8 -*

import DatabaseOpenHelper
from Config import *
import json


class DataManager:
    db_cursor = None
    db_helper = None  # type: DatabaseOpenHelper

    def __init__(self):
        self.db_helper = DatabaseOpenHelper.get_db_helper()
        self.db_cursor = self.db_helper.db_cursor
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

        # self.db_helper._execute(books_name_sql)
        self.db_cursor.execute(books_name_sql)
        t = []
        for item in self.db_cursor.fetchall():
            t.append(item[0])
        return tuple(t)


class UserManager:
    db_cursor = None
    db_helper = None

    def __init__(self):
        self.db_helper = DatabaseOpenHelper.get_db_helper()
        self.db_cursor = self.db_helper.db_cursor
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
