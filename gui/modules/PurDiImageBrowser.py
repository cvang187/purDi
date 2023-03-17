import os

from PySide6 import QtGui
from PySide6.QtCore import Qt, QDir, QSize, Signal, qWarning, Slot
from PySide6.QtGui import QPixmap, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QAbstractItemView, QListView
from tqdm import tqdm


class PurDiImageBrowser(QListView):
    """
    Columns: pixmap, location, file_name
    """

    cache_updated = Signal(bool)

    def __init__(self, parent):
        super(PurDiImageBrowser, self).__init__()
        self.parent = parent
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.model.setSortRole(Qt.ItemDataRole.DisplayRole)
        self.max_icon_size = 100
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self._img_uri = os.path.abspath("output")
        self._img_dir = QDir(self._img_uri)
        self._cache_uri = os.path.abspath("output/.cache")
        self._cache_dir = QDir(self._cache_uri)
        self._cached = []

        # update image browser on init
        self.update_view()

    @Slot()
    def update_view(self):
        """
        Resizes images in /output/.cache to approximately 100x100 width or height.
        New resized pixmap is displayed in the main window. Otherwise, displaying
        full-sized images in a QListWidget can get very ram hungry fast.
        :return:
        """
        if not self._cache_dir.exists():
            QDir.mkdir(self._cache_dir, self._cache_uri)

        try:
            self.append_items_to_view()
        except FileNotFoundError:
            qWarning(b"Cache for image not found. Generating cache now.")
        else:
            self.generate_cache()
        finally:
            self.append_items_to_view()

    @Slot()
    def append_items_to_view(self):
        self._cache_dir.refresh()

        for index, cache in enumerate(
            self._cache_dir.entryInfoList(
                QDir.Filter.Files, QDir.SortFlag.Time.LocaleAware
            )
        ):
            if cache.fileName().replace(".png", ".jpg") not in self._cached:
                pixmap = QPixmap(cache.absoluteFilePath())

                location = QStandardItem(f"{cache.filePath().replace('.cache/', '')}")
                file_name = QStandardItem(cache.fileName())
                image = QStandardItem(cache.absoluteFilePath())
                image.appendColumn([location, file_name])

                image.setToolTip(cache.fileName())
                image.setText(
                    f"{cache.filePath().replace('.cache/', '').replace('.jpg', '.png')}"
                )
                image.setData(pixmap, Qt.ItemDataRole.DecorationRole)

                # self.model.appendRow(image)
                self.model.insertRow(0, image)

                self._cached.append(cache.fileName())

        self.setCurrentIndex(self.model.index(0, 0))
        # self.setCurrentIndex(self.model.index(
        #     self.currentIndex().row(), self.currentIndex().column()
        # ))

    def generate_cache(self):
        """
        Generates 100x100 QPixmap on the fly and saves it into output/.cache folder.
        Also converts from .png to .jpg to reduce disk storage size.
            Preferable to call update_cache() as this - generate_cache() - is a helper method
        :return:
        """

        if self._img_dir.exists() and not self._img_dir.isEmpty():
            self._img_dir.refresh()

            for index, img in enumerate(
                tqdm(
                    self._img_dir.entryInfoList(
                        QDir.Filter.Files, QDir.SortFlag.Time.LocaleAware
                    ),
                    desc=f"Generating image cache",
                )
            ):
                if img.fileName().replace(".png", ".jpg") not in self._cached:
                    pixmap = QPixmap(img.absoluteFilePath())
                    pixmap_scaled = pixmap.scaled(
                        QSize(self.max_icon_size, self.max_icon_size),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation,
                    )
                    pixmap_scaled.save(
                        os.path.join(
                            self._cache_uri, img.fileName().replace(".png", ".jpg")
                        ),
                        quality=90,
                    )
                    self._cached.append(img.fileName())

        self.cache_updated.emit(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, arg__1: QtGui.QContextMenuEvent) -> None:
        ...

    def keyboardSearch(self, search: str) -> None:
        super().keyboardSearch(search)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.clearSelection()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyReleaseEvent(event)
