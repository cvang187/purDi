import PySide6
from PySide6.QtCore import QEvent, QEasingCurve, QPropertyAnimation, Signal, QSettings
from PySide6.QtGui import QEnterEvent, Qt
from PySide6.QtWidgets import (
    QDockWidget,
)


class PurDiDockWidget(QDockWidget):
    view_changed = Signal()

    def __init__(self, parent):
        super(PurDiDockWidget, self).__init__(parent)
        self.parent = parent
        self.anim = QPropertyAnimation(self, b"maximumWidth")
        self._is_visible = True
        self._auto_hide_enabled = False
        self.allowed_min_width = 75
        self.allowed_max_width = 400
        self.left_mouse_button = Qt.MouseButton.LeftButton

    def enterEvent(self, event: QEnterEvent) -> None:
        if self._auto_hide_enabled is False:
            return
        elif self._is_visible is False and self._auto_hide_enabled:
            self.animate_right_dock(
                start=self.width(), end=self.allowed_max_width, visibility=True
            )
            event.accept()
        else:
            event.ignore()

    def leaveEvent(self, event: QEvent) -> None:
        if self._auto_hide_enabled is False:
            return
        elif self._is_visible is True and self._auto_hide_enabled:
            self.animate_right_dock(
                start=self.width(), end=self.allowed_min_width, visibility=False
            )
            event.accept()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if (
            self.left_mouse_button is not None
            and event.button() == self.left_mouse_button
        ):
            if self._auto_hide_enabled is False:
                self._auto_hide_enabled = True
                return

            self._auto_hide_enabled = False

    @property
    def is_visible(self):
        return self._is_visible

    def setting_visibility(self, tf: bool):
        self._is_visible = tf

    # TODO: fix animation. kind of finicky
    def animate_right_dock(self, start: int, end: int, visibility: bool):
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.setDuration(2000)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()

        self.anim.valueChanged.connect(self.setMinimumWidth(end))
        self.anim.finished.connect(self.setting_visibility(visibility))

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        super().closeEvent(event)
