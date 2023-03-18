# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QStatusBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QToolBox,
    QVBoxLayout,
    QWidget,
)

from gui.modules.PurDiDockWidget import PurDiDockWidget
from gui.modules.PurDiImageBrowser import PurDiImageBrowser
from gui.modules.PurDiPromptSuggestion import PurDiPromptSuggestion


class Ui_BasePurDi(object):
    def setupUi(self, BasePurDi):
        if not BasePurDi.objectName():
            BasePurDi.setObjectName("BasePurDi")
        BasePurDi.setWindowModality(Qt.ApplicationModal)
        BasePurDi.resize(1843, 1151)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BasePurDi.sizePolicy().hasHeightForWidth())
        BasePurDi.setSizePolicy(sizePolicy)
        BasePurDi.setMinimumSize(QSize(1280, 800))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(49, 54, 59, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(192, 191, 188, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush3)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush4 = QBrush(QColor(24, 24, 24, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush4)
        brush5 = QBrush(QColor(190, 246, 122, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush5)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush3)
        brush6 = QBrush(QColor(98, 160, 234, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Link, brush6)
        brush7 = QBrush(QColor(181, 131, 90, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush7)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush3)
        brush8 = QBrush(QColor(246, 245, 244, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush8)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
        # endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        brush9 = QBrush(QColor(159, 159, 159, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush10 = QBrush(QColor(118, 118, 118, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush3)
        brush11 = QBrush(QColor(0, 0, 255, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush11)
        brush12 = QBrush(QColor(255, 0, 255, 255))
        brush12.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush12)
        brush13 = QBrush(QColor(247, 247, 247, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush13)
        brush14 = QBrush(QColor(255, 255, 220, 255))
        brush14.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush14)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
        # endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush15 = QBrush(QColor(177, 177, 177, 255))
        brush15.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush15)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush11)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush12)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush13)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush14)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
        # endif
        BasePurDi.setPalette(palette)
        icon = QIcon()
        iconThemeName = "media-flash"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(".", QSize(), QIcon.Normal, QIcon.Off)

        BasePurDi.setWindowIcon(icon)
        BasePurDi.setWindowOpacity(1.000000000000000)
        BasePurDi.setLayoutDirection(Qt.LeftToRight)
        BasePurDi.setAutoFillBackground(False)
        BasePurDi.setStyleSheet("")
        BasePurDi.setIconSize(QSize(48, 48))
        BasePurDi.setTabShape(QTabWidget.Rounded)
        BasePurDi.setDockNestingEnabled(True)
        BasePurDi.setDockOptions(
            QMainWindow.AllowNestedDocks
            | QMainWindow.AllowTabbedDocks
            | QMainWindow.AnimatedDocks
            | QMainWindow.ForceTabbedDocks
            | QMainWindow.GroupedDragging
            | QMainWindow.VerticalTabs
        )
        BasePurDi.setUnifiedTitleAndToolBarOnMac(True)
        self.actionOpen = QAction(BasePurDi)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QAction(BasePurDi)
        self.actionSave.setObjectName("actionSave")
        self.actionSettings = QAction(BasePurDi)
        self.actionSettings.setObjectName("actionSettings")
        self.actionUndo = QAction(BasePurDi)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QAction(BasePurDi)
        self.actionRedo.setObjectName("actionRedo")
        self.actionFilters = QAction(BasePurDi)
        self.actionFilters.setObjectName("actionFilters")
        self.centralwidget = QWidget(BasePurDi)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setMaximumSize(QSize(8192, 8192))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush)
        palette1.setBrush(QPalette.Active, QPalette.Midlight, brush)
        brush16 = QBrush(QColor(127, 127, 127, 255))
        brush16.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Dark, brush16)
        brush17 = QBrush(QColor(170, 170, 170, 255))
        brush17.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Mid, brush17)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Shadow, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Highlight, brush5)
        palette1.setBrush(QPalette.Active, QPalette.HighlightedText, brush3)
        palette1.setBrush(QPalette.Active, QPalette.AlternateBase, brush)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipBase, brush14)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
        # endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush)
        brush18 = QBrush(QColor(202, 202, 202, 255))
        brush18.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Inactive, QPalette.Midlight, brush18)
        palette1.setBrush(QPalette.Inactive, QPalette.Dark, brush9)
        brush19 = QBrush(QColor(184, 184, 184, 255))
        brush19.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Inactive, QPalette.Mid, brush19)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Shadow, brush10)
        palette1.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette1.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush13)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush14)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
        # endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Midlight, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Dark, brush16)
        palette1.setBrush(QPalette.Disabled, QPalette.Mid, brush17)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Shadow, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Highlight, brush5)
        palette1.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush13)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush14)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
        # endif
        self.centralwidget.setPalette(palette1)
        self.centralwidget.setStyleSheet("")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        BasePurDi.setCentralWidget(self.centralwidget)
        self.right_top_dock_widget = PurDiDockWidget(BasePurDi)
        self.right_top_dock_widget.setObjectName("right_top_dock_widget")
        sizePolicy.setHeightForWidth(
            self.right_top_dock_widget.sizePolicy().hasHeightForWidth()
        )
        self.right_top_dock_widget.setSizePolicy(sizePolicy)
        self.right_top_dock_widget.setMinimumSize(QSize(420, 600))
        self.right_top_dock_widget.setMaximumSize(QSize(420, 8192))
        self.right_top_dock_widget.setMouseTracking(True)
        self.right_top_dock_widget.setFloating(False)
        self.right_top_dock_widget.setFeatures(
            QDockWidget.DockWidgetClosable
            | QDockWidget.DockWidgetFloatable
            | QDockWidget.DockWidgetMovable
        )
        self.right_top_dock_widget.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea
        )
        self.right_dock_main = QWidget()
        self.right_dock_main.setObjectName("right_dock_main")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.right_dock_main.sizePolicy().hasHeightForWidth()
        )
        self.right_dock_main.setSizePolicy(sizePolicy1)
        self.right_dock_main.setMinimumSize(QSize(75, 300))
        self.right_dock_main.setMaximumSize(QSize(420, 8192))
        self.verticalLayout = QVBoxLayout(self.right_dock_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.right_dock_layout = QVBoxLayout()
        self.right_dock_layout.setSpacing(15)
        self.right_dock_layout.setObjectName("right_dock_layout")
        self.right_dock_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.right_dock_layout.setContentsMargins(0, 0, -1, 0)
        self.right_dock_tab_widget = QTabWidget(self.right_dock_main)
        self.right_dock_tab_widget.setObjectName("right_dock_tab_widget")
        self.right_dock_tab_widget.setEnabled(True)
        sizePolicy.setHeightForWidth(
            self.right_dock_tab_widget.sizePolicy().hasHeightForWidth()
        )
        self.right_dock_tab_widget.setSizePolicy(sizePolicy)
        self.right_dock_tab_widget.setMinimumSize(QSize(400, 650))
        self.right_dock_tab_widget.setMaximumSize(QSize(400, 8192))
        self.right_dock_tab_widget.setSizeIncrement(QSize(0, 0))
        self.right_dock_tab_widget.setTabPosition(QTabWidget.East)
        self.right_dock_tab_widget.setUsesScrollButtons(True)
        self.right_dock_tab_widget.setTabsClosable(False)
        self.right_dock_tab_widget.setMovable(True)
        self.right_dock_tab_widget.setTabBarAutoHide(True)
        self.right_dock_inference = QWidget()
        self.right_dock_inference.setObjectName("right_dock_inference")
        sizePolicy1.setHeightForWidth(
            self.right_dock_inference.sizePolicy().hasHeightForWidth()
        )
        self.right_dock_inference.setSizePolicy(sizePolicy1)
        self.right_dock_inference.setMinimumSize(QSize(350, 530))
        self.verticalLayout_15 = QVBoxLayout(self.right_dock_inference)
        self.verticalLayout_15.setSpacing(5)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.right_dock_inference_tab = QTabWidget(self.right_dock_inference)
        self.right_dock_inference_tab.setObjectName("right_dock_inference_tab")
        sizePolicy.setHeightForWidth(
            self.right_dock_inference_tab.sizePolicy().hasHeightForWidth()
        )
        self.right_dock_inference_tab.setSizePolicy(sizePolicy)
        self.right_dock_inference_tab.setMinimumSize(QSize(0, 0))
        self.right_dock_inference_tab.setAcceptDrops(True)
        self.right_dock_inference_tab.setLayoutDirection(Qt.LeftToRight)
        self.right_dock_inference_tab.setAutoFillBackground(False)
        self.right_dock_inference_tab.setStyleSheet("")
        self.right_dock_inference_tab.setInputMethodHints(Qt.ImhNone)
        self.right_dock_inference_tab.setTabPosition(QTabWidget.South)
        self.right_dock_inference_tab.setElideMode(Qt.ElideLeft)
        self.right_dock_inference_tab.setUsesScrollButtons(True)
        self.right_dock_inference_tab.setDocumentMode(False)
        self.right_dock_inference_tab.setTabsClosable(False)
        self.right_dock_inference_tab.setMovable(True)
        self.right_dock_inference_tab.setTabBarAutoHide(False)
        self.right_dock_inference_txt2img = QWidget()
        self.right_dock_inference_txt2img.setObjectName("right_dock_inference_txt2img")
        self.right_dock_inference_txt2img.setAcceptDrops(False)
        self.right_dock_inference_txt2img.setAutoFillBackground(False)
        self.verticalLayout_6 = QVBoxLayout(self.right_dock_inference_txt2img)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 10, 0, 10)
        self.inference_general_setting = QGroupBox(self.right_dock_inference_txt2img)
        self.inference_general_setting.setObjectName("inference_general_setting")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.inference_general_setting.sizePolicy().hasHeightForWidth()
        )
        self.inference_general_setting.setSizePolicy(sizePolicy2)
        self.inference_general_setting.setMaximumSize(QSize(350, 16777215))
        self.inference_general_setting.setStyleSheet("border-color: rgba(0, 0, 0, 0);")
        self.verticalLayout_11 = QVBoxLayout(self.inference_general_setting)
        self.verticalLayout_11.setSpacing(5)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.width_layout = QHBoxLayout()
        self.width_layout.setSpacing(10)
        self.width_layout.setObjectName("width_layout")
        self.width_layout.setContentsMargins(0, -1, -1, -1)
        self.width_label = QLabel(self.inference_general_setting)
        self.width_label.setObjectName("width_label")

        self.width_layout.addWidget(self.width_label)

        self.width_slider_bar = QSlider(self.inference_general_setting)
        self.width_slider_bar.setObjectName("width_slider_bar")
        self.width_slider_bar.setMinimum(128)
        self.width_slider_bar.setMaximum(2048)
        self.width_slider_bar.setValue(512)
        self.width_slider_bar.setSliderPosition(512)
        self.width_slider_bar.setOrientation(Qt.Horizontal)
        self.width_slider_bar.setInvertedAppearance(False)
        self.width_slider_bar.setInvertedControls(False)

        self.width_layout.addWidget(self.width_slider_bar)

        self.width_field = QLineEdit(self.inference_general_setting)
        self.width_field.setObjectName("width_field")
        sizePolicy2.setHeightForWidth(self.width_field.sizePolicy().hasHeightForWidth())
        self.width_field.setSizePolicy(sizePolicy2)
        self.width_field.setMinimumSize(QSize(0, 0))
        self.width_field.setMaximumSize(QSize(60, 16777215))
        self.width_field.setInputMethodHints(Qt.ImhDigitsOnly)
        self.width_field.setMaxLength(32767)

        self.width_layout.addWidget(self.width_field)

        self.verticalLayout_11.addLayout(self.width_layout)

        self.height_layout = QHBoxLayout()
        self.height_layout.setSpacing(10)
        self.height_layout.setObjectName("height_layout")
        self.height_layout.setContentsMargins(0, -1, -1, -1)
        self.height_label = QLabel(self.inference_general_setting)
        self.height_label.setObjectName("height_label")

        self.height_layout.addWidget(self.height_label)

        self.height_slider_bar = QSlider(self.inference_general_setting)
        self.height_slider_bar.setObjectName("height_slider_bar")
        self.height_slider_bar.setMinimum(128)
        self.height_slider_bar.setMaximum(2048)
        self.height_slider_bar.setValue(512)
        self.height_slider_bar.setSliderPosition(512)
        self.height_slider_bar.setOrientation(Qt.Horizontal)
        self.height_slider_bar.setInvertedAppearance(False)
        self.height_slider_bar.setInvertedControls(False)

        self.height_layout.addWidget(self.height_slider_bar)

        self.height_field = QLineEdit(self.inference_general_setting)
        self.height_field.setObjectName("height_field")
        sizePolicy2.setHeightForWidth(
            self.height_field.sizePolicy().hasHeightForWidth()
        )
        self.height_field.setSizePolicy(sizePolicy2)
        self.height_field.setMaximumSize(QSize(60, 16777215))
        self.height_field.setInputMethodHints(Qt.ImhDigitsOnly)

        self.height_layout.addWidget(self.height_field)

        self.verticalLayout_11.addLayout(self.height_layout)

        self.batch_layout = QHBoxLayout()
        self.batch_layout.setObjectName("batch_layout")
        self.select_n_sample = QLineEdit(self.inference_general_setting)
        self.select_n_sample.setObjectName("select_n_sample")

        self.batch_layout.addWidget(self.select_n_sample)

        self.select_batch_size = QLineEdit(self.inference_general_setting)
        self.select_batch_size.setObjectName("select_batch_size")

        self.batch_layout.addWidget(self.select_batch_size)

        self.verticalLayout_11.addLayout(self.batch_layout)

        self.seed_layout = QHBoxLayout()
        self.seed_layout.setObjectName("seed_layout")
        self.seed_layout.setContentsMargins(-1, 0, -1, -1)
        self.select_seed = QLineEdit(self.inference_general_setting)
        self.select_seed.setObjectName("select_seed")
        self.select_seed.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.select_seed.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.select_seed.setClearButtonEnabled(False)

        self.seed_layout.addWidget(self.select_seed)

        self.random_seed = QPushButton(self.inference_general_setting)
        self.random_seed.setObjectName("random_seed")
        sizePolicy2.setHeightForWidth(self.random_seed.sizePolicy().hasHeightForWidth())
        self.random_seed.setSizePolicy(sizePolicy2)
        self.random_seed.setFlat(True)

        self.seed_layout.addWidget(self.random_seed)

        self.verticalLayout_11.addLayout(self.seed_layout)

        self.schedulers_label = QLabel(self.inference_general_setting)
        self.schedulers_label.setObjectName("schedulers_label")

        self.verticalLayout_11.addWidget(self.schedulers_label)

        self.scheduler_drop_down_box = QComboBox(self.inference_general_setting)
        self.scheduler_drop_down_box.setObjectName("scheduler_drop_down_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.scheduler_drop_down_box.sizePolicy().hasHeightForWidth()
        )
        self.scheduler_drop_down_box.setSizePolicy(sizePolicy3)

        self.verticalLayout_11.addWidget(self.scheduler_drop_down_box)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cfg_label = QLabel(self.inference_general_setting)
        self.cfg_label.setObjectName("cfg_label")
        self.cfg_label.setScaledContents(False)

        self.horizontalLayout_3.addWidget(self.cfg_label)

        self.cfg_slider_bar = QSlider(self.inference_general_setting)
        self.cfg_slider_bar.setObjectName("cfg_slider_bar")
        self.cfg_slider_bar.setInputMethodHints(
            Qt.ImhDigitsOnly | Qt.ImhNoPredictiveText
        )
        self.cfg_slider_bar.setMaximum(15)
        self.cfg_slider_bar.setSliderPosition(7)
        self.cfg_slider_bar.setOrientation(Qt.Horizontal)
        self.cfg_slider_bar.setInvertedAppearance(False)
        self.cfg_slider_bar.setTickInterval(5)

        self.horizontalLayout_3.addWidget(self.cfg_slider_bar)

        self.cfg_field = QLineEdit(self.inference_general_setting)
        self.cfg_field.setObjectName("cfg_field")
        sizePolicy2.setHeightForWidth(self.cfg_field.sizePolicy().hasHeightForWidth())
        self.cfg_field.setSizePolicy(sizePolicy2)
        self.cfg_field.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.cfg_field)

        self.verticalLayout_11.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.steps_label = QLabel(self.inference_general_setting)
        self.steps_label.setObjectName("steps_label")

        self.horizontalLayout_10.addWidget(self.steps_label)

        self.steps_slider_bar = QSlider(self.inference_general_setting)
        self.steps_slider_bar.setObjectName("steps_slider_bar")
        self.steps_slider_bar.setValue(30)
        self.steps_slider_bar.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.steps_slider_bar)

        self.steps_field = QLineEdit(self.inference_general_setting)
        self.steps_field.setObjectName("steps_field")
        self.steps_field.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_10.addWidget(self.steps_field)

        self.verticalLayout_11.addLayout(self.horizontalLayout_10)

        self.verticalLayout_6.addWidget(self.inference_general_setting)

        self.img_options_setting = QGroupBox(self.right_dock_inference_txt2img)
        self.img_options_setting.setObjectName("img_options_setting")
        sizePolicy1.setHeightForWidth(
            self.img_options_setting.sizePolicy().hasHeightForWidth()
        )
        self.img_options_setting.setSizePolicy(sizePolicy1)
        self.img_options_setting.setMinimumSize(QSize(0, 0))
        self.img_options_setting.setMaximumSize(QSize(350, 16777215))
        self.img_options_setting.setStyleSheet("border-color: rgba(191, 64, 64, 0);")
        self.verticalLayout_3 = QVBoxLayout(self.img_options_setting)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toolBox = QToolBox(self.img_options_setting)
        self.toolBox.setObjectName("toolBox")
        self.page_5 = QWidget()
        self.page_5.setObjectName("page_5")
        self.page_5.setGeometry(QRect(0, 0, 344, 488))
        self.verticalLayout_35 = QVBoxLayout(self.page_5)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.label_15 = QLabel(self.page_5)
        self.label_15.setObjectName("label_15")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy4)
        self.label_15.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_15.setWordWrap(True)

        self.verticalLayout_35.addWidget(self.label_15)

        self.txt2img_checkbox = QCheckBox(self.page_5)
        self.txt2img_checkbox.setObjectName("txt2img_checkbox")
        self.txt2img_checkbox.setChecked(True)

        self.verticalLayout_35.addWidget(self.txt2img_checkbox)

        self.toolBox.addItem(self.page_5, "Text-to-Image")
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.page_2.setGeometry(QRect(0, 0, 344, 488))
        self.verticalLayout_32 = QVBoxLayout(self.page_2)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.label_10 = QLabel(self.page_2)
        self.label_10.setObjectName("label_10")
        sizePolicy4.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy4)
        self.label_10.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_10.setWordWrap(True)

        self.verticalLayout_32.addWidget(self.label_10)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_18 = QLabel(self.page_2)
        self.label_18.setObjectName("label_18")

        self.horizontalLayout_4.addWidget(self.label_18)

        self.max_iter_to_alter_field = QLineEdit(self.page_2)
        self.max_iter_to_alter_field.setObjectName("max_iter_to_alter_field")
        self.max_iter_to_alter_field.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_4.addWidget(self.max_iter_to_alter_field)

        self.verticalLayout_32.addLayout(self.horizontalLayout_4)

        self.attend_excite_checkbox = QCheckBox(self.page_2)
        self.attend_excite_checkbox.setObjectName("attend_excite_checkbox")
        self.attend_excite_checkbox.setChecked(False)

        self.verticalLayout_32.addWidget(self.attend_excite_checkbox)

        self.toolBox.addItem(self.page_2, "Attend And Excite")
        self.page_3 = QWidget()
        self.page_3.setObjectName("page_3")
        self.page_3.setGeometry(QRect(0, 0, 344, 488))
        self.verticalLayout_33 = QVBoxLayout(self.page_3)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.label_11 = QLabel(self.page_3)
        self.label_11.setObjectName("label_11")
        sizePolicy4.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy4)
        self.label_11.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_11.setWordWrap(True)

        self.verticalLayout_33.addWidget(self.label_11)

        self.multidiffusion_panorama_checkbox = QCheckBox(self.page_3)
        self.multidiffusion_panorama_checkbox.setObjectName(
            "multidiffusion_panorama_checkbox"
        )
        self.multidiffusion_panorama_checkbox.setChecked(False)

        self.verticalLayout_33.addWidget(self.multidiffusion_panorama_checkbox)

        self.toolBox.addItem(self.page_3, "MultiDiffusion")
        self.page_4 = QWidget()
        self.page_4.setObjectName("page_4")
        self.page_4.setGeometry(QRect(0, 0, 344, 488))
        self.verticalLayout_34 = QVBoxLayout(self.page_4)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.label_12 = QLabel(self.page_4)
        self.label_12.setObjectName("label_12")
        sizePolicy4.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy4)
        self.label_12.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_12.setWordWrap(True)

        self.verticalLayout_34.addWidget(self.label_12)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QLabel(self.page_4)
        self.label_8.setObjectName("label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.sag_scale_field = QLineEdit(self.page_4)
        self.sag_scale_field.setObjectName("sag_scale_field")
        self.sag_scale_field.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.sag_scale_field)

        self.verticalLayout_34.addLayout(self.horizontalLayout_5)

        self.self_attention_guidance_checkbox = QCheckBox(self.page_4)
        self.self_attention_guidance_checkbox.setObjectName(
            "self_attention_guidance_checkbox"
        )
        self.self_attention_guidance_checkbox.setChecked(False)

        self.verticalLayout_34.addWidget(self.self_attention_guidance_checkbox)

        self.toolBox.addItem(self.page_4, "Self-Attention Guidance")

        self.verticalLayout_3.addWidget(self.toolBox)

        self.verticalLayout_6.addWidget(self.img_options_setting)

        self.right_dock_inference_tab.addTab(self.right_dock_inference_txt2img, "")
        self.right_dock_inference_img2img = QWidget()
        self.right_dock_inference_img2img.setObjectName("right_dock_inference_img2img")
        self.right_dock_inference_img2img.setStyleSheet(
            "border-color: rgba(191, 64, 64, 0);"
        )
        self.verticalLayout_9 = QVBoxLayout(self.right_dock_inference_img2img)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.img2img_container = QGroupBox(self.right_dock_inference_img2img)
        self.img2img_container.setObjectName("img2img_container")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(
            self.img2img_container.sizePolicy().hasHeightForWidth()
        )
        self.img2img_container.setSizePolicy(sizePolicy5)
        self.img2img_container.setMinimumSize(QSize(350, 150))
        self.verticalLayout_10 = QVBoxLayout(self.img2img_container)
        self.verticalLayout_10.setSpacing(10)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.img2img_select_box = QListWidget(self.img2img_container)
        self.img2img_select_box.setObjectName("img2img_select_box")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.img2img_select_box.sizePolicy().hasHeightForWidth()
        )
        self.img2img_select_box.setSizePolicy(sizePolicy6)
        self.img2img_select_box.setMinimumSize(QSize(0, 100))
        self.img2img_select_box.setDragDropMode(QAbstractItemView.DragDrop)
        self.img2img_select_box.setDefaultDropAction(Qt.LinkAction)
        self.img2img_select_box.setIconSize(QSize(128, 128))
        self.img2img_select_box.setMovement(QListView.Snap)
        self.img2img_select_box.setFlow(QListView.LeftToRight)
        self.img2img_select_box.setProperty("isWrapping", True)
        self.img2img_select_box.setResizeMode(QListView.Adjust)
        self.img2img_select_box.setSpacing(10)
        self.img2img_select_box.setGridSize(QSize(87, 128))
        self.img2img_select_box.setViewMode(QListView.IconMode)
        self.img2img_select_box.setItemAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.img2img_select_box)

        self.img2img_clear_btn = QPushButton(self.img2img_container)
        self.img2img_clear_btn.setObjectName("img2img_clear_btn")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(
            self.img2img_clear_btn.sizePolicy().hasHeightForWidth()
        )
        self.img2img_clear_btn.setSizePolicy(sizePolicy7)
        self.img2img_clear_btn.setFlat(True)

        self.verticalLayout_10.addWidget(self.img2img_clear_btn)

        self.verticalLayout_9.addWidget(self.img2img_container)

        self.img2img_options = QGroupBox(self.right_dock_inference_img2img)
        self.img2img_options.setObjectName("img2img_options")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(
            self.img2img_options.sizePolicy().hasHeightForWidth()
        )
        self.img2img_options.setSizePolicy(sizePolicy8)
        self.verticalLayout_14 = QVBoxLayout(self.img2img_options)
        self.verticalLayout_14.setSpacing(5)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.image_variation_toolbox = QToolBox(self.img2img_options)
        self.image_variation_toolbox.setObjectName("image_variation_toolbox")
        sizePolicy.setHeightForWidth(
            self.image_variation_toolbox.sizePolicy().hasHeightForWidth()
        )
        self.image_variation_toolbox.setSizePolicy(sizePolicy)
        self.page = QWidget()
        self.page.setObjectName("page")
        self.page.setGeometry(QRect(0, 0, 170, 95))
        self.verticalLayout_19 = QVBoxLayout(self.page)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.img2img_deviation_percent = QLabel(self.page)
        self.img2img_deviation_percent.setObjectName("img2img_deviation_percent")
        self.img2img_deviation_percent.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.verticalLayout_19.addWidget(self.img2img_deviation_percent)

        self.img_deviation_layout = QHBoxLayout()
        self.img_deviation_layout.setSpacing(10)
        self.img_deviation_layout.setObjectName("img_deviation_layout")
        self.img_deviation_layout.setContentsMargins(-1, 0, -1, -1)
        self.img2img_strength_slider_bar = QSlider(self.page)
        self.img2img_strength_slider_bar.setObjectName("img2img_strength_slider_bar")
        sizePolicy9 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(
            self.img2img_strength_slider_bar.sizePolicy().hasHeightForWidth()
        )
        self.img2img_strength_slider_bar.setSizePolicy(sizePolicy9)
        self.img2img_strength_slider_bar.setMaximum(100)
        self.img2img_strength_slider_bar.setValue(75)
        self.img2img_strength_slider_bar.setOrientation(Qt.Horizontal)

        self.img_deviation_layout.addWidget(self.img2img_strength_slider_bar)

        self.img2img_strength_field = QLineEdit(self.page)
        self.img2img_strength_field.setObjectName("img2img_strength_field")
        self.img2img_strength_field.setMaximumSize(QSize(60, 16777215))
        self.img2img_strength_field.setInputMethodHints(Qt.ImhDigitsOnly)
        self.img2img_strength_field.setMaxLength(32767)

        self.img_deviation_layout.addWidget(self.img2img_strength_field)

        self.verticalLayout_19.addLayout(self.img_deviation_layout)

        self.verticalSpacer_3 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_19.addItem(self.verticalSpacer_3)

        self.img2img_checkbox = QCheckBox(self.page)
        self.img2img_checkbox.setObjectName("img2img_checkbox")
        self.img2img_checkbox.setChecked(True)

        self.verticalLayout_19.addWidget(self.img2img_checkbox)

        self.image_variation_toolbox.addItem(self.page, "Image-to-Image")
        self.ControlNet = QWidget()
        self.ControlNet.setObjectName("ControlNet")
        self.ControlNet.setGeometry(QRect(0, 0, 360, 429))
        self.verticalLayout_12 = QVBoxLayout(self.ControlNet)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_19 = QLabel(self.ControlNet)
        self.label_19.setObjectName("label_19")
        sizePolicy4.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy4)
        self.label_19.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_19.setWordWrap(True)

        self.verticalLayout_12.addWidget(self.label_19)

        self.verticalSpacer_2 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_12.addItem(self.verticalSpacer_2)

        self.controlnet_method_combobox = QComboBox(self.ControlNet)
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.addItem("")
        self.controlnet_method_combobox.setObjectName("controlnet_method_combobox")
        sizePolicy10 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(
            self.controlnet_method_combobox.sizePolicy().hasHeightForWidth()
        )
        self.controlnet_method_combobox.setSizePolicy(sizePolicy10)
        self.controlnet_method_combobox.setMaximumSize(QSize(16777215, 100))
        self.controlnet_method_combobox.setIconSize(QSize(75, 75))

        self.verticalLayout_12.addWidget(self.controlnet_method_combobox)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.canny_low_threshold = QLineEdit(self.ControlNet)
        self.canny_low_threshold.setObjectName("canny_low_threshold")

        self.horizontalLayout_6.addWidget(self.canny_low_threshold)

        self.canny_high_threshold = QLineEdit(self.ControlNet)
        self.canny_high_threshold.setObjectName("canny_high_threshold")

        self.horizontalLayout_6.addWidget(self.canny_high_threshold)

        self.verticalLayout_12.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.canny_conditioning_scale = QLineEdit(self.ControlNet)
        self.canny_conditioning_scale.setObjectName("canny_conditioning_scale")

        self.horizontalLayout_9.addWidget(self.canny_conditioning_scale)

        self.verticalLayout_12.addLayout(self.horizontalLayout_9)

        self.controlnet_checkbox = QCheckBox(self.ControlNet)
        self.controlnet_checkbox.setObjectName("controlnet_checkbox")

        self.verticalLayout_12.addWidget(self.controlnet_checkbox)

        self.image_variation_toolbox.addItem(self.ControlNet, "ControlNet")
        self.cycle_diffusion_widget = QWidget()
        self.cycle_diffusion_widget.setObjectName("cycle_diffusion_widget")
        self.cycle_diffusion_widget.setGeometry(QRect(0, 0, 95, 404))
        self.verticalLayout_30 = QVBoxLayout(self.cycle_diffusion_widget)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.cycle_diffusion_label = QLabel(self.cycle_diffusion_widget)
        self.cycle_diffusion_label.setObjectName("cycle_diffusion_label")
        sizePolicy4.setHeightForWidth(
            self.cycle_diffusion_label.sizePolicy().hasHeightForWidth()
        )
        self.cycle_diffusion_label.setSizePolicy(sizePolicy4)
        self.cycle_diffusion_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.cycle_diffusion_label.setWordWrap(True)

        self.verticalLayout_30.addWidget(self.cycle_diffusion_label)

        self.verticalSpacer_4 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_30.addItem(self.verticalSpacer_4)

        self.cycle_diffusion_checkbox = QCheckBox(self.cycle_diffusion_widget)
        self.cycle_diffusion_checkbox.setObjectName("cycle_diffusion_checkbox")
        self.cycle_diffusion_checkbox.setAutoExclusive(False)

        self.verticalLayout_30.addWidget(self.cycle_diffusion_checkbox)

        self.image_variation_toolbox.addItem(
            self.cycle_diffusion_widget, "Cycle Diffusion"
        )
        self.depth_to_image_widget = QWidget()
        self.depth_to_image_widget.setObjectName("depth_to_image_widget")
        self.depth_to_image_widget.setGeometry(QRect(0, 0, 86, 244))
        self.verticalLayout_31 = QVBoxLayout(self.depth_to_image_widget)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.label_9 = QLabel(self.depth_to_image_widget)
        self.label_9.setObjectName("label_9")
        sizePolicy4.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy4)
        self.label_9.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_9.setWordWrap(True)

        self.verticalLayout_31.addWidget(self.label_9)

        self.verticalSpacer_5 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_31.addItem(self.verticalSpacer_5)

        self.depth_to_image_checkbox = QCheckBox(self.depth_to_image_widget)
        self.depth_to_image_checkbox.setObjectName("depth_to_image_checkbox")

        self.verticalLayout_31.addWidget(self.depth_to_image_checkbox)

        self.image_variation_toolbox.addItem(
            self.depth_to_image_widget, "Depth-to-Image"
        )
        self.image_variation_widget = QWidget()
        self.image_variation_widget.setObjectName("image_variation_widget")
        self.image_variation_widget.setGeometry(QRect(0, 0, 93, 276))
        self.verticalLayout_29 = QVBoxLayout(self.image_variation_widget)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.img2img_image_variation_label = QLabel(self.image_variation_widget)
        self.img2img_image_variation_label.setObjectName(
            "img2img_image_variation_label"
        )
        sizePolicy4.setHeightForWidth(
            self.img2img_image_variation_label.sizePolicy().hasHeightForWidth()
        )
        self.img2img_image_variation_label.setSizePolicy(sizePolicy4)
        self.img2img_image_variation_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.img2img_image_variation_label.setWordWrap(True)

        self.verticalLayout_29.addWidget(self.img2img_image_variation_label)

        self.verticalSpacer_6 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_29.addItem(self.verticalSpacer_6)

        self.img2img_image_variation_checkbox = QCheckBox(self.image_variation_widget)
        self.img2img_image_variation_checkbox.setObjectName(
            "img2img_image_variation_checkbox"
        )
        self.img2img_image_variation_checkbox.setAutoExclusive(False)

        self.verticalLayout_29.addWidget(self.img2img_image_variation_checkbox)

        self.image_variation_toolbox.addItem(
            self.image_variation_widget, "Image Variation"
        )
        self.instruct_pix2pix_widget = QWidget()
        self.instruct_pix2pix_widget.setObjectName("instruct_pix2pix_widget")
        self.instruct_pix2pix_widget.setGeometry(QRect(0, 0, 136, 272))
        self.verticalLayout_18 = QVBoxLayout(self.instruct_pix2pix_widget)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label_13 = QLabel(self.instruct_pix2pix_widget)
        self.label_13.setObjectName("label_13")
        sizePolicy4.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy4)
        self.label_13.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_13.setWordWrap(True)

        self.verticalLayout_18.addWidget(self.label_13)

        self.verticalSpacer_7 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_18.addItem(self.verticalSpacer_7)

        self.verticalLayout_36 = QVBoxLayout()
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(-1, 5, -1, 0)
        self.img_guidance_scale_label = QLabel(self.instruct_pix2pix_widget)
        self.img_guidance_scale_label.setObjectName("img_guidance_scale_label")

        self.verticalLayout_36.addWidget(self.img_guidance_scale_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.img_guidance_slider_bar = QSlider(self.instruct_pix2pix_widget)
        self.img_guidance_slider_bar.setObjectName("img_guidance_slider_bar")
        self.img_guidance_slider_bar.setMaximum(5)
        self.img_guidance_slider_bar.setSliderPosition(2)
        self.img_guidance_slider_bar.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.img_guidance_slider_bar)

        self.img_guidance_scale_field = QLineEdit(self.instruct_pix2pix_widget)
        self.img_guidance_scale_field.setObjectName("img_guidance_scale_field")
        sizePolicy2.setHeightForWidth(
            self.img_guidance_scale_field.sizePolicy().hasHeightForWidth()
        )
        self.img_guidance_scale_field.setSizePolicy(sizePolicy2)
        self.img_guidance_scale_field.setMinimumSize(QSize(60, 0))
        self.img_guidance_scale_field.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.img_guidance_scale_field)

        self.verticalLayout_36.addLayout(self.horizontalLayout)

        self.verticalLayout_18.addLayout(self.verticalLayout_36)

        self.instruct_pix2pix_checkbox = QCheckBox(self.instruct_pix2pix_widget)
        self.instruct_pix2pix_checkbox.setObjectName("instruct_pix2pix_checkbox")

        self.verticalLayout_18.addWidget(self.instruct_pix2pix_checkbox)

        self.image_variation_toolbox.addItem(
            self.instruct_pix2pix_widget, "InstructPix2Pix"
        )
        self.page_6 = QWidget()
        self.page_6.setObjectName("page_6")
        self.page_6.setGeometry(QRect(0, 0, 100, 324))
        self.verticalLayout_37 = QVBoxLayout(self.page_6)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.label_16 = QLabel(self.page_6)
        self.label_16.setObjectName("label_16")
        sizePolicy4.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy4)
        self.label_16.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_16.setWordWrap(True)

        self.verticalLayout_37.addWidget(self.label_16)

        self.verticalSpacer_8 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_37.addItem(self.verticalSpacer_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.pix2pix_source_field = QLineEdit(self.page_6)
        self.pix2pix_source_field.setObjectName("pix2pix_source_field")

        self.horizontalLayout_2.addWidget(self.pix2pix_source_field)

        self.pix2pix_target_field = QLineEdit(self.page_6)
        self.pix2pix_target_field.setObjectName("pix2pix_target_field")

        self.horizontalLayout_2.addWidget(self.pix2pix_target_field)

        self.verticalLayout_37.addLayout(self.horizontalLayout_2)

        self.pix2pix_zero_checkbox = QCheckBox(self.page_6)
        self.pix2pix_zero_checkbox.setObjectName("pix2pix_zero_checkbox")

        self.verticalLayout_37.addWidget(self.pix2pix_zero_checkbox)

        self.image_variation_toolbox.addItem(self.page_6, "Pix2Pix Zero-shot")

        self.verticalLayout_14.addWidget(self.image_variation_toolbox)

        self.verticalLayout_9.addWidget(self.img2img_options)

        self.right_dock_inference_tab.addTab(self.right_dock_inference_img2img, "")
        self.right_dock_inference_general = QWidget()
        self.right_dock_inference_general.setObjectName("right_dock_inference_general")
        self.verticalLayout_17 = QVBoxLayout(self.right_dock_inference_general)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.optimization_options = QGroupBox(self.right_dock_inference_general)
        self.optimization_options.setObjectName("optimization_options")
        self.verticalLayout_20 = QVBoxLayout(self.optimization_options)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.optimization_toolbox = QToolBox(self.optimization_options)
        self.optimization_toolbox.setObjectName("optimization_toolbox")
        self.attention_slicing_item = QWidget()
        self.attention_slicing_item.setObjectName("attention_slicing_item")
        self.attention_slicing_item.setGeometry(QRect(0, 0, 131, 398))
        self.verticalLayout_24 = QVBoxLayout(self.attention_slicing_item)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.label = QLabel(self.attention_slicing_item)
        self.label.setObjectName("label")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        self.verticalLayout_24.addWidget(self.label)

        self.attention_slicing_checkbox = QCheckBox(self.attention_slicing_item)
        self.attention_slicing_checkbox.setObjectName("attention_slicing_checkbox")
        self.attention_slicing_checkbox.setChecked(False)

        self.verticalLayout_24.addWidget(self.attention_slicing_checkbox)

        self.optimization_toolbox.addItem(
            self.attention_slicing_item, "Attention Slicing"
        )
        self.cpu_offload_item = QWidget()
        self.cpu_offload_item.setObjectName("cpu_offload_item")
        self.cpu_offload_item.setGeometry(QRect(0, 0, 167, 387))
        self.verticalLayout_25 = QVBoxLayout(self.cpu_offload_item)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.label_2 = QLabel(self.cpu_offload_item)
        self.label_2.setObjectName("label_2")
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)
        self.label_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_2.setWordWrap(True)

        self.verticalLayout_25.addWidget(self.label_2)

        self.model_cpu_offload_checkbox = QCheckBox(self.cpu_offload_item)
        self.model_cpu_offload_checkbox.setObjectName("model_cpu_offload_checkbox")
        self.model_cpu_offload_checkbox.setChecked(False)

        self.verticalLayout_25.addWidget(self.model_cpu_offload_checkbox)

        self.label_17 = QLabel(self.cpu_offload_item)
        self.label_17.setObjectName("label_17")
        sizePolicy4.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy4)
        self.label_17.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_17.setWordWrap(True)

        self.verticalLayout_25.addWidget(self.label_17)

        self.sequential_cpu_offload_checkbox = QCheckBox(self.cpu_offload_item)
        self.sequential_cpu_offload_checkbox.setObjectName(
            "sequential_cpu_offload_checkbox"
        )

        self.verticalLayout_25.addWidget(self.sequential_cpu_offload_checkbox)

        self.line = QFrame(self.cpu_offload_item)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_25.addWidget(self.line)

        self.cpu_offload_disable = QCheckBox(self.cpu_offload_item)
        self.cpu_offload_disable.setObjectName("cpu_offload_disable")
        self.cpu_offload_disable.setChecked(True)

        self.verticalLayout_25.addWidget(self.cpu_offload_disable)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_25.addItem(self.verticalSpacer)

        self.optimization_toolbox.addItem(self.cpu_offload_item, "CPU Offload")
        self.cudnn_item = QWidget()
        self.cudnn_item.setObjectName("cudnn_item")
        self.cudnn_item.setGeometry(QRect(0, 0, 98, 302))
        self.verticalLayout_21 = QVBoxLayout(self.cudnn_item)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_3 = QLabel(self.cudnn_item)
        self.label_3.setObjectName("label_3")
        sizePolicy4.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy4)
        self.label_3.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_3.setWordWrap(True)

        self.verticalLayout_21.addWidget(self.label_3)

        self.cudnn_checkbox = QCheckBox(self.cudnn_item)
        self.cudnn_checkbox.setObjectName("cudnn_checkbox")
        self.cudnn_checkbox.setChecked(True)

        self.verticalLayout_21.addWidget(self.cudnn_checkbox)

        self.optimization_toolbox.addItem(self.cudnn_item, "cuDNN Auto-Tuner")
        self.half_precision_item = QWidget()
        self.half_precision_item.setObjectName("half_precision_item")
        self.half_precision_item.setGeometry(QRect(0, 0, 360, 636))
        self.verticalLayout_26 = QVBoxLayout(self.half_precision_item)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.label_4 = QLabel(self.half_precision_item)
        self.label_4.setObjectName("label_4")
        sizePolicy4.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy4)
        self.label_4.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_4.setWordWrap(True)

        self.verticalLayout_26.addWidget(self.label_4)

        self.half_precision_checkbox = QCheckBox(self.half_precision_item)
        self.half_precision_checkbox.setObjectName("half_precision_checkbox")
        self.half_precision_checkbox.setChecked(True)

        self.verticalLayout_26.addWidget(self.half_precision_checkbox)

        self.optimization_toolbox.addItem(self.half_precision_item, "Half Precision")
        self.memory_efficient_item = QWidget()
        self.memory_efficient_item.setObjectName("memory_efficient_item")
        self.memory_efficient_item.setGeometry(QRect(0, 0, 187, 126))
        self.verticalLayout_23 = QVBoxLayout(self.memory_efficient_item)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.label_5 = QLabel(self.memory_efficient_item)
        self.label_5.setObjectName("label_5")
        sizePolicy4.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy4)
        self.label_5.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_5.setWordWrap(True)

        self.verticalLayout_23.addWidget(self.label_5)

        self.memory_efficient_attention_checkbox = QCheckBox(self.memory_efficient_item)
        self.memory_efficient_attention_checkbox.setObjectName(
            "memory_efficient_attention_checkbox"
        )
        self.memory_efficient_attention_checkbox.setChecked(True)

        self.verticalLayout_23.addWidget(self.memory_efficient_attention_checkbox)

        self.optimization_toolbox.addItem(
            self.memory_efficient_item, "Memory Efficient Attention - Xformer"
        )
        self.tf32_item = QWidget()
        self.tf32_item.setObjectName("tf32_item")
        self.tf32_item.setGeometry(QRect(0, 0, 100, 654))
        self.verticalLayout_28 = QVBoxLayout(self.tf32_item)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.label_6 = QLabel(self.tf32_item)
        self.label_6.setObjectName("label_6")
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_6.setWordWrap(True)

        self.verticalLayout_28.addWidget(self.label_6)

        self.tf32_item_checkbox = QCheckBox(self.tf32_item)
        self.tf32_item_checkbox.setObjectName("tf32_item_checkbox")
        self.tf32_item_checkbox.setChecked(True)

        self.verticalLayout_28.addWidget(self.tf32_item_checkbox)

        self.optimization_toolbox.addItem(self.tf32_item, "TensorFloat32")
        self.sliced_vae_item = QWidget()
        self.sliced_vae_item.setObjectName("sliced_vae_item")
        self.sliced_vae_item.setGeometry(QRect(0, 0, 264, 206))
        self.verticalLayout_27 = QVBoxLayout(self.sliced_vae_item)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_7 = QLabel(self.sliced_vae_item)
        self.label_7.setObjectName("label_7")
        sizePolicy4.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy4)
        self.label_7.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_7.setWordWrap(True)

        self.verticalLayout_27.addWidget(self.label_7)

        self.sliced_vae_decode_checkbox = QCheckBox(self.sliced_vae_item)
        self.sliced_vae_decode_checkbox.setObjectName("sliced_vae_decode_checkbox")
        self.sliced_vae_decode_checkbox.setChecked(False)

        self.verticalLayout_27.addWidget(self.sliced_vae_decode_checkbox)

        self.optimization_toolbox.addItem(self.sliced_vae_item, "Sliced VAE")

        self.verticalLayout_20.addWidget(self.optimization_toolbox)

        self.verticalLayout_17.addWidget(self.optimization_options)

        self.inference_general_options = QGroupBox(self.right_dock_inference_general)
        self.inference_general_options.setObjectName("inference_general_options")
        self.inference_general_options.setStyleSheet(
            "border-color: rgba(255, 255, 255, 0);"
        )
        self.verticalLayout_22 = QVBoxLayout(self.inference_general_options)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.prompt_weight_checkbox = QCheckBox(self.inference_general_options)
        self.prompt_weight_checkbox.setObjectName("prompt_weight_checkbox")
        self.prompt_weight_checkbox.setChecked(True)

        self.horizontalLayout_11.addWidget(self.prompt_weight_checkbox)

        self.latent_upscale_2x = QCheckBox(self.inference_general_options)
        self.latent_upscale_2x.setObjectName("latent_upscale_2x")

        self.horizontalLayout_11.addWidget(self.latent_upscale_2x)

        self.nsfw_checkbox = QCheckBox(self.inference_general_options)
        self.nsfw_checkbox.setObjectName("nsfw_checkbox")
        self.nsfw_checkbox.setChecked(True)

        self.horizontalLayout_11.addWidget(self.nsfw_checkbox)

        self.verticalLayout_22.addLayout(self.horizontalLayout_11)

        self.verticalLayout_17.addWidget(self.inference_general_options)

        self.right_dock_inference_tab.addTab(self.right_dock_inference_general, "")

        self.verticalLayout_15.addWidget(self.right_dock_inference_tab)

        self.right_dock_tab_widget.addTab(self.right_dock_inference, "")
        self.right_dock_train = QWidget()
        self.right_dock_train.setObjectName("right_dock_train")
        self.right_dock_train.setEnabled(False)
        sizePolicy.setHeightForWidth(
            self.right_dock_train.sizePolicy().hasHeightForWidth()
        )
        self.right_dock_train.setSizePolicy(sizePolicy)
        self.horizontalLayout_7 = QHBoxLayout(self.right_dock_train)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.sb_tab_sub_r_train = QTabWidget(self.right_dock_train)
        self.sb_tab_sub_r_train.setObjectName("sb_tab_sub_r_train")
        self.sb_tab_sub_r_train.setEnabled(False)
        self.sb_tab_sub_r_train.setTabPosition(QTabWidget.South)
        self.train_dreambooth = QWidget()
        self.train_dreambooth.setObjectName("train_dreambooth")
        sizePolicy.setHeightForWidth(
            self.train_dreambooth.sizePolicy().hasHeightForWidth()
        )
        self.train_dreambooth.setSizePolicy(sizePolicy)
        self.sb_tab_sub_r_train.addTab(self.train_dreambooth, "")
        self.train_textual_inversion = QWidget()
        self.train_textual_inversion.setObjectName("train_textual_inversion")
        sizePolicy.setHeightForWidth(
            self.train_textual_inversion.sizePolicy().hasHeightForWidth()
        )
        self.train_textual_inversion.setSizePolicy(sizePolicy)
        self.sb_tab_sub_r_train.addTab(self.train_textual_inversion, "")
        self.train_lora = QWidget()
        self.train_lora.setObjectName("train_lora")
        sizePolicy.setHeightForWidth(self.train_lora.sizePolicy().hasHeightForWidth())
        self.train_lora.setSizePolicy(sizePolicy)
        self.sb_tab_sub_r_train.addTab(self.train_lora, "")

        self.horizontalLayout_7.addWidget(self.sb_tab_sub_r_train)

        self.right_dock_tab_widget.addTab(self.right_dock_train, "")
        self.chat_mode = QWidget()
        self.chat_mode.setObjectName("chat_mode")
        self.right_dock_tab_widget.addTab(self.chat_mode, "")
        self.right_dock_general = QWidget()
        self.right_dock_general.setObjectName("right_dock_general")
        sizePolicy1.setHeightForWidth(
            self.right_dock_general.sizePolicy().hasHeightForWidth()
        )
        self.right_dock_general.setSizePolicy(sizePolicy1)
        self.right_dock_general.setMaximumSize(QSize(16777215, 8192))
        self.right_dock_general.setStyleSheet("border-color: rgba(0, 0, 0, 0);")
        self.horizontalLayout_8 = QHBoxLayout(self.right_dock_general)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.sb_r_general_v_layout = QVBoxLayout()
        self.sb_r_general_v_layout.setSpacing(10)
        self.sb_r_general_v_layout.setObjectName("sb_r_general_v_layout")
        self.sb_r_general_v_layout.setContentsMargins(-1, -1, -1, 0)
        self.gb_general_layer = QGroupBox(self.right_dock_general)
        self.gb_general_layer.setObjectName("gb_general_layer")
        self.verticalLayout_16 = QVBoxLayout(self.gb_general_layer)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.layers_list = QListWidget(self.gb_general_layer)
        self.layers_list.setObjectName("layers_list")
        self.layers_list.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.layers_list.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.SelectedClicked
        )
        self.layers_list.setAlternatingRowColors(False)
        self.layers_list.setIconSize(QSize(75, 75))
        self.layers_list.setResizeMode(QListView.Fixed)
        self.layers_list.setSpacing(5)
        self.layers_list.setUniformItemSizes(True)
        self.layers_list.setItemAlignment(Qt.AlignCenter)

        self.verticalLayout_16.addWidget(self.layers_list)

        self.label_20 = QLabel(self.gb_general_layer)
        self.label_20.setObjectName("label_20")

        self.verticalLayout_16.addWidget(self.label_20)

        self.edit_theme_button = QPushButton(self.gb_general_layer)
        self.edit_theme_button.setObjectName("edit_theme_button")
        self.edit_theme_button.setFlat(True)

        self.verticalLayout_16.addWidget(self.edit_theme_button)

        self.sb_r_general_v_layout.addWidget(self.gb_general_layer)

        self.sb_r_general_v_layout.setStretch(0, 50)

        self.horizontalLayout_8.addLayout(self.sb_r_general_v_layout)

        self.right_dock_tab_widget.addTab(self.right_dock_general, "")

        self.right_dock_layout.addWidget(self.right_dock_tab_widget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 0, 50, 30)
        self.generate_img_progress = QProgressBar(self.right_dock_main)
        self.generate_img_progress.setObjectName("generate_img_progress")
        sizePolicy10.setHeightForWidth(
            self.generate_img_progress.sizePolicy().hasHeightForWidth()
        )
        self.generate_img_progress.setSizePolicy(sizePolicy10)
        self.generate_img_progress.setMinimumSize(QSize(330, 30))
        self.generate_img_progress.setMaximumSize(QSize(380, 30))
        self.generate_img_progress.setMaximum(1000)
        self.generate_img_progress.setValue(0)
        self.generate_img_progress.setTextVisible(True)
        self.generate_img_progress.setInvertedAppearance(True)

        self.verticalLayout_2.addWidget(self.generate_img_progress)

        self.prompt_field = QTabWidget(self.right_dock_main)
        self.prompt_field.setObjectName("prompt_field")
        sizePolicy.setHeightForWidth(self.prompt_field.sizePolicy().hasHeightForWidth())
        self.prompt_field.setSizePolicy(sizePolicy)
        self.prompt_field.setMinimumSize(QSize(300, 30))
        self.prompt_field.setMaximumSize(QSize(380, 150))
        self.prompt_field.setAutoFillBackground(False)
        self.prompt_field.setStyleSheet("color: rgb(36, 31, 49);")
        self.prompt_field.setTabPosition(QTabWidget.South)
        self.prompt_field.setTabShape(QTabWidget.Rounded)
        self.prompt_field.setTabBarAutoHide(False)
        self.prompt_positive_tab = QWidget()
        self.prompt_positive_tab.setObjectName("prompt_positive_tab")
        sizePolicy.setHeightForWidth(
            self.prompt_positive_tab.sizePolicy().hasHeightForWidth()
        )
        self.prompt_positive_tab.setSizePolicy(sizePolicy)
        self.prompt_positive_tab.setMinimumSize(QSize(330, 0))
        self.prompt_positive_tab.setMaximumSize(QSize(380, 300))
        self.verticalLayout_4 = QVBoxLayout(self.prompt_positive_tab)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.prompt_positive_field = PurDiPromptSuggestion(self.prompt_positive_tab)
        self.prompt_positive_field.setObjectName("prompt_positive_field")
        sizePolicy.setHeightForWidth(
            self.prompt_positive_field.sizePolicy().hasHeightForWidth()
        )
        self.prompt_positive_field.setSizePolicy(sizePolicy)
        self.prompt_positive_field.setMinimumSize(QSize(350, 0))
        self.prompt_positive_field.setMaximumSize(QSize(380, 300))
        self.prompt_positive_field.setStyleSheet("color: rgb(36, 31, 49);")
        self.prompt_positive_field.setFrameShape(QFrame.NoFrame)
        self.prompt_positive_field.setFrameShadow(QFrame.Plain)
        self.prompt_positive_field.setLineWidth(0)
        self.prompt_positive_field.setBackgroundVisible(False)

        self.verticalLayout_4.addWidget(self.prompt_positive_field)

        self.prompt_field.addTab(self.prompt_positive_tab, "")
        self.prompt_negative_tab = QWidget()
        self.prompt_negative_tab.setObjectName("prompt_negative_tab")
        sizePolicy.setHeightForWidth(
            self.prompt_negative_tab.sizePolicy().hasHeightForWidth()
        )
        self.prompt_negative_tab.setSizePolicy(sizePolicy)
        self.prompt_negative_tab.setMaximumSize(QSize(380, 300))
        self.verticalLayout_5 = QVBoxLayout(self.prompt_negative_tab)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.prompt_negative_field = PurDiPromptSuggestion(self.prompt_negative_tab)
        self.prompt_negative_field.setObjectName("prompt_negative_field")
        sizePolicy.setHeightForWidth(
            self.prompt_negative_field.sizePolicy().hasHeightForWidth()
        )
        self.prompt_negative_field.setSizePolicy(sizePolicy)
        self.prompt_negative_field.setMaximumSize(QSize(380, 300))
        self.prompt_negative_field.setStyleSheet("color: rgb(36, 31, 49);")
        self.prompt_negative_field.setBackgroundVisible(False)
        self.prompt_negative_field.setCenterOnScroll(False)

        self.verticalLayout_5.addWidget(self.prompt_negative_field)

        self.prompt_field.addTab(self.prompt_negative_tab, "")

        self.verticalLayout_2.addWidget(self.prompt_field)

        self.generate_button = QPushButton(self.right_dock_main)
        self.generate_button.setObjectName("generate_button")
        sizePolicy10.setHeightForWidth(
            self.generate_button.sizePolicy().hasHeightForWidth()
        )
        self.generate_button.setSizePolicy(sizePolicy10)
        self.generate_button.setMaximumSize(QSize(380, 16777215))
        self.generate_button.setCheckable(True)
        self.generate_button.setAutoExclusive(True)
        self.generate_button.setAutoRepeatDelay(298)
        self.generate_button.setFlat(False)

        self.verticalLayout_2.addWidget(self.generate_button)

        self.right_dock_layout.addLayout(self.verticalLayout_2)

        self.right_dock_layout.setStretch(0, 100)
        self.right_dock_layout.setStretch(1, 10)

        self.verticalLayout.addLayout(self.right_dock_layout)

        self.right_top_dock_widget.setWidget(self.right_dock_main)
        BasePurDi.addDockWidget(Qt.RightDockWidgetArea, self.right_top_dock_widget)
        self.toolbar_left = QToolBar(BasePurDi)
        self.toolbar_left.setObjectName("toolbar_left")
        self.toolbar_left.setAcceptDrops(True)
        self.toolbar_left.setMovable(False)
        self.toolbar_left.setAllowedAreas(Qt.LeftToolBarArea | Qt.RightToolBarArea)
        self.toolbar_left.setOrientation(Qt.Vertical)
        self.toolbar_left.setIconSize(QSize(50, 50))
        self.toolbar_left.setFloatable(False)
        BasePurDi.addToolBar(Qt.LeftToolBarArea, self.toolbar_left)
        self.status_bar = QStatusBar(BasePurDi)
        self.status_bar.setObjectName("status_bar")
        self.status_bar.setMaximumSize(QSize(8192, 16777215))
        self.status_bar.setAcceptDrops(True)
        self.status_bar.setStyleSheet("background-color: rgb(37, 41, 43);")
        self.status_bar.setSizeGripEnabled(False)
        BasePurDi.setStatusBar(self.status_bar)
        self.left_dock_widget = QDockWidget(BasePurDi)
        self.left_dock_widget.setObjectName("left_dock_widget")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(
            self.left_dock_widget.sizePolicy().hasHeightForWidth()
        )
        self.left_dock_widget.setSizePolicy(sizePolicy11)
        self.left_dock_widget.setMinimumSize(QSize(200, 162))
        self.left_dock_widget.setMaximumSize(QSize(8192, 8192))
        self.left_dock_widget.setLayoutDirection(Qt.LeftToRight)
        self.left_dock_widget.setFeatures(
            QDockWidget.DockWidgetClosable
            | QDockWidget.DockWidgetFloatable
            | QDockWidget.DockWidgetMovable
        )
        self.left_widget = QWidget()
        self.left_widget.setObjectName("left_widget")
        sizePolicy.setHeightForWidth(self.left_widget.sizePolicy().hasHeightForWidth())
        self.left_widget.setSizePolicy(sizePolicy)
        self.left_widget.setMinimumSize(QSize(200, 32))
        self.left_widget.setBaseSize(QSize(0, 0))
        self.verticalLayout_13 = QVBoxLayout(self.left_widget)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_13.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_13.setContentsMargins(0, 15, 0, 0)
        self.left_layout = QVBoxLayout()
        self.left_layout.setSpacing(0)
        self.left_layout.setObjectName("left_layout")
        self.left_layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.left_layout.setContentsMargins(-1, 0, -1, -1)
        self.left_frame = QFrame(self.left_widget)
        self.left_frame.setObjectName("left_frame")
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setMinimumSize(QSize(0, 0))
        self.left_frame.setMaximumSize(QSize(8192, 8192))
        self.left_frame.setStyleSheet("border-color: rgba(191, 64, 64, 0);")
        self.left_frame.setFrameShape(QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Sunken)
        self.left_frame.setLineWidth(0)
        self.bottom_widget_layout = QVBoxLayout(self.left_frame)
        self.bottom_widget_layout.setSpacing(0)
        self.bottom_widget_layout.setObjectName("bottom_widget_layout")
        self.bottom_widget_layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.bottom_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.left_tab_widget = QTabWidget(self.left_frame)
        self.left_tab_widget.setObjectName("left_tab_widget")
        self.left_tab_widget.setEnabled(True)
        sizePolicy.setHeightForWidth(
            self.left_tab_widget.sizePolicy().hasHeightForWidth()
        )
        self.left_tab_widget.setSizePolicy(sizePolicy)
        self.left_tab_widget.setMinimumSize(QSize(0, 0))
        self.left_tab_widget.setMaximumSize(QSize(8192, 8192))
        self.left_tab_widget.setFocusPolicy(Qt.TabFocus)
        self.left_tab_widget.setAcceptDrops(True)
        self.left_tab_widget.setLayoutDirection(Qt.LeftToRight)
        self.left_tab_widget.setAutoFillBackground(False)
        self.left_tab_widget.setStyleSheet("")
        self.left_tab_widget.setTabPosition(QTabWidget.South)
        self.left_tab_widget.setDocumentMode(False)
        self.left_tab_widget.setTabsClosable(False)
        self.left_tab_widget.setMovable(True)
        self.left_tab_widget.setTabBarAutoHide(True)
        self.image_browser_widget = QWidget()
        self.image_browser_widget.setObjectName("image_browser_widget")
        sizePolicy.setHeightForWidth(
            self.image_browser_widget.sizePolicy().hasHeightForWidth()
        )
        self.image_browser_widget.setSizePolicy(sizePolicy)
        self.image_browser_widget.setMinimumSize(QSize(0, 0))
        self.image_browser_widget.setMaximumSize(QSize(8192, 8192))
        self.image_browser_widget.setAutoFillBackground(False)
        self.image_browser_widget.setStyleSheet("")
        self.img_browser_search_layout = QVBoxLayout(self.image_browser_widget)
        self.img_browser_search_layout.setSpacing(0)
        self.img_browser_search_layout.setObjectName("img_browser_search_layout")
        self.img_browser_search_layout.setContentsMargins(0, 0, 0, 0)
        self.image_browser_layout = QHBoxLayout()
        self.image_browser_layout.setSpacing(5)
        self.image_browser_layout.setObjectName("image_browser_layout")
        self.image_browser_layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.image_browser_search = QLineEdit(self.image_browser_widget)
        self.image_browser_search.setObjectName("image_browser_search")
        self.image_browser_search.setMaximumSize(QSize(8192, 30))
        self.image_browser_search.setClearButtonEnabled(False)

        self.image_browser_layout.addWidget(self.image_browser_search)

        self.image_browser_sort = QComboBox(self.image_browser_widget)
        self.image_browser_sort.addItem("")
        self.image_browser_sort.addItem("")
        self.image_browser_sort.addItem("")
        self.image_browser_sort.addItem("")
        self.image_browser_sort.setObjectName("image_browser_sort")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(
            self.image_browser_sort.sizePolicy().hasHeightForWidth()
        )
        self.image_browser_sort.setSizePolicy(sizePolicy12)
        self.image_browser_sort.setMaximumSize(QSize(8192, 30))

        self.image_browser_layout.addWidget(self.image_browser_sort)

        self.img_browser_search_layout.addLayout(self.image_browser_layout)

        self.image_browser = PurDiImageBrowser(self.image_browser_widget)
        self.image_browser.setObjectName("image_browser")
        sizePolicy.setHeightForWidth(
            self.image_browser.sizePolicy().hasHeightForWidth()
        )
        self.image_browser.setSizePolicy(sizePolicy)
        self.image_browser.setMinimumSize(QSize(0, 0))
        self.image_browser.setMaximumSize(QSize(8192, 8192))
        self.image_browser.setFocusPolicy(Qt.ClickFocus)
        self.image_browser.setStyleSheet("")
        self.image_browser.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
        )
        self.image_browser.setDragEnabled(True)
        self.image_browser.setDefaultDropAction(Qt.CopyAction)
        self.image_browser.setAlternatingRowColors(False)
        self.image_browser.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.image_browser.setIconSize(QSize(100, 100))
        self.image_browser.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.image_browser.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.image_browser.setMovement(QListView.Snap)
        self.image_browser.setFlow(QListView.LeftToRight)
        self.image_browser.setResizeMode(QListView.Adjust)
        self.image_browser.setLayoutMode(QListView.Batched)
        self.image_browser.setSpacing(5)
        self.image_browser.setGridSize(QSize(100, 100))
        self.image_browser.setViewMode(QListView.IconMode)
        self.image_browser.setModelColumn(0)
        self.image_browser.setUniformItemSizes(False)
        self.image_browser.setBatchSize(100)
        self.image_browser.setWordWrap(False)
        self.image_browser.setItemAlignment(Qt.AlignCenter)

        self.img_browser_search_layout.addWidget(self.image_browser)

        self.img_browser_search_layout.setStretch(1, 1)
        icon1 = QIcon()
        iconThemeName = "image-x-generic"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(".", QSize(), QIcon.Normal, QIcon.Off)

        self.left_tab_widget.addTab(self.image_browser_widget, icon1, "")
        self.bottom_dock_prompts = QWidget()
        self.bottom_dock_prompts.setObjectName("bottom_dock_prompts")
        sizePolicy.setHeightForWidth(
            self.bottom_dock_prompts.sizePolicy().hasHeightForWidth()
        )
        self.bottom_dock_prompts.setSizePolicy(sizePolicy)
        self.bottom_dock_prompts.setMaximumSize(QSize(8192, 8192))
        self.bottom_dock_prompts.setStyleSheet("")
        self.verticalLayout_7 = QVBoxLayout(self.bottom_dock_prompts)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.bottom_dock_prompts_layout = QHBoxLayout()
        self.bottom_dock_prompts_layout.setSpacing(6)
        self.bottom_dock_prompts_layout.setObjectName("bottom_dock_prompts_layout")
        self.bottom_dock_prompts_layout.setContentsMargins(-1, 0, -1, -1)
        self.bottom_prompts_search_bar_btn = QLineEdit(self.bottom_dock_prompts)
        self.bottom_prompts_search_bar_btn.setObjectName(
            "bottom_prompts_search_bar_btn"
        )
        self.bottom_prompts_search_bar_btn.setMaximumSize(QSize(16777215, 30))

        self.bottom_dock_prompts_layout.addWidget(self.bottom_prompts_search_bar_btn)

        self.bottom_prompts_sort = QComboBox(self.bottom_dock_prompts)
        self.bottom_prompts_sort.addItem("")
        self.bottom_prompts_sort.addItem("")
        self.bottom_prompts_sort.setObjectName("bottom_prompts_sort")
        self.bottom_prompts_sort.setMaximumSize(QSize(16777215, 30))

        self.bottom_dock_prompts_layout.addWidget(self.bottom_prompts_sort)

        self.verticalLayout_7.addLayout(self.bottom_dock_prompts_layout)

        self.bottom_dock_prompts_table = QTableWidget(self.bottom_dock_prompts)
        if self.bottom_dock_prompts_table.columnCount() < 1:
            self.bottom_dock_prompts_table.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        self.bottom_dock_prompts_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if self.bottom_dock_prompts_table.rowCount() < 10:
            self.bottom_dock_prompts_table.setRowCount(10)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(6, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(7, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(8, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setVerticalHeaderItem(9, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(0, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(1, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(2, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(3, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(4, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(5, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(6, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.bottom_dock_prompts_table.setItem(7, 0, __qtablewidgetitem18)
        self.bottom_dock_prompts_table.setObjectName("bottom_dock_prompts_table")
        self.bottom_dock_prompts_table.setMinimumSize(QSize(0, 0))
        self.bottom_dock_prompts_table.setStyleSheet("")
        self.bottom_dock_prompts_table.setAutoScroll(True)
        self.bottom_dock_prompts_table.setEditTriggers(
            QAbstractItemView.AnyKeyPressed
            | QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
        )
        self.bottom_dock_prompts_table.setDragEnabled(True)
        self.bottom_dock_prompts_table.setDragDropMode(QAbstractItemView.DragDrop)
        self.bottom_dock_prompts_table.setDefaultDropAction(Qt.CopyAction)
        self.bottom_dock_prompts_table.setAlternatingRowColors(True)
        self.bottom_dock_prompts_table.setIconSize(QSize(0, 0))
        self.bottom_dock_prompts_table.setTextElideMode(Qt.ElideRight)
        self.bottom_dock_prompts_table.setShowGrid(True)
        self.bottom_dock_prompts_table.setGridStyle(Qt.SolidLine)
        self.bottom_dock_prompts_table.setSortingEnabled(True)
        self.bottom_dock_prompts_table.setWordWrap(True)
        self.bottom_dock_prompts_table.setCornerButtonEnabled(True)
        self.bottom_dock_prompts_table.horizontalHeader().setVisible(True)
        self.bottom_dock_prompts_table.horizontalHeader().setCascadingSectionResizes(
            False
        )
        self.bottom_dock_prompts_table.horizontalHeader().setMinimumSectionSize(700)
        self.bottom_dock_prompts_table.horizontalHeader().setDefaultSectionSize(896)
        self.bottom_dock_prompts_table.horizontalHeader().setProperty(
            "showSortIndicator", True
        )
        self.bottom_dock_prompts_table.horizontalHeader().setStretchLastSection(True)
        self.bottom_dock_prompts_table.verticalHeader().setVisible(True)
        self.bottom_dock_prompts_table.verticalHeader().setDefaultSectionSize(24)
        self.bottom_dock_prompts_table.verticalHeader().setProperty(
            "showSortIndicator", True
        )
        self.bottom_dock_prompts_table.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_7.addWidget(self.bottom_dock_prompts_table)

        icon2 = QIcon()
        iconThemeName = "text-x-generic"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(".", QSize(), QIcon.Normal, QIcon.Off)

        self.left_tab_widget.addTab(self.bottom_dock_prompts, icon2, "")
        self.history_widget = QWidget()
        self.history_widget.setObjectName("history_widget")
        sizePolicy.setHeightForWidth(
            self.history_widget.sizePolicy().hasHeightForWidth()
        )
        self.history_widget.setSizePolicy(sizePolicy)
        self.history_widget.setMaximumSize(QSize(8192, 8192))
        self.history_widget.setStyleSheet("")
        self.verticalLayout_8 = QVBoxLayout(self.history_widget)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.history_layout_horizontal = QHBoxLayout()
        self.history_layout_horizontal.setSpacing(6)
        self.history_layout_horizontal.setObjectName("history_layout_horizontal")
        self.history_layout_horizontal.setContentsMargins(0, 0, -1, -1)
        self.history_search_bar_btn = QLineEdit(self.history_widget)
        self.history_search_bar_btn.setObjectName("history_search_bar_btn")
        self.history_search_bar_btn.setMaximumSize(QSize(8192, 30))

        self.history_layout_horizontal.addWidget(self.history_search_bar_btn)

        self.history_sort = QComboBox(self.history_widget)
        self.history_sort.addItem("")
        self.history_sort.addItem("")
        self.history_sort.addItem("")
        self.history_sort.addItem("")
        self.history_sort.setObjectName("history_sort")
        sizePolicy7.setHeightForWidth(
            self.history_sort.sizePolicy().hasHeightForWidth()
        )
        self.history_sort.setSizePolicy(sizePolicy7)
        self.history_sort.setMaximumSize(QSize(8192, 30))

        self.history_layout_horizontal.addWidget(self.history_sort)

        self.verticalLayout_8.addLayout(self.history_layout_horizontal)

        self.img_history_table = QTableWidget(self.history_widget)
        if self.img_history_table.columnCount() < 7:
            self.img_history_table.setColumnCount(7)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(2, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(3, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(4, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(5, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.img_history_table.setHorizontalHeaderItem(6, __qtablewidgetitem25)
        if self.img_history_table.rowCount() < 10:
            self.img_history_table.setRowCount(10)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(0, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(1, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(2, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(3, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(4, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(5, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(6, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(7, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(8, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.img_history_table.setVerticalHeaderItem(9, __qtablewidgetitem35)
        self.img_history_table.setObjectName("img_history_table")
        self.img_history_table.setMaximumSize(QSize(8192, 8192))
        self.img_history_table.setStyleSheet("")
        self.img_history_table.setDragEnabled(True)
        self.img_history_table.setDragDropMode(QAbstractItemView.DragDrop)
        self.img_history_table.setDefaultDropAction(Qt.CopyAction)
        self.img_history_table.setAlternatingRowColors(True)
        self.img_history_table.setTextElideMode(Qt.ElideLeft)
        self.img_history_table.setSortingEnabled(True)
        self.img_history_table.horizontalHeader().setVisible(True)
        self.img_history_table.horizontalHeader().setCascadingSectionResizes(True)
        self.img_history_table.horizontalHeader().setMinimumSectionSize(22)
        self.img_history_table.horizontalHeader().setDefaultSectionSize(120)
        self.img_history_table.horizontalHeader().setStretchLastSection(True)
        self.img_history_table.verticalHeader().setCascadingSectionResizes(True)
        self.img_history_table.verticalHeader().setDefaultSectionSize(24)
        self.img_history_table.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_8.addWidget(self.img_history_table)

        self.left_tab_widget.addTab(self.history_widget, "")

        self.bottom_widget_layout.addWidget(self.left_tab_widget)

        self.left_layout.addWidget(self.left_frame)

        self.verticalLayout_13.addLayout(self.left_layout)

        self.left_dock_widget.setWidget(self.left_widget)
        BasePurDi.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock_widget)
        self.left_dock_widget.raise_()

        self.retranslateUi(BasePurDi)

        self.right_dock_tab_widget.setCurrentIndex(0)
        self.right_dock_inference_tab.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.image_variation_toolbox.setCurrentIndex(1)
        self.optimization_toolbox.setCurrentIndex(3)
        self.sb_tab_sub_r_train.setCurrentIndex(0)
        self.prompt_field.setCurrentIndex(0)
        self.left_tab_widget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(BasePurDi)

    # setupUi

    def retranslateUi(self, BasePurDi):
        BasePurDi.setWindowTitle(
            QCoreApplication.translate(
                "BasePurDi", "PurDi - AI Enhanced Image Generator & Editor", None
            )
        )
        # if QT_CONFIG(tooltip)
        BasePurDi.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.actionOpen.setText(QCoreApplication.translate("BasePurDi", "Open", None))
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(
            QCoreApplication.translate("BasePurDi", "Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("BasePurDi", "Save", None))
        # if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(
            QCoreApplication.translate("BasePurDi", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSettings.setText(
            QCoreApplication.translate("BasePurDi", "Settings", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionSettings.setShortcut(
            QCoreApplication.translate("BasePurDi", "Ctrl+Alt+Shift+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("BasePurDi", "Undo", None))
        # if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(
            QCoreApplication.translate("BasePurDi", "Ctrl+Z", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("BasePurDi", "Redo", None))
        # if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(
            QCoreApplication.translate("BasePurDi", "Ctrl+Shift+Z", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionFilters.setText(
            QCoreApplication.translate("BasePurDi", "Filters", None)
        )
        self.right_top_dock_widget.setWindowTitle(
            QCoreApplication.translate("BasePurDi", "Dock", None)
        )
        # if QT_CONFIG(tooltip)
        self.right_dock_inference_tab.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(accessibility)
        self.right_dock_inference_txt2img.setAccessibleName("")
        # endif // QT_CONFIG(accessibility)
        self.inference_general_setting.setTitle(
            QCoreApplication.translate("BasePurDi", "General", None)
        )
        self.width_label.setText(QCoreApplication.translate("BasePurDi", "W:", None))
        self.width_field.setInputMask("")
        self.width_field.setText(QCoreApplication.translate("BasePurDi", "512", None))
        self.width_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "768", None)
        )
        self.height_label.setText(QCoreApplication.translate("BasePurDi", "H:", None))
        self.height_field.setText(QCoreApplication.translate("BasePurDi", "512", None))
        self.height_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "768", None)
        )
        self.select_n_sample.setText("")
        self.select_n_sample.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "imgs to generate", None)
        )
        self.select_batch_size.setText("")
        self.select_batch_size.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "batch size", None)
        )
        # if QT_CONFIG(tooltip)
        self.select_seed.setToolTip(
            QCoreApplication.translate(
                "BasePurDi",
                "Leave blank to always use random seed for each image",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.select_seed.setText("")
        self.select_seed.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "seed", None)
        )
        self.random_seed.setText(
            QCoreApplication.translate("BasePurDi", "Random", None)
        )
        self.schedulers_label.setText(
            QCoreApplication.translate("BasePurDi", "Schedulers:", None)
        )
        self.cfg_label.setText(QCoreApplication.translate("BasePurDi", "CFG: ", None))
        self.cfg_field.setText(QCoreApplication.translate("BasePurDi", "6", None))
        self.cfg_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "7.0", None)
        )
        self.steps_label.setText(
            QCoreApplication.translate("BasePurDi", "Steps: ", None)
        )
        self.steps_field.setText(QCoreApplication.translate("BasePurDi", "20", None))
        self.steps_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "30", None)
        )
        self.img_options_setting.setTitle(
            QCoreApplication.translate("BasePurDi", "Options", None)
        )
        self.label_15.setText(
            QCoreApplication.translate(
                "BasePurDi", "Normal Text-to-Image with no options.", None
            )
        )
        self.txt2img_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_5),
            QCoreApplication.translate("BasePurDi", "Text-to-Image", None),
        )
        self.label_10.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Guides the generative model to modify the cross-attention values during image generation to attend to all subjects in the text.",
                None,
            )
        )
        self.label_18.setText(
            QCoreApplication.translate(
                "BasePurDi", "Max number of iterations to alter", None
            )
        )
        self.max_iter_to_alter_field.setText(
            QCoreApplication.translate("BasePurDi", "20", None)
        )
        self.attend_excite_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_2),
            QCoreApplication.translate("BasePurDi", "Attend And Excite", None),
        )
        self.label_11.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "MultiDiffusion, a unified framework that enables versatile and controllable image generation, using a pre-trained text-to-image diffusion model, without any further training or finetuning.",
                None,
            )
        )
        self.multidiffusion_panorama_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_3),
            QCoreApplication.translate("BasePurDi", "MultiDiffusion", None),
        )
        self.label_12.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Guides diffusion models to generate images with higher quality and coherence.",
                None,
            )
        )
        self.label_8.setText(
            QCoreApplication.translate(
                "BasePurDi", "Self-Attention Guidance Scale (0 - 1):", None
            )
        )
        self.sag_scale_field.setText(
            QCoreApplication.translate("BasePurDi", ".75", None)
        )
        # if QT_CONFIG(tooltip)
        self.self_attention_guidance_checkbox.setToolTip(
            QCoreApplication.translate("BasePurDi", "Self-Attention Guidance", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.self_attention_guidance_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_4),
            QCoreApplication.translate("BasePurDi", "Self-Attention Guidance", None),
        )
        self.right_dock_inference_tab.setTabText(
            self.right_dock_inference_tab.indexOf(self.right_dock_inference_txt2img),
            QCoreApplication.translate("BasePurDi", "text", None),
        )
        # if QT_CONFIG(tooltip)
        self.right_dock_inference_tab.setTabToolTip(
            self.right_dock_inference_tab.indexOf(self.right_dock_inference_txt2img),
            QCoreApplication.translate(
                "BasePurDi", "Text to Text Image Generation", None
            ),
        )
        # endif // QT_CONFIG(tooltip)
        self.img2img_container.setTitle(
            QCoreApplication.translate("BasePurDi", "Image to Image", None)
        )
        self.img2img_clear_btn.setText(
            QCoreApplication.translate("BasePurDi", "Clear", None)
        )
        self.img2img_options.setTitle(
            QCoreApplication.translate("BasePurDi", "Options", None)
        )
        self.img2img_deviation_percent.setText(
            QCoreApplication.translate(
                "BasePurDi", "Original Image Deviation (%)", None
            )
        )
        self.img2img_strength_field.setInputMask("")
        self.img2img_strength_field.setText(
            QCoreApplication.translate("BasePurDi", "75", None)
        )
        self.img2img_strength_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "75%", None)
        )
        self.img2img_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.page),
            QCoreApplication.translate("BasePurDi", "Image-to-Image", None),
        )
        self.label_19.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Enables conditional inputs like edge maps, segmentation maps, keypoints, etc for finer control of output image structure",
                None,
            )
        )
        self.controlnet_method_combobox.setItemText(
            0, QCoreApplication.translate("BasePurDi", "Canny Edge Detection", None)
        )
        self.controlnet_method_combobox.setItemText(
            1, QCoreApplication.translate("BasePurDi", "Depth Map Detection", None)
        )
        self.controlnet_method_combobox.setItemText(
            2, QCoreApplication.translate("BasePurDi", "HED Edge Detection", None)
        )
        self.controlnet_method_combobox.setItemText(
            3, QCoreApplication.translate("BasePurDi", "M-LSD Line Detection", None)
        )
        self.controlnet_method_combobox.setItemText(
            4, QCoreApplication.translate("BasePurDi", "OpenPose Bone Detection", None)
        )
        self.controlnet_method_combobox.setItemText(
            5, QCoreApplication.translate("BasePurDi", "Scribble", None)
        )
        self.controlnet_method_combobox.setItemText(
            6, QCoreApplication.translate("BasePurDi", "Semantic Segmentation", None)
        )

        # if QT_CONFIG(statustip)
        self.canny_low_threshold.setStatusTip(
            QCoreApplication.translate("BasePurDi", "Default is 100", None)
        )
        # endif // QT_CONFIG(statustip)
        self.canny_low_threshold.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Low Threshold", None)
        )
        # if QT_CONFIG(statustip)
        self.canny_high_threshold.setStatusTip(
            QCoreApplication.translate("BasePurDi", "Default is 200", None)
        )
        # endif // QT_CONFIG(statustip)
        self.canny_high_threshold.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "High Threshold", None)
        )
        self.canny_conditioning_scale.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Conditioning Scale", None)
        )
        self.controlnet_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.ControlNet),
            QCoreApplication.translate("BasePurDi", "ControlNet", None),
        )
        self.cycle_diffusion_label.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "A Text-Guided Image-to-Image Generation model proposed in Unifying Diffusion Models\u2019 Latent Space, with Applications to CycleDiffusion and Guidance by Chen Henry Wu, Fernando De la Torre. WARNING: Only 1.4 checkpoints",
                None,
            )
        )
        self.cycle_diffusion_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.cycle_diffusion_widget),
            QCoreApplication.translate("BasePurDi", "Cycle Diffusion", None),
        )
        self.label_9.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "A depth-guided diffusion model by CompVis, Stability AI, and LAION. It uses MiDas to infer depth based on an image.",
                None,
            )
        )
        self.depth_to_image_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.depth_to_image_widget),
            QCoreApplication.translate("BasePurDi", "Depth-to-Image", None),
        )
        self.img2img_image_variation_label.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Generate variations from an input image using a fine-tuned version of Stable Diffusion model by Justin Pinkney. Does not take text prompt into consideration.",
                None,
            )
        )
        self.img2img_image_variation_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.image_variation_widget),
            QCoreApplication.translate("BasePurDi", "Image Variation", None),
        )
        self.label_13.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "A method for editing images from human instructions: given an input image and a written instruction that tells the model what to do, our model follows these instructions to edit the image.",
                None,
            )
        )
        self.img_guidance_scale_label.setText(
            QCoreApplication.translate("BasePurDi", "Image Guidance Scale", None)
        )
        self.img_guidance_scale_field.setText(
            QCoreApplication.translate("BasePurDi", "2", None)
        )
        self.instruct_pix2pix_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.instruct_pix2pix_widget),
            QCoreApplication.translate("BasePurDi", "InstructPix2Pix", None),
        )
        self.label_16.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "A diffusion-based image-to-image approach that allows users to specify the edit direction on-the-fly and allows editing real and synthetic images while preserving the input image's structure",
                None,
            )
        )
        self.pix2pix_source_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Source Subject", None)
        )
        self.pix2pix_target_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Target Subject", None)
        )
        self.pix2pix_zero_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Enable", None)
        )
        self.image_variation_toolbox.setItemText(
            self.image_variation_toolbox.indexOf(self.page_6),
            QCoreApplication.translate("BasePurDi", "Pix2Pix Zero-shot", None),
        )
        self.right_dock_inference_tab.setTabText(
            self.right_dock_inference_tab.indexOf(self.right_dock_inference_img2img),
            QCoreApplication.translate("BasePurDi", "img", None),
        )
        # if QT_CONFIG(tooltip)
        self.right_dock_inference_tab.setTabToolTip(
            self.right_dock_inference_tab.indexOf(self.right_dock_inference_img2img),
            QCoreApplication.translate("BasePurDi", "Image to Image Generation", None),
        )
        # endif // QT_CONFIG(tooltip)
        self.optimization_options.setTitle(
            QCoreApplication.translate("BasePurDi", "Optimizations", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "For even additional memory savings, you can use a sliced version of attention that performs the computation in steps instead of all at once. Attention slicing is useful even if a batch size of just 1 is used - as long as the model uses more than one attention head. If there is more than one attention head the *QK^T* attention matrix can be computed sequentially for each head which can save a significant amount of memory.",
                None,
            )
        )
        self.attention_slicing_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Attention Slicing", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.attention_slicing_item),
            QCoreApplication.translate("BasePurDi", "Attention Slicing", None),
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "For additional memory savings, you can offload the weights to CPU and only load them to GPU when performing the forward pass.",
                None,
            )
        )
        self.model_cpu_offload_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Model CPU Offload", None)
        )
        self.label_17.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "This method works at the submodule level, not on whole models. This is the best way to minimize memory consumption, but inference is much slower due to the iterative nature of the process.",
                None,
            )
        )
        self.sequential_cpu_offload_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Sequential CPU Offload", None)
        )
        self.cpu_offload_disable.setText(
            QCoreApplication.translate("BasePurDi", "Disable", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.cpu_offload_item),
            QCoreApplication.translate("BasePurDi", "CPU Offload", None),
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "NVIDIA cuDNN supports many algorithms to compute a convolution. Autotuner runs a short benchmark and selects the kernel with the best performance on a given hardware for a given input size.",
                None,
            )
        )
        self.cudnn_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "cuDNN", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.cudnn_item),
            QCoreApplication.translate("BasePurDi", "cuDNN Auto-Tuner", None),
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "To save more GPU memory and get more speed, you can load and run the model weights directly in half precision. This involves loading the float16 version of the weights, which was saved to a branch named fp16, and telling PyTorch to use the float16 type when loading them:",
                None,
            )
        )
        self.half_precision_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "half-precision", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.half_precision_item),
            QCoreApplication.translate("BasePurDi", "Half Precision", None),
        )
        self.label_5.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Optimizes the bandwidth in the attention block for speed boost and memory efficiency. Requires PyTorch > 1.12, CUDA available, and xFormers",
                None,
            )
        )
        self.memory_efficient_attention_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Memory Efficient Attention", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.memory_efficient_item),
            QCoreApplication.translate(
                "BasePurDi", "Memory Efficient Attention - Xformer", None
            ),
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "On Ampere and later CUDA devices matrix multiplications and convolutions can use the TensorFloat32 (TF32) mode for faster but slightly less accurate computations. By default PyTorch enables TF32 mode for convolutions but not matrix multiplications, and unless a network requires full float32 precision we recommend enabling this setting for matrix multiplications, too. It can significantly speed up computations with typically negligible loss of numerical accuracy.",
                None,
            )
        )
        self.tf32_item_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "tf32", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.tf32_item),
            QCoreApplication.translate("BasePurDi", "TensorFloat32", None),
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "To decode large batches of images with limited VRAM, or to enable batches with 32 images or more, you can use sliced VAE decode that decodes the batch latents one image at a time.\n"
                "\n"
                "You likely want to couple this with enable_attention_slicing() or enable_xformers_memory_efficient_attention() to further minimize memory use.",
                None,
            )
        )
        self.sliced_vae_decode_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Sliced VAE", None)
        )
        self.optimization_toolbox.setItemText(
            self.optimization_toolbox.indexOf(self.sliced_vae_item),
            QCoreApplication.translate("BasePurDi", "Sliced VAE", None),
        )
        self.inference_general_options.setTitle(
            QCoreApplication.translate("BasePurDi", "General Options", None)
        )
        self.prompt_weight_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "Prompt Weighting", None)
        )
        self.latent_upscale_2x.setText(
            QCoreApplication.translate("BasePurDi", "2x Upscale", None)
        )
        self.nsfw_checkbox.setText(
            QCoreApplication.translate("BasePurDi", "NSFW", None)
        )
        self.right_dock_inference_tab.setTabText(
            self.right_dock_inference_tab.indexOf(self.right_dock_inference_general),
            QCoreApplication.translate("BasePurDi", "General", None),
        )
        self.right_dock_tab_widget.setTabText(
            self.right_dock_tab_widget.indexOf(self.right_dock_inference),
            QCoreApplication.translate("BasePurDi", "Inference", None),
        )
        # if QT_CONFIG(tooltip)
        self.right_dock_tab_widget.setTabToolTip(
            self.right_dock_tab_widget.indexOf(self.right_dock_inference),
            QCoreApplication.translate(
                "BasePurDi",
                "General parameters for inferencing and generating images",
                None,
            ),
        )
        # endif // QT_CONFIG(tooltip)
        self.sb_tab_sub_r_train.setTabText(
            self.sb_tab_sub_r_train.indexOf(self.train_dreambooth),
            QCoreApplication.translate("BasePurDi", "Dream Booth", None),
        )
        self.sb_tab_sub_r_train.setTabText(
            self.sb_tab_sub_r_train.indexOf(self.train_textual_inversion),
            QCoreApplication.translate("BasePurDi", "Textual", None),
        )
        self.sb_tab_sub_r_train.setTabText(
            self.sb_tab_sub_r_train.indexOf(self.train_lora),
            QCoreApplication.translate("BasePurDi", "LORA", None),
        )
        self.right_dock_tab_widget.setTabText(
            self.right_dock_tab_widget.indexOf(self.right_dock_train),
            QCoreApplication.translate("BasePurDi", "Train", None),
        )
        self.right_dock_tab_widget.setTabText(
            self.right_dock_tab_widget.indexOf(self.chat_mode),
            QCoreApplication.translate("BasePurDi", "Chat", None),
        )
        self.gb_general_layer.setTitle(
            QCoreApplication.translate("BasePurDi", "Layers", None)
        )
        self.label_20.setText(
            QCoreApplication.translate("BasePurDi", "Change Theme", None)
        )
        self.edit_theme_button.setText(
            QCoreApplication.translate("BasePurDi", "Edit Theme", None)
        )
        self.right_dock_tab_widget.setTabText(
            self.right_dock_tab_widget.indexOf(self.right_dock_general),
            QCoreApplication.translate("BasePurDi", "General", None),
        )
        self.prompt_positive_field.setPlainText("")
        self.prompt_positive_field.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "a shiba inu on the moon", None)
        )
        self.prompt_field.setTabText(
            self.prompt_field.indexOf(self.prompt_positive_tab),
            QCoreApplication.translate("BasePurDi", "+", None),
        )
        # if QT_CONFIG(tooltip)
        self.prompt_field.setTabToolTip(
            self.prompt_field.indexOf(self.prompt_positive_tab),
            QCoreApplication.translate("BasePurDi", "positive prompts", None),
        )
        # endif // QT_CONFIG(tooltip)
        self.prompt_negative_field.setDocumentTitle("")
        self.prompt_negative_field.setPlainText("")
        self.prompt_negative_field.setPlaceholderText(
            QCoreApplication.translate(
                "BasePurDi", "watermark, logo, disfigure... etc, etc", None
            )
        )
        self.prompt_field.setTabText(
            self.prompt_field.indexOf(self.prompt_negative_tab),
            QCoreApplication.translate("BasePurDi", "-", None),
        )
        # if QT_CONFIG(tooltip)
        self.prompt_field.setTabToolTip(
            self.prompt_field.indexOf(self.prompt_negative_tab),
            QCoreApplication.translate("BasePurDi", "negative prompts", None),
        )
        # endif // QT_CONFIG(tooltip)
        self.generate_button.setText(
            QCoreApplication.translate("BasePurDi", "Generate", None)
        )
        self.toolbar_left.setWindowTitle(
            QCoreApplication.translate("BasePurDi", "toolBar", None)
        )
        self.left_dock_widget.setWindowTitle(
            QCoreApplication.translate("BasePurDi", "Image Browser", None)
        )
        self.image_browser_search.setText("")
        self.image_browser_search.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Search", None)
        )
        self.image_browser_sort.setItemText(
            0, QCoreApplication.translate("BasePurDi", "Newest", None)
        )
        self.image_browser_sort.setItemText(
            1, QCoreApplication.translate("BasePurDi", "Oldest", None)
        )
        self.image_browser_sort.setItemText(
            2, QCoreApplication.translate("BasePurDi", "A - Z", None)
        )
        self.image_browser_sort.setItemText(
            3, QCoreApplication.translate("BasePurDi", "Z - A", None)
        )

        self.left_tab_widget.setTabText(
            self.left_tab_widget.indexOf(self.image_browser_widget),
            QCoreApplication.translate("BasePurDi", "Images", None),
        )
        self.bottom_prompts_search_bar_btn.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Search", None)
        )
        self.bottom_prompts_sort.setItemText(
            0, QCoreApplication.translate("BasePurDi", "A - Z", None)
        )
        self.bottom_prompts_sort.setItemText(
            1, QCoreApplication.translate("BasePurDi", "Z - A", None)
        )

        ___qtablewidgetitem = self.bottom_dock_prompts_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("BasePurDi", "Prompt", None)
        )
        ___qtablewidgetitem1 = self.bottom_dock_prompts_table.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BasePurDi", "1", None))
        ___qtablewidgetitem2 = self.bottom_dock_prompts_table.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BasePurDi", "2", None))
        ___qtablewidgetitem3 = self.bottom_dock_prompts_table.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BasePurDi", "3", None))
        ___qtablewidgetitem4 = self.bottom_dock_prompts_table.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("BasePurDi", "4", None))
        ___qtablewidgetitem5 = self.bottom_dock_prompts_table.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("BasePurDi", "5", None))
        ___qtablewidgetitem6 = self.bottom_dock_prompts_table.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("BasePurDi", "6", None))
        ___qtablewidgetitem7 = self.bottom_dock_prompts_table.verticalHeaderItem(6)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("BasePurDi", "7", None))
        ___qtablewidgetitem8 = self.bottom_dock_prompts_table.verticalHeaderItem(7)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("BasePurDi", "8", None))
        ___qtablewidgetitem9 = self.bottom_dock_prompts_table.verticalHeaderItem(8)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("BasePurDi", "9", None))
        ___qtablewidgetitem10 = self.bottom_dock_prompts_table.verticalHeaderItem(9)
        ___qtablewidgetitem10.setText(
            QCoreApplication.translate("BasePurDi", "10", None)
        )

        __sortingEnabled = self.bottom_dock_prompts_table.isSortingEnabled()
        self.bottom_dock_prompts_table.setSortingEnabled(False)
        ___qtablewidgetitem11 = self.bottom_dock_prompts_table.item(0, 0)
        ___qtablewidgetitem11.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "illustration of jupiter clouds by dan mumford, alien landscape and vegetation, epic scene, a lot of swirling clouds, high exposure, highly detailed, realistic, vibrant blue tinted colors, uhd",
                None,
            )
        )
        ___qtablewidgetitem12 = self.bottom_dock_prompts_table.item(1, 0)
        ___qtablewidgetitem12.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "illustration of jupiter clouds by dan mumford, alien landscape and vegetation, epic scene, a lot of swirling clouds, high exposure, highly detailed, realistic, vibrant blue tinted colors, uhd",
                None,
            )
        )
        ___qtablewidgetitem13 = self.bottom_dock_prompts_table.item(2, 0)
        ___qtablewidgetitem13.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "casa com arquitetura contempor\u00e2nea, com \u00e1rea de jardim, lago ornamental, dia ensolarado, imagem para capa de revista de arquitetura",
                None,
            )
        )
        ___qtablewidgetitem14 = self.bottom_dock_prompts_table.item(3, 0)
        ___qtablewidgetitem14.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "maximalist chaotic San Francisco, birds eye view, illustrated by Herg\u00e9, style of tin tin comics, pen and ink",
                None,
            )
        )
        ___qtablewidgetitem15 = self.bottom_dock_prompts_table.item(4, 0)
        ___qtablewidgetitem15.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "boy at cozy gaming control room in bedroom , massive , big screen, high tech , advanced , warzone, messy cluttered bedroom, cozy, nostalgic,",
                None,
            )
        )
        ___qtablewidgetitem16 = self.bottom_dock_prompts_table.item(5, 0)
        ___qtablewidgetitem16.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Vintage 60's cartoon style. cluttered bedroom interior; teenage youth inside a bedroom; by Hajime Sorayama, Greg Tocchini, Virgil Finlay, popart, colors, neon lights. line art.",
                None,
            )
        )
        ___qtablewidgetitem17 = self.bottom_dock_prompts_table.item(6, 0)
        ___qtablewidgetitem17.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Architectural digest photo of a maximalist bathroom living room with lots of flowers and plants, golden light, award winning masterpiece with incredible details big windows, highly detailed, harper's bazaar art, fashion magazine, smooth, sharp focus, 8 k, octane render",
                None,
            )
        )
        ___qtablewidgetitem18 = self.bottom_dock_prompts_table.item(7, 0)
        ___qtablewidgetitem18.setText(
            QCoreApplication.translate(
                "BasePurDi",
                "Cute and adorable cartoon rabbit baby, fantasy, dreamlike, surrealism, super cute, trending on artstation",
                None,
            )
        )
        self.bottom_dock_prompts_table.setSortingEnabled(__sortingEnabled)

        # if QT_CONFIG(tooltip)
        self.bottom_dock_prompts_table.setToolTip(
            QCoreApplication.translate(
                "BasePurDi", "Shows saved prompts that can be re-used", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.left_tab_widget.setTabText(
            self.left_tab_widget.indexOf(self.bottom_dock_prompts),
            QCoreApplication.translate("BasePurDi", "Prompts", None),
        )
        self.history_search_bar_btn.setPlaceholderText(
            QCoreApplication.translate("BasePurDi", "Search", None)
        )
        self.history_sort.setItemText(
            0, QCoreApplication.translate("BasePurDi", "A - Z", None)
        )
        self.history_sort.setItemText(
            1, QCoreApplication.translate("BasePurDi", "Z - A", None)
        )
        self.history_sort.setItemText(
            2, QCoreApplication.translate("BasePurDi", "Scheduler", None)
        )
        self.history_sort.setItemText(
            3, QCoreApplication.translate("BasePurDi", "Model", None)
        )

        ___qtablewidgetitem19 = self.img_history_table.horizontalHeaderItem(0)
        ___qtablewidgetitem19.setText(
            QCoreApplication.translate("BasePurDi", "prompt", None)
        )
        ___qtablewidgetitem20 = self.img_history_table.horizontalHeaderItem(1)
        ___qtablewidgetitem20.setText(
            QCoreApplication.translate("BasePurDi", "negative", None)
        )
        ___qtablewidgetitem21 = self.img_history_table.horizontalHeaderItem(2)
        ___qtablewidgetitem21.setText(
            QCoreApplication.translate("BasePurDi", "seed", None)
        )
        ___qtablewidgetitem22 = self.img_history_table.horizontalHeaderItem(3)
        ___qtablewidgetitem22.setText(
            QCoreApplication.translate("BasePurDi", "scheduler", None)
        )
        ___qtablewidgetitem23 = self.img_history_table.horizontalHeaderItem(4)
        ___qtablewidgetitem23.setText(
            QCoreApplication.translate("BasePurDi", "width", None)
        )
        ___qtablewidgetitem24 = self.img_history_table.horizontalHeaderItem(5)
        ___qtablewidgetitem24.setText(
            QCoreApplication.translate("BasePurDi", "height", None)
        )
        ___qtablewidgetitem25 = self.img_history_table.horizontalHeaderItem(6)
        ___qtablewidgetitem25.setText(
            QCoreApplication.translate("BasePurDi", "model", None)
        )
        ___qtablewidgetitem26 = self.img_history_table.verticalHeaderItem(0)
        ___qtablewidgetitem26.setText(
            QCoreApplication.translate("BasePurDi", "1", None)
        )
        ___qtablewidgetitem27 = self.img_history_table.verticalHeaderItem(1)
        ___qtablewidgetitem27.setText(
            QCoreApplication.translate("BasePurDi", "2", None)
        )
        ___qtablewidgetitem28 = self.img_history_table.verticalHeaderItem(2)
        ___qtablewidgetitem28.setText(
            QCoreApplication.translate("BasePurDi", "3", None)
        )
        ___qtablewidgetitem29 = self.img_history_table.verticalHeaderItem(3)
        ___qtablewidgetitem29.setText(
            QCoreApplication.translate("BasePurDi", "4", None)
        )
        ___qtablewidgetitem30 = self.img_history_table.verticalHeaderItem(4)
        ___qtablewidgetitem30.setText(
            QCoreApplication.translate("BasePurDi", "5", None)
        )
        ___qtablewidgetitem31 = self.img_history_table.verticalHeaderItem(5)
        ___qtablewidgetitem31.setText(
            QCoreApplication.translate("BasePurDi", "6", None)
        )
        ___qtablewidgetitem32 = self.img_history_table.verticalHeaderItem(6)
        ___qtablewidgetitem32.setText(
            QCoreApplication.translate("BasePurDi", "7", None)
        )
        ___qtablewidgetitem33 = self.img_history_table.verticalHeaderItem(7)
        ___qtablewidgetitem33.setText(
            QCoreApplication.translate("BasePurDi", "8", None)
        )
        ___qtablewidgetitem34 = self.img_history_table.verticalHeaderItem(8)
        ___qtablewidgetitem34.setText(
            QCoreApplication.translate("BasePurDi", "9", None)
        )
        ___qtablewidgetitem35 = self.img_history_table.verticalHeaderItem(9)
        ___qtablewidgetitem35.setText(
            QCoreApplication.translate("BasePurDi", "10", None)
        )
        self.left_tab_widget.setTabText(
            self.left_tab_widget.indexOf(self.history_widget),
            QCoreApplication.translate("BasePurDi", "History", None),
        )

    # retranslateUi
