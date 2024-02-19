from PySide2 import QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds

class MyDockableButton(MayaQWidgetDockableMixin, QtWidgets.QPushButton):

    def __init__(self):
        super(MyDockableButton,self).__init__()

        self.setWindowTitle("Dockable Window")
        self.setText("My Button")

if __name__ == "__main__":

    try:
        if button and button.parent():
            workspace_control_name = button.parent().objectName()

            if cmds.window(workspace_control_name, exists=True):
                cmds.deleteUI(workspace_control_name)

    except:
        pass

    button = MyDockableButton()
    button.show(dockable=True, uiScript="pass")