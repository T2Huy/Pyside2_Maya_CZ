from functools import partial

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CustomColorButton(QtWidgets.QWidget):

    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, color=QtCore.Qt.white, parent=None):
        super(CustomColorButton, self).__init__(parent)

        self.setObjectName("CustomColorButton")
        self.create_control()

        self.set_size(50, 14)
        self.set_color(color)

    def create_control(self):

        """create the colorSliderGrp"""
        window = cmds.window()
        color_slider_name = cmds.colorSliderGrp()
        # print(f"original name: {self._name}")

        """find the colorSliderGrp widget"""
        self._color_slider_obj = omui.MQtUtil.findControl(color_slider_name)
        if self._color_slider_obj:
            self._color_slider_widget = wrapInstance(int(self._color_slider_obj), QtWidgets.QWidget)

            """reparent the colorSliderGrp widget to this widget"""
            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.setObjectName("main_layout")
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self._color_slider_widget)

            """update the colorSliderGrp control name (used by Maya)"""
            # self._name = omui.MQtUtil.fullName(int(color_slider_obj))
            # print(f"new name: {self._name}")

            """Identify/store the color sliderGrp's child widgets (and hide if necessary)"""
            # children = self._color_slider_widget.children()
            # for child in children:
            #     print(child)
            #     print(child.objectName())
            # print("---")

            self._slider_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "slider")
            if self._slider_widget:
                self._slider_widget.hide()

            self._color_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "port")

            cmds.colorSliderGrp(self.get_full_name(), e=True, changeCommand=partial(self.on_color_changed))

        cmds.deleteUI(window, window=True)

    def get_full_name(self):
        return omui.MQtUtil.fullName(int(self._color_slider_obj))
    def set_size(self, width, height):
        self._color_slider_widget.setFixedWidth(width)
        self._color_widget.setFixedHeight(height)

    def set_color(self, color):
        color = QtGui.QColor(color)

        cmds.colorSliderGrp(self.get_full_name(), e=True, rgbValue=(color.redF(), color.greenF(), color.blueF()))
        self.on_color_changed()

    def get_color(self):
        color = cmds.colorSliderGrp(self.get_full_name(), q=True, rgbValue=True)

        color = QtGui.QColor(color[0] * 255, color[1] * 255, color[2] * 255)
        return color

    def on_color_changed(self, *args):
        self.color_changed.emit(self.get_color())


class EmbeddingMayaControls(QtWidgets.QDialog):

    WINDOW_TITLE = "Embedding Maya Controls"

    def __init__(self, parent=maya_main_window()):
        super(EmbeddingMayaControls, self).__init__(parent)

        self.setObjectName("EmbeddingMayaControls")

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.abotu(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(320, 150)

        self.foreground_color = QtCore.Qt.white
        self.background_color = QtCore.Qt.black

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.foreground_color_btn = CustomColorButton(self.foreground_color)
        self.background_color_btn = CustomColorButton(self.background_color)

        self.print_fg_color_btn = QtWidgets.QPushButton("Get FG")
        self.print_bg_color_btn = QtWidgets.QPushButton("Get BG")

        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        color_layout = QtWidgets.QFormLayout()
        color_layout.addRow("Foreground:", self.foreground_color_btn)
        color_layout.addRow("Background:", self.background_color_btn)

        color_grp = QtWidgets.QGroupBox("Color Options")
        color_grp.setObjectName("colorGrp")
        color_grp.setLayout(color_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addWidget(self.print_fg_color_btn)
        button_layout.addWidget(self.print_bg_color_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.addWidget(color_grp)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.foreground_color_btn.color_changed.connect(self.on_foreground_color_change)
        self.background_color_btn.color_changed.connect(self.on_background_color_change)

        self.print_fg_color_btn.clicked.connect(self.get_current_foreground_color)
        self.print_bg_color_btn.clicked.connect(self.get_current_background_color)

        self.close_btn.clicked.connect(self.close)

    def on_foreground_color_change(self, new_color):
        print(f"New foreground color: ({new_color.red()}, {new_color.green()}, {new_color.blue()})")

    def on_background_color_change(self, new_color):
        print(f"New background color: ({new_color.red()}, {new_color.green()}, {new_color.blue()})")

    def get_current_foreground_color(self):
        current_color = self.foreground_color_btn.get_color()
        print(f"Current foreground color: ({current_color.red()}, {current_color.green()}, {current_color.blue()})")

    def get_current_background_color(self):
        current_color = self.background_color_btn.get_color()
        print(f"Current background color: ({current_color.red()}, {current_color.green()}, {current_color.blue()})")

if __name__ == "__main__":
    try:
        embedded_dialog.close()
        embedded_dialog.deleteLater()
    except:
        pass

    embedded_dialog = EmbeddingMayaControls()
    embedded_dialog.show()

