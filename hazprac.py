from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import buttons
import os
import Rules
import conditions
import database


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('File Organizer')
        main_window_vbox = QVBoxLayout()
        icon1_hbox = QHBoxLayout()
        icon2_hbox = QHBoxLayout()
        icon3_hbox = QHBoxLayout()
        panel1_vbox = QVBoxLayout()
        panel2_vbox = QVBoxLayout()
        panel3_vbox = QVBoxLayout()
        no_rule_label = QLabel("No rule selected")
        no_rule_label.setAlignment(Qt.AlignCenter)
        frame = QFrame()
        chk_vbox = QVBoxLayout()
        all_panel_hbox = QHBoxLayout()
        btm_hbox = QHBoxLayout()
        panel3_hbox = QHBoxLayout()
        panel3_grid = QGridLayout()
        model = QStandardItemModel()

        btn1 = QPushButton()
        btn2 = QPushButton()
        btn3 = QPushButton()
        btn1.setIcon(QIcon('icons/add folder.png'))
        btn1.setToolTip('Add Folder')
        btn2.setIcon(QIcon('icons/add rule.png'))
        btn2.setToolTip('Add Rule')
        btn3.setIcon(QIcon('icons/pause.png'))
        btn3.setToolTip('Pause')

        # Panel 1 starts from here...

        icon1_hbox.addWidget(btn1)
        icon1_hbox.addStretch()
        folders_label = QLabel("Folders")
        listbox1 = QListWidget()
        panel1_vbox.addLayout(icon1_hbox)
        panel1_vbox.addWidget(folders_label)
        panel1_vbox.addWidget(listbox1)

        # Panel 2 starts from here...

        icon2_hbox.addWidget(btn2)
        icon2_hbox.addStretch()
        panel2_vbox.addLayout(icon2_hbox)

        rules_label = QLabel("Rules")
        panel2_vbox.addWidget(rules_label)

        listbox2 = QListWidget()
        panel2_vbox.addWidget(listbox2)
        listbox2.setLayout(chk_vbox)

        # Panel 3 starts from here...

        icon3_hbox.addStretch()
        icon3_hbox.addWidget(btn3)
        panel3_vbox.addLayout(icon3_hbox)

        label_panel3 = QLabel("NAME: ")
        line_edit = QLineEdit()
        panel3_hbox.addWidget(label_panel3)
        panel3_hbox.addWidget(line_edit)
        panel3_vbox.addLayout(panel3_hbox)

        # Added the third panel window here...
        # Also added the icon to add rules and conditions...
        # Used Grid Layout here...

        panel3_label_rule1 = QLabel('If all of the following conditions are met: ')
        combobox = QComboBox()
        combobox.setModel(model)
        combobox1 = QComboBox()
        combobox1.setModel(model)

        # Display Calender Here....

        date_edit = QDateEdit(calendarPopup=True)
        date_edit.setDateTime(QDateTime.currentDateTime())
        date_edit.setHidden(True)

        def update_date():
            value_date_edit = date_edit.date().toString('yyyyMMdd')
            conditions.date_widget_value = int(value_date_edit)

        date_edit.editingFinished.connect(update_date)

        condition_combobox_data = {
            'Size': ['B', 'KB', 'MB', 'GB', 'TB', 'PB'],
            'Image Extension': ['.jpg', '.png', '.gif'],
            'Video Extension': ['.mp4', '.mkv', '.m4p', '.m4v'],
            'Audio Extension': ['.mp3', '.mp4a', '.gig'],
            'Empty Files': ['0 bytes'],
            'Date Added': ['is', 'is before', 'is after']
        }
        for condition_combobox_key, condition_combobox_value in condition_combobox_data.items():
            combobox_item = QStandardItem(condition_combobox_key)
            model.appendRow(combobox_item)
            for value in condition_combobox_value:
                combobox1_item = QStandardItem(value)
                combobox_item.appendRow(combobox1_item)

        def update_combobox1(index):
            index_value = model.index(index, 0, combobox.rootModelIndex())
            combobox1.setRootModelIndex(index_value)
            combobox1.setCurrentIndex(0)

        combobox.currentIndexChanged.connect(update_combobox1)
        update_combobox1(0)

        line_edit3 = QLineEdit()
        line_edit3.setHidden(True)
        line_edit3.setValidator(QDoubleValidator())

        def get_value():
            conditions.line_edit_value = line_edit3.text()
        line_edit3.editingFinished.connect(get_value)

        def onActivated():
            conditions.combobox_value = combobox.currentText()
            if combobox.currentText() == 'Size':
                line_edit3.setHidden(False)
            else:
                line_edit3.setHidden(True)
            if combobox.currentText() == 'Date Added':
                date_edit.setHidden(False)
            else:
                date_edit.setHidden(True)

        combobox.activated.connect(onActivated)

        def combobox1_onActivated():
            conditions.combobox1_value = combobox1.currentText()

        combobox1.activated.connect(combobox1_onActivated)
        # here int values are as row, column, row_span, column_span....
        # Same for the next grid layout...

        panel3_grid.addWidget(panel3_label_rule1, 0, 0, 1, 3)
        panel3_grid.addWidget(combobox, 1, 0)
        panel3_grid.addWidget(combobox1, 1, 1)
        panel3_grid.addWidget(line_edit3, 1, 2)
        panel3_grid.addWidget(date_edit, 1, 2)

        panel3_label_rule2 = QLabel('Do the following to the selected folder/files: ')
        combobox2 = QComboBox()
        combobox2.addItem('Copy')
        combobox2.addItem('Move')
        combobox2.addItem('Delete')
        combobox2.addItem('Trash Bin')
        combobox2.addItem('Rename')
        select_folder_btn = QPushButton("Select Folder")

        def select_folder_clicked():
            selected_path = QFileDialog.getExistingDirectory()
            select_folder_btn.setText("to " + QDir(selected_path).dirName())
            conditions.target_path = selected_path

        select_folder_btn.clicked.connect(select_folder_clicked)

        line_edit2 = QLineEdit()
        line_edit2.setHidden(True)
        panel3_grid.addWidget(panel3_label_rule2, 2, 0, 1, 3)
        panel3_grid.addWidget(combobox2, 4, 0)
        panel3_grid.addWidget(select_folder_btn, 4, 1)
        panel3_grid.addWidget(line_edit2, 4, 2)
        panel3_grid.setVerticalSpacing(20)
        # Prevent rows from stretching to take all available space
        panel3_grid.setRowStretch(panel3_grid.rowCount(), 1)

        def on_Activated():
            conditions.combobox2_value = combobox2.currentText()
            if combobox2.currentText() == 'Rename':
                line_edit2.setHidden(False)
                select_folder_btn.setHidden(True)
            else:
                line_edit2.setHidden(True)
                if combobox2.currentText() == 'Copy' or combobox2.currentText() == 'Move':
                    select_folder_btn.setHidden(False)
                elif combobox2.currentText() == 'Delete' or combobox2.currentText() == 'Trash Bin':
                    select_folder_btn.setHidden(True)

        combobox2.activated.connect(on_Activated)

        panel3_vbox.addLayout(panel3_grid)

        # bottom buttons...

        save_btn = QPushButton("Save")
        discard_btn = QPushButton("Discard")
        btm_hbox.addStretch()
        btm_hbox.addWidget(save_btn)
        btm_hbox.addWidget(discard_btn)
        panel3_vbox.addLayout(btm_hbox)

        # Buttons/Icons clicked actions are defined here...
        # They have been imported from buttons python file...
        def update_folder_list():
            listbox1.insertItem(0, buttons.selected_folders)

        btn1.clicked.connect(buttons.add_folder_clicked)
        btn1.clicked.connect(update_folder_list)

        def update_rule_list():
            checkbox = QListWidgetItem()
            checkbox.setFlags(checkbox.flags() | Qt.ItemIsUserCheckable)
            checkbox.setCheckState(Qt.Unchecked)
            text, ok = QInputDialog.getText(self, 'New rule', 'Enter name:')
            if ok and text:
                checkbox.setText(text)
                listbox2.addItem(checkbox)

        def rule_item_clicked():
            i = listbox2.selectedItems()[0]
            line_edit.setText(i.text())

        listbox2.itemClicked.connect(rule_item_clicked)

        def update_rule_name():
            i = listbox2.selectedItems()[0]
            i.setText(line_edit.text())

        line_edit.editingFinished.connect(update_rule_name)

        btn2.clicked.connect(update_rule_list)
        btn3.clicked.connect(buttons.resume_pause_clicked)
        save_btn.clicked.connect(buttons.save_button_clicked)
        discard_btn.clicked.connect(buttons.discard_button_clicked)

        def selectionChanged(item):
            root_dir = buttons.a.get(item.text())
            conditions.original_path = root_dir

        listbox1.itemClicked.connect(selectionChanged)

        def ruleSelected():
            frame.setLayout(panel3_vbox)
            frame.show()
            no_rule_label.hide()
        listbox2.itemClicked.connect(ruleSelected)

        # part of database system...
        def rule_insertion():
            conn = database.sql_connection()
            database.rule_table(conn)
            for i in range(len(listbox2)):
                t = 1
                values = (listbox2.item(i).text(), t)
                t += 1
                if database.rule_insert(conn, values):
                    print("R Records Inserted")
                else:
                    print("R Records not Inserted")

        listbox1.itemClicked.connect(rule_insertion)

        # Packing layouts into the main window which is in vertical layout...

        all_panel_hbox.addLayout(panel1_vbox)
        all_panel_hbox.addLayout(panel2_vbox)
        all_panel_hbox.addWidget(no_rule_label)
        all_panel_hbox.addWidget(frame)
        frame.hide()
        # Stretch factor of 1,1,3 leads to 20%, 20%, 60% used space
        # for panel 1,2,3 respectively
        all_panel_hbox.setStretchFactor(panel1_vbox, 1)
        all_panel_hbox.setStretchFactor(panel2_vbox, 1)
        all_panel_hbox.setStretchFactor(frame, 3)
        all_panel_hbox.setStretchFactor(no_rule_label, 3)
        main_window_vbox.addLayout(all_panel_hbox)

        self.setLayout(main_window_vbox)
