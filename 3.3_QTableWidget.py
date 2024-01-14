from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class TableDialog(QtWidgets.QDialog):
    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole + 1
    def __init__(self,parent=maya_main_window()):
        super(TableDialog,self).__init__(parent)

        self.setWindowTitle("Table")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        self.setMinimumWidth(500)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.table_wdg = QtWidgets.QTableWidget()
        self.table_wdg.setColumnCount(5)
        self.table_wdg.setColumnWidth(0, 22)
        self.table_wdg.setColumnWidth(2, 70)
        self.table_wdg.setColumnWidth(3, 70)
        self.table_wdg.setColumnWidth(4, 70)
        self.table_wdg.setHorizontalHeaderLabels(["", "Name", "TransX", "TransY", "TransZ"])
        header_view = self.table_wdg.horizontalHeader()
        header_view.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.set_cell_changed_connection_enabled(True)

        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)

    def set_cell_changed_connection_enabled(self, enabled):
        if enabled:
            self.table_wdg.cellChanged.connect(self.on_cell_changed)
        else:
            self.table_wdg.cellChanged.disconnect(self.on_cell_changed)

    def showEvent(self, e):
        super(TableDialog,self).showEvent(e)
        self.refresh_table()

    def keyPressEvent(self,e):
        super(TableDialog, self).keyPressEvent(e)
        e.accept()

    def refresh_table(self):
        self.set_cell_changed_connection_enabled(False)
        self.table_wdg.setRowCount(0)

        meshes = cmds.ls(type="mesh")
        for i in range(len(meshes)):
            transform_name = cmds.listRelatives(meshes[i], parent=True)[0]
            translation = cmds.getAttr(f"{transform_name}.translate")[0]
            visible = cmds.getAttr(f"{transform_name}.visibility")

            self.table_wdg.insertRow(i)
            self.insert_item(i, 0, "", "visibility", visible, True)
            self.insert_item(i, 1, transform_name, None, transform_name, False)
            self.insert_item(i, 2, self.float_to_string(translation[0]), "tx", translation[0], False)
            self.insert_item(i, 3, self.float_to_string(translation[1]), "ty", translation[1], False)
            self.insert_item(i, 4, self.float_to_string(translation[2]), "tz", translation[2], False)

        self.set_cell_changed_connection_enabled(True)


    def insert_item(self, row, column, text, attr, value, is_boolean):
        item = QtWidgets.QTableWidgetItem(text)
        self.set_item_attr(item, attr)
        self.set_item_value(item, value)
        if is_boolean:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.set_item_checked(item, value)

        self.table_wdg.setItem(row, column, item)

    def on_cell_changed(self, row, column):
        self.set_cell_changed_connection_enabled(False)

        item = self.table_wdg.item(row, column)
        if column == 1:
            self.rename(item)
        else:
            is_boolean = column == 0
            self.update_attr(self.get_full_attribute_name(row, item), item, is_boolean)

        self.set_cell_changed_connection_enabled(True)

    def update_attr(self, attr_name, item, is_boolean):
        if is_boolean:
            value = self.is_item_checked(item)
            self.set_item_text(item,"")
        else:
            text = self.get_item_text(item)
            try:
                value = float(text)
            except ValueError:
                self.revert_original_value(item, is_boolean)
                return

        try:
            cmds.setAttr(attr_name, value)
        except:
            self.revert_original_value(item, is_boolean)
            return

        new_value = cmds.getAttr(attr_name)
        if is_boolean:
            self.set_item_checked(item, new_value)
        else:
            self.set_item_text(item, self.float_to_string(new_value))
        self.set_item_value(item, new_value)


    def rename(self, item):
        old_name = self.get_item_value(item)
        new_name = self.get_item_text(item)
        if old_name != new_name:
            actual_new_name = cmds.rename(old_name, new_name)
            if actual_new_name != new_name:
                self.set_item_text(item, actual_new_name)

            self.set_item_value(item, actual_new_name)
    def set_item_text(self, item, text):
        item.setText(text)

    def get_item_text(self, item):
        return item.text()

    def set_item_checked(self, item, checked):
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def is_item_checked(self, item):
        return item.checkState() == QtCore.Qt.Checked

    def set_item_attr(self, item, attr):
        item.setData(self.ATTR_ROLE, attr)

    def get_item_attr(self, item):
        return item.data(self.ATTR_ROLE)

    def set_item_value(self, item, value):
        item.setData(self.VALUE_ROLE, value)

    def get_item_value(self, item):
        return item.data(self.VALUE_ROLE)

    def get_full_attribute_name(self, row, item):
        node_name = self.table_wdg.item(row, 1).data(self.VALUE_ROLE)
        attr_name = self.get_item_attr(item)
        return f"{node_name}.{attr_name}"

    def float_to_string(self, value):
        return f"{value:.4f}"

    def revert_original_value(self, item, is_boolean):
        original_value = self.get_item_value(item)
        if is_boolean:
            self.set_item_checked(item, original_value)
        else:
            self.set_item_text(item, self.float_to_string(original_value))

if __name__ == "__main__":

    try:
        table_dialog.close()
        table_dialog.deleteLater()
    except:
        pass

    table_dialog = TableDialog()
    table_dialog.show()