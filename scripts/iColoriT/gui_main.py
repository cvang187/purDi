import time

import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QImage
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDockWidget,
)

from scripts.iColoriT.gui.gui_draw import GUIDraw
from scripts.iColoriT.gui.gui_gamut import GUIGamut
from scripts.iColoriT.gui.gui_palette import GUIPalette
from scripts.iColoriT.gui.gui_vis import GUI_VIS


class IColorDockWidget(QDockWidget):
    def __init__(
        self,
        color_model,
        img_file=None,
        load_size=221,
        win_size=720,
        device="cpu",
        parent=None,
    ):
        super(IColorDockWidget, self).__init__(parent)
        self.parent = parent
        self.color_ui = IColoriTUI(color_model, img_file, load_size, win_size, device)
        self.setWidget(self.color_ui)
        self.setFloating(True)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar
        )
        self.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
            | Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.setWindowIcon(QIcon("gui/icon.png"))
        self.setWindowTitle("iColoriT")


class IColoriTUI(QWidget):
    image_ready = Signal()

    def __init__(
        self,
        color_model,
        img_file=None,
        load_size=224,
        win_size=256,
        device="cpu",
        parent=None,
    ):
        # draw the layout
        super(IColoriTUI, self).__init__(parent)
        self.parent = parent

        # main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # gamut layout
        self.gamutWidget = GUIGamut(gamut_size=110)
        gamut_layout = self.add_widget(self.gamutWidget, "ab Color Gamut")
        color_layout = QVBoxLayout()

        color_layout.addLayout(gamut_layout)
        main_layout.addLayout(color_layout)

        # palette
        self.usedPalette = GUIPalette(grid_sz=(10, 3))
        up_layout = self.add_widget(self.usedPalette, "Recently used colors")
        color_layout.addLayout(up_layout)

        self.colorPush = QPushButton()  # to visualize the selected color
        self.colorPush.setFixedWidth(self.usedPalette.width())
        self.colorPush.setFixedHeight(35)
        self.colorPush.setStyleSheet("background-color: grey")
        color_push_layout = self.add_widget(self.colorPush, "Current Color")
        color_layout.addLayout(color_push_layout)
        color_layout.setAlignment(Qt.AlignTop)

        # drawPad layout
        draw_pad_layout = QVBoxLayout()
        main_layout.addLayout(draw_pad_layout)
        self.drawWidget = GUIDraw(
            color_model, load_size=load_size, win_size=win_size, device=device
        )
        draw_pad_layout = self.add_widget(self.drawWidget, "Drawing Pad")
        main_layout.addLayout(draw_pad_layout)

        draw_pad_menu = QHBoxLayout()

        self.bGray = QCheckBox("&Gray")
        self.bGray.setToolTip("show gray-scale image")

        self.bLoad = QPushButton("&Load")
        self.bLoad.setToolTip("load an input image")
        self.bSave = QPushButton("&Save")
        self.bSave.setToolTip("Save the current result.")

        draw_pad_menu.addWidget(self.bGray)
        draw_pad_menu.addWidget(self.bLoad)
        draw_pad_menu.addWidget(self.bSave)

        draw_pad_layout.addLayout(draw_pad_menu)
        self.visWidget = GUI_VIS(win_size=win_size, scale=win_size / float(load_size))
        vis_widget_layout = self.add_widget(self.visWidget, "Colorized Result")
        main_layout.addLayout(vis_widget_layout)

        self.bRestart = QPushButton("&Restart")
        self.bRestart.setToolTip("Restart the system")

        self.bQuit = QPushButton("&Quit")
        self.bQuit.setToolTip("Quit the system.")
        vis_widget_menu = QHBoxLayout()
        vis_widget_menu.addWidget(self.bRestart)

        vis_widget_menu.addWidget(self.bQuit)
        vis_widget_layout.addLayout(vis_widget_menu)

        self.drawWidget.update()
        self.visWidget.update()

        # self.colorPush.clicked.connect(self.drawWidget.change_color)

        # color indicator
        self.drawWidget.update_color.connect(self.colorPush.setStyleSheet)

        # update result
        self.drawWidget.update_result.connect(self.visWidget.update_result)  # pyqt5

        # update gamut
        self.drawWidget.update_gammut.connect(self.gamutWidget.set_gamut)  # pyqt5
        self.drawWidget.update_ab.connect(self.gamutWidget.set_ab)
        self.gamutWidget.update_color.connect(self.drawWidget.set_color)

        # connect palette
        self.drawWidget.used_colors.connect(self.usedPalette.set_colors)  # pyqt5
        self.usedPalette.update_color.connect(self.drawWidget.set_color)
        self.usedPalette.update_color.connect(self.gamutWidget.set_ab)

        # menu events
        self.bGray.setChecked(True)
        self.bRestart.clicked.connect(self.reset)
        self.bQuit.clicked.connect(self.quit)
        self.bGray.toggled.connect(self.enable_gray)
        self.bSave.clicked.connect(self.save)
        self.bLoad.clicked.connect(self.load)

        self.start_t = time.time()

        if img_file is not None:
            self.drawWidget.init_result(img_file)
        print("UI initialized")

    @staticmethod
    def add_widget(widget, title):
        widget_layout = QVBoxLayout()
        widget_box = QGroupBox()
        widget_box.setTitle(title)
        vbox_t = QVBoxLayout()
        vbox_t.addWidget(widget)
        widget_box.setLayout(vbox_t)
        widget_layout.addWidget(widget_box)

        return widget_layout

    def next_image(self):
        self.drawWidget.next_image()

    def reset(self):
        # self.start_t = time.time()
        print(
            "============================reset all========================================="
        )
        self.visWidget.reset()
        self.gamutWidget.reset()
        self.usedPalette.reset()
        self.drawWidget.reset()
        self.update()
        self.colorPush.setStyleSheet("background-color: grey")

    def enable_gray(self):
        self.drawWidget.enable_gray()

    def quit(self):
        self.close()

    def save(self):
        self.drawWidget.save_result()

    def load(self):
        self.drawWidget.load_image()

    def change_color(self):
        print("change color")
        self.drawWidget.change_color(use_suggest=True)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_R:
    #         self.reset()
    #
    #     if event.key() == Qt.Key_Q:
    #         self.save()
    #         self.quit()
    #
    #     if event.key() == Qt.Key_S:
    #         self.save()
    #
    #     if event.key() == Qt.Key_G:
    #         self.bGray.toggle()
    #
    #     if event.key() == Qt.Key_L:
    #         self.load()
