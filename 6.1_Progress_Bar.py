import time

from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class ProgressDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Progress"

    def __init__(self, parent=maya_main_window()):
        super(ProgressDialog,self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(300, 120)

        self.create_widgets()
        self.create_layout()
        self.create_connections()


    def create_widgets(self):
        self.progress_bar_button = QtWidgets.QPushButton("Do It!")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.progress_bar_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.progress_bar_button.clicked.connect(self.run_progress)

    def run_progress(self):
        number_of_operations = 10

        progress_dialog = QtWidgets.QProgressDialog("Waiting to process...", "Cancel", 0, number_of_operations, self)
        progress_dialog.setWindowTitle("Progress...")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()

        QtCore.QCoreApplication.processEvents()

        for i in range(1, number_of_operations + 1):
            if progress_dialog.wasCanceled():
                break

            progress_dialog.setLabelText(f"Processing operation: {i} (of {number_of_operations})")
            progress_dialog.setValue(i)
            time.sleep(0.5)

            QtCore.QCoreApplication.processEvents()

        progress_dialog.close()

if __name__ == "__main__":
    try:
        progress_bar_dialog.close()
        progress_bar_dialog.deleteLater()
    except:
        pass

    progress_bar_dialog = ProgressDialog()
    progress_bar_dialog.show()