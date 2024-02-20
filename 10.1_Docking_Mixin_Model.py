from PySide2 import QtWidgets
from shiboken2 import getCppPointer

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.OpenMayaUI import MQtUtil

import maya.cmds as cmds

class MyDockableButtonStatic(MayaQWidgetDockableMixin, QtWidgets.QPushButton):

    UI_NAME = "MyDockableButtonStatic"

    def __init__(self):
        super(MyDockableButtonStatic, self).__init__()

        self.setObjectName(self.UI_NAME)

        self.setWindowTitle("Dockable Window")
        self.setText("My Button")

        workspace_control_name = f"{self.UI_NAME}WorkspaceControl"

        if cmds.workspaceControl(workspace_control_name, q=True, exists=True):
            workspace_control_ptr = int(MQtUtil.findControl(workspace_control_name))
            widget_ptr = int(getCppPointer(self)[0])

            MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)

if __name__ == "__main__":

    try:
        if button and button.parent():
            workspace_control_name = button.parent().objectName()

            if cmds.window(workspace_control_name, exists=True):
                cmds.deleteUI(workspace_control_name)

    except:
        pass

    button = MyDockableButtonStatic()

    ui_script = f"from Pyside2_for_Maya.My_Dockable_button import MyDockableButtonStatic\nbutton = MyDockableButtonStatic()"

    button.show(dockable=True, uiScript=ui_script)