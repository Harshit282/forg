from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import Rules
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
            print("F Records Inserted")
        else:
            print("F Records not Inserted")


def resume_pause_clicked():
    save_button_clicked()
    database.retrieve_values()
    conditions.conditions_applied()


def save_button_clicked():
    database.insertRule()


def remove_folder_button_clicked():
    database.remove_folder()


def remove_rule_button_clicked():
    database.remove_rule()
