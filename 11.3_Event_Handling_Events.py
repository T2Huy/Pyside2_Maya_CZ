from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

    def focusInEvent(self, focus_event):
        print("Info: Line Edit has focus")

    def focusOutEvent(self, focus_event):
        print("Info: Line Edit lost focus")

class ColorChangeWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ColorChangeWidget, self).__init__(parent)

        self.setFixedSize(24, 24)
        self.color = QtCore.Qt.blue

    def enterEvent(self, event):
        self.color = QtCore.Qt.yellow
        self.update()

    def leaveEvent(self, event):
        self.color = QtCore.Qt.blue
        self.update()

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.fillRect(paint_event.rect(), self.color)

class EventsDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Events Dialog"

    def __init__(self, parent=maya_main_window()):
        super(EventsDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_widgets()
        self.create_layout()
        self.create_connections()


    def create_widgets(self):
        self.name_label = QtWidgets.QLabel("Name: ")
        self.line_edit = LineEdit()

        self.color_button = ColorChangeWidget()
        self.hide_button = QtWidgets.QPushButton('Hide')

    def create_layout(self):
        self.hori_layout = QtWidgets.QHBoxLayout()
        self.vert_layout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.color_button)
        button_layout.addStretch()
        button_layout.addWidget(self.hide_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addLayout(self.hori_layout)
        main_layout.addLayout(self.vert_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.hide_button.clicked.connect(self.hide)

    def showEvent(self, show_event):
        print("Info: Show Event occurred")

    def hideEvent(self, hide_event):
        print("Info: Hide Event occurred")

    def closeEvent(self, close_event):
        if self.isVisible():
            reply = QtWidgets.QMessageBox.question(self, 'Close', "Are you sure you want to close?")
            if reply == QtWidgets.QMessageBox.No:
                close_event.ignore()

    def resizeEvent(self, resize_event):
        if resize_event.size().width() > 250:
            self.hori_layout.addWidget(self.name_label)
            self.hori_layout.addWidget(self.line_edit)
        else:
            self.vert_layout.addWidget(self.name_label)
            self.vert_layout.addWidget(self.line_edit)

if __name__ == "__main__":

    try:
        event_dialog.close()
        event_dialog.deleteLater()
    except:
        pass

    event_dialog = EventsDialog()
    event_dialog.show()