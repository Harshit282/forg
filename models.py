from PyQt5.QtCore import *
from PyQt5.QtSql import *

class RuleTableModel(QSqlTableModel):

    def flags(self, index):
        fl = QSqlTableModel.flags(self, index)
        # 2nd row is Rule Name in RULE table
        # which needs to have a CheckBox
        if index.column() == 1:
            fl |= Qt.ItemIsUserCheckable
        return fl

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.CheckStateRole and (
            self.flags(index) & Qt.ItemIsUserCheckable != Qt.NoItemFlags
        ):
            # 3rd row is State in RULE table
            state = index.sibling(index.row(), 2)
            return state.data(Qt.EditRole)
        else:
            return QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole and (
            self.flags(index) & Qt.ItemIsUserCheckable != Qt.NoItemFlags
        ):
            state = index.sibling(index.row(), 2)
            ret = self.setData(state, value, Qt.EditRole)
            # Emit data changed signal only if setData returns true
            if ret:
                self.dataChanged.emit(index, index)
            return ret
        return QSqlTableModel.setData(self, index, value, role)
