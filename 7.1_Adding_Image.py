from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CustomImageWidget(QtWidgets.QWidget):

    def __init__(self, width, height, image_path, parent=None):
        super(CustomImageWidget, self).__init__(parent)

        self.set_size(width, height)
        self.set_image(image_path)
        self.set_background_color(QtCore.Qt.black)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_image(self, image_path):
        image = QtGui.QImage(image_path)
        image = image.scaled(self.width(), self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(image)

        self.update()

    def set_background_color(self, color):
        self.background_color = color

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.fillRect(0, 0, self.width(), self.height(), self.background_color)
        painter.drawPixmap(self.rect(), self.pixmap)


class OpenImportDialog(QtWidgets.QDialog):

    FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    selected_filter = "Maya (*.ma *.mb)"

    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = OpenImportDialog()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialog, self).__init__(parent)

        self.setWindowTitle("Open/Import/Reference")
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowTitleHint)

        self.create_widgets()
        self.create_layout()
        self.create_connection()

    def create_widgets(self):
        self.create_title_label()

        self.filepath_le = QtWidgets.QLineEdit()
        self.select_filepath_btn = QtWidgets.QPushButton()
        self.select_filepath_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.select_filepath_btn.setToolTip("Select File")

        self.open_rb = QtWidgets.QRadioButton("Open")
        self.open_rb.setChecked(True)
        self.import_rb = QtWidgets.QRadioButton("Import")
        self.reference_rb = QtWidgets.QRadioButton("Reference")

        self.force_cb = QtWidgets.QCheckBox("Force")

        self.green_btn = QtWidgets.QPushButton("Green")
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_title_label(self):
        # image_path = "C:/Users/My_PC/Downloads/pyside2.jpg"
        image_path = "C:/Users/My_PC/Downloads/pyside2_with_alpha.png"

        # image = QtGui.QImage(image_path)
        # image = image.scaled(280, 140, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        #
        # pixmap = QtGui.QPixmap()
        # pixmap.convertFromImage(image)

        self.title_label = CustomImageWidget(280, 140, image_path)
        self.title_label.set_background_color(QtCore.Qt.red)
        # self.title_label = QtWidgets.QLabel("My Pyside2 Utility")
        # self.title_label.setPixmap(pixmap)

    def create_layout(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)
        file_path_layout.addWidget(self.select_filepath_btn)

        radio_button_layout = QtWidgets.QHBoxLayout()
        radio_button_layout.addWidget(self.open_rb)
        radio_button_layout.addWidget(self.import_rb)
        radio_button_layout.addWidget(self.reference_rb)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("File:", file_path_layout)
        form_layout.addRow("", radio_button_layout)
        form_layout.addRow("", self.force_cb)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.green_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connection(self):
        self.select_filepath_btn.clicked.connect(self.show_file_select_dialog)

        self.open_rb.toggled.connect(self.update_force_visibility)

        self.green_btn.clicked.connect(self.set_background_green)
        self.apply_btn.clicked.connect(self.load_file)
        self.close_btn.clicked.connect(self.close)

    def show_file_select_dialog(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", self.FILE_FILTERS, self.selected_filter)
        if file_path:
            self.filepath_le.setText(file_path)

    def update_force_visibility(self):
        self.force_cb.setVisible(checked)

    def load_file(self):
        file_path = self.filepath_le.text()
        if not file_path:
            return

        file_info = QtCore.QFileInfo(file_path)
        if not file_info.exists():
            om.MGlobal.displayError(f"File does not exist: {file_path}")
            return

        if self.open_rb.isChecked():
            self.open_file(file_path)
        elif self.import_rb.isChecked():
            self.import_file(file_path)
        else:
            self.referencer_file(file_path)

    def open_file(self, file_path):
        force = self.force_cb.isChecked()
        if not force and cmds.file(q=True, modified=True):
            result = QtWidgets.QMessageBox.question(self, "Modified", "Current scene has unsaved changes. Continue?")
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                force = True
            else:
                return

        cmds.file(file_path, open=True, ignoreVersion=True, force=force)

    def import_file(self, file_path):
        cmds.file(file_path, i=True, ignoreVersion=True)

    def referencer_file(self, file_path):
        cmds.file(file_path, reference=True, ignoreVersion=True)

    def set_background_green(self):
        self.title_label.set_background_color(QtCore.Qt.green)

if __name__ == "__main__":

    try:
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass

    open_import_dialog = OpenImportDialog()
    open_import_dialog.show()