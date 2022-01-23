import hazprac
import buttons
import os
import Rules
import datetime
import database

condition_value = ''  # combobox_value
operator_value = ''   # combobox1_value
size_value = ''
ext_value = ''
date_edit_value = 0
unit_value = ''
actions_value = ''
original_path = r''
target_path = r''
rename_value = r''
# https://stackoverflow.com/a/14996816
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def human_size(n_bytes):
    i = 0
    while n_bytes >= 1000 and i < len(suffixes) - 1:
        n_bytes /= 1000.
        i += 1
    f = ('%.1f' % n_bytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def conditions_applied():
    global operator_value, actions_value
    condition_value = str(database.list[1])[1:-2]
    if condition_value == 'Extension':
        operator_value = str(database.list[2])[1:-2]
        if operator_value == 'is':
            actions_value = str(database.list[7])[1:-2]
            ext_value = str(database.list[4])[1:-2]
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    if a.endswith(ext_value):
                        run_task(actions_value, a)
        elif operator_value == 'is not':
            pass

    if condition_value == 'Date Added':
        operator_value = str(database.list[2])[1:-2]
        date_edit_value = str(database.list[5])[1:-2]
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                file_date = int(datetime.datetime.fromtimestamp(os.path.getctime(a)).strftime('%Y%m%d'))
                if operator_value == 'is':
                    if date_edit_value == file_date:
                        run_task(actions_value, a)
                if operator_value == 'is before':
                    if date_edit_value > file_date:
                        run_task(actions_value, a)
                if operator_value == 'is after':
                    if date_edit_value < file_date:
                        run_task(actions_value, a)

    if condition_value == 'Size':
        operator_value = str(database.list[2])[1:-2]
        size_value = str(database.list[3])[1:-2]
        unit_value = str(database.list[6])[1:-2]
        if operator_value == 'is':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    if size_of_file == size_value + " " + unit_value:
                        run_task(actions_value, a)
        elif operator_value == 'greater than':
            pass
        elif operator_value == 'less than':
            pass


def run_task(actions_value, file_to_process):  # file_to process == a
    target_path = str(database.list[8])[1:-2]
    if actions_value == 'Copy':
        Rules.copy(file_to_process, target_path)
    elif actions_value == 'Move':
        Rules.move(file_to_process, target_path)
    elif actions_value == 'Delete':
        Rules.delete(file_to_process)
    elif actions_value == 'Trash Bin':
        Rules.trash_bin(file_to_process)
    elif actions_value == 'Rename':
        Rules.rename(file_to_process)
