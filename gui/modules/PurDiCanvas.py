import os

import PIL.ImageQt
import numpy as np
import qimage2ndarray
import torch
from PIL.Image import Image
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (
    Signal,
    QPointF,
    QRectF,
    QEvent,
    qWarning,
    Slot,
    QRect,
)
from PySide6.QtGui import (
    Qt,
    QPixmap,
    QImage,
    QCursor,
    QColor,
    QUndoCommand,
    QMouseEvent,
    QStandardItemModel,
    QPainter,
    QPen,
    QActionGroup,
)
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsItem,
    QSizePolicy,
    QMenu,
    QApplication,
    QGraphicsRectItem,
)

from gui.modules.PurDiToolBoxWidget import PurDiToolBoxWidget
from gui.purDi_Actions import PurDiActions, create_actions


class UndoRedoItemMoved(QUndoCommand):
    def __init__(self, old_positions, new_positions):
        super().__init__()
        self.old_positions = old_positions
        self.new_positions = new_positions

    def redo(self):
        for item, pos in self.new_positions.items():
            x, y = QPointF.x(pos), QPointF.y(pos)
            item.setPos(QPointF(x, y))

    def undo(self):
        for item, pos in self.old_positions.items():
            x, y = QPointF.x(pos), QPointF.y(pos)
            item.setPos(QPointF(x, y))


class PurDiGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.setShapeMode(QGraphicsPixmapItem.HeuristicMaskShape)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            enabled=True,
        )

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        super().contextMenuEvent(event)


