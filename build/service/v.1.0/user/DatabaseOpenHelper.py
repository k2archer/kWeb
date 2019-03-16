# -*- coding: utf-8 -*

import MySQLdb
import Config
from Config import DatabaseInfo
from Config import TableConfig
from warnings import filterwarnings

filterwarnings('error', category=MySQLdb.Warning)


class DatabaseOpenHelper:
    db_connection = None
    db_cursor = None

    def __init__(self):
        self.connect_database()
        # self.create_database()

        pass

    def connect_database(self):
        self.db_connection = MySQLdb.connect(
            host=DatabaseInfo.host, port=DatabaseInfo.port,
            user=DatabaseInfo.user, passwd=DatabaseInfo.password,
            db=DatabaseInfo.name, charset='utf8')
        self.db_cursor = self.db_connection.cursor()
        self.db_connection.select_db(Config.DatabaseConfig.DATABASE_NAME)
        return self.db_connection

    def create_database(self):
        if self.db_connection is None:
            print 'db connect is None'
            return
        else:
            # print 'db is connected.'
            self.db_cursor = self.db_connection.cursor()
            self._execute(Config.DatabaseConfig.deleteDatabase)
            self._execute(Config.DatabaseConfig.createDatabase)
            # data = self.db_cursor.fetchone()
            # print data

            self.create_tables()
            return self.db_cursor
        pass

    def create_tables(self):
        if self.db_cursor is None:
            print 'db cursor is None'
            return

        self._execute("USE " + Config.DatabaseConfig.DATABASE_NAME)
        self._execute(TableConfig.createUserInfoTable)
        self._execute(TableConfig.createBookTable)
        self._execute(TableConfig.createOrderListTable)

        self.demo_data()
        pass

    def _execute(self, query):
        try:
            self.db_cursor.close()
            self.db_cursor = self.db_connection.cursor()
            self.db_cursor.execute(query)
        except MySQLdb.Warning, w:
            print str(w)

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

            demo_book = [['9787121269394', u'Android 开发艺术探索'], ['9787115439789', u'Android 第一行代码']]
            for i in demo_book:
                add_test_book_info = "INSERT INTO " + TableConfig.BookInfo.TABLE_NAME \
                                     + " ( " + TableConfig.BookInfo.CODE + ', ' + TableConfig.BookInfo.NAME + " )" \
                                     + " VALUES (" + '\'' + i[0] + '\'' + ',' + '\'' + i[1] + '\'' + ')'
                self.db_cursor.execute(add_test_book_info)

            # self.db_cursor.execute("select * from " + TableConfig.BookInfo.TABLE_NAME)
            # data = self.db_cursor.fetchall()
            # print data

            demo_order = [['1', '1'], ['1', '2'], ['2', '2']]
            for i in demo_order:
                add_test_orders_list = "INSERT INTO " + TableConfig.Order.TABLE_NAME \
                                       + " ( " + TableConfig.UserInfo.ID + ', ' + TableConfig.BookInfo.ID + " )" \
                                       + " VALUES (" + '\'' + i[0] + '\'' + ',' + '\'' + i[1] + '\'' + ')'
                self.db_cursor.execute(add_test_orders_list)

            # self.db_cursor.execute("select * from " + TableConfig.Order.TABLE_NAME)
            # data = self.db_cursor.fetchall()
            # print data

        self.db_connection.commit()
        # self.db_connection.close()
        pass


db_helper = DatabaseOpenHelper()


def get_db_helper():
    # type: () -> DatabaseOpenHelper
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
