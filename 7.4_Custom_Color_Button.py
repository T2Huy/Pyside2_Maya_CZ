from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CustomColorButton(QtWidgets.QLabel):

    color_changed = QtCore.Signal()

    def __init__(self, color=QtCore.Qt.white, parent = None):
        super(CustomColorButton, self).__init__(parent)

        self._color = QtGui.QColor() # Invalid Color

        self.set_size(50, 14)
        self.set_color(color)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_color(self, color):
        color = QtGui.QColor(color)

        if self._color != color:
            self._color =color

            pixmap = QtGui.QPixmap(self.size())
            pixmap.fill(self._color)
            self.setPixmap(pixmap)

            self.color_changed.emit()

    def get_color(self):
        return self._color

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(self.get_color(), self, options=QtWidgets.QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.set_color(color)

    def mouseReleaseEvent(self, mouse_event):
        if mouse_event.button() == QtCore.Qt.LeftButton:
            self.select_color()

class CustomColorButtonDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Custom Color Dialog"

    def __init__(self, parent=maya_main_window()):
        super(CustomColorButtonDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOs=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(320, 150)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
    def create_widgets(self):
        self.foreground_color_btn = CustomColorButton(QtCore.Qt.white)
        self.background_color_btn = CustomColorButton(QtCore.Qt.black)

        self.print_btn = QtWidgets.QPushButton("Print")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        color_layout = QtWidgets.QFormLayout()
        color_layout.addRow("Foreground:", self.foreground_color_btn)
        color_layout.addRow("Background:", self.background_color_btn)

        color_grp = QtWidgets.QGroupBox("Color Options")
        color_grp.setLayout(color_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.print_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4,4,4,4)
        main_layout.addWidget(color_grp)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)


    def create_connections(self):
        self.foreground_color_btn.color_changed.connect(self.print_color)
        self.background_color_btn.color_changed.connect(self.print_color)

        self.print_btn.clicked.connect(self.print_color)
        self.close_btn.clicked.connect(self.close)

    def print_color(self):
        fg_color = self.foreground_color_btn.get_color()
        bg_color = self.background_color_btn.get_color()

        print(f"Foreground Color: [{fg_color.red()}, {fg_color.green()}, {fg_color.blue()}]")
        print(f"Background Color: [{bg_color.red()}, {bg_color.green()}, {bg_color.blue()}]")

if __name__ == "__main__":
    try:
        custom_color_dialog.close()
        custom_color_dialog.deleteLater()
    except:
        pass

    custom_color_dialog = CustomColorButtonDialog()
    custom_color_dialog.show()
