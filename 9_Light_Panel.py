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

        if color != self.get_color():
            cmds.colorSliderGrp(self.get_full_name(), e=True, rgbValue=(color.redF(), color.greenF(), color.blueF()))
            self.on_color_changed()

    def get_color(self):
        color = cmds.colorSliderGrp(self.get_full_name(), q=True, rgbValue=True)

        color = QtGui.QColor(color[0] * 255, color[1] * 255, color[2] * 255)
        return color

    def on_color_changed(self, *args):
        self.color_changed.emit(self.get_color())

class LightItem(QtWidgets.QWidget):

    SUPPORTED_TYPES = ["ambientLight", "directionalLight", "pointLight", "spotLight"]
    EMIT_TYPES = ["directionalLight", "pointLight", "spotLight"]

    def __init__(self, shape_name, parent=None):
        super(LightItem, self).__init__(parent)

        self.setFixedHeight(26)

        self.shape_name = shape_name

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.light_type_btn = QtWidgets.QPushButton()
        self.light_type_btn.setFixedSize(20, 20)
        self.light_type_btn.setFlat(True)

        self.visibility_cb = QtWidgets.QCheckBox()

        self.transform_name_label = QtWidgets.QLabel("placeholder")
        self.transform_name_label.setFixedWidth(120)
        self.transform_name_label.setAlignment(QtCore.Qt.AlignCenter)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb = QtWidgets.QDoubleSpinBox()
            self.intensity_dsb.setRange(0.0, 100.0)
            self.intensity_dsb.setDecimals(3)
            self.intensity_dsb.setSingleStep(0.1)
            self.intensity_dsb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

            self.color_btn = CustomColorButton()

            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb = QtWidgets.QCheckBox()
                self.emit_specular_cb = QtWidgets.QCheckBox()

        self.update_values()

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.light_type_btn)
        main_layout.addWidget(self.visibility_cb)
        main_layout.addWidget(self.transform_name_label)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            main_layout.addWidget(self.intensity_dsb)
            main_layout.addSpacing(10)
            main_layout.addWidget(self.color_btn)

            if light_type in self.EMIT_TYPES:
                main_layout.addSpacing(34)
                main_layout.addWidget(self.emit_diffuse_cb)
                main_layout.addSpacing(50)
                main_layout.addWidget(self.emit_specular_cb)

        main_layout.addStretch()

    def create_connections(self):
        self.light_type_btn.clicked.connect(self.select_light)
        self.visibility_cb.toggled.connect(self.set_visibility)

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb.editingFinished.connect(self.on_intensity_changed)
            self.color_btn.color_changed.connect(self.set_color)

            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb.toggled.connect(self.set_emit_diffuse)
                self.emit_specular_cb.toggled.connect(self.set_emit_specular)

    def update_values(self):
        self.light_type_btn.setIcon(self.get_light_type_icon())
        self.visibility_cb.setChecked(self.is_visible())
        self.transform_name_label.setText(self.get_transform_name())

        light_type = self.get_light_type()
        if light_type in self.SUPPORTED_TYPES:
            self.intensity_dsb.setValue(self.get_intensity())
            self.color_btn.set_color(self.get_color())

            if light_type in self.EMIT_TYPES:
                self.emit_diffuse_cb.setChecked(self.emits_diffuse())
                self.emit_specular_cb.setChecked(self.emits_specular())

    def get_transform_name(self):
        return cmds.listRelatives(self.shape_name, parent=True)[0]

    def get_attribute_value(self, name, attribute):
        return cmds.getAttr(f"{name}.{attribute}")

    def set_attribute_value(self, name, attribute, *args):
        attr_name = f"{name}.{attribute}"
        cmds.setAttr(attr_name, *args)

    def get_light_type(self):
        return cmds.objectType(self.shape_name)

    def get_light_type_icon(self):
        light_type = self.get_light_type()

        icon = QtGui.QIcon()
        if light_type == "ambientLight":
            icon = QtGui.QIcon(":ambientLight.svg")
        elif light_type == "directionalLight":
            icon = QtGui.QIcon(":directionalLight.svg")
        elif light_type == "pointLight":
            icon = QtGui.QIcon(":pointLight.svg")
        elif light_type == "spotLight":
            icon = QtGui.QIcon(":spotLight.svg")
        else:
            icon = QtGui.QIcon(":Light.png")

        return icon

    def is_visible(self):
        transform_name = self.get_transform_name()
        return self.get_attribute_value(transform_name, "visibility")

    def get_intensity(self):
        return self.get_attribute_value(self.shape_name, "intensity")

    def get_color(self):
        temp_color = self.get_attribute_value(self.shape_name, "color")[0]
        return QtGui.QColor(temp_color[0] * 255, temp_color[1] * 255, temp_color[2] * 255)

    def emits_diffuse(self):
        return self.get_attribute_value(self.shape_name, "emitDiffuse")

    def emits_specular(self):
        return self.get_attribute_value(self.shape_name, "emitSpecular")

    def select_light(self):
        cmds.select(self.get_transform_name())

    def set_visibility(self, checked):
        self.set_attribute_value(self.get_transform_name(), "visibility", checked)

    def on_intensity_changed(self):
        self.set_attribute_value(self.shape_name, "intensity", self.intensity_dsb.value())

    def set_color(self, color):
        self.set_attribute_value(self.shape_name, "color", color.redF(), color.greenF(), color.blueF())

    def set_emit_diffuse(self, checked):
        self.set_attribute_value(self.shape_name, "emitDiffuse", checked)

    def set_emit_specular(self, checked):
        self.set_attribute_value(self.shape_name, "emitSpecular", checked)

