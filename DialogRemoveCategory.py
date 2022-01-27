from PyQt5 import QtWidgets, QtCore, QtGui
import MainWindowQt
import config
from category import Category
from storage_item import StorageItem


class ConfirmButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, on_release=None):
        super().__init__(parent)
        self._on_release = on_release

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if not (self._on_release is None):
            self._on_release(event)



class DialogRemoveCategory(object):
    def setupUi(self, Dialog, main_window_setup):
        self.main_window = main_window_setup
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 268)
        Dialog.setStyleSheet("background-color: #ebe8d4;")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 75))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet("border: black; padding: 2px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(config.max_category_length)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.confirmButton = ConfirmButton(parent=self.verticalLayoutWidget, on_release=self.on_confirm_button_release)
        self.confirmButton.setStyleSheet("background-color: #ceebcf;")
        self.confirmButton.setObjectName("category_add_confirm_button")
        self.verticalLayout.addWidget(self.confirmButton)

        self.error_text = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.error_text.setText("")
        self.error_text.setStyleSheet("color: red; background-color")
        self.error_text.setObjectName("category_add_error_label")
        self.verticalLayout.addWidget(self.error_text)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Название удаляемой категории:"))
        self.confirmButton.setText(_translate("Dialog", "Подтвердить"))


    def on_confirm_button_release(self, event):
        name = self.lineEdit.text()
        name = name.capitalize()
        if Category.does_name_exist(name):
            Category.get_by_name(name).delete()
            self.error_text.setText('')
            self.main_window.get_categories_and_put_in_scroll()
        else:
            self.error_text.setText(f'Категории "{name}" не существует.')

