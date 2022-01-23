import hazprac
import buttons
import os
import Rules
import datetime

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
    global operator_value, actions_value, condition_value, date_edit_value, unit_value, size_value, ext_value
    if condition_value == 'Extension':
        if operator_value == 'is':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    if a.endswith(ext_value):
                        run_task(actions_value, a)
        elif operator_value == 'is not':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    if a.endswith(ext_value):
                        pass
                    else:
                        run_task(actions_value, a)

    if condition_value == 'Date Added':
        dt = datetime.datetime.strptime(date_edit_value, '%Y-%m-%d')
        new_dt = int(dt.strftime('%Y%m%d'))
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                file_date = int(datetime.datetime.fromtimestamp(os.path.getctime(a)).strftime('%Y%m%d'))
                if operator_value == 'is':
                    if new_dt == file_date:
                        run_task(actions_value, a)
                if operator_value == 'is before':
                    if new_dt > file_date:
                        run_task(actions_value, a)
                if operator_value == 'is after':
                    if new_dt < file_date:
                        run_task(actions_value, a)

    if condition_value == 'Size':
        if operator_value == 'is':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    if size_of_file == size_value + " " + unit_value:
                        run_task(actions_value, a)
        elif operator_value == 'greater than':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    if size_of_file > size_value + " " + unit_value:
                        run_task(actions_value, a)
        elif operator_value == 'less than':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    if size_of_file < size_value + " " + unit_value:
                        run_task(actions_value, a)


def run_task(action_performed, file_to_process):  # file_to process == a
    global target_path
    if action_performed == 'Copy':
        Rules.copy(file_to_process, target_path)
    elif action_performed == 'Move':
        Rules.move(file_to_process, target_path)
    elif action_performed == 'Delete':
        Rules.delete(file_to_process)
    elif action_performed == 'Trash Bin':
        Rules.trash_bin(file_to_process)
    elif action_performed == 'Rename':
        Rules.rename(file_to_process)
