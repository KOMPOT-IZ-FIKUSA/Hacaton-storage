from PyQt5 import QtCore, QtWidgets, QtGui


class CategoryLabel(QtWidgets.QLabel):
	def __init__(self, main_window, category, bg_color, parent=None, on_click=None, on_mouse_enter=None, on_mouse_leave=None):
		super().__init__(parent)
		self.main_window = main_window
		self.category = category
		self._on_click = on_click
		self._on_mouse_enter = on_mouse_enter
		self._on_mouse_leave = on_mouse_leave
		self.original_bg_color = bg_color
		self.setStyleSheet(f"background-color: {self.original_bg_color};")

	def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
		super(CategoryLabel, self).mouseReleaseEvent(event)
		if not (self._on_click is None):
			self._on_click(self.main_window, self, event)

	def enterEvent(self, event: QtCore.QEvent) -> None:
		if not (self._on_mouse_enter is None):
			self._on_mouse_enter(self, event)

	def leaveEvent(self, event: QtCore.QEvent) -> None:
		if not (self._on_mouse_leave is None):
			self._on_mouse_leave(self, event)
