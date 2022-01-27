from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication

from category import Category
import PyQt5
from category_label import CategoryLabel
from DialogCreateCategoryQt import DialogCreateCategory
from DialogRemoveCategory import DialogRemoveCategory
from DialogRenameCategory import DialogRenameCategory
from SelectWindowQt import SelectWindowSetup, SelectWindow

global_category_object_name_i = 1
scroll_categories_labels_colors = ("#e7e693", "#d9c478")
light_green = "#ceebcf"


class MainWindowSetup(object):
    def setupUi(self, window : QtWidgets.QMainWindow):
        self.window = window
        window.setObjectName("MainWindow")
        window.setWindowModality(QtCore.Qt.NonModal)
        window.setFixedSize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(window.sizePolicy().hasHeightForWidth())
        window.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 401, 551))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.scroll_area = QtWidgets.QScrollArea(self.groupBox)
        self.scroll_area.setGeometry(QtCore.QRect(10, 30, 381, 511))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("CategoriesScroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setBaseSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.label_upper_scroll = QtWidgets.QLabel(self.groupBox)
        self.label_upper_scroll.setGeometry(QtCore.QRect(110, 0, 161, 20))
        self.label_upper_scroll.setAlignment(QtCore.Qt.AlignCenter)
        self.label_upper_scroll.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(630, 450, 161, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.buttons_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setObjectName("buttonsLayout")
        
        self.add_category_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.add_category_button.setObjectName("pushButton")
        self.buttons_layout.addWidget(self.add_category_button)
        self.rename_category_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.rename_category_button.setObjectName("pushButton_2")
        self.buttons_layout.addWidget(self.rename_category_button)
        self.delete_category_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.delete_category_button.setObjectName("pushButton_3")
        self.buttons_layout.addWidget(self.delete_category_button)
        
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        window.setStyleSheet("background-color: #ebe8d4")
        for b in [self.add_category_button, self.rename_category_button, self.delete_category_button]:
            b.setStyleSheet(f"background-color: {light_green}")
        self.labels_in_scroll = []
        self.retranslateUi(window)
        self.get_categories_and_put_in_scroll()
        self.add_category_button.mouseReleaseEvent = self.open_create_category_dialog
        self.delete_category_button.mouseReleaseEvent = self.open_delete_category_dialog
        self.rename_category_button.mouseReleaseEvent = self.open_rename_category_dialog
        QtCore.QMetaObject.connectSlotsByName(window)

        self.select_window = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление складом"))
        self.label_upper_scroll.setText(_translate("MainWindow", "Список категорий товаров"))
        self.add_category_button.setText(_translate("MainWindow", "Добавить категорию"))
        self.rename_category_button.setText(_translate("MainWindow", "Переименовать категорию"))
        self.delete_category_button.setText(_translate("MainWindow", "Удалить категорию"))


    def get_categories_and_put_in_scroll(self):
        global global_category_object_name_i
        categories = Category.get_all_categories()
        for l in self.labels_in_scroll:
            l : QtWidgets.QLabel
            l.setParent(None)
            l.deleteLater()
        self.labels_in_scroll.clear()

        color_i = 0
        for c in categories:
            new_label = CategoryLabel(
                self,
                c,
                scroll_categories_labels_colors[color_i],
                parent=self.scrollAreaWidgetContents,
                on_click=MainWindowSetup.on_category_label_release,
                on_mouse_enter=self.on_category_label_mouse_enter,
                on_mouse_leave=self.on_category_label_mouse_leave
            )
            new_label.setObjectName(str(global_category_object_name_i))
            global_category_object_name_i += 1
            self.verticalLayout_3.addWidget(new_label)

            new_label.setAlignment(QtCore.Qt.AlignCenter)
            new_label.setFixedHeight(20)
            color_i = 1 - color_i

            new_label.setText(c.get_name())
            self.labels_in_scroll.append(new_label)

    def on_category_label_release(main_window_setup, label: CategoryLabel, event: QtGui.QMouseEvent):
        select_window = SelectWindow(main_window_setup.window.show)
        select_window_setup = SelectWindowSetup()
        select_window_setup.setupUi(main_window_setup, select_window, label.category)
        if not (main_window_setup.select_window is None):
            main_window_setup.select_window.close()
        main_window_setup.select_window = select_window
        main_window_setup.select_window.show()
        main_window_setup.window.hide()



    def on_category_label_mouse_enter(main_window_setup, label: CategoryLabel, event: QtGui.QMouseEvent):
        label.setStyleSheet(f"background-color: {light_green}")
        QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)

    def on_category_label_mouse_leave(main_window_setup, label: CategoryLabel, event: QtGui.QMouseEvent):
        label.setStyleSheet(f"background-color: {label.original_bg_color}")
        QApplication.restoreOverrideCursor()

    def open_create_category_dialog(self, event):
        dialog = QtWidgets.QDialog()
        dialog.ui = DialogCreateCategory()
        dialog.ui.setupUi(dialog, self)
        dialog.exec_()
        dialog.show()

    def open_delete_category_dialog(self, event):
        dialog = QtWidgets.QDialog()
        dialog.ui = DialogRemoveCategory()
        dialog.ui.setupUi(dialog, self)
        dialog.exec_()
        dialog.show()

    def open_rename_category_dialog(self, event):
        dialog = QtWidgets.QDialog()
        dialog.ui = DialogRenameCategory()
        dialog.ui.setupUi(dialog, self)
        dialog.exec_()
        dialog.show()