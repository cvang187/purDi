from PySide6 import QtGui
from PySide6.QtGui import QPixmap


def q_pixmap_to_image(pixmap):
    from PIL import Image

    width = pixmap.width()
    height = pixmap.height()
    image = pixmap.toImage()

    byte_count = image.bytesPerLine() * height
    data = image.constBits().asstring(byte_count)
    return Image.frombuffer("RGBA", (width, height), data, "raw", "BGRA", 0, 1)


def q_image_to_image(qimage):
    from PIL import Image

    width = qimage.width()
    height = qimage.height()
    image = qimage

    byte_count = image.bytesPerLine() * height
    data = image.constBits().asstring(byte_count)
    return Image.frombuffer("RGBA", (width, height), data, "raw", "BGRA", 0, 1)


def image_to_q_pixmap(image):
    from PIL.ImageQt import ImageQt

    return QPixmap.fromImage(ImageQt(image))


def q_image_to_cv_mat_format(in_image):
    """Converts a QImage into an opencv MAT format"""
    import numpy as np

    in_image = in_image.convertToFormat(QtGui.QImage.Format.Format_RGBA8888)

    width = in_image.width()
    height = in_image.height()

    ptr = in_image.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr


def image_to_qt_pixmap(image):
    from PIL.ImageQt import ImageQt

    return QPixmap.fromImage(ImageQt(image))


def working_directory(local_path: str) -> str:
    """
    Helper function that gets the absolute path to wherever the calling parent is from.
    :param local_path:
    :return:
    """
    import os

    absolute_path = os.path.dirname(__file__)
    working_path = local_path
    return os.path.join(absolute_path, working_path)
