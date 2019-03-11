class DatabaseInfo:
    # database info
    host = '127.0.0.1'
    port = 3307
    user = 'root'
    password = 'usbw'
    name = ''


class DatabaseConfig:
    def __init__(self):
        pass

    DATABASE_NAME = "klibrary"
    createDatabase = "CREATE DATABASE IF NOT EXISTS " + DATABASE_NAME + ' character SET utf8mb4;'
    deleteDatabase = 'DROP DATABASE IF EXISTS ' + DATABASE_NAME + ';'


class TableConfig:
    def __init__(self):
        pass

    class UserInfo:
        def __init__(self):
            pass

        TABLE_NAME = 'users'
        ID = 'user_id'
        NAME = 'user_name'
        PASSWORD = 'user_password'

    createUserInfoTable = 'CREATE TABLE IF NOT EXISTS ' \
                          + UserInfo.TABLE_NAME + ' (' \
                          + UserInfo.ID + ' INTEGER AUTO_INCREMENT PRIMARY KEY, ' \
                          + UserInfo.NAME + ' VARCHAR(18) NOT NULL UNIQUE' + ',' \
                          + UserInfo.PASSWORD + ' VARCHAR(18) NOT NULL' + ');'

    deleteUserInfoTable = "TRUNCATE " + UserInfo.TABLE_NAME + ";"

    class BookInfo:
        def __init__(self):
            pass

        TABLE_NAME = "books"
        ID = "book_id"
        CODE = "book_code"
        NAME = "book_name"

    createBookTable = "CREATE TABLE IF NOT EXISTS " \
                      + BookInfo.TABLE_NAME + "(" \
                      + BookInfo.ID + " INTEGER PRIMARY KEY AUTO_INCREMENT, " \
                      + BookInfo.CODE + " BIGINT NOT NULL UNIQUE, " \
                      + BookInfo.NAME + " TEXT" + ")"

    deleteBookTable = "TRUNCATE " + BookInfo.TABLE_NAME + ";"

    class Order:
        def __init__(self):
            pass

        TABLE_NAME = "orders"
        ID = "order_id"
        USER_ID = "user_id"
        BOOK_ID = "book_id"

    createOrderListTable = "CREATE TABLE IF NOT EXISTS " \
                           + Order.TABLE_NAME + "(" \
                           + Order.ID + " INTEGER PRIMARY KEY AUTO_INCREMENT, " \
                           + Order.USER_ID + " INTEGER, " \
                           + Order.BOOK_ID + " INTEGER" + ")"

    deleteOrderListTable = "TRUNCATE " + Order.TABLE_NAME + ";"
