import sqlite3
from sqlite3 import Error
import buttons
import Rules
# import conditions

selected_rule = ''
selected_folder = ''
list = []


def getSelectedRule(rule):
    global selected_rule
    selected_rule = rule.text()


def getSelectedFolder(folder):
    global selected_folder
    selected_folder = folder.text()


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
unique (Folder_Path))""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def rule_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists RULE(
F_ID      integer            NOT_NULL,
Rule_Name   TEXT             NOT NULL PRIMARY KEY,
FOREIGN KEY(F_ID) REFERENCES FOLDER(ID))""")
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
        cursor.execute('INSERT INTO RULE(F_ID, Rule_Name) VALUES(?, ?)', values)
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
        path = c.fetchone()
        path = str(path)[2:-3]
        buttons.add_list_items(row, path)


def initRules():
    conn = sql_connection()
    folder_table(conn)
    c = conn.cursor()
    c.execute("""select ID from FOLDER where Folder_Name = ?""", [selected_folder])
    f_id = c.fetchone()
    f_id = str(f_id)[1:-2]
    rule_table(conn)
    c.execute("""select Rule_Name from RULE where RULE.F_ID = ?""", [f_id])
    for row in c.fetchall():
        row = str(row)[2:-3]
        Rules.rules_list.append(row)


def insertRule():
    conn = sql_connection()
    folder_table(conn)
    rule_name = selected_rule
    folder_name = selected_folder
    c = conn.cursor()
    c.execute('select ID from FOLDER where Folder_Name = ?', [folder_name])
    folder_id = c.fetchone()
    folder_id = str(folder_id)[1:-2]
    rule_table(conn)
    values = (folder_id, rule_name)
    if rule_insert(conn, values):
        print("R Records Inserted")
    else:
        print("R Records not Inserted")


def condition_table(con):
    print("i called")
    try:
        cursor = con.cursor()
        cursor.execute("""
        CREATE TABLE if not exists CONDITIONS(
        Rule         Text,
        Condition    Text,
        Operator     Text,
        Size         double,
        Extension    Text,
        Date         Text,
        Unit         Text,
        Actions      Text,
        Target_Path  Text,
        Rename       Text,
        unique (Rule))
        """)
    except Error as er:
        print(er)
    finally:
        con.commit()


def insertCondition(value):
    value = value.text()
    con = sql_connection()
    condition_table(con)
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO CONDITIONS(Rule) VALUES(?)', [value])
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def retrieve_values():
    con = sql_connection()
    global list
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM CONDITIONS WHERE Rule = ?', [selected_rule])
        for row in cursor.fetchall():
            row = str(row)[2:-3]
            list.append(row)
        list = list[0].split()
        # conditions.condition_value = list[1]
        # conditions.operator_value = list[2]
        # conditions.size_value = list[3]
        # conditions.ext_value = list[4]
        # conditions.date_edit_value = list[5]
        # conditions.unit_value = list[6]
        # conditions.actions_value = list[7]
        # conditions.target_path = list[8]
        # conditions.rename_value = list[9]
    except Error as er:
        print(er)
    finally:
        con.commit()
