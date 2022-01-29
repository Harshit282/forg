import sqlite3
from sqlite3 import Error
import conditions

selected_rule = ''
selected_folder = ''
retrieved_list = []


def getSelectedRule(rule):
    global selected_rule
    selected_rule = rule.data()


def getSelectedFolder(folder):
    global selected_folder
    selected_folder = folder.data()


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
F_ID      integer            NOT NULL,
Rule_Name   TEXT             NOT NULL PRIMARY KEY,
State       integer,
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


def get_folder_id():
    conn = sql_connection()
    folder_name = selected_folder
    c = conn.cursor()
    c.execute('select ID from FOLDER where Folder_Name = ?', [folder_name])
    folder_id = c.fetchone()
    folder_id = str(folder_id)[1:-2]
    return folder_id


def condition_table(con):
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
        unique (Rule),
        FOREIGN KEY(Rule) REFERENCES RULE(Rule_Name))
        """)
    except Error as er:
        print(er)
    finally:
        con.commit()


def insertCondition(value):
    value = value.data()
    con = sql_connection()
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
    global retrieved_list
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM CONDITIONS WHERE Rule = ?', [selected_rule])
        for row in cursor.fetchall():
            row = str(row)[1:-1]
            retrieved_list.clear()
            retrieved_list.append(row)
        retrieved_list = retrieved_list[0].split(",")
        conditions.rule_name = retrieved_list[0][1:-1]
        conditions.condition_value = retrieved_list[1][2:-1]
        conditions.operator_value = retrieved_list[2][2:-1]
        conditions.size_value = retrieved_list[3][1:]
        conditions.ext_value = retrieved_list[4][2:-1]
        conditions.date_edit_value = retrieved_list[5][2:-1]
        conditions.unit_value = retrieved_list[6][2:-1]
        conditions.actions_value = retrieved_list[7][2:-1]
        conditions.target_path = retrieved_list[8][2:-1]
        conditions.rename_value = retrieved_list[9][2:-1]
        # print(conditions.rule_name, conditions.condition_value, conditions.operator_value, conditions.size_value,
        #       conditions.ext_value, conditions.date_edit_value, conditions.unit_value, conditions.actions_value,
        #       conditions.target_path, conditions.rename_value)
    except Error as er:
        print(er)
    finally:
        con.commit()


def remove_folder():
    con = sql_connection()
    try:
        if selected_folder:
            cursor = con.cursor()
            cursor.execute('DELETE FROM CONDITIONS WHERE Rule IN (SELECT Rule_Name FROM RULE WHERE F_ID IN (SELECT ID '
                           'FROM FOLDER WHERE Folder_Name = ?))', [selected_folder])
            cursor.execute('DELETE FROM RULE WHERE F_ID IN (SELECT ID FROM FOLDER WHERE Folder_Name = ?)',
                           [selected_folder])
            cursor.execute('DELETE FROM FOLDER WHERE Folder_Name = ?', [selected_folder])
            print("folder deletion successful")
            return True
        else:
            print("no folder selected for deletion")
            return False
    except Error as er:
        print(er)
    finally:
        con.commit()


def remove_rule():
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('DELETE FROM CONDITIONS WHERE Rule = ?', [selected_rule])
        cursor.execute('DELETE FROM RULE WHERE Rule_Name = ?', [selected_rule])
    except Error as er:
        print(er)
    finally:
        con.commit()


def update_condition_rule(name):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('UPDATE CONDITIONS SET Rule = ? WHERE Rule = ?', (name, selected_rule))
        print("Old name:  {}".format(selected_rule))
        print("New name:  {}".format(name))
        return True
    except Error as er:
        print(er)
        return False
    finally:
        con.commit()


def init_database():
    con = sql_connection()
    folder_table(con)
    rule_table(con)
    condition_table(con)


# For background helper
def get_folders_list():
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('SELECT Folder_Path FROM FOLDER')
        list_without_tuples = []
        for path in cursor.fetchall():
            list_without_tuples.append(str(path)[2:-3])
        return list_without_tuples
    except Error as er:
        print(er)


def get_rules_list(f_path):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute("""SELECT Rule_Name FROM Rule WHERE F_ID IN(SELECT ID FROM FOLDER WHERE Folder_Path = ?) 
        AND State = (2)""",
                       [f_path])
        list_without_tuples = []
        for path in cursor.fetchall():
            list_without_tuples.append(str(path)[2:-3])
        return list_without_tuples
    except Error as er:
        print(er)


def get_rules_info(r_name):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM CONDITIONS WHERE Rule = ?', [r_name])
        list_without_tuples = []
        for row in cursor.fetchall():
            row = str(row)[1:-1]
            list_without_tuples.clear()
            list_without_tuples.append(row)
        list_without_tuples = list_without_tuples[0].split(",")
        rule_name = list_without_tuples[0][1:-1]
        condition_value = list_without_tuples[1][2:-1]
        operator_value = list_without_tuples[2][2:-1]
        size_value = list_without_tuples[3][1:]
        ext_value = list_without_tuples[4][2:-1]
        date_edit_value = list_without_tuples[5][2:-1]
        unit_value = list_without_tuples[6][2:-1]
        actions_value = list_without_tuples[7][2:-1]
        target_path = list_without_tuples[8][2:-1]
        rename_value = list_without_tuples[9][2:-1]
        list_without_tuples = [rule_name, condition_value, operator_value, size_value, ext_value, date_edit_value,
                               unit_value, actions_value, target_path, rename_value]
        return list_without_tuples
    except Error as er:
        print(er)
