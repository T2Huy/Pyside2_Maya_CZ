from PySide2 import QtWidgets
from shiboken2 import getCppPointer

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.OpenMayaUI import MQtUtil

import maya.cmds as cmds

class MyDockableButton(MayaQWidgetDockableMixin, QtWidgets.QPushButton):

    def __init__(self, workspace_control_name=None):
        super(MyDockableButton, self).__init__()

        self.setWindowTitle("Dockable Window")
        self.setText("My Button")

        if workspace_control_name:
            workspace_control_ptr = MQtUtil.findControl(workspace_control_name)

            if workspace_control_ptr is not None:
                widget_ptr = int(getCppPointer(self)[0])

                MQtUtil.addWidgetToMayaLayout(widget_ptr, int(workspace_control_ptr))

if __name__ == "__main__":

    try:
        if button and button.parent():
            workspace_control_name = button.parent().objectName()

            if cmds.window(workspace_control_name, exists=True):
                cmds.deleteUI(workspace_control_name)

    except:
        pass

    button = MyDockableButton()

    workspace_control_name = f"{button.objectName()}WorkspaceControl"
    ui_script = f"from Pyside2_for_Maya.My_Dockable_button import MyDockableButton\nbutton = MyDockableButton('{workspace_control_name}')"

    button.show(dockable=True, uiScript=ui_script)