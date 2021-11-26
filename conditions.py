import hazprac
import buttons
import os
import Rules
import datetime
from hurry.filesize import size

combobox_value = ''
combobox1_value = ''
combobox2_value = ''
date_widget_value = 0
line_edit_value = ''
original_path = r''
target_path = r''


def conditions_applied():
    if combobox_value == 'Image Extension' or combobox_value == 'Audio Extension' or combobox_value == 'Video Extension':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                if a.endswith(combobox1_value):
                    run_task(combobox2_value, a)

    if combobox_value == 'Date Added':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                file_date = int(datetime.datetime.fromtimestamp(os.path.getctime(a)).strftime('%Y%m%d'))
                # print(file_date)
                # print(date_widget_value)
                if combobox1_value == 'is':
                    if date_widget_value == file_date:
                        run_task(combobox2_value, a)
                if combobox1_value == 'is before':
                    if date_widget_value > file_date:
                        run_task(combobox2_value, a)
                if combobox1_value == 'is after':
                    if date_widget_value < file_date:
                        run_task(combobox2_value, a)

    if combobox_value == 'Empty files':
        pass
    if combobox_value == 'Old Files':
        pass
    if combobox_value == 'Size':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                size_of_file = size(os.path.getsize(a))
                if size_of_file == line_edit_value + combobox1_value:
                    run_task(combobox2_value, a)


def run_task(combobox_value, file_to_process):  # file_to process == a
    if combobox_value == 'Copy':
        Rules.copy(file_to_process, target_path)
    elif combobox_value == 'Move':
        Rules.move(file_to_process, target_path)
    elif combobox_value == 'Delete':
        Rules.delete(file_to_process)
    elif combobox_value == 'Trash Bin':
        Rules.trash_bin(file_to_process)
    elif combobox_value == 'Rename':
        Rules.rename(file_to_process)