class LightPanelDialog(QtWidgets.QDialog):
    WINDOW_TITLE = "Light Panel"
    def __init__(self, parent=maya_main_window()):
        super(LightPanelDialog, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)

        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macsOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.resize(500, 260)

        self.light_items = []

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.refreshButton = QtWidgets.QPushButton("Refresh Lights")

    def create_layout(self):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addSpacing(100)
        header_layout.addWidget(QtWidgets.QLabel("Light"))
        header_layout.addSpacing(50)
        header_layout.addWidget(QtWidgets.QLabel("Intensity"))
        header_layout.addSpacing(44)
        header_layout.addWidget(QtWidgets.QLabel("Color"))
        header_layout.addSpacing(24)
        header_layout.addWidget(QtWidgets.QLabel("Emit Diffuse"))
        header_layout.addSpacing(10)
        header_layout.addWidget(QtWidgets.QLabel("Emit Spec"))
        header_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refreshButton)

        light_list_wdg = QtWidgets.QWidget()

        self.light_layout = QtWidgets.QVBoxLayout(light_list_wdg)
        self.light_layout.setContentsMargins(2,2,2,2)
        self.light_layout.setSpacing(3)
        self.light_layout.setAlignment(QtCore.Qt.AlignTop)

        light_list_scroll_area = QtWidgets.QScrollArea()
        light_list_scroll_area.setWidgetResizable(True)
        light_list_scroll_area.setWidget(light_list_wdg)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(light_list_scroll_area)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.refreshButton.clicked.connect(self.refresh_lights)

    def get_lights_in_scene(self):
        return cmds.ls(type="light")

    def refresh_lights(self):
        self.clear_lights()

        scene_lights = self.get_lights_in_scene()
        for light in scene_lights:
            light_item = LightItem(light)

            self.light_layout.addWidget(light_item)
            self.light_items.append(light_item)


    def clear_lights(self):
        self.light_items = []

        while self.light_layout.count() > 0:
            light_item = self.light_layout.takeAt(0)
            if light_item.widget():
                light_item.widget().deleteLater()

    def showEvent(self, event):
        self.refresh_lights()

    def closeEvent(self, event):
        self.clear_lights()

if __name__ == "__main__":
    try:
        light_panel_dialog.close()
        light_panel_dialog.deleteLater()
    except:
        pass

    light_panel_dialog = LightPanelDialog()
    light_panel_dialog.show()