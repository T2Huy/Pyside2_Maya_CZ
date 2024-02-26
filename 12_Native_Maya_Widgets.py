from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class NativeMayaWidgetsDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Native Maya Widgets"

    def __init__(self, parent=maya_main_window()):
        super(NativeMayaWidgetsDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(200, 100)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_timer_fired)
        # self.timer.start()

        self.main_window = maya_main_window()
        self.main_window.installEventFilter(self)

    def create_widgets(self):
        pass

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)

    def create_connections(self):
        app = QtWidgets.QApplication.instance()
        app.focusChanged.connect(self.on_focus_changed)

    def print_hierarchy(self, widget):
        if widget:
            output = []

            name = widget.objectName()
            if not name:
                name = "<Object name not set>"

            output.append(f"Widget: {name}")

            parent_widget = widget.parentWidget()
            while parent_widget:
                parent_name = parent_widget.objectName()

                output.append(f"--> Parent: {parent_name}")
                parent_widget = parent_widget.parentWidget()

            output.append("---")

            print("\n".join(output))

    def on_timer_fired(self):
        # focus_widget = QtWidgets.QApplication.focusWidget()
        # if focus_widget:
        #     print(f"Widget with focus (object name): {focus_widget.objectName()}")

        pos = QtGui.QCursor.pos()
        widget_under_mouse = QtWidgets.QApplication.widgetAt(pos)

        self.print_hierarchy(widget_under_mouse)

    def on_focus_changed(self, old_widget, new_widget):
        if self.isVisible():
            if new_widget:
                # print(f"Widget with focus (object name): {new_widget.objectName()}")
                self.print_hierarchy(new_widget)

    def closeEvent(self, event):
        self.timer.stop()

        self.main_window.removeEventFilter(self)

    def eventFilter(self, obj, event):

        if obj == self.main_window:
            if event.type() == QtCore.QEvent.Type.HoverMove:
                pos = self.main_window.mapToGlobal(event.pos())

                widget = QtWidgets.QApplication.widgetAt(pos)

                self.print_hierarchy(widget)

if __name__ == "__main__":

    try:
        native_maya_widgets_dialog.close()
        native_maya_widgets_dialog.deleteLater()
    except:
        pass

    native_maya_widgets_dialog = NativeMayaWidgetsDialog()
    native_maya_widgets_dialog.show()