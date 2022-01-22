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

    if combobox_value == 'Empty Files':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                size_of_file = size(os.path.getsize(a))
                if size_of_file == '0B':
                    run_task(combobox2_value, a)

    if combobox_value == 'Old Files':
        pass

    if combobox_value == 'Size':
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                size_of_file = human_size(os.path.getsize(a))
                if size_of_file == line_edit_value + " " + combobox1_value:
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
