import cv2
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen


class UserEdit(object):
    def __init__(self, mode, win_size, load_size, img_size):
        self.mode = mode
        self.win_size = win_size
        self.img_size = img_size
        self.load_size = load_size
        print("image_size", self.img_size)
        max_width = np.max(self.img_size)
        self.scale = float(max_width) / self.load_size  # original image to 224 ration
        self.dw = int((self.win_size - img_size[0]) // 2)
        self.dh = int((self.win_size - img_size[1]) // 2)
        self.img_w = img_size[0]
        self.img_h = img_size[1]
        self.ui_count = 0
        print(self)

    def scale_point(self, in_x, in_y, w):
        x = int((in_x - self.dw) / float(self.img_w) * self.load_size) + w
        y = int((in_y - self.dh) / float(self.img_h) * self.load_size) + w
        return x, y

    def __str__(self):
        return "add (%s) with win_size %3.3f, load_size %3.3f" % (
            self.mode,
            self.win_size,
            self.load_size,
        )


class PointEdit(UserEdit):
    def __init__(self, win_size, load_size, img_size):
        UserEdit.__init__(self, "point", win_size, load_size, img_size)
        self.width = None
        self.user_color = None
        self.color = None
        self.pnt = None

    def add(self, pnt, color, user_color, width, ui_count):
        self.pnt = pnt
        self.color = color
        self.user_color = user_color
        self.width = width
        self.ui_count = ui_count

    def select_old(self, pnt, ui_count):
        self.pnt = pnt
        self.ui_count = ui_count
        return self.user_color, self.width

    def update_color(self, color, user_color):
        self.color = color
        self.user_color = user_color

    def update_input(self, im, mask, vis_im):
        w = int(self.width / self.scale)
        point = self.pnt
        x1, y1 = self.scale_point(point.x(), point.y(), -w)
        tl = (x1, y1)

        # x2, y2 = self.scale_point(point.x(), point.y(), w)
        # br = (x2, y2)

        br = (x1 + 1, y1 + 1)  # hint size fixed to 2
        c = (self.color.red(), self.color.green(), self.color.blue())
        uc = (self.user_color.red(), self.user_color.green(), self.user_color.blue())
        cv2.rectangle(mask, tl, br, 255, -1)
        cv2.rectangle(im, tl, br, c, -1)
        cv2.rectangle(vis_im, tl, br, uc, -1)

    def is_same(self, pnt):
        dx = abs(self.pnt.x() - pnt.x())
        dy = abs(self.pnt.y() - pnt.y())
        return dx <= self.width + 1 and dy <= self.width + 1

    def update_painter(self, painter):
        w = max(3, self.width)
        c = self.color
        r = c.red()
        g = c.green()
        b = c.blue()
        ca = QColor(c.red(), c.green(), c.blue(), 255)
        d_to_black = r * r + g * g + b * b
        d_to_white = (
            (255 - r) * (255 - r) + (255 - g) * (255 - g) + (255 - r) * (255 - r)
        )
        if d_to_black > d_to_white:
            painter.setPen(QPen(Qt.black, 1))
        else:
            painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(ca)
        painter.drawRoundedRect(
            self.pnt.x() - w, self.pnt.y() - w, 1 + 2 * w, 1 + 2 * w, 2, 2
        )


class UIControl:
    def __init__(self, win_size=256, load_size=224):
        self.img_size = None
        self.win_size = win_size
        self.load_size = load_size
        self.reset()
        self.user_edit = None
        self.userEdits = []
        self.ui_count = 0

    def set_image_size(self, img_size):
        self.img_size = img_size

    def add_stroke(self, prev_point, next_point, color, user_color, width):
        pass

    def erase_point(self, pnt):
        is_erase = False
        for id, ue in enumerate(self.userEdits):
            if ue.is_same(pnt):
                self.userEdits.remove(ue)
                print("remove user edit %d\n" % id)
                is_erase = True
                break
        return is_erase

    def add_point(self, pnt, color, user_color, width):
        self.ui_count += 1
        print("process add Point")
        self.user_edit = None
        is_new = True
        for id, ue in enumerate(self.userEdits):
            if ue.is_same(pnt):
                self.user_edit = ue
                is_new = False
                print("select user edit %d\n" % id)
                break

        if self.user_edit is None:
            self.user_edit = PointEdit(self.win_size, self.load_size, self.img_size)
            self.userEdits.append(self.user_edit)
            print("add user edit %d\n" % len(self.userEdits))
            self.user_edit.add(pnt, color, user_color, width, self.ui_count)
            return user_color, width, is_new
        else:
            user_color, width = self.user_edit.select_old(pnt, self.ui_count)
            return user_color, width, is_new

    def move_point(self, pnt, color, user_color, width):
        self.user_edit.add(pnt, color, user_color, width, self.ui_count)

    def update_color(self, color, user_color):
        self.user_edit.update_color(color, user_color)

    def update_painter(self, painter):
        for ue in self.userEdits:
            if ue is not None:
                ue.update_painter(painter)

    @staticmethod
    def get_stroke_image(im):
        return im

    def used_colors(self):  # get recently used colors
        if len(self.userEdits) == 0:
            return None
        n_edits = len(self.userEdits)
        ui_counts = np.zeros(n_edits)
        ui_colors = np.zeros((n_edits, 3))
        for n, ue in enumerate(self.userEdits):
            ui_counts[n] = ue.ui_count
            c = ue.user_color
            ui_colors[n, :] = [c.red(), c.green(), c.blue()]

        ui_counts = np.array(ui_counts)
        ids = np.argsort(-ui_counts)
        ui_colors = ui_colors[ids, :]
        unique_colors = []
        for ui_color in ui_colors:
            is_exit = False
            for u_color in unique_colors:
                d = np.sum(np.abs(u_color - ui_color))
                if d < 0.1:
                    is_exit = True
                    break

            if not is_exit:
                unique_colors.append(ui_color)

        unique_colors = np.vstack(unique_colors)
        return unique_colors / 255.0

    def get_input(self):
        h = self.load_size
        w = self.load_size
        im = np.zeros((h, w, 3), np.uint8)
        mask = np.zeros((h, w, 1), np.uint8)
        vis_im = np.zeros((h, w, 3), np.uint8)

        for ue in self.userEdits:
            ue.update_input(im, mask, vis_im)

        return im, mask

    def reset(self):
        self.userEdits = []
        self.user_edit = None
        self.ui_count = 0