class PurDiCanvasScene(QGraphicsScene):
    items_moved = Signal(object, object)
    zoom = Signal()

    def __init__(self, view_rect):
        super().__init__()
        self.old_positions = {}
        self._center_view_pos = view_rect
        self.image_latent_currently_decoding = []

        # Fix scene not updating latent images as they are added
        # to the scene (animation/live preview)
        self.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)

        # out-paint
        self._start = QPointF()
        self._mask_rect: QGraphicsRectItem = QGraphicsRectItem()
        self._mask_image_bounding_rect: QGraphicsRectItem = QGraphicsRectItem()
        self.drawing_mask_rect: bool = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_positions = {index: index.pos() for index in self.selectedItems()}

        key_modifiers = QApplication.keyboardModifiers()
        shift = Qt.KeyboardModifier.ShiftModifier
        if (
            self.itemAt(event.scenePos(), QtGui.QTransform()) is None
            and key_modifiers & Qt.KeyboardModifier.ShiftModifier == shift
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self.drawing_mask_rect = True
            self._mask_rect = QGraphicsRectItem()

            rect_pen = QPen()
            rect_pen.setStyle(Qt.PenStyle.NoPen)
            rect_pen.setColor(Qt.GlobalColor.white)
            self._mask_rect.setPen(rect_pen)
            self._mask_rect.setBrush(QColor(92, 212, 193, 125))
            self._mask_rect.setFlag(
                QGraphicsItem.GraphicsItemFlag.ItemIsMovable
                | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
                True,
            )
            self.addItem(self._mask_rect)

            self._start = event.scenePos()
            mask_size = QRectF(self._start, self._start)
            self._mask_rect.setRect(mask_size)
        super(PurDiCanvasScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self._mask_rect is not None and self.drawing_mask_rect:
            mask_size = QRectF(self._start, event.scenePos()).normalized()

            self._mask_rect.setRect(mask_size)

        super(PurDiCanvasScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.old_positions:
            self.items_moved.emit(
                self.old_positions,
                {index: index.pos() for index in self.old_positions.keys()},
            )
        self.old_positions = {}

        if self.drawing_mask_rect:
            image = self._mask_rect.collidingItems(
                Qt.ItemSelectionMode.IntersectsItemShape
            )
            print(f"items: {image}")

        self._mask_rect = None
        self.drawing_mask_rect = False
        super(PurDiCanvasScene, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete and self.selectedItems():
            [self.removeItem(image) for image in self.selectedItems()]
            event.accept()
        elif event.key() == Qt.Key.Key_Escape and self.selectedItems():
            self.clearSelection()
            event.accept()
        else:
            event.ignore()
            super().keyPressEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def show_image(
        self,
        image: QImage | QPixmap | QGraphicsRectItem | Image | torch.Tensor | np.ndarray,
        url: str = None,
        pos: QPointF = None,
        is_latent: bool = False,
    ) -> None:
        """
        Set the scene's current image pixmap to the input QImage or QPixmap.
        Raises a RuntimeError if the input image has type other than QImage or QPixmap.
        :type image: QImage | QPixmap | Image | torch.Tensor
        :param url:
        :param pos:
        :param is_latent: True if the image being rendered is image latent from a diffuser pipeline
        """
        pixmap = None

        if isinstance(image, QPixmap):
            pixmap = image
        elif isinstance(image, QImage):
            pixmap = QPixmap.fromImage(image)
        elif isinstance(image, Image):
            from PIL.ImageQt import ImageQt

            img = ImageQt(image)
            pixmap = QPixmap(img)
        elif isinstance(image, torch.Tensor):
            from PIL.ImageQt import ImageQt
            from torchvision import transforms

            convert = transforms.ToPILImage()
            img = convert(image[0])
            q_img = ImageQt(img)
            pixmap = QPixmap(q_img)
        elif isinstance(image, np.ndarray):
            try:
                qimage = qimage2ndarray.array2qimage(image, True)
                pixmap = QPixmap.fromImage(qimage)
            except ImportError:
                qWarning(b"qimage2ndarray module not found")
        else:
            print("input image must be a QImage, QPixmap, or numpy.ndarray.")

        if pixmap and not pixmap.isNull():
            self.zoom.emit()
            item = PurDiGraphicsPixmapItem(pixmap)
            if isinstance(url, str) and url is not None:
                item.setData(Qt.ItemDataRole.DisplayRole, url)
            if pos is not None:
                item.setPos(pos)
            else:
                item_width_offset = round(item.boundingRect().width() / 4)
                item_height_offset = round(item.boundingRect().height() / 4)
                item.setPos(
                    self._center_view_pos - item_width_offset,
                    self._center_view_pos - item_height_offset,
                )
                item.moveBy(
                    self._center_view_pos - item_width_offset,
                    self._center_view_pos - item_height_offset,
                )

            if is_latent:
                # item.setFlag(
                #     QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
                #     | QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
                #     enabled=False,
                # )
                self.image_latent_currently_decoding.append(item)

            self.addItem(item)

    @Slot()
    def delete_latents_from_scene(self):
        for image in self.image_latent_currently_decoding:
            try:
                self.removeItem(image)
            except ValueError:
                print(f"Skipping {image} because it was already removed.")


class PurDiCanvasView(QGraphicsView):
    mouse_left_button_pressed = Signal(float, float)
    mouse_left_button_released = Signal(float, float)
    mouse_middle_button_pressed = Signal(float, float)
    mouse_middle_button_released = Signal(float, float)
    mouse_right_button_pressed = Signal(float, float)
    mouse_right_button_released = Signal(float, float)
    mouse_left_button_double_clicked = Signal(float, float)

    rectChanged = Signal(QRect)
    image_processed = Signal()

    def __init__(self, parent=None):
        super(PurDiCanvasView, self).__init__(parent)
        self.parent = parent

        self._max_canvas_size = 25000
        self._center_canvas_pos = self._max_canvas_size / 2
        self.setSceneRect(
            QRectF(
                self._center_canvas_pos,
                self._center_canvas_pos,
                self._max_canvas_size,
                self._max_canvas_size,
            )
        )  # x, y, w, h

        self.scene = PurDiCanvasScene(view_rect=self._center_canvas_pos)
        self.setScene(self.scene)

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.setRenderHint(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.LosslessImageRendering,
            enabled=True,
        )
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # mouse input
        self.mouse_left_btn = Qt.MouseButton.LeftButton
        self.mouse_middle_btn = Qt.MouseButton.MiddleButton
        self.mouse_right_btn = Qt.MouseButton.RightButton
        self.dummy_modifiers = Qt.KeyboardModifier(
            Qt.KeyboardModifier.ShiftModifier
            # | Qt.KeyboardModifier.ControlModifier
            # | Qt.KeyboardModifier.AltModifier
            # | Qt.KeyboardModifier.MetaModifier
        )
        self._is_panning = False

        # zoom in/out properties
        self._initial_zoom_times: int = 20
        self.zoom_times = self._initial_zoom_times
        self.zoom_in_factor: float = 1.15
        self.zoom_out_factor: float = 1.0 / self.zoom_in_factor

        # Track mouse position. e.g., For displaying coordinates in a UI.
        self.setMouseTracking(True)

        self.scene.zoom.connect(self.reset_zoom)
        self.setUpdatesEnabled(True)

        # context menu
        self.bg_remove_mask_only = True
        self.bg_remove_model = "u2net"
        self.colorizer_icon = os.path.abspath("gui/icons/colorizer.svg")
        self.remove_bg_icon = os.path.abspath("gui/icons/background_removal.svg")
        self.colorizer_action = create_actions(
            parent=self,
            icon_path=self.colorizer_icon,
            icon_txt="Colorizer",
            icon_tool_tip="Re-color image",
        )
        self.remove_bg_action = create_actions(
            parent=self,
            icon_path=self.remove_bg_icon,
            icon_txt="Remove Background",
            icon_tool_tip="A background removal network",
        )
        self.mask_person_action = create_actions(
            parent=self,
            icon_path=self.remove_bg_icon,
            icon_txt="Mask Person",
            icon_tool_tip="Mask person for inpainting",
        )
        self.mask_bg_action = create_actions(
            parent=self,
            icon_path=self.remove_bg_icon,
            icon_txt="Mask Background",
            icon_tool_tip="Mask background for inpainting",
        )
        self.mask_clothing_action = create_actions(
            parent=self,
            icon_path=self.remove_bg_icon,
            icon_txt="Mask Clothing",
            icon_tool_tip="Mask clothing for inpainting",
        )
        self.canvas_context_menu_action_group = QActionGroup(self)
        self.remove_bg_action.setActionGroup(self.canvas_context_menu_action_group)
        self.mask_bg_action.setActionGroup(self.canvas_context_menu_action_group)
        self.mask_clothing_action.setActionGroup(self.canvas_context_menu_action_group)
        self.mask_person_action.setActionGroup(self.canvas_context_menu_action_group)

        self.colorizer_action.triggered.connect(self.run_colorizer)
        self.remove_bg_action.triggered.connect(self.run_bg_removal)
        self.mask_bg_action.triggered.connect(self.run_bg_removal)
        self.mask_clothing_action.triggered.connect(self.run_bg_removal)
        self.mask_person_action.triggered.connect(self.run_bg_removal)

        # self.inpainting = False
        # self.previous_pos = None
        # self.painter = QPainter()
        # self.pen = QPen()
        # self.pen.setWidth(10)
        # self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        # self.image_for_inpaint = None
        # self.pixmap = QPixmap()

    def fake_left_mouse_button_for_scrolling(self, event):
        """ScrollHandDrag ONLY works with LeftButton, so fake it.
        Use a bunch of dummy modifiers to notify that event should NOT be handled as usual.
        :param event:
        :return:
        """
        dummy_event = QMouseEvent(
            QEvent.Type.MouseButtonPress,
            QPointF(event.pos()),
            Qt.MouseButton.LeftButton,
            event.buttons(),
            self.dummy_modifiers,
        )
        return dummy_event

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        # TODO: make qpainter work for manual inpainting....
        # if self.inpainting:
        #     with QPainter(self) as painter:
        #         self.image_for_inpaint = self.scene.selectedItems()[0].boundingRect().toRect()
        #
        #         pos = self.scene.selectedItems()[0].scenePos()
        #         image_width = self.image_for_inpaint.width()
        #         image_height = self.image_for_inpaint.height()
        #
        #         self.pixmap = QPixmap(QSize(image_width, image_height))
        #
        #         painter.drawPixmap(pos.x(), pos.y(), self.pixmap)

        QGraphicsView.paintEvent(self, event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if (
            self.mouse_middle_btn is not None
            and event.button() == self.mouse_middle_btn
        ):
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            if self.mouse_middle_btn == Qt.MouseButton.LeftButton:
                QGraphicsView.mousePressEvent(self, event)
            else:
                self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
                dummy_event = self.fake_left_mouse_button_for_scrolling(event)
                self.mousePressEvent(dummy_event)
            event.accept()
            self._is_panning = True

        # TODO: finish implementing out-painting
        key_modifiers = QApplication.keyboardModifiers()
        shift = Qt.KeyboardModifier.ShiftModifier

        # elif key_modifiers & Qt.KeyboardModifier.ShiftModifier == shift:
        #     if event.button() == self.mouse_left_btn:
        #         self.drawing_mask_rect = True
        #         self.cursor_start_position = event.pos()
        #         # self.mask_rect.setGeometry(
        #         #     QRect(self.cursor_start_position, QSize()).normalized()
        #         # )
        #
        #         # self.mask_rec_select.show()
        #         # self.rectChanged.emit(self.mask_rect.geometry())

        # if self.inpainting:
        #     self.previous_pos = event.position().toPoint()

        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        # TODO: make qpainter work for manual inpainting....
        # if self.inpainting:
        #     current_pos = event.position().toPoint()
        #     self.painter.begin(self.scene.selectedItems()[0])
        #     self.painter.setRenderHints(QPainter.Antialiasing, True)
        #     self.painter.setPen(self.pen)
        #     self.painter.drawLine(self.previous_pos, current_pos)
        #     self.painter.end()
        #
        #     self.previous_pos = current_pos
        #     self.update()

        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

        if (
            self.mouse_middle_btn is not None
            and event.button() == self.mouse_middle_btn
        ):
            if self.mouse_middle_btn == Qt.MouseButton.LeftButton:
                QGraphicsView.mouseReleaseEvent(self, event)
            else:
                self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
                dummy_event = self.fake_left_mouse_button_for_scrolling(event)
                self.mouseReleaseEvent(dummy_event)
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            event.accept()
            self._is_panning = False

        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if (
            event.button() == self.mouse_left_btn
            and len(self.scene.selectedItems()) == 1
        ):
            self.fitInView(self.itemAt(event.pos()), Qt.AspectRatioMode.KeepAspectRatio)
            # TODO: disable image movement for inpainting
            # self.scene.selectedItems()[0].setFlag(
            #     QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            #     QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            #     enabled=False,
            # )
            # self.parent.inpainting = True

        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """
        Shows default PurDiGraphicsView context menu if no images are selected.
        Else if image(s) are selected it has its own context menu to show.
        :param event:
        :return:
        """
        try:
            menu = QMenu(self)
            tool_actions = PurDiToolBoxWidget(self)
        except ModuleNotFoundError:
            print(f"Unable to create QMenu() or PurDiToolBoxWidget()")
        else:
            if len(self.scene.selectedItems()) == 0:
                menu.exec(event.globalPos())
                event.accept()
            else:
                edit_menu = menu.addMenu("Edit")
                extract_menu = menu.addMenu("Extract")

                edit_menu.addAction(self.colorizer_action)

                extract_menu.addAction(self.mask_bg_action)
                extract_menu.addAction(self.mask_clothing_action)
                extract_menu.addAction(self.mask_person_action)
                extract_menu.addSeparator()
                extract_menu.addAction(self.remove_bg_action)

                menu.addSeparator()
                menu.addAction(tool_actions.pa.horizontal_flip_img_action)
                menu.addAction(tool_actions.pa.vertical_flip_img_action)

                menu.exec(event.globalPos())
                event.accept()
        finally:
            super().contextMenuEvent(event)
            event.ignore()

    @Slot()
    def run_bg_removal(self):
        """
        Powered by U2Net for image segmentation tasks like background removal
        or clothing extraction/masking for other diffuser pipelines like inpainting
        """

        # TODO: Move into a QRunnable to prevent UI freezes when loading model
        from scripts.rembg.session_factory import new_session
        from scripts.FileUtils import u2net_clothes_split_mask
        from scripts.rembg.bg import remove
        from PIL import ImageChops, ImageQt

        pixmap = self.scene.selectedItems()[0].pixmap()
        full_path = self.scene.selectedItems()[0].data(Qt.ItemDataRole.DisplayRole)
        path, img_name = os.path.split(full_path)
        # img_name = img_name[:-4]

        if self.remove_bg_action.isChecked():
            self.bg_remove_model = "u2net"
            self.bg_remove_mask_only = False
        elif self.mask_bg_action.isChecked():
            self.bg_remove_model = "u2net"
            self.bg_remove_mask_only = True
        elif self.mask_person_action.isChecked():
            self.bg_remove_model = "u2net_human_seg"
            self.bg_remove_mask_only = True
        elif self.mask_clothing_action.isChecked():
            self.bg_remove_model = "u2net_cloth_seg"
            self.bg_remove_mask_only = True

        # TODO: remove - for debug only
        print(self.bg_remove_model)
        print(self.bg_remove_mask_only)

        image = ImageQt.fromqpixmap(pixmap)
        session = new_session(model_name=self.bg_remove_model)

        results = remove(
            data=image,
            alpha_matting=False,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10,
            session=session,
            only_mask=self.bg_remove_mask_only,
            post_process_mask=True,
        )

        if self.mask_clothing_action.isChecked():
            results = u2net_clothes_split_mask(image=results, w_split=1, h_split=3)
        else:
            results = [results]

        for index, mask in enumerate(results):
            if (
                self.bg_remove_mask_only
                and not self.mask_bg_action.isChecked()
                and not self.mask_clothing_action.isChecked()
            ):
                mask = mask.convert("RGB")
                mask = PIL.ImageChops.invert(mask)

            # self.scene.show_image(mask)
            file_name = os.path.join(
                path, f"{img_name[:50]}_{self.bg_remove_model}_{index}.png"
            )
            mask.save(file_name)

        self.image_processed.emit()

    @Slot()
    def run_colorizer(self):
        """
        A CNN to change an image's color. Eventually move it out of a
        pop-up dock widget and into the main UI. For now, quick and dirty
        implementation.
        """

        # TODO: Move into a QRunnable to prevent UI freezes when loading model
        # TODO: move into purDi_app
        import os
        from timm.models import create_model
        from scripts.iColoriT import gui_main

        # TODO: If colorizer breaks, needs modeling module
        import scripts.iColoriT.modeling

        import warnings

        warnings.filterwarnings("ignore", category=UserWarning)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_name = "icolorit_base_4ch_patch16_224"
        model_dir = os.path.join(os.path.abspath("models"), f"{model_name}.pth")

        img = self.scene.selectedItems()[0]
        if isinstance(img, QGraphicsItem):
            try:
                model = create_model(
                    model_name=model_name,
                    checkpoint_path=model_dir,
                    pretrained=False,
                    drop_path_rate=0.0,
                    drop_block_rate=None,
                    use_rpb=True,
                    avg_hint=True,
                    head_mode="cnn",
                    mask_cent=False,
                )
                model.to(device)
                checkpoint = torch.load(model_dir, map_location=torch.device(device))
                model.load_state_dict(checkpoint["model"], strict=False)
                model.eval()
            except ValueError:
                pass
            else:
                img = img.data(Qt.ItemDataRole.DisplayRole)
                popup = gui_main.IColorDockWidget(
                    color_model=model,
                    img_file=img,
                    load_size=224,
                    win_size=600,
                    device=device,
                    parent=self,
                )
                popup.show()

                # TODO: delete model....

    @Slot()
    def reset_zoom(self):
        if self.zoom_times == self._initial_zoom_times:
            return
        self.zoom_times = self._initial_zoom_times

    def wheelEvent(self, event):
        try:
            pos = self.mapToScene(QCursor.pos())
        except ValueError:
            print("Unable to map scene to QCursor.pos()")
        else:
            if event.angleDelta().y() > 0:
                self.scale(self.zoom_in_factor, self.zoom_in_factor)
                self.translate(pos.x(), pos.y())
                event.accept()
            elif event.angleDelta().y() < 0:
                self.scale(self.zoom_out_factor, self.zoom_out_factor)
                self.translate(pos.x(), pos.y())
                event.accept()
        finally:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            super().dragEnterEvent(event)
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            super().dragMoveEvent(event)
            event.ignore()

    def dropEvent(self, event):
        event.setDropAction(Qt.DropAction.CopyAction)
        scene_pos = self.mapToScene(event.pos())
        pixmap_list = []
        try:
            image_model = QStandardItemModel()
            image_model.dropMimeData(
                event.mimeData(), event.dropAction(), 0, 0, QtCore.QModelIndex()
            )
            for row in range(image_model.rowCount()):
                url = image_model.item(row, 0).text()
                pixmap_list.append(url)

        except ValueError:
            print("Unable to map event to scene")
        else:
            if event.mimeData().hasUrls():
                for index, url in enumerate(event.mimeData().urls()):
                    image = url.toLocalFile()
                    pixmap_list.append(image)
        finally:
            for index, url in enumerate(pixmap_list):
                self.scene.show_image(image=QPixmap(url), url=url, pos=scene_pos)
                event.accept()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)

    # def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
    #     if event.key() == Qt.Key.Key_Delete and self.scene.selectedItems():
    #         [self.scene.removeItem(image) for image in self.scene.selectedItems()]
    #         event.accept()
    #     elif event.key() == Qt.Key.Key_Escape and self.scene.selectedItems():
    #         self.scene.clearSelection()
    #         event.accept()
    #     else:
    #         event.ignore()
    #         super().keyPressEvent(event)
