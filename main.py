from PyQt5.QtWidgets import QApplication ,QMainWindow
import MainWindowQt
import sys


def application():
	app = QApplication(sys.argv)
	window = QMainWindow()


	main_window_setup = MainWindowQt.MainWindowSetup()
	main_window_setup.setupUi(window)

	window.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	application()