from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class TreeViewDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Tree View Dialog"

    def __init__(self, parent=maya_main_window()):
        super(TreeViewDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(500, 400)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        root_path = f"{cmds.internalVar(userAppDir=True)}scripts"

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(root_path)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(root_path))
        self.tree_view.hideColumn(1)
        self.tree_view.setColumnWidth(0, 240)

        # self.model.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        self.model.setNameFilters(["*.py"])
        self.model.setNameFilterDisables(False)

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.tree_view)

    def create_connections(self):
        self.tree_view.doubleClicked.connect(self.on_double_clicked)

    def on_double_clicked(self, index):
        path = self.model.filePath(index)

        if self.model.isDir(index):
            print(f"Directory selected: {path}")
        else:
            print(f"File selected: {path}")

if __name__ == "__main__":

    try:
        tree_view_dialog.close()
        tree_view_dialog.deleteLater()
    except:
        pass

    tree_view_dialog = TreeViewDialog()
    tree_view_dialog.show()