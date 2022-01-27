import typing

from PyQt5 import QtWidgets, QtCore, QtGui, Qt

from DialogCreatePropertyQt import DialogCreateProperty
from DialogRenameProperty import DialogRenameProperty
from DialogRemoveItem import DialogRemoveItem
from storage_item import StorageItem

light_green_egb = (221, 251, 219)
light_gray = "#aaaaaa"
light_yellow = "#f2f0ba"
light_green = "#ddfbdc"
light_red = "#ffbbdc"
green = "#b8f9b6"



class MyButton(QtWidgets.QPushButton):
    def __init__(self, parent, select_window_setup, on_release):
        super().__init__(parent)
        self.select_window_setup = select_window_setup
        self.on_release = on_release

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.on_release(self.select_window_setup, event)

class SelectWindow(QtWidgets.QMainWindow):
    def __init__(self, on_close):
        super().__init__()
        self.on_close = on_close

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.on_close()
        event.accept()


class MyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent, select_window_setup):
        super().__init__(parent)
        self.select_window_setup = select_window_setup
        self.select_window_setup: SelectWindowSetup
        self.listen_changes = False




    def dataChanged(self, topLeft: QtCore.QModelIndex, bottomRight: QtCore.QModelIndex,
                    roles: typing.Iterable[int] = ...) -> None:
        super().dataChanged(topLeft, bottomRight, roles)
        if not self.listen_changes: return
        row, column = topLeft.row(), topLeft.column()

        item = self.item(row, column)

        if item:
            self.stop_listen_changes()
            item.setText(item.text().replace("\'", "").replace("\"", ""))
            self.start_listen_changes()
            if row == 0:
                property_name = self.horizontalHeaderItem(column).text()
                if len(item.text()) > 0:
                    self.select_window_setup.select_properties[property_name] = item.text()
                else:
                    if property_name in self.select_window_setup.select_properties:
                        self.select_window_setup.select_properties.pop(property_name)
                self.select_window_setup.get_all_data_and_put_into_table()


            elif row > 1:
                if item.text() == "":  # Если убираем пробелы и ничего не остаётся, ставим тильду
                    item.setText("~")
                    return
                properties_names = StorageItem.get_properties_and_id_names(self.select_window_setup.category)
                properties = []
                for column_i in range(self.columnCount()):
                    item1 = self.item(row, column_i)
                    if item1:
                        value = item1.text()
                    else:
                        value = "~"
                    properties.append(value)

                id_ = properties[0]
                #  очищаем от id
                properties = properties[1:]
                properties_names = properties_names[1:]

                storage_item = StorageItem(self.select_window_setup.category, dict(zip(properties_names, properties)), id_=id_)
                storage_item.save()

                storage_item = StorageItem.get_by_id(self.select_window_setup.category, storage_item.id)
                property_name = self.horizontalHeaderItem(column).text().capitalize()
                self.stop_listen_changes()
                item.setText(storage_item.properties[property_name].capitalize())
                self.start_listen_changes()


    def start_listen_changes(self):
        self.listen_changes = True

    def stop_listen_changes(self):
        self.listen_changes = False

