# -*- coding: utf-8 -*

import MySQLdb
import DatabaseOpenHelper
from Config import *
import json

import Logger


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

        books_name_sql = "SELECT " + TableConfig.BookInfo.NAME + ',' + TableConfig.BookInfo.CODE\
                         + " FROM " + TableConfig.BookInfo.TABLE_NAME \
                         + " WHERE " + TableConfig.BookInfo.ID + ' IN (' + books_id_sql + ');'

        # self.db_helper._execute(books_name_sql)

        book_list = None
        try:
            self.db_cursor.execute(books_name_sql)
            book_list = self.db_cursor.fetchall()
        except MySQLdb.Error, e:
            error_message = "Mysql Error %d: %s" % (e.args[0], e.args[1])
            Logger.get_logger().exception(error_message + '\n' + books_name_sql + '\n')
            book_list = None
            pass

        ordered_list = []
        for item in book_list:
            json_body = {"book_name": item[0], "book_code": item[1]}
            ordered_list.append(json_body)
        return tuple(ordered_list)

    def get_recommended_list(self, user_name):

        books_sql = "SELECT " + TableConfig.BookInfo.NAME + ',' + TableConfig.BookInfo.CODE \
                    + " FROM " + TableConfig.BookInfo.TABLE_NAME + " LIMIT 5;"
        self.db_cursor.execute(books_sql)

        book_list = None
        try:
            self.db_cursor.execute(books_sql)
            book_list = self.db_cursor.fetchall()
        except MySQLdb.Error, e:
            error_message = "Mysql Error %d: %s" % (e.args[0], e.args[1])
            Logger.get_logger().exception(error_message + '\n' + books_sql + '\n')
            book_list = None
            pass

        # book_code = None
        # json_body = {"book_code": book_code, "book_name": book_list}
        # print json.dumps(json_body, ensure_ascii=False)  # 强制非 ascii 字符生成相对应的字符编码

        recommended_list = []
        for item in book_list:
            # print item[0]
            json_body = {"book_name": item[0], "book_code": item[1]}
            recommended_list.append(json_body)
        # print recommended_list
        return tuple(recommended_list)
        pass


class UserManager:
    db_cursor = None
    db_helper = None

    def __init__(self):
        self.db_helper = DatabaseOpenHelper.get_db_helper()
        self.db_cursor = self.db_helper.db_cursor
        pass

    def login(self, user_name, user_password):
        if self.db_cursor is None or self.db_helper is None:
            return None

        login_sql = "SELECT * FROM " + TableConfig.UserInfo.TABLE_NAME \
                    + ' WHERE ' + TableConfig.UserInfo.NAME + ' = ' + '\'' + user_name + '\'' \
                    + ' AND ' + TableConfig.UserInfo.PASSWORD + ' = ' + '\'' + user_password + '\''
        # print login_sql

        data = None
        try:
            self.db_cursor.execute(login_sql)
            data = self.db_cursor.fetchone()
            # print data
            data = data is not None
        except MySQLdb.Error, e:
            error_message = "Mysql Error %d: %s" % (e.args[0], e.args[1])
            Logger.get_logger().exception(error_message + '\n' + login_sql + '\n')
            data = None
            pass

        return data
        pass


user_manager_instance = UserManager()


def get_user_manager():
    return user_manager_instance


data_manager_instance = DataManager()


def get_data_manager():
    return data_manager_instance


def main():
    # user_manager = UserManager()
    # user_manager.login("admin", "admin")
    #
    # data_manager = DataManager()
    # data_manager.get_orders_list('admin')

    pass


if __name__ == '__main__':
    main()
