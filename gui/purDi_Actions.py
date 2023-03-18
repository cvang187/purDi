from PySide6 import QtGui
from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QPixmap, Qt
from PySide6.QtWidgets import QToolButton, QPushButton


class PurDiActions(QAction):
    """
    Helper class to generate QToolButtons & QActions
    """

    def __init__(self):
        super(PurDiActions, self).__init__()

        self.instagram_filter_icon_path = "gui/icons/instagram.svg"
        self.eraser_icon_path = "gui/icons/eraser.svg"
        self.white_balance_icon_path = "gui/icons/white_balance.svg"
        self.image_colorizer_icon_path = "gui/icons/colorizer.svg"
        self.blur_background_icon_path = "gui/icons/portrait_mode.svg"
        self.greyscale_background_icon_path = "gui/icons/grayscale_background.svg"
        self.background_removal_icon_path = "gui/icons/background_removal.svg"
        self.horizontal_flip_img_icon_path = "gui/icons/flip_left_right.svg"
        self.vertical_flip_img_icon_path = "gui/icons/flip_top_bottom.svg"
        self.panorama_icon_path = "gui/icons/panorama.svg"
        self.rotate_left_icon_path = "gui/icons/rotate_left.svg"
        self.rotate_right_icon_path = "gui/icons/rotate_right.svg"
        self.crop_tool_icon_path = "gui/icons/crop.svg"
        self.path_select_icon_path = "gui/icons/select_path.svg"
        self.rect_select_icon_path = "gui/icons/select_rect.svg"
        self.paintbrush_icon_path = "gui/icons/paint.svg"
        self.eye_drop_icon_path = "gui/icons/color_picker.svg"
        self.cursor_icon_path = "gui/icons/cursor.svg"

        # create image editing buttons as QToolButtons for the toolbox
        self.cursor_tool_btn = self.create_toolbox_buttons(
            self.cursor_icon_path, "", "Cursor"
        )
        self.eyedropper_btn = self.create_toolbox_buttons(
            self.eye_drop_icon_path, "", "Eye Dropper"
        )
        self.paintbrush_btn = self.create_toolbox_buttons(
            self.paintbrush_icon_path, "", "Paint Brush"
        )
        self.rect_select_btn = self.create_toolbox_buttons(
            self.rect_select_icon_path, "", "Rectangle Tool"
        )
        self.path_select_btn = self.create_toolbox_buttons(
            self.path_select_icon_path, "", "Path Tool"
        )
        self.crop_image_btn = self.create_toolbox_buttons(
            self.crop_tool_icon_path, "", "Crop"
        )
        self.rotate_img_left_btn = self.create_toolbox_buttons(
            self.rotate_left_icon_path,
            "",
            "Rotate Image Left",
        )
        self.rotate_img_right_btn = self.create_toolbox_buttons(
            self.rotate_right_icon_path,
            "",
            "Rotate Image Left",
        )
        self.horizontal_flip_img_btn = self.create_toolbox_buttons(
            self.horizontal_flip_img_icon_path,
            "",
            "Horizontal Image Flip",
        )
        self.vertical_flip_img_btn = self.create_toolbox_buttons(
            self.vertical_flip_img_icon_path,
            "",
            "Vertical Image Flip",
        )
        self.panorama_btn = self.create_toolbox_buttons(
            self.panorama_icon_path, "", "Apply Panorama"
        )
        self.background_removal_btn = self.create_toolbox_buttons(
            self.background_removal_icon_path,
            "",
            "Remove Background",
        )
        self.greyscale_background_btn = self.create_toolbox_buttons(
            self.greyscale_background_icon_path,
            "",
            "Greyscale Background",
        )
        self.blur_background_btn = self.create_toolbox_buttons(
            self.blur_background_icon_path,
            "",
            "Background Blur",
        )
        self.image_colorizer_btn = self.create_toolbox_buttons(
            self.image_colorizer_icon_path,
            "",
            "Colorizer",
        )
        self.white_balance_btn = self.create_toolbox_buttons(
            self.white_balance_icon_path,
            "",
            "White Balance",
        )
        self.eraser_btn = self.create_toolbox_buttons(
            self.eraser_icon_path, "", "Eraser"
        )
        self.instagram_filters_btn = self.create_toolbox_buttons(
            self.instagram_filter_icon_path,
            "",
            "Instagram Filters",
        )

        # create image editing buttons as QActions for the toolbox
        self.cursor_tool_action = self.create_toolbox_actions(
            self, self.cursor_icon_path, "Cursor", "Cursor"
        )
        self.eyedropper_action = self.create_toolbox_actions(
            self, self.eye_drop_icon_path, "Eyedropper", "Eye Dropper"
        )
        self.paintbrush_action = self.create_toolbox_actions(
            self, self.paintbrush_icon_path, "Paint Brush", "Paint Brush"
        )
        self.rect_select_action = self.create_toolbox_actions(
            self, self.rect_select_icon_path, "Rectangle Tool", "Rectangle Tool"
        )
        self.path_select_action = self.create_toolbox_actions(
            self, self.path_select_icon_path, "Path Tool", "Path Tool"
        )
        self.crop_image_action = self.create_toolbox_actions(
            self, self.crop_tool_icon_path, "Crop", "Crop"
        )
        self.rotate_img_left_action = self.create_toolbox_actions(
            self,
            self.rotate_left_icon_path,
            "Rotate Left",
            "Rotate Image Left",
        )
        self.rotate_img_right_action = self.create_toolbox_actions(
            self,
            self.rotate_right_icon_path,
            "Rotate Right",
            "Rotate Image Left",
        )
        self.horizontal_flip_img_action = self.create_toolbox_actions(
            self,
            self.horizontal_flip_img_icon_path,
            "",
            "Horizontal Image Flip",
        )
        self.vertical_flip_img_action = self.create_toolbox_actions(
            self,
            self.vertical_flip_img_icon_path,
            "",
            "Vertical Image Flip",
        )
        self.panorama_action = self.create_toolbox_actions(
            self, self.panorama_icon_path, "", "Apply Panorama"
        )
        self.background_removal_action = self.create_toolbox_actions(
            self,
            self.background_removal_icon_path,
            "Remove Background",
            "Remove Background",
        )
        self.greyscale_background_action = self.create_toolbox_actions(
            self,
            self.greyscale_background_icon_path,
            "",
            "Greyscale Background",
        )
        self.blur_background_action = self.create_toolbox_actions(
            self,
            self.blur_background_icon_path,
            "Blur Background",
            "Background Blur",
        )
        self.image_colorizer_action = self.create_toolbox_actions(
            self,
            self.image_colorizer_icon_path,
            "",
            "Colorizer",
        )
        self.white_balance_action = self.create_toolbox_actions(
            self,
            self.white_balance_icon_path,
            "",
            "White Balance",
        )
        self.eraser_action = self.create_toolbox_actions(
            self, self.eraser_icon_path, "", "Eraser"
        )
        self.instagram_filters_action = self.create_toolbox_actions(
            self,
            self.instagram_filter_icon_path,
            "",
            "Instagram Filters",
        )

    @staticmethod
    def add_actions_to_widget(widget: QObject, actions_list: list) -> None:
        """
        Loops through a list of QActions and add to a widget
        :param widget:
        :param actions_list:
        :return:
        """
        for _, action in enumerate(actions_list):
            widget.addAction(action)

    @staticmethod
    def add_buttons_to_widget(widget: QObject, buttons_list: list) -> None:
        """
        Loops through a list of buttons and add it to a widget
        :param widget:
        :param buttons_list:
        :return:
        """
        for _, button in enumerate(buttons_list):
            widget.addWidget(button)

    @staticmethod
    def set_icon_color(
        icon_path: str, replace_color="black", new_color="white"
    ) -> QPixmap:
        """
        Sets the icon color of the button
        :param icon_path: the filename of the icon to set
        :param replace_color: the color that the icon should be replaced with
        :param new_color: the color that the icon should be set to
        """
        pixmap = QPixmap(icon_path)
        mask = pixmap.createMaskFromColor(
            QtGui.QColor(replace_color), Qt.MaskMode.MaskOutColor
        )
        pixmap.fill((QtGui.QColor(new_color)))
        pixmap.setMask(mask)
        return pixmap

    def create_toolbox_actions(
        self, parent, icon_path: str, icon_txt: str = "", icon_tool_tip: str = ""
    ) -> QAction:
        """
        A function that helps create a QAction instead of repeating the same
        code over and over just to make the toolbar buttons.
        :param icon_txt: the text to show in the icon
        :param icon_tool_tip: the tool tip to show on the icon
        :param icon_path: the path to the icon
        :param parent: self
        """
        create_action_pixmap = self.set_icon_color(icon_path)
        create_action = QAction(create_action_pixmap, icon_txt, parent)
        create_action.setToolTip(icon_tool_tip)
        # create_action.setCheckable(True)
        # create_action.setEnabled(False)
        return create_action

    def create_toolbox_buttons(
        self, icon_path: str, icon_txt: str = "", icon_tool_tip: str = ""
    ) -> QPushButton:
        """
        A function that helps create a QAction instead of repeating the same
        code over and over just to make the toolbar buttons.
        :param icon_txt: the text to show in the icon
        :param icon_tool_tip: the tool tip to show on the icon
        :param icon_path: the path to the icon
        """
        pixmap = self.set_icon_color(icon_path)
        create_button = QPushButton()
        create_button.setIcon(pixmap)
        create_button.setText(icon_txt)
        create_button.setToolTip(icon_tool_tip)
        create_button.setCheckable(True)
        return create_button
