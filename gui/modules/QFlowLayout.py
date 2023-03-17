from PySide6 import QtCore, QtWidgets


class QFlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, h_spacing=-1, v_spacing=-1):
        super(QFlowLayout, self).__init__(parent)
        self._horizontal_spacing = h_spacing
        self._vertical_spacing = v_spacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontal_spacing(self):
        if self._horizontal_spacing >= 0:
            return self._horizontal_spacing
        return self.smart_spacing(
            QtWidgets.QStyle.PixelMetric.PM_LayoutHorizontalSpacing
        )

    def vertical_spacing(self):
        if self._vertical_spacing >= 0:
            return self._vertical_spacing
        return self.smart_spacing(QtWidgets.QStyle.PixelMetric.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.do_layout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(QFlowLayout, self).setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def do_layout(self, rect, debug):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        line_height = 0
        for item in self._items:
            widget = item.widget()
            h_space = self.horizontal_spacing()
            if h_space == -1:
                h_space = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.ControlType.PushButton,
                    QtWidgets.QSizePolicy.ControlType.PushButton,
                    QtCore.Qt.Orientation.Horizontal,
                )
            v_space = self.vertical_spacing()
            if v_space == -1:
                v_space = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.ControlType.PushButton,
                    QtWidgets.QSizePolicy.ControlType.PushButton,
                    QtCore.Qt.Orientation.Vertical,
                )
            next_x = x + item.sizeHint().width() + h_space
            if next_x - h_space > effective.right() and line_height > 0:
                x = effective.x()
                y = y + line_height + v_space
                next_x = x + item.sizeHint().width() + h_space
                line_height = 0
            if not debug:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        return y + line_height - rect.y() + bottom

    def smart_spacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()
