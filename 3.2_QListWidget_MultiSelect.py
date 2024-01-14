from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class MultiSelectDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(MultiSelectDialog, self).__init__(parent)

        self.setWindowTitle("Multi-Select")
        self.setFixedWidth(220)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)

        self.create_widgets()
        self.create_layout()
        self.create_connection()

    def create_widgets(self):
        self.list_wdg = QtWidgets.QListWidget()
        # self.list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # self.list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.list_wdg.addItems(["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6"])

        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connection(self):
        self.list_wdg.itemSelectionChanged.connect(self.print_selected_item)

        self.close_btn.clicked.connect(self.close)

    def print_selected_item(self):
        items = self.list_wdg.selectedItems()

        selected_item_labels = []
        for item in items:
            selected_item_labels.append(item.text())

        print(f"Selected Items: {selected_item_labels}")


if __name__ == "__main__":

    try:
        multi_select_dialog.close()
        multi_select_dialog.deleteLater()
    except:
        pass

    multi_select_dialog = MultiSelectDialog()
    multi_select_dialog.show()
