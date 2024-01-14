from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class Custom_Cell_Dialogs(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(Custom_Cell_Dialogs,self).__init__(parent)

        self.setWindowTitle("Custom Cell")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        self.setMinimumWidth(500)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.table_wdg = QtWidgets.QTableWidget()
        self.table_wdg.setColumnCount(3)
        self.table_wdg.setColumnWidth(0,150)
        self.table_wdg.setColumnWidth(1,150)
        self.table_wdg.setColumnWidth(2,150)
        self.table_wdg.setHorizontalHeaderLabels(["QPushButton", "QSpinBox", "QComboBox"])
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
        button_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)

    def showEvent(self, e):
        super(Custom_Cell_Dialogs,self).showEvent(e)
        self.refresh_table()

    def keyPressEvent(self,e):
        super(Custom_Cell_Dialogs, self).keyPressEvent(e)
        e.accept()

    def refresh_table(self):
        self.table_wdg.setRowCount(0)
        self.table_wdg.insertRow(0)

        btn = QtWidgets.QPushButton("Button")
        btn.clicked.connect(self.on_button_pressed)
        self.table_wdg.setCellWidget(0,0,btn)

        spin_box = QtWidgets.QSpinBox()
        spin_box.valueChanged.connect(self.on_value_change)
        self.table_wdg.setCellWidget(0,1,spin_box)

        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(["Item 1", "Item 2", "Item 3"])
        combo_box.currentTextChanged.connect(self.on_current_text_changed)
        self.table_wdg.setCellWidget(0,2,combo_box)


    def on_button_pressed(self):
        print("Button was pressed")

    def on_value_change(self, value):
        print(f"Spinbox value change: {value}")

    def on_current_text_changed(self, text):
        print(f"ComboBox text changed: {text}")


if __name__ == "__main__":

    try:
        custom_cell_dialog.close()
        custom_cell_dialog.deleteLater()
    except:
        pass

    custom_cell_dialog = Custom_Cell_Dialogs()
    custom_cell_dialog.show()