from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSizePolicy

from gui.modules.QFlowLayout import QFlowLayout


# class QLayerList(QtWidgets.QListWidget):
class QLayerList(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super(QLayerList, self).__init__(parent)

        self.parent = parent
        # self.layout = QFlowLayout()
        self.layerButtons = []
        self.currentButton = None
        self.init()

    def get_total_layers(self):
        if getattr(self.parent, "image_viewer", None):
            layer_history_map = self.parent.view.layer_history
            return len(layer_history_map.keys())
        else:
            return 0

    def on_layer_select(self):
        button = self.sender()
        button.setIconSize(QtCore.QSize(100, 100))
        self.currentButton.setStyleSheet("background-color: rgb(44, 44, 44);")

        selected_layer_index = button.objectName().split("Layer ")[-1]
        selected_layer_index = int(selected_layer_index)
        self.parent.view.current_layer = selected_layer_index
        for lb in self.layerButtons:
            if lb.objectName() == button.objectName():
                lb.setChecked(True)
                lb.setStyleSheet("background-color: rgb(22, 22, 22);")
                self.currentButton = lb
                pixmap = self.parent.view.get_current_layer_latest_pixmap()
                self.parent.view.show_image(pixmap, False)
            else:
                lb.setChecked(False)
                lb.setIconSize(QtCore.QSize(50, 50))
                lb.setStyleSheet("background-color: rgb(44, 44, 44);")

    # def update_scroll_view(self):
    #     self.scroll = QtWidgets.QScrollArea()
    #     self.content = QtWidgets.QWidget()
    #
    #     # self.content.setLayout(self.layout)
    #     # self.content.setContentsMargins(0, 0, 0, 0)
    #
    #     # Scroll Area Properties
    #     # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #     # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #     # self.scroll.setWidgetResizable(True)
    #     self.scroll.setWidget(self.content)
    #     self.setWidget(self.scroll)

    def on_layer_duplicate(self):
        self.parent.view.duplicate_current_layer()
        self.currentButton.setChecked(False)
        self.currentButton.setIconSize(QtCore.QSize(50, 50))
        self.currentButton.setStyleSheet("background-color: rgb(44, 44, 44);")

        self.current_layer = self.parent.view.current_layer
        pixmap = self.parent.get_current_layer_latest_pixmap()

        button = QtWidgets.QToolButton(self)
        button.setText("Layer " + str(self.current_layer + 1))
        button.setIcon(QtGui.QIcon(pixmap))
        button.setIconSize(QtCore.QSize(100, 100))
        # button.setMinimumHeight(50)
        # button.setMinimumWidth(400)
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        button.setCheckable(True)
        button.setObjectName("Layer " + str(self.current_layer))
        button.clicked.connect(self.on_layer_select)
        button.setChecked(True)
        # button.setAutoExclusive(True)
        # button.setStyleSheet("background-color: rgb(22, 22, 22);")
        self.currentButton = button

        self.layerButtons.append(button)
        # self.layout.addWidget(button)
        self.addWidget(button)

        self.update_scroll_view()

    def on_layer_delete(self):
        object_name = self.currentButton.objectName()

        if len(self.layerButtons) > 1:
            # Can only delete second, third, etc. layers
            # Cannot delete when only 1 layer is open

            layer_index = object_name.split("Layer ")[-1]
            layer_index = int(layer_index)

            if self.parent.view.current_layer == layer_index:
                # Current layer matches
                # Switch to a different layer first
                layer_list = list(reversed(self.layerButtons))

                next_layer = None
                new_layer_buttons = []

                for i, l in enumerate(layer_list):
                    if l.objectName() == object_name:
                        # l is the layer being deleted
                        # The next layer in the layer we want to switch to

                        next_index = i + 1 if (i + 1 < len(layer_list)) else (i - 1)

                        if next_index >= 0:
                            next_layer = layer_list[next_index]
                            next_layer.setChecked(True)
                            next_layer_index = int(
                                next_layer.objectName().split("Layer ")[-1]
                            )

                            if next_layer_index is not None:
                                self.layout.removeWidget(l)
                                self.currentButton = next_layer
                                self.currentButton.setIconSize(QtCore.QSize(100, 100))
                                self.currentButton.setStyleSheet(
                                    "background-color: rgb(22, 22, 22);"
                                )
                                self.parent.view.current_layer = next_layer_index
                                pixmap = (
                                    self.parent.view.get_current_layer_latest_pixmap()
                                )
                                self.parent.view.show_image(pixmap, False)
                                del self.parent.view.layer_history[layer_index]
                    else:
                        new_layer_buttons.append(l)

                self.layerButtons = list(reversed(new_layer_buttons))

    def setIconPixmapWithColor(
        self, button, filename, findColor="black", newColor="white"
    ):
        pixmap = QPixmap(filename)
        mask = pixmap.createMaskFromColor(
            QtGui.QColor(findColor), Qt.MaskMode.MaskOutColor
        )
        pixmap.fill((QtGui.QColor(newColor)))
        pixmap.setMask(mask)
        button.setIcon(QtGui.QIcon(pixmap))

    def init(self):
        self.num_layers = self.get_total_layers()
        self.current_layer = self.parent.view.current_layer
        pixmap = self.parent.get_current_layer_latest_pixmap()

        if not self.currentButton:
            title_bar = QtWidgets.QWidget()
            title_bar.setContentsMargins(0, 0, 0, 0)
            title_bar_layout = QtWidgets.QHBoxLayout()
            title_bar_layout.setContentsMargins(0, 0, 0, 0)
            title_bar.setLayout(title_bar_layout)
            title_bar.setMinimumWidth(180)
            title_bar_layout.setSpacing(0)

            self.layer_duplicate_button = QtWidgets.QPushButton()
            self.setIconPixmapWithColor(
                self.layer_duplicate_button, "icons/duplicate.svg"
            )
            self.layer_duplicate_button.setIconSize(QtCore.QSize(20, 20))
            self.layer_duplicate_button.setToolTip("Duplicate Layer")
            self.layer_duplicate_button.clicked.connect(self.on_layer_duplicate)

            layer_delete_button = QtWidgets.QPushButton()
            self.setIconPixmapWithColor(layer_delete_button, "icons/trash.svg")
            layer_delete_button.setIconSize(QtCore.QSize(20, 20))
            layer_delete_button.setToolTip("Delete Layer")
            layer_delete_button.clicked.connect(self.on_layer_delete)

            tools = QtWidgets.QWidget()
            tools_layout = QtWidgets.QHBoxLayout()
            tools_layout.addWidget(self.layer_duplicate_button)
            tools_layout.addWidget(layer_delete_button)
            tools.setLayout(tools_layout)

            title_bar_layout.addWidget(tools)
            title_bar_layout.setAlignment(tools, Qt.AlignmentFlag.AlignCenter)

            self.layout.addWidget(title_bar)

        for i in range(self.num_layers):
            button = QtWidgets.QToolButton(self)
            button.setText("Layer " + str(i + 1))
            button.setIcon(QtGui.QIcon(pixmap))
            button.setIconSize(QtCore.QSize(100, 100))
            button.setMinimumHeight(50)
            # button.setMinimumWidth(180)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            button.setCheckable(True)
            button.setObjectName("Layer " + str(i))
            button.clicked.connect(self.on_layer_select)
            button.setStyleSheet("background-color: rgb(22, 22, 22);")
            if i == self.current_layer:
                button.setChecked(True)
                self.currentButton = button
            else:
                button.setChecked(False)

            self.layerButtons.append(button)
            self.layout.addWidget(button)

        self.update_scroll_view()

    def update(self):
        self.init()

    def set_button_pixmap(self, pixmap):
        self.currentButton.setIcon(QtGui.QIcon(pixmap))
