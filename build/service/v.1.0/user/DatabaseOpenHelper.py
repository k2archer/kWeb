# -*- coding: utf-8 -*

import MySQLdb
import Config
from Config import DatabaseInfo
from Config import TableConfig


class DatabaseOpenHelper:
    db_connection = None
    db_cursor = None

    def __init__(self):
        self.connect_database()
        self.create_database()
        self.create_tables()
        self.demo_data()

        pass

    def connect_database(self):
        self.db_connection = MySQLdb.connect(
            host=DatabaseInfo.host, port=DatabaseInfo.port,
            user=DatabaseInfo.user, passwd=DatabaseInfo.password,
            db=DatabaseInfo.name, charset='utf8')
        return self.db_connection

    def create_database(self):
        if self.db_connection is None:
            print 'db connect is None'
            return
        else:
            # print 'db is connected.'
            self.db_cursor = self.db_connection.cursor()
            self.db_cursor.execute(Config.DatabaseConfig.deleteDatabase)
            self.db_cursor.execute(Config.DatabaseConfig.createDatabase)
            # data = self.db_cursor.fetchone()
            # print data
            return self.db_cursor
        pass

    def create_tables(self):
        if self.db_cursor is None:
            print 'db cursor is None'
            return
        else:
            self.db_cursor.execute("USE " + Config.DatabaseConfig.DATABASE_NAME)
            self.db_cursor.execute(TableConfig.createUserInfoTable)
            self.db_cursor.execute(TableConfig.createBookTable)
            self.db_cursor.execute(TableConfig.createOrderListTable)
            pass
        pass

    pass

    def demo_data(self):
        if self.db_cursor is None:
            print 'demo_data(): db cursor is None'
            return
        else:
            demo_user = [['admin', 'admin'], ['test', 'test'], ['pk', 'asdfasdf']]
            for i in demo_user:
                add_test_user_info = "INSERT INTO " + TableConfig.UserInfo.TABLE_NAME \
                                     + " ( " + TableConfig.UserInfo.NAME + ', ' + TableConfig.UserInfo.PASSWORD + " )" \
                                     + " VALUES (" + '\'' + i[0] + '\'' + ',' + '\'' + i[1] + '\'' + ')'
                self.db_cursor.execute(add_test_user_info)

            # self.db_cursor.execute("select * from " + TableConfig.UserInfo.TABLE_NAME)
            # data = self.db_cursor.fetchall()
            # print data

            demo_book = [['9787121269394', 'Android 1'], ['9787115439789', 'Android 2']]
            for i in demo_book:
                add_test_book_info = "INSERT INTO " + TableConfig.BookInfo.TABLE_NAME \
                                     + " ( " + TableConfig.BookInfo.CODE + ', ' + TableConfig.BookInfo.NAME + " )" \
                                     + " VALUES (" + '\'' + i[0] + '\'' + ',' + '\'' + i[1] + '\'' + ')'
                self.db_cursor.execute(add_test_book_info)

            # self.db_cursor.execute("select * from " + TableConfig.BookInfo.TABLE_NAME)
            # data = self.db_cursor.fetchall()
            # print data

            demo_order = [['1', '2'], ['2', '2']]
            for i in demo_order:
                add_test_orders_list = "INSERT INTO " + TableConfig.Order.TABLE_NAME \
                                     + " ( " + TableConfig.UserInfo.ID + ', ' + TableConfig.BookInfo.ID + " )" \
                                     + " VALUES (" + '\'' + i[0] + '\'' + ',' + '\'' + i[1] + '\'' + ')'
                self.db_cursor.execute(add_test_orders_list)

            # self.db_cursor.execute("select * from " + TableConfig.Order.TABLE_NAME)
            # data = self.db_cursor.fetchall()
            # print data

        pass


db_helper = DatabaseOpenHelper()


def get_db_helper():
    return db_helper


# def main():
#     db_helper = DatabaseOpenHelper()
#     db_helper.connect_database()
#     db_helper.create_database()
#     db_helper.create_tables()
#     db_helper.demo_data()
#     pass


if __name__ == '__main__':
    # main()
    pass
