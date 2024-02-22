from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CustomPlainTextEdit(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super(CustomPlainTextEdit, self).__init__(parent)

    def keyPressEvent(self, key_event):
        # print(f"Key Pressed {key_event.text()}")

        ctrl = key_event.modifiers() == QtCore.Qt.ControlModifier
        # print(f"Control Modifier: {ctrl}")

        shift = key_event.modifiers() == QtCore.Qt.ShiftModifier
        # print(f"Shift Modifier: {shift}")

        alt = key_event.modifiers() == QtCore.Qt.AltModifier
        # print(f"Shift Modifier: {alt}")

        ctrl_alt = key_event.modifiers() == (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
        # print(f"Ctrl + Alt modifier: {ctrl_alt}")

        # if shift:
        #     return

        key = key_event.key()

        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            if ctrl:
                print("Execute Code")
                return
            elif ctrl_alt:
                print("Execute Line")
                return

        # if key == QtCore.Qt.Key_A:
        #     print("A key pressed")
        # elif key == QtCore.Qt.Key_Return:
        #     print("Return key pressed")
        # elif key == QtCore.Qt.Key_Enter:
        #     print("Enter key pressed")


        super(CustomPlainTextEdit, self).keyPressEvent(key_event)

    def keyReleaseEvent(self, key_event):
        # print(f"Key Released {key_event.text()}")

        super(CustomPlainTextEdit, self).keyReleaseEvent(key_event)

class KeypressDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Keypress Dialog"

    def __init__(self, parent=maya_main_window()):
        super(KeypressDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.plain_text = CustomPlainTextEdit()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.plain_text)

if __name__ == "__main__":

    try:
        keypress_dialog.close()
        keypress_dialog.deleteLater()
    except:
        pass

    keypress_dialog = KeypressDialog()
    keypress_dialog.show()