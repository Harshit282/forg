import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error as er:
        print(er)


def sql_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists FOLDER(
ID      integer        PRIMARY KEY      AUTOINCREMENT,
Folder_ID     TEXT             NOT NULL,
Folder_Name   TEXT             NOT NULL,
Folder_Path   TEXT             NOT NULL)""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def rule_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists RULE(
ID      integer        PRIMARY KEY      AUTOINCREMENT,
Rule_Name   TEXT             NOT NULL,
Rule_ID     TEXT             NOT NULL)""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def sql_insert(con, values):
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO FOLDER(Folder_ID, Folder_Name, Folder_Path) VALUES(?, ?, ?)', values)
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def rule_insert(con, values):
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO RULE(Rule_Name, Rule_ID) VALUES(?, ?)', values)
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False
