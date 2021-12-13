from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import Rules
import conditions
import database

selected_folders = ''

a = dict()


def add_list_items(name, path):
    a[name] = path


def add_folder_clicked():
    global selected_folders
    folder_path = QFileDialog.getExistingDirectory()
    folder_name = QDir(folder_path)
    selected_folders = folder_name.dirName()
    add_list_items(selected_folders, folder_name.path())


def resume_pause_clicked():
    conditions.conditions_applied()


def save_button_clicked():
    conn = dbms.sql_connection()
    dbms.sql_table(conn)
    t = 1
    # Here t is the folder_id (needs to changed)
    for i in a:

        values = (t, i, a.get(i))
        t += 1
        if dbms.sql_insert(conn, values):
            print("F Records Inserted")
        else:
            print("F Records not Inserted")


def discard_button_clicked():
    print("Hello u added me")
