from PyQt5 import QtWidgets, QtCore, QtGui

import config
from storage_item import StorageItem


class ConfirmButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, on_release=None):
        super().__init__(parent)
        self._on_release = on_release

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if not (self._on_release is None):
            self._on_release(event)


class DialogRenameProperty(object):
    def setupUi(self, Dialog, select_window_setup):
        self.select_window_setup = select_window_setup
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 268)
        Dialog.setStyleSheet("background-color: #ebe8d4;")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 150))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.label1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label1.setStyleSheet("border: black; padding: 2px;")
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label1)
        self.lineEdit1 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit1.sizePolicy().hasHeightForWidth())
        self.lineEdit1.setSizePolicy(sizePolicy)
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit1.setMaxLength(config.max_category_length)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit1)

        self.label2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label2.setStyleSheet("border: black; padding: 2px;")
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.lineEdit2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit2.sizePolicy().hasHeightForWidth())
        self.lineEdit2.setSizePolicy(sizePolicy)
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit2.setMaxLength(config.max_category_length)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit2)

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
        self.label1.setText(_translate("Dialog", "Старое название свойства:"))
        self.label2.setText(_translate("Dialog", "Новое название свойства:"))
        self.confirmButton.setText(_translate("Dialog", "Подтвердить"))

    def on_confirm_button_release(self, event):
        old = self.lineEdit1.text().capitalize()
        new = self.lineEdit2.text().capitalize()

        if len(old.replace("\'", "").replace('\"', "")) == 0:
            self.error_text.setText('Неккоректное название')
            return
        if len(new.replace("\'", "").replace('\"', "")) == 0:
            self.error_text.setText('Неккоректное название')
            return
        category = self.select_window_setup.category
        properties = StorageItem.get_properties_and_id_names(category)[1:]
        if old in properties and new not in properties:
            StorageItem.rename_property(category, old, new)
            self.select_window_setup.get_all_data_and_put_into_table()
