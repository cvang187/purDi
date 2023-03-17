from typing import Union

import numpy as np
import qimage2ndarray
import torch
from PIL.Image import Image
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Signal, QPointF, QPoint, QRectF, QEvent, qWarning, Slot, QRect, QSize
from PySide6.QtGui import (
    Qt,
    QPixmap,
    QImage,
    QCursor,
    QBrush,
    QColor,
    QUndoCommand,
    QMouseEvent,
    QStandardItemModel, QPainter, QPainterPath,
)
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsItem,
    QSizePolicy,
    QMenu, QRubberBand, QApplication,
)

from gui.modules.PurDiToolBoxWidget import PurDiToolBoxWidget
from gui.purDi_Actions import PurDiActions


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


class PurDiGraphicsItem(QGraphicsPixmapItem):
    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent) -> None:
        super().contextMenuEvent(event)


class PurDiCanvasScene(QGraphicsScene):
    items_moved = Signal(object, object)
    zoom = Signal()

    def __init__(self, view_rect):
        super().__init__()
        self.setBackgroundBrush(QBrush(QColor(50, 50, 50)))
        self.old_positions = {}
        self.image_latent_currently_decoding = []
        self._center_view_pos = view_rect

        # Fix scene not updating latent images as they are added to the scene (animation/live preview)
        self.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)

    def drawBackground(
        self, painter: QtGui.QPainter, rect: Union[QtCore.QRectF, QtCore.QRect]
    ) -> None:
        pass

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_positions = {idx: idx.pos() for idx in self.selectedItems()}

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self.old_positions:
            self.items_moved.emit(
                self.old_positions,
                {index: index.pos() for index in self.old_positions.keys()},
            )
        self.old_positions = {}

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

    def show_image(
        self,
        image: QImage | QPixmap | Image | torch.Tensor | np.ndarray,
        pos: QPointF = None,
        is_latent: bool = False
    ) -> None:
        """
        Set the scene's current image pixmap to the input QImage or QPixmap.
        Raises a RuntimeError if the input image has type other than QImage or QPixmap.
        :type image: QImage | QPixmap | Image | torch.Tensor
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
            item = PurDiGraphicsItem(pixmap)
            item.setShapeMode(QGraphicsPixmapItem.HeuristicMaskShape)
            # item.setFlag(
            #     QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            #     | QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            # )
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

            if pos is not None:
                item.setPos(pos)
            else:
                width = round(item.boundingRect().width() / 4)
                height = round(item.boundingRect().height() / 4)
                item.setPos(
                    self._center_view_pos - width,
                    self._center_view_pos - height
                )
                item.moveBy(
                    self._center_view_pos - width,
                    self._center_view_pos - height
                )

            if is_latent:
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

    def __init__(self, parent=None):
        super(PurDiCanvasView, self).__init__()
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
        # self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.setRenderHint(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform |
            QPainter.RenderHint.LosslessImageRendering,
            enabled=True
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
        self._is_left_mouse_button_pressed = False
        self._is_select_tool = False
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

        self.mask_rect = QPainter()
        self.mask_rect.setPen(QColor.fromRgb(0, 0, 0, 0))
        self.mask_rect.setBrush(Qt.BrushStyle.CrossPattern)
        # self.mask_rec_select: QRubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.mask_rect_size: QRect = QRect(0, 0, 0, 0)
        self.cursor_start_position: QPoint = QPoint()
        self.cursor_end_position: QPoint = QPoint()
        self.drawing_mask_rect: bool = False

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

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        key_modifiers = QApplication.keyboardModifiers()
        shift = Qt.KeyboardModifier.ShiftModifier

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

        elif key_modifiers & Qt.KeyboardModifier.ShiftModifier == shift:
            if event.button() == self.mouse_left_btn:
                self.drawing_mask_rect = True
                self.cursor_start_position = event.pos()
                # self.mask_rect.setGeometry(
                #     QRect(self.cursor_start_position, QSize()).normalized()
                # )

                # self.mask_rec_select.show()
                # self.rectChanged.emit(self.mask_rect.geometry())

        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.drawing_mask_rect:
            # self.mask_rect.setGeometry(
            #     QRect(self.cursor_start_position, self.cursor_end_position).normalized()
            # )

            # self.cursor_end_position = event.pos()
            # w = self.cursor_start_position.x() - self.cursor_end_position.x()
            # h = self.cursor_start_position.y() - self.cursor_start_position.y()
            # self.mask_rect.setGeometry(
            #     QRect(self.cursor_start_position, QSize(w, h)).normalized()
            # )
            self.rectChanged.emit(self.mask_rect_size)
            # self.rectChanged.emit(self.mask_rect.geometry())

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

        elif event.button() == self.mouse_left_btn and self.drawing_mask_rect:
            self.cursor_end_position = event.pos()

            start_x = self.cursor_start_position.x()
            start_y = self.cursor_start_position.y()
            end_x = self.cursor_end_position.x()
            end_y = self.cursor_end_position.y()
            self.mask_rect_size = QRect(
                QPoint(start_x, start_y), QSize(end_x - start_x, end_y - start_y)
            )

            self.mask_rect.drawRect(self.mask_rect_size)
            self.drawing_mask_rect = False

            print(f"Image Mask Size: {self.mask_rect_size}")
            print(f"End POS: x({end_x + start_x}), y({end_y + start_y})")
            print(f"cursor_start_pos: {self.cursor_start_position}")
            print(f"cursor_end_pos: {self.cursor_end_position}\n")

        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if (
            event.button() == self.mouse_left_btn
            and len(self.scene.selectedItems()) == 1
        ):
            self.fitInView(self.itemAt(event.pos()), Qt.AspectRatioMode.KeepAspectRatio)
            return

        super().mouseDoubleClickEvent(event)

    # TODO: implement real context menu
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
                menu.addAction(tool_actions.pa.cursor_tool_action)
                menu.addAction(tool_actions.pa.image_colorizer_action)
                menu.addAction(tool_actions.pa.blur_background_action)
                menu.exec(event.globalPos())
                event.accept()
            else:
                menu.addAction(tool_actions.pa.horizontal_flip_img_action)
                menu.addAction(tool_actions.pa.vertical_flip_img_action)
                menu.exec(event.globalPos())
                event.accept()
        finally:
            super().contextMenuEvent(event)
            event.ignore()

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
                self.scene.show_image(QPixmap(url), scene_pos)
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
