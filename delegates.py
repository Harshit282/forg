from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import QDir


class ConditionItemDelegate(QStyledItemDelegate):
    def setEditorData(self, editor, index):
        # Target_Path - QPushButton
        print("Column : {}".format(index.column()))
        if index.column() == 8:
            value = index.data()
            if value:
                folder = QDir(value).dirName()
                editor.setText("To {}".format(folder))
                editor.setToolTip(value)
            else:
                editor.setText("Select Folder")
                editor.setToolTip("")
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)
    def setModelData(self, editor, model, index):
        # Target_Path - QPushButton
        if index.column() == 8:
            value = editor.toolTip()
            if value:
                model.setData(index, value)
            else:
                model.setData(index, "")
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)
