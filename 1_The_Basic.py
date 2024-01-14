from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

""" Return Maya Main window Pointer"""
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class MyLineEdit(QtWidgets.QLineEdit):

    enter_pressed = QtCore.Signal(str)

    """Enter/Return Key Press Event"""

    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Enter :
            self.enter_pressed.emit("Enter Key Pressed")
        elif e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit("Return Key Pressed")
class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.lineedit = MyLineEdit()
        # self.combobox = QtWidgets.QComboBox()
        # self.combobox.addItems(["ComboBoxItem 1", "ComboBoxItem 2", "ComboBoxItem 3", "ComboBoxItem 4"])

        # self.lineedit = QtWidgets.QLineEdit()
        # self.checkbox1 = QtWidgets.QCheckBox()
        # self.checkbox2 = QtWidgets.QCheckBox()

        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancle_btn = QtWidgets.QPushButton("Cancle")

    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()

        form_layout.addRow("Name: ", self.lineedit)

        # form_layout.addRow("ComboBox: ", self.combobox)

        # form_layout.addRow("Name: ", self.lineedit)
        # form_layout.addRow("Hidden: ", self.checkbox1)
        # form_layout.addRow("Locked: ", self.checkbox2)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancle_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.lineedit.enter_pressed.connect(self.on_enter_pressed)

        # self.combobox.activated.connect(self.on_activated_int)
        # self.combobox.activated[str].connect(self.on_activated_str)

        # self.lineedit.textChanged.connect(self.print_hello_name())
        # self.checkbox1.toggled.connect(self.print_is_hidden())

        self.cancle_btn.clicked.connect(self.close)

    def on_enter_pressed(self, text):
        print(text)

    # @QtCore.Slot(int)
    # def on_activated_int(self, index):
    #     print(f"ComboBox Index: {index}")

    # @QtCore.Slot(str)
    # def on_activated_str(self, text):
    #     print(f"ComboBox Text: {text}")

    # def print_hello_name(self, name):
    #     name = self.lineedit.text()
    #     print(f"Hello {name}")
    #
    # def print_is_hidden(self):
    #     hidden = self.checkbox1.isChecked()
    #     if hidden:
    #         print("Hidden")
    #     else:
    #         print("Visible")

if __name__ == "__main__":

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = TestDialog()
    test_dialog.show()