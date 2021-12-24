import sqlite3
from sqlite3 import Error
import buttons


def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error as er:
        print(er)


def folder_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists FOLDER(
ID      integer        PRIMARY KEY      AUTOINCREMENT,
Folder_Name   TEXT             NOT NULL,
Folder_Path   TEXT             NOT NULL,
unique (Folder_Name, Folder_Path))""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def rule_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists RULE(
ID      integer        PRIMARY KEY      AUTOINCREMENT,
Rule_Name   TEXT             NOT NULL)""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def sql_insert(con, values):
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO FOLDER(Folder_Name, Folder_Path) VALUES(?, ?)', values)
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def rule_insert(con, values):
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO RULE(Rule_Name) VALUES(?)', values)
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def init_folder_list():
    conn = sql_connection()
    folder_table(conn)
    c = conn.cursor()
    c.execute("""select Folder_Name from FOLDER""")
    for row in c.fetchall():
        # A list item is returned, so remove ' and , from it
        row = str(row)[2:-3]
        c.execute('select Folder_Path from FOLDER where Folder_Name = ?', [row])
        print(row)
        path = c.fetchone()
        path = str(path)[2:-3]
        print(path)
        buttons.add_list_items(row, path)