class SelectWindowSetup(object):
    def setupUi(self, main_window_setup, window, category):
        self.category = category
        self.window = window
        self.main_window_setup = main_window_setup
        window.setObjectName("SelectWindow")
        window.setFixedSize(800, 610)
        window.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        window.setDocumentMode(False)
        window.setTabShape(QtWidgets.QTabWidget.Rounded)
        window.setDockNestingEnabled(False)
        window.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")

        self.all_items = []
        self.all_items = StorageItem.get_all_items_with_ids(category)

        self.tableWidget = MyTableWidget(self.centralwidget, self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 681, 541))
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.add_property_button = QtWidgets.QTextBrowser(self.centralwidget)
        self.add_property_button.setGeometry(QtCore.QRect(710, 10, 81, 41))
        self.add_property_button.setObjectName("add_property_button")
        self.add_property_button.setStyleSheet(f"background-color: {light_green}")
        self.rename_property_button = QtWidgets.QTextBrowser(self.centralwidget)
        self.rename_property_button.setGeometry(QtCore.QRect(710, 61, 81, 41))
        self.rename_property_button.setObjectName("rename_property_button")
        self.rename_property_button.setStyleSheet(f"background-color: {light_green}")
        self.to_main_window_button = MyButton(self.centralwidget, self, SelectWindowSetup.on_back_button_release)
        self.to_main_window_button.setGeometry(QtCore.QRect(710, 560, 81, 31))
        self.to_main_window_button.setObjectName("button_back_from_select")
        self.to_main_window_button.setStyleSheet(f"background-color: {light_yellow}")
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.add_item_button = MyButton(self.centralwidget, self, SelectWindowSetup.on_add_item_button_release)
        self.add_item_button.setGeometry(QtCore.QRect(20, 560, 120, 31))
        self.add_item_button.setObjectName("button_add_item")
        self.add_item_button.setStyleSheet(f"background-color: {green}")

        self.remove_item_button = MyButton(self.centralwidget, self, SelectWindowSetup.open_remove_item_dialog)
        self.remove_item_button.setGeometry(QtCore.QRect(151, 560, 120, 31))
        self.remove_item_button.setObjectName("button_remove_item")
        self.remove_item_button.setStyleSheet(f"background-color: {light_red}")



        self.add_property_button.mouseReleaseEvent = self.open_create_property_dialog
        self.rename_property_button.mouseReleaseEvent = self.open_rename_property_dialog

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.select_properties = {}
        self.get_all_data_and_put_into_table()



    def retranslateUi(self, SelectWindow):
        self.add_item_button.setText("Добавить товар")
        self.remove_item_button.setText("Удалить товар")
        _translate = QtCore.QCoreApplication.translate
        SelectWindow.setWindowTitle(_translate("SelectWindow", "Поиск"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("SelectWindow", "Цвет"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SelectWindow", "Поиск"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SelectWindow", "                 "))
        self.add_property_button.setHtml(_translate("SelectWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Добавить</p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">свойство</p></body></html>"))
        self.rename_property_button.setHtml(_translate("SelectWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Переименовать</p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">свойство</p></body></html>"))
        self.to_main_window_button.setText(_translate("SelectWindow", "Назад"))

    @staticmethod
    def on_back_button_release(select_window_setup: MyButton, event):
        select_window_setup.window.hide()
        select_window_setup.main_window_setup.window.show()

    def clear_table(self):
        for column in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, column)
                if item:
                    item.setText("")

    def get_all_data_and_put_into_table(self):
        self.tableWidget.stop_listen_changes()
        self.clear_table()

        properties_with_id = StorageItem.get_properties_and_id_names(self.category)
        columns_count = len(properties_with_id)

        if len(list(self.select_properties.keys())) == 0:
            all_items = StorageItem.get_all_items_with_ids(self.category)
        else:
            all_items = StorageItem.select(self.category, self.select_properties)


        t = []
        for item in all_items:
            t.append([item.id])
            for property_name in properties_with_id[1:]:
                t[-1].append(item.properties[property_name])

        all_items = t



        rows_count = len(all_items) + 1 + 1  # + 1 пробел + 1 строка поиска

        self.tableWidget.setColumnCount(columns_count)
        self.tableWidget.setRowCount(rows_count)


        for i in range(columns_count):
            #  Названия свойств
            item = self.tableWidget.horizontalHeaderItem(i)
            item = item or QtWidgets.QTableWidgetItem()
            property_name = properties_with_id[i]
            item.setText(property_name)
            self.tableWidget.setHorizontalHeaderItem(i, item)

            #  Первая строка
            item = self.tableWidget.item(0, i)
            item = item or QtWidgets.QTableWidgetItem()
            item.setBackground(QtGui.QColor(*light_green_egb))
            if property_name in self.select_properties:
                item.setText(self.select_properties[property_name])
            self.tableWidget.setItem(0, i, item)

            item = self.tableWidget.item(1, i)
            item = item or QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.tableWidget.setItem(1, i, item)


        #  Опустошение слева
        for i in range(1, rows_count):
            self.tableWidget.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem())

        # Поиск
        item = self.tableWidget.verticalHeaderItem(0)
        item = item or QtWidgets.QTableWidgetItem()
        item.setText("Поиск")
        self.tableWidget.setVerticalHeaderItem(0, item)

        for item_i in range(len(all_items)):


            row_i = item_i + 2
            for column_i in range(columns_count):
                item = self.tableWidget.item(row_i, column_i)
                item = item or QtWidgets.QTableWidgetItem()
                value = all_items[item_i][column_i]
                value = "~" if value is None else str(value)
                value = value.capitalize()
                item.setText(value)
                self.tableWidget.setItem(row_i, column_i, item)

                if column_i == 0:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)


        self.tableWidget.start_listen_changes()


    def open_create_property_dialog(self, event):
        dialog = QtWidgets.QDialog()
        dialog.ui = DialogCreateProperty()
        dialog.ui.setupUi(dialog, self)
        dialog.exec_()
        dialog.show()

    def open_rename_property_dialog(self, event):
        dialog = QtWidgets.QDialog()
        dialog.ui = DialogRenameProperty()
        dialog.ui.setupUi(dialog, self)
        dialog.exec_()
        dialog.show()

    def open_remove_item_dialog(self, event):
        dialog = QtWidgets.QDialog()
        dialog.ui = DialogRemoveItem()
        dialog.ui.setupUi(dialog, self)
        dialog.exec_()
        dialog.show()

    def on_add_item_button_release(setup_select_window, event):
        empty_object = StorageItem(setup_select_window.category, {})
        empty_object.save()
        setup_select_window.get_all_data_and_put_into_table()
