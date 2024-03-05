from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class PopupWindow(QtWidgets.QWidget):

    def __init__(self, name, parent=None):
        super(PopupWindow, self).__init__(parent)

        self.setWindowTitle(f"{name} Options")

        self.setWindowFlags(QtCore.Qt.Popup)

        self.create_widgets()
        self.create_layout()
    def create_widgets(self):
        self.size_sb = QtWidgets.QSpinBox()
        self.size_sb.setRange(1, 100)
        self.size_sb.setValue(12)

        self.opacity_sb = QtWidgets.QSpinBox()
        self.opacity_sb.setRange(0, 100)
        self.opacity_sb.setValue(100)

    def create_layout(self):
        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Size:", self.size_sb)
        layout.addRow("Opacity:", self.opacity_sb)

class ToolboxButton(QtWidgets.QPushButton):

    def __init__(self, name, parent=None):
        super(ToolboxButton, self).__init__(parent)

        self.pop_up_window = PopupWindow(name, self)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_pop_up_window)


    def show_pop_up_window(self, pos):
        pop_up_pos = self.mapToGlobal(QtCore.QPoint(8, self.height() + 8))
        self.pop_up_window.move(pop_up_pos)

        self.pop_up_window.show()

    # def mousePressEvent(self, mouse_event):
    #     if (mouse_event.button() == QtCore.Qt.RightButton):
    #
    #         # pop_up_pos = self.mapToGlobal(mouse_event.pos())
    #         # self.pop_up_window.move(pop_up_pos)
    #
    #         pop_up_pos = self.mapToGlobal(QtCore.QPoint(8, self.height() + 8 ))
    #         self.pop_up_window.move(pop_up_pos)
    #
    #         self.pop_up_window.show()
    #         return
    #
    #     super(ToolboxButton, self).mousePressEvent(mouse_event)

class ToolboxDialog(QtWidgets.QDialog):

    IMAGE_DIR = "C:/Users/My_PC/Desktop/icon"

    def __init__(self, parent=maya_main_window()):
        super(ToolboxDialog, self).__init__(parent)

        self.setWindowTitle("Toolbox")
        self.setFixedSize(150, 40)

        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
    def create_widgets(self):
        self.pencil_btn = ToolboxButton("Pencil")
        self.pencil_btn.setFixedSize(30, 30)
        self.pencil_btn.setCheckable(True)
        self.pencil_btn.setChecked(True)
        self.pencil_btn.setIcon(QtGui.QIcon(f"{ToolboxDialog.IMAGE_DIR}/pencil.png"))

        self.brush_btn = ToolboxButton("Brush")
        self.brush_btn.setFixedSize(30, 30)
        self.brush_btn.setCheckable(True)
        self.brush_btn.setChecked(True)
        self.brush_btn.setIcon(QtGui.QIcon(f"{ToolboxDialog.IMAGE_DIR}/brush.png"))

        self.eraser_btn = ToolboxButton("Eraser")
        self.eraser_btn.setFixedSize(30, 30)
        self.eraser_btn.setCheckable(True)
        self.eraser_btn.setChecked(True)
        self.eraser_btn.setIcon(QtGui.QIcon(f"{ToolboxDialog.IMAGE_DIR}/eraser.png"))

        self.text_btn = ToolboxButton("Text")
        self.text_btn.setFixedSize(30, 30)
        self.text_btn.setCheckable(True)
        self.text_btn.setChecked(True)
        self.text_btn.setIcon(QtGui.QIcon(f"{ToolboxDialog.IMAGE_DIR}/text.png"))

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(5,5,5,5)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.pencil_btn)
        main_layout.addWidget(self.brush_btn)
        main_layout.addWidget(self.eraser_btn)
        main_layout.addWidget(self.text_btn)
        main_layout.addStretch()

    def create_connections(self):
        self.pencil_btn.clicked.connect(self.on_checked_state_changed)
        self.brush_btn.clicked.connect(self.on_checked_state_changed)
        self.eraser_btn.clicked.connect(self.on_checked_state_changed)
        self.text_btn.clicked.connect(self.on_checked_state_changed)

    def on_checked_state_changed(self):
        button = self.sender()

        self.pencil_btn.setChecked(button == self.pencil_btn)
        self.brush_btn.setChecked(button == self.brush_btn)
        self.eraser_btn.setChecked(button == self.eraser_btn)
        self.text_btn.setChecked(button == self.text_btn)

if __name__ == "__main__":

    try:
        toolbox_dialog.close()
        toolbox_dialog.deleteLater()
    except:
        pass

    toolbox_dialog = ToolboxDialog()
    toolbox_dialog.show()