import os

from PIL import Image
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QDockWidget, QFileDialog

from gui.modules import util
from gui.modules.QFlowLayout import QFlowLayout
from gui.purDi_Actions import PurDiActions


class PurDiToolBoxWidget(QDockWidget):
    tool_checked = Signal(bool)

    def __init__(self, parent):
        super().__init__()
        self.select_cursor_selected = False
        self.parent = parent

        # hide QDockWidget titlebar
        self.setTitleBarWidget(QWidget())

        self.pa = PurDiActions()
        self.tools_buttons_list = [
            self.pa.cursor_tool_btn,
            self.pa.rect_select_btn,
            self.pa.path_select_btn,
            self.pa.paintbrush_btn,
            self.pa.eraser_btn,
            self.pa.crop_image_btn,
            self.pa.eyedropper_btn,
            self.pa.rotate_img_left_btn,
            self.pa.rotate_img_right_btn,
            self.pa.horizontal_flip_img_btn,
            self.pa.vertical_flip_img_btn,
            self.pa.background_removal_btn,
            self.pa.greyscale_background_btn,
            self.pa.blur_background_btn,
            self.pa.image_colorizer_btn,
            self.pa.white_balance_btn,
            self.pa.panorama_btn,
            self.pa.instagram_filters_btn,
        ]

        self.setLayout(QVBoxLayout())

        toolbar_content = QWidget()
        toolbar_layout = QFlowLayout(toolbar_content)
        toolbar_layout.setSpacing(0)

        self.pa.add_buttons_to_widget(toolbar_layout, self.tools_buttons_list)

        self.setWidget(toolbar_content)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(QtCore.QRect(10, 28, 80, 350))
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setStyleSheet("background-color: #232629;")

        self.pa.cursor_tool_btn.toggled.connect(self.select_cursor)

    def select_cursor(self):
        is_checked = self.pa.cursor_tool_btn.isChecked()
        if is_checked:
            print("Cursor Selected")
            self.select_cursor_selected = True

        self.tool_checked.emit(is_checked)
        print(f"{is_checked}")
        print(f"emitting signal: {self.tool_checked.emit(is_checked)}\n")

    def on_rotate_left_tool_button(self):
        # pixmap = self.get_current_layer_latest_pixmap()
        pixmap = self.parent.view.scene.selectedItems()
        pil = util.q_pixmap_to_image(pixmap)
        pil = pil.rotate(90, expand=True)
        updated_pixmap = util.image_to_qt_pixmap(pil)
        self.parent.view.show_image(updated_pixmap)

    def on_rotate_right_tool_button(self):
        # pixmap = self.get_current_layer_latest_pixmap()
        pixmap = self.parent.view.scene.selectedItems()
        pil = util.q_pixmap_to_image(pixmap)
        pil = pil.rotate(-90, expand=True)
        updated_pixmap = util.image_to_qt_pixmap(pil)
        self.parent.view.show_image(updated_pixmap)

    def on_horizontal_flip_tool_button(self, checked):
        if checked:
            pixmap = self.get_current_layer_latest_pixmap()
            pil = util.q_pixmap_to_image(pixmap)
            pil = pil.transpose(Image.FLIP_LEFT_RIGHT)
            updated_pixmap = util.image_to_qt_pixmap(pil)
            self.parent.view.show_image(
                updated_pixmap, True, "Flip Left-Right", "Tool", None, None
            )
        self.pa.horizontal_flip_img_btn.setChecked(False)

    def on_vertical_flip_tool_button(self, checked):
        if checked:
            pixmap = self.get_current_layer_latest_pixmap()
            pil = util.q_pixmap_to_image(pixmap)
            pil = pil.transpose(Image.FLIP_TOP_BOTTOM)
            updated_pixmap = util.image_to_qt_pixmap(pil)
            self.parent.view.show_image(
                updated_pixmap, True, "Flip Top-Bottom", "Tool", None, None
            )
        self.pa.vertical_flip_img_btn.setChecked(False)

    @QtCore.Signal
    def on_portrait_mode_complete(self, tool):
        background_removed = None
        if tool.backgroundRemoved:
            background_removed = tool.backgroundRemoved
            background_removed = util.image_to_qt_pixmap(background_removed)

        output = tool.output
        if output is not None and background_removed is not None:
            # Depth prediction output
            # Blurred based on predicted depth
            updated_pixmap = util.image_to_qt_pixmap(output)

            # Draw foreground on top of the blurred background
            painter = QPainter(updated_pixmap)
            painter.drawPixmap(QtCore.QPoint(), background_removed)
            painter.end()

            self.parent.view.show_image(updated_pixmap)

        self.pa.blur_background_btn.setChecked(False)
        del tool

    def on_portrait_mode_tool_button(self, checked):
        if checked:
            current_pixmap = self.get_current_layer_latest_pixmap()
            image = util.q_pixmap_to_image(current_pixmap)

            from gui.modules.QPortraitMode import QToolPortraitMode

            # Run human segmentation with alpha matting
            widget = QToolPortraitMode(None, image, self.on_portrait_mode_complete)
            widget.show()

    @QtCore.Signal
    def on_background_removal_complete(self, tool):
        output = tool.output
        if output is not None:
            # Save new pixmap
            updated_pixmap = util.image_to_qt_pixmap(output)
            self.parent.view.show_image(
                updated_pixmap, True, "Background Removal"
            )

        self.pa.background_removal_btn.setChecked(False)
        del tool

    def on_background_removal_tool_button(self, checked):
        if checked:
            current_pixmap = self.get_current_layer_latest_pixmap()
            image = util.q_pixmap_to_image(current_pixmap)

            from gui.modules.QBackgroundRemovalTool import QToolBackgroundRemoval

            widget = QToolBackgroundRemoval(
                None, image, self.on_background_removal_complete
            )
            widget.show()

    # TODO: Fix?
    # @QtCore.Signal
    def on_grayscale_background_completed(self, tool):
        foreground = None
        foreground_pixmap = None

        if tool.output:
            foreground = tool.output
            foreground_pixmap = util.image_to_qt_pixmap(foreground)

        background = util.q_pixmap_to_image(self.get_current_layer_latest_pixmap())
        if foreground is not None and background is not None:
            # Depth prediction output
            # Blurred based on predicted depth
            # Grayscale the background
            from PIL import ImageOps

            background = ImageOps.grayscale(background)
            background_pixmap = util.image_to_qt_pixmap(background)

            # Draw foreground on top of the blurred background
            painter = QPainter(background_pixmap)
            painter.drawPixmap(QtCore.QPoint(), foreground_pixmap)
            painter.end()

            self.parent.view.show_image(background_pixmap)

        # TODO: Fix grayscale tool button
        # self.GrayscaleBackgroundToolButton.setChecked(False)
        del tool

    def on_grayscale_background_tool_button(self, checked):
        if checked:
            current_pixmap = self.get_current_layer_latest_pixmap()
            image = util.q_pixmap_to_image(current_pixmap)

            from gui.modules.QGrayScaleBackgroundTool import QToolGrayscaleBackground

            # Run human segmentation with alpha matting
            widget = QToolGrayscaleBackground(
                None, image, self.on_grayscale_background_completed
            )
            widget.show()

    @QtCore.Signal
    def on_colorizer_complete(self, tool):
        if tool:
            output = tool.output
            if output is not None:
                # Show Interactive Colorization widget
                current_pixmap = self.get_current_layer_latest_pixmap()
                image = util.q_pixmap_to_image(current_pixmap)
                import numpy as np
                import cv2
                import torch

                image = np.asarray(image)
                print("Original image size", image.shape)

                # h, w, c = image.shape
                # max_width = max(h, w)

                b, g, r, a = cv2.split(image)

                from scripts.colorizer.ColorizerMain import IColoriTUI

                colorizer_widget = IColoriTUI(
                    None,
                    viewer=self.parent.view,
                    alphaChannel=a,
                    color_model=output,
                    im_bgr=np.dstack((b, g, r)),
                    load_size=224,
                    win_size=720,
                    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
                )
                colorizer_widget.setWindowModality(
                    QtCore.Qt.WindowModality.ApplicationModal
                )

                colorizer_widget.showMaximized()

                # Create a local event loop for this widget
                loop = QtCore.QEventLoop()
                colorizer_widget.destroyed.connect(loop.quit)
                loop.exec()  # wait

            # TODO: Fix Colorizer tool button
            self.pa.image_colorizer_btn.setChecked(False)
            del tool

    def on_colorizer_tool_button(self):
        from gui.modules.QToolColorizer import QToolColorizer

        widget = QToolColorizer(None, None, self.on_colorizer_complete)
        widget.show()

    # TODO: instagram filter needs refactor/cleaning
    # def on_instagram_filters_tool_button(self):
    #     class QInstagramToolDockWidget(QDockWidget):
    #         def __init__(self, parent, main_window):
    #             QDockWidget.__init__(self, parent)
    #             self.parent = parent
    #             self.closed = False
    #             self.main_window = main_window
    #             self.setWindowTitle("Filters")
    #
    #         def closeEvent(self, event):
    #             self.destroyed.emit()
    #             event.accept()
    #             self.closed = True
    #             self.main_window.InstagramFiltersToolButton.setChecked(False)
    #             self.main_window.image_viewer.set_image(
    #                 self.main_window.image_viewer.pixmap(), True, "Instagram Filters"
    #             )
    #
    #     # self.enable_tool("instagram_filters") if checked else self.disable_tool(
    #     #     "instagram_filters"
    #     # )
    #     current_pixmap = self.get_current_layer_latest_pixmap()
    #     image = util.q_pixmap_to_image(current_pixmap)
    #
    #     from scripts.instagram_filters import QToolInstagramFilters
    #
    #     tool = QToolInstagramFilters(self, image)
    #     self.insta_filter_dock = QInstagramToolDockWidget(None, self)
    #     self.insta_filter_dock.setWidget(tool)
    #     self.addDockWidget(
    #         QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self.insta_filter_dock
    #     )
    #
    #     widget = self.insta_filter_dock
    #
    #     widget.show()
    #
    #     # Create a local event loop for this widget
    #     loop = QtCore.QEventLoop()
    #     self.insta_filter_dock.destroyed.connect(loop.quit)
    #     tool.destroyed.connect(loop.quit)
    #     loop.exec()  # wait
    # else:
    #     # self.disable_tool("instagram_filters")
    #     self.insta_filter_dock.hide()

    @QtCore.Signal
    def on_anime_gan_v2_complete(self, tool):
        output = tool.output
        if output is not None:
            # Save new pixmap
            updated_pixmap = util.image_to_qt_pixmap(output)
            self.parent.view.show_image(updated_pixmap, True, "Anime GAN v2")

        # TODO: add animeGAN button to purDi_Actions.py
        # self.AnimeGanV2ToolButton.setChecked(False)
        del tool

    def on_anime_gan_v2_tool_button(self):
        current_pixmap = self.get_current_layer_latest_pixmap()
        image = util.q_pixmap_to_image(current_pixmap)

        from gui.modules.QAnimeGANv2 import QToolAnimeGANv2

        widget = QToolAnimeGANv2(None, image, self.on_anime_gan_v2_complete)
        widget.show()

    # TODO: Not needed because of background removal already existing?
    # @QtCore.Signal
    # def on_human_segmentation_completed(self, tool):
    #     output = tool.output
    #     if output is not None:
    #         # Save new pixmap
    #         updated_pixmap = self.ImageToQPixmap(output)
    #         self.image_viewer.setImage(updated_pixmap, True, "Human Segmentation")
    #
    #     self.HumanSegmentationToolButton.setChecked(False)
    #     del tool
    #     tool = None
    #
    # def on_human_segmentation_tool_button(self, checked):
    #     if checked:
    #         self.InitTool()
    #         current_pixmap = self.getCurrentLayerLatestPixmap()
    #         image = util.q_pixmap_to_image(current_pixmap)
    #
    #         from QToolHumanSegmentation import QToolHumanSegmentation
    #
    #         widget = QToolHumanSegmentation(
    #             None, image, self.on_human_segmentation_completed
    #         )
    #         widget.show()

    def on_panorama_tool_button(self, checked):
        if checked:
            if self.parent.view.current_filename:
                pixmap = self.get_current_layer_latest_pixmap()
                first = util.q_pixmap_to_image(pixmap)

                if pixmap:
                    # Open second image
                    filepath, _ = QFileDialog.getOpenFileName(self, "Open Image")
                    if len(filepath) and os.path.isfile(filepath):
                        import cv2

                        second = cv2.imread(filepath)

                        # Stitch the pair of images
                        from scripts.panorama.image_stitching import (
                            stitch_image_pair,
                            NotEnoughMatchPointsError,
                        )
                        import numpy as np
                        import cv2

                        first = np.asarray(first)
                        print(first.shape, second.shape)
                        b1, g1, r1, _ = cv2.split(np.asarray(first))
                        dst = None
                        try:
                            dst = stitch_image_pair(
                                np.dstack((r1, g1, b1)), second, stitch_direc=1
                            )
                        except NotEnoughMatchPointsError:
                            # show dialog with error
                            pass

                        if dst is not None:
                            dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)

                            print(dst.shape)
                            dst = Image.fromarray(dst).convert("RGBA")

                            # Save result
                            updated_pixmap = util.image_to_qt_pixmap(dst)
                            self.parent.view.show_image(
                                updated_pixmap,
                                True,
                                "Landscape Panorama",
                                "Tool",
                                None,
                                None,
                            )
        self.pa.panorama_btn.setChecked(False)
