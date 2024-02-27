from PySide2 import QtCore, QtGui, QtWidgets
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

    def set_drop_enable(self, enabled):
        self.setAcceptDrops(enabled)

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
        print("Enter Event")
        
        mime_data = drag_event.mimeData()
        # if mime_data.hasFormat("text/plain") or mime_data.hasFormat("text/uri-list"):
        if mime_data.hasText() or mime_data.hasUrls():
            drag_event.acceptProposedAction()

    def dragLeaveEvent(self, drag_event):
        print("Leave Event")

    def dragMoveEvent(self, drag_event):
        print("Move Event")
        # drag_event.setAccepted(drag_event.pos().x() < 100)

    def dropEvent(self, drop_event):
        print("Drop Event")

        if drop_event.mimeData().hasUrls():
            urls = drop_event.mimeData().urls()

            file_path = urls[0].toLocalFile()
            self.open_file(file_path)

            return

        super(TextEditor, self).dropEvent(drop_event)

class TextEditorDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Drag and Drop Dialog"

    def __init__(self, parent=maya_main_window()):
        super(TextEditorDialog, self).__init__(parent)

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
        self.editor = TextEditor()

        self.drop_enabled_cb = QtWidgets.QCheckBox("Drop Enabled")
        self.drop_enabled_cb.setChecked(True)

        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(4)
        button_layout.addWidget(self.drop_enabled_cb)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.editor)

        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.drop_enabled_cb.toggled.connect(self.editor.set_drop_enable)

        self.clear_btn.clicked.connect(self.clear_editor)
        self.close_btn.clicked.connect(self.close)

    def clear_editor(self):
        self.editor.setPlainText("")

if __name__ == "__main__":
    try:
        text_editor_dialog.close()
        text_editor_dialog.deleteLater()
    except:
        pass

    text_editor_dialog = TextEditorDialog()
    text_editor_dialog.show()
