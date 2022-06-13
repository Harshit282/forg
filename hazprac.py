from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
import buttons
import os
import actions
import conditions
import database
import models
import delegates
import preview
import emptylabels


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('File Organizer')
        database.init_database()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database.db")
        db.open()
        self.condition_model = QSqlTableModel(self)
        self.condition_model.setTable("CONDITIONS")
        self.condition_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.condition_mapper = QDataWidgetMapper(self)
        self.condition_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.condition_mapper.setModel(self.condition_model)
        self.condition_mapper.setItemDelegate(delegates.ConditionItemDelegate(self))
        main_window_vbox = QVBoxLayout()
        icon1_hbox = QHBoxLayout()
        icon2_hbox = QHBoxLayout()
        icon3_hbox = QHBoxLayout()
        panel1_vbox = QVBoxLayout()
        folder_widget = QWidget()
        panel2_vbox = QVBoxLayout(folder_widget)
        panel3_vbox = QVBoxLayout()

        no_rule_label = emptylabels.EmptyLabel("No Rule Selected", "icons/norule.png")
        no_folder_label = emptylabels.EmptyLabel("No Folder Selected", "icons/nofolder.png")
        frame = QFrame()
        all_panel_hbox = QHBoxLayout()
        btm_hbox = QHBoxLayout()
        panel3_hbox = QHBoxLayout()
        panel3_condition_hbox1_layout = QHBoxLayout()
        panel3_condition_hbox2_layout = QHBoxLayout()
        panel3_condition_vbox_layout = QVBoxLayout()
        model = QStandardItemModel()

        add_folder_button = QPushButton()
        add_rule_button = QPushButton()
        preview_button = QPushButton()
        preview_button.setIcon(QIcon('icons/preview.png'))
        preview_button.setToolTip("Preview rule")
        btn3 = QPushButton()
        add_folder_button.setIcon(QIcon('icons/add folder.png'))
        add_folder_button.setToolTip('Add Folder')
        add_rule_button.setIcon(QIcon('icons/add rule.png'))
        btn3.setIcon(QIcon('icons/pause.png'))
        btn3.setToolTip('Pause')
        remove_folder_btn = QPushButton()
        remove_folder_btn.setIcon(QIcon('icons/remove icon.png'))
        remove_folder_btn.setToolTip('Remove Folder')

        # Panel 1 starts from here...

        icon1_hbox.addWidget(add_folder_button)
        icon1_hbox.addWidget(remove_folder_btn)
        icon1_hbox.addStretch()
        folders_label = QLabel("Folders")
        self.folder_model = QSqlTableModel(self)
        self.folder_model.setTable("FOLDER")
        self.folder_model.select()
        folder_listview = QListView()
        folder_listview.setModel(self.folder_model)
        folder_listview.setModelColumn(1)
        folder_listview.setEditTriggers(QListView.NoEditTriggers)
        panel1_vbox.addLayout(icon1_hbox)
        panel1_vbox.addWidget(folders_label)
        panel1_vbox.addWidget(folder_listview)

        # Panel 2 starts from here...

        icon2_hbox.addWidget(add_rule_button)
        icon2_hbox.addStretch()
        panel2_vbox.addLayout(icon2_hbox)

        rules_label = QLabel("Rules")
        panel2_vbox.addWidget(rules_label)

        rule_listview = QListWidget()
        self.rule_model = models.RuleTableModel(self)
        self.rule_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.rule_model.setTable("RULE")
        rule_listview = QListView()
        rule_listview.setModel(self.rule_model)
        rule_listview.setModelColumn(1)
        rule_listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        panel2_vbox.addWidget(rule_listview)

        # Panel 3 starts from here...

        icon3_hbox.addStretch()
        icon3_hbox.addWidget(preview_button)
        icon3_hbox.addWidget(btn3)
        panel3_vbox.addLayout(icon3_hbox)

        label_panel3 = QLabel("NAME: ")
        rule_name = QLineEdit()
        panel3_hbox.addWidget(label_panel3)
        panel3_hbox.addWidget(rule_name)
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
            date_edit.date().toString('yyyyMMdd')

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


        def onActivated():
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

        # here int values are as row, column, row_span, column_span....
        # Same for the next grid layout...

        panel3_condition_hbox1_layout.addWidget(condition)
        panel3_condition_hbox1_layout.addWidget(operator)
        panel3_condition_hbox1_layout.addWidget(size_value)
        panel3_condition_hbox1_layout.addWidget(unit)
        panel3_condition_hbox1_layout.addWidget(date_edit)
        panel3_condition_hbox1_layout.addWidget(ext_value)
        panel3_condition_hbox1_layout.addStretch()

        panel3_label_rule2 = QLabel('Do the following to the selected folder/files: ')
        actions = QComboBox()
        actions.addItem('Copy')
        actions.addItem('Move')
        actions.addItem('Delete')
        actions.addItem('Trash Bin')
        actions.addItem('Rename')
        select_folder_btn = QPushButton()

        def select_folder_clicked():
            selected_path = QFileDialog.getExistingDirectory()
            select_folder_btn.setToolTip(selected_path)
            if selected_path:
                select_folder_btn.setText("To {}"
                    .format(QDir(selected_path).dirName()))

        select_folder_btn.clicked.connect(select_folder_clicked)


        rename_value = QLineEdit()
        rename_value.setHidden(True)
        panel3_condition_hbox2_layout.addWidget(actions)
        panel3_condition_hbox2_layout.addWidget(select_folder_btn)
        panel3_condition_hbox2_layout.addWidget(rename_value)
        panel3_condition_hbox2_layout.addStretch()
        panel3_condition_vbox_layout.addSpacing(20)
        panel3_condition_vbox_layout.addWidget(panel3_label_rule1)
        panel3_condition_vbox_layout.addLayout(panel3_condition_hbox1_layout)
        panel3_condition_vbox_layout.addSpacing(20)
        panel3_condition_vbox_layout.addWidget(panel3_label_rule2)
        panel3_condition_vbox_layout.addLayout(panel3_condition_hbox2_layout)
        # TODO: Prevent child Hboxes also inherit this spacing
        panel3_condition_vbox_layout.setAlignment(Qt.AlignTop)
        self.condition_mapper.addMapping(condition, 1, b'currentText')
        self.condition_mapper.addMapping(operator, 2, b'currentText')
        self.condition_mapper.addMapping(size_value, 3)
        self.condition_mapper.addMapping(ext_value, 4)
        self.condition_mapper.addMapping(date_edit, 5, b'date')
        self.condition_mapper.addMapping(unit, 6, b'currentText')
        self.condition_mapper.addMapping(actions, 7, b'currentText')
        self.condition_mapper.addMapping(select_folder_btn, 8)
        self.condition_mapper.addMapping(rename_value, 9)

        def on_Activated():
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

        panel3_vbox.addLayout(panel3_condition_vbox_layout)

        # bottom buttons...

        save_btn = QPushButton("Save")
        discard_btn = QPushButton("Discard")
        remove_rule_btn = QPushButton("Remove Rule")
        btm_hbox.addStretch()
        btm_hbox.addWidget(save_btn)
        btm_hbox.addWidget(discard_btn)
        btm_hbox.addWidget(remove_rule_btn)
        panel3_vbox.addLayout(btm_hbox)

        # Buttons/Icons clicked actions are defined here...
        # They have been imported from buttons python file...
        def update_folder_model():
            self.folder_model.select()

        def rule_item_clicked(item):
            rule_name.setText(item.data())

        rule_listview.selectionModel().currentChanged.connect(rule_item_clicked)

        def update_rule_name():
            # Make sure line edit is not blank
            if rule_name.text():
                # Update in RULE table
                index = rule_listview.selectionModel().currentIndex()
                inserted = self.rule_model.setData(index, rule_name.text())
                # Update in CONDITION table if returns True
                if inserted:
                    success = database.update_condition_rule(rule_name.text())
                    if success:
                        # Update runtime variable holding rule name
                        database.getSelectedRule(index)
                    else:
                        # If CONDITIONS table updatation fails,
                        # revert RULE table modifications
                        self.rule_model.revert()
                # Failed, probably due to being duplicate
                else:
                    self.rule_model.revert()
                    QMessageBox.warning(self, "Rename Failed",
                                        "Rule with that name already exists.")
                    # Focus rename widget and select text
                    rule_name.setFocus()
                    rule_name.selectAll()
            else:
                # Blank name was given
                QMessageBox.warning(self, "Rename Failed",
                                    "Rule name can not be blank")

        rule_name.returnPressed.connect(update_rule_name)

        def save_button_clicked():
            self.condition_mapper.submit()

        def discard_button_clicked():
            self.condition_mapper.revert()
        discard_btn.clicked.connect(discard_button_clicked)

        btn3.clicked.connect(buttons.resume_pause_clicked)
        save_btn.clicked.connect(save_button_clicked)
        save_btn.clicked.connect(buttons.save_button_clicked)
        remove_folder_btn.clicked.connect(update_folder_model)

        def folder_selected(index):
            folder_widget.show()
            no_folder_label.hide()
            no_rule_label.show()
            # Folder_Path is 3rd column
            path = index.sibling(index.row(), 2).data()
            conditions.original_path = path
            remove_folder_btn.setEnabled(True)
            remove_folder_btn.setToolTip("Remove Folder")
            add_rule_button.setEnabled(True)
            add_rule_button.setToolTip("Add Rule")

        def ruleSelected(item):
            frame.setLayout(panel3_vbox)
            frame.show()
            no_rule_label.hide()

        rule_listview.selectionModel().currentChanged.connect(ruleSelected)

        def ruleUnselected():
            frame.hide()
            no_rule_label.show()

        def folder_unselected():
            folder_widget.hide()
            no_rule_label.hide()
            no_folder_label.show()
            remove_folder_btn.setEnabled(False)
            remove_folder_btn.setToolTip("Select a folder first")
            add_rule_button.setEnabled(False)
            add_rule_button.setToolTip("Select a folder first")
            database.selected_folder = ''
        # For first launch
        folder_unselected()

        # part of database system...
        rule_listview.selectionModel().currentChanged.connect(database.getSelectedRule)
        rule_listview.selectionModel().currentChanged.connect(database.insertCondition)
        folder_listview.clicked.connect(database.getSelectedFolder)
        folder_listview.clicked.connect(folder_selected)
        folder_listview.clicked.connect(ruleUnselected)

        def init_rules():
            self.rule_model.setFilter("F_ID = {}".format(database.get_folder_id()))
            self.rule_model.select()
        folder_listview.clicked.connect(init_rules)

        def update_rule_list():
            text, ok = QInputDialog.getText(self, 'New rule', 'Enter name:')
            if ok and text:
                database.selected_rule = text
                record = self.rule_model.record()
                record.setValue("F_ID", database.get_folder_id())
                record.setValue("Rule_Name", text)
                record.setValue("State", 0)
                if (self.rule_model.insertRecord(-1, record)):
                    database.selected_rule = ''
                    init_rules()
                    ruleUnselected()
                else:
                    QMessageBox.warning(self, "Failed",
                                        "Rule with that name already exists")

        add_rule_button.clicked.connect(update_rule_list)

        def add_folder():
            added = buttons.add_folder_clicked()
            if added:
                ruleUnselected()
                folder_unselected()
                update_folder_model()
                init_rules()
            # Folder dialog was closed without selecting folder
            elif (added is None):
                pass
            else:
                QMessageBox.warning(self, "Failed", "Folder with same path already exists")
        add_folder_button.clicked.connect(add_folder)

        def remove_folder():
            removed = buttons.remove_folder_button_clicked()
            if removed:
                ruleUnselected()
                folder_unselected()
                update_folder_model()
                init_rules()

        def change_rule():
            self.condition_model.setFilter("Rule = '{}'".format(database.selected_rule))
            self.condition_model.select()
            self.condition_mapper.toFirst()

        def show_preview():
            buttons.resume_pause_clicked(True)
            msg = "List of files that satisfy the condition"
            dial = preview.PreviewDialog("Preview Rule", msg, conditions.files)
            # It will show dialog and pause the code execution until dialog is closed
            # using dial.open() is recommended in documention but it doesn't work for me.
            dial.exec_()
            conditions.files.clear()

        preview_button.clicked.connect(show_preview)

        rule_listview.selectionModel().currentChanged.connect(change_rule)

        remove_rule_btn.clicked.connect(buttons.remove_rule_button_clicked)
        remove_rule_btn.clicked.connect(init_rules)
        remove_rule_btn.clicked.connect(ruleUnselected)
        remove_folder_btn.clicked.connect(remove_folder)

        # Packing layouts into the main window which is in vertical layout...

        all_panel_hbox.addLayout(panel1_vbox)
        all_panel_hbox.addWidget(folder_widget)
        all_panel_hbox.addWidget(no_rule_label, Qt.AlignCenter)
        all_panel_hbox.addWidget(no_folder_label, Qt.AlignCenter)
        all_panel_hbox.addWidget(frame)
        frame.hide()
        # Stretch factor of 1,1,3 leads to 20%, 20%, 60% used space
        # for panel 1,2,3 respectively
        all_panel_hbox.setStretchFactor(panel1_vbox, 1)
        all_panel_hbox.setStretchFactor(folder_widget, 1)
        all_panel_hbox.setStretchFactor(frame, 3)
        all_panel_hbox.setStretchFactor(no_rule_label, 3)
        all_panel_hbox.setStretchFactor(no_folder_label, 3)
        # main_window_vbox.addWidget(file_list)
        main_window_vbox.addLayout(all_panel_hbox)

        self.setLayout(main_window_vbox)
