from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
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
        con = database.sql_connection()
        database.condition_table(con)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database.db")
        db.open()
        self.condition_model = QSqlTableModel(self)
        self.condition_model.setTable("CONDITIONS")
        self.condition_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.condition_mapper = QDataWidgetMapper(self)
        self.condition_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.condition_mapper.setModel(self.condition_model)
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
        database.init_folder_list()
        for k in buttons.a.keys():
            listbox1.addItem(k)

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
        condition = QComboBox()
        condition.setModel(model)
        operator = QComboBox()
        operator.setModel(model)

        # Display Calender Here....

        date_edit = QDateEdit(calendarPopup=True)
        date_edit.setDateTime(QDateTime.currentDateTime())
        date_edit.setHidden(True)

        def update_date():
            value_date_edit = date_edit.date().toString('yyyyMMdd')
            # conditions.date_edit_value = int(value_date_edit)

        date_edit.editingFinished.connect(update_date)

        condition_combobox_data = {
            'Size': ['is', 'less than', 'greater than'],
            'Extension': ['is', 'is not'],
            'Date Added': ['is', 'is before', 'is after']
        }
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        for condition_combobox_key, condition_combobox_value in condition_combobox_data.items():
            combobox_item = QStandardItem(condition_combobox_key)
            model.appendRow(combobox_item)
            for size_value in condition_combobox_value:
                combobox1_item = QStandardItem(size_value)
                combobox_item.appendRow(combobox1_item)

        def update_combobox1(index):
            index_value = model.index(index, 0, condition.rootModelIndex())
            operator.setRootModelIndex(index_value)
            operator.setCurrentIndex(0)

        condition.currentTextChanged.connect(lambda x: update_combobox1(condition.currentIndex()))
        update_combobox1(0)

        size_value = QLineEdit()
        size_value.setValidator(QDoubleValidator())
        ext_value = QLineEdit()
        ext_value.setHidden(True)
        unit = QComboBox()
        for u in units:
            unit.addItem(u)

        def on_unit_changed():
            # conditions.unit_value = unit.currentText()
            pass

        unit.currentIndexChanged.connect(on_unit_changed)

        def get_size_value():
            # conditions.size_value = size_value.text()
            pass

        size_value.editingFinished.connect(get_size_value)

        def get_ext_value():
            # conditions.ext_value = ext_value.text()
            pass

        size_value.editingFinished.connect(get_ext_value)

        def onActivated():
            # conditions.condition_value = condition.currentText()
            if condition.currentText() == 'Extension':
                ext_value.setHidden(False)
                size_value.setHidden(True)
                unit.setHidden(True)
                date_edit.setHidden(True)
            if condition.currentText() == 'Date Added':
                date_edit.setHidden(False)
                size_value.setHidden(True)
                ext_value.setHidden(True)
                unit.setHidden(True)
            if condition.currentText() == 'Size':
                size_value.setHidden(False)
                unit.setHidden(False)
                date_edit.setHidden(True)
                ext_value.setHidden(True)

        condition.currentIndexChanged.connect(onActivated)

        def combobox1_onActivated():
            # conditions.operator_value = operator.currentText()
            pass

        operator.activated.connect(combobox1_onActivated)
        # here int values are as row, column, row_span, column_span....
        # Same for the next grid layout...

        panel3_grid.addWidget(panel3_label_rule1, 0, 0, 1, 3)
        panel3_grid.addWidget(condition, 1, 0)
        panel3_grid.addWidget(operator, 1, 1)
        panel3_grid.addWidget(size_value, 1, 2)
        panel3_grid.addWidget(unit, 1, 3)
        panel3_grid.addWidget(date_edit, 1, 2)
        panel3_grid.addWidget(ext_value, 1, 2)

        panel3_label_rule2 = QLabel('Do the following to the selected folder/files: ')
        actions = QComboBox()
        actions.addItem('Copy')
        actions.addItem('Move')
        actions.addItem('Delete')
        actions.addItem('Trash Bin')
        actions.addItem('Rename')
        select_folder_btn = QPushButton("Select Folder")

        def select_folder_clicked():
            selected_path = QFileDialog.getExistingDirectory()
            select_folder_btn.setText(selected_path)
            # conditions.target_path = selected_path

        select_folder_btn.clicked.connect(select_folder_clicked)

        rename_value = QLineEdit()
        rename_value.setHidden(True)
        panel3_grid.addWidget(panel3_label_rule2, 2, 0, 1, 3)
        panel3_grid.addWidget(actions, 4, 0)
        panel3_grid.addWidget(select_folder_btn, 4, 1)
        panel3_grid.addWidget(rename_value, 4, 2)
        panel3_grid.setVerticalSpacing(20)
        # Prevent rows from stretching to take all available space
        panel3_grid.setRowStretch(panel3_grid.rowCount(), 1)
        self.condition_mapper.addMapping(condition, 1, b'currentText')
        self.condition_mapper.addMapping(operator, 2, b'currentText')
        self.condition_mapper.addMapping(size_value, 3)
        self.condition_mapper.addMapping(ext_value, 4)
        self.condition_mapper.addMapping(date_edit, 5, b'date')
        self.condition_mapper.addMapping(unit, 6, b'currentText')
        self.condition_mapper.addMapping(actions, 7, b'currentText')
        self.condition_mapper.addMapping(select_folder_btn, 8, b'text')
        self.condition_mapper.addMapping(rename_value, 9)

        def on_Activated():
            # conditions.actions_value = actions.currentText()
            if actions.currentText() == 'Rename':
                rename_value.setHidden(False)
                select_folder_btn.setHidden(True)
            else:
                rename_value.setHidden(True)
                if actions.currentText() == 'Copy' or actions.currentText() == 'Move':
                    select_folder_btn.setHidden(False)
                elif actions.currentText() == 'Delete' or actions.currentText() == 'Trash Bin':
                    select_folder_btn.setHidden(True)

        actions.currentIndexChanged.connect(on_Activated)

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
            if buttons.folder_inserted:
                listbox1.addItem(list(buttons.a)[-1])
                buttons.folder_inserted = False

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

        def add_rules(name):
            checkbox = QListWidgetItem()
            checkbox.setFlags(checkbox.flags() | Qt.ItemIsUserCheckable)
            checkbox.setCheckState(Qt.Unchecked)
            checkbox.setText(name)
            listbox2.addItem(checkbox)

        def rule_item_clicked(item):
            if item.isSelected():
                line_edit.setText(item.text())

        listbox2.itemClicked.connect(rule_item_clicked)

        def update_rule_name():
            i = listbox2.selectedItems()[0]
            i.setText(line_edit.text())

        line_edit.editingFinished.connect(update_rule_name)

        def save_button_clicked():
            self.condition_mapper.submit()

        def discard_button_clicked():
            self.condition_mapper.revert()
        discard_btn.clicked.connect(discard_button_clicked)

        btn2.clicked.connect(update_rule_list)
        btn3.clicked.connect(buttons.resume_pause_clicked)
        save_btn.clicked.connect(save_button_clicked)
        save_btn.clicked.connect(buttons.save_button_clicked)
        discard_btn.clicked.connect(buttons.discard_button_clicked)

        def selectionChanged(item):
            root_dir = buttons.a.get(item.text())
            conditions.original_path = root_dir
            listbox2.clear()
            Rules.rules_list.clear()
            database.initRules()
            for r in Rules.rules_list:
                print(r)
                add_rules(r)

        def ruleSelected(item):
            if item.isSelected():
                frame.setLayout(panel3_vbox)
                frame.show()
                no_rule_label.hide()

        listbox2.itemClicked.connect(ruleSelected)

        def ruleUnselected():
            frame.hide()
            no_rule_label.show()

        # part of database system...
        listbox2.itemClicked.connect(database.getSelectedRule)
        listbox2.itemClicked.connect(database.insertCondition)
        listbox1.itemClicked.connect(database.getSelectedFolder)
        listbox1.itemClicked.connect(selectionChanged)
        listbox1.itemClicked.connect(ruleUnselected)

        def change_rule():
            print("rule changed")
            print(database.selected_rule)
            self.condition_model.setFilter("Rule = '{}'".format(database.selected_rule))
            self.condition_model.select()
            self.condition_mapper.toFirst()

        listbox2.itemClicked.connect(change_rule)

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
