from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class MovableWidget(QtWidgets.QWidget):
    def __init__(self, x, y, width, height, color, parent=None):
        super(MovableWidget,self).__init__(parent)

        self.setFixedSize(width, height)
        self.move(x, y)

        self.color = color
        self.original_color = color

        self.move_enable = False

    def mousePressEvent(self, mouse_event):
        print("Mouse Button Press")

        if mouse_event.button() == QtCore.Qt.LeftButton:
            self.initial_pos = self.pos()
            self.global_pos = mouse_event.globalPos()

            self.move_enable = True

    def mouseReleaseEvent(self, mouse_event):
        print("Mouse Button Release")

        if self.move_enable:
            self.move_enable = False

    def mouseDoubleClickEvent(self, mouse_event):
        print("Mouse Double-Clicked")

        if self.color == self.original_color:
            self.color = QtCore.Qt.yellow
        else:
            self.color = self.original_color

        self.update()

    def mouseMoveEvent(self, mouse_event):
        print("Mouse Move")

        if self.move_enable:
            diff = mouse_event.globalPos() - self.global_pos
            self.move(self.initial_pos + diff)

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.fillRect(paint_event.rect(), self.color)


class MouseEventDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Mouse Event Dialog"

    def __init__(self, parent=maya_main_window()):
        super(MouseEventDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(400, 400)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.red_widget = MovableWidget(100, 100, 24, 24, QtCore.Qt.red, self)
        self.blue_widget = MovableWidget(200, 200, 24, 24, QtCore.Qt.blue, self)

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)


if __name__ == "__main__":
    try:
        mouse_event_dialog.close()
        mouse_event_dialog.deleteLater()
    except:
        pass

    mouse_event_dialog = MouseEventDialog()
    mouse_event_dialog.show()