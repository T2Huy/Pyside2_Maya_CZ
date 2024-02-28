from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class TextEditor(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

    def open_file(self, file_path):
        if file_path:
            file_info = QtCore.QFileInfo(file_path)
            if file_info.exists() and file_info.isFile():
                f = QtCore.QFile(file_info.absoluteFilePath())
                if f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                    text_stream = QtCore.QTextStream(f)
                    text_stream.setCodec("UTF-8")

                    text = text_stream.readAll()

                    f.close()

                    self.setPlainText(text)

    def dragEnterEvent(self, drag_event):
        if drag_event.mimeData().hasText() or drag_event.mimeData().hasUrls():
            drag_event.acceptProposedAction()

    def dropEvent(self, drop_event):
        if drop_event.mimeData().hasUrls():
            urls = drop_event.mimeData().urls()

            file_path = urls[0].toLocalFile()
            self.open_file(file_path)

            return

        super(TextEditor, self).dropEvent(drop_event)

class TextEditorDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "File Explorer Drag and Drop"

    def __init__(self, parent=maya_main_window()):
        super(TextEditorDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(800, 400)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.editor = TextEditor()

        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.close_btn = QtWidgets.QPushButton("Close")

        self.create_tree_view()

    def create_tree_view(self):
        root_path = f"{cmds.internalVar(userAppDir=True)}scripts"

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(root_path)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(root_path))
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(3)
        self.tree_view.setColumnWidth(0, 240)
        self.tree_view.setFixedWidth(360)

        self.tree_view.setDragEnabled(True)

        self.model.setNameFilters(["*.py"])
        self.model.setNameFilterDisables(False)

    def create_layout(self):
        side_bar_layout = QtWidgets.QHBoxLayout()
        side_bar_layout.addWidget(self.tree_view)
        side_bar_layout.addWidget(self.editor)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(4)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addLayout(side_bar_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.tree_view.doubleClicked.connect(self.open_file)

        self.clear_btn.clicked.connect(self.clear_editor)
        self.close_btn.clicked.connect(self.close)

    def clear_editor(self):
        self.editor.setPlainText("")

    def open_file(self, index):
        if not self.model.isDir(index):
            file_path = self.model.filePath(index)
            self.editor.open_file(file_path)

if __name__ == "__main__":
    try:
        text_editor_dialog.close()
        text_editor_dialog.deleteLater()
    except:
        pass
    text_editor_dialog = TextEditorDialog()
    text_editor_dialog.show()