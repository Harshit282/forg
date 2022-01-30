from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conditions
import database

def add_folder_clicked():
    global folder_inserted
    folder_path = QFileDialog.getExistingDirectory()
    # folder_path will be a empty string if no directory is choosen,
    # and an empty string evaluates to false in python
    if folder_path:
        folder = QDir(folder_path)
        selected_folder = folder.dirName()
        conn = database.sql_connection()
        database.folder_table(conn)
        values = (selected_folder, str(folder_path))
        if database.sql_insert(conn, values):
            # After insertion of a folder, no folder will be selected
            database.selected_folder = ''
            return True
            print("F Records Inserted")
        else:
            return False
            print("F Records not Inserted")


def resume_pause_clicked():
    database.retrieve_values(database.selected_rule)
    conditions.conditions_applied(conditions.original_path)


def save_button_clicked():
    pass


def remove_folder_button_clicked():
    return database.remove_folder()


def remove_rule_button_clicked():
    database.remove_rule()
