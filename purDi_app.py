# This Python file uses the following encoding: utf-8
import os.path

import numpy as np
from PIL import Image
import diffusers
import torch
from PySide6 import QtCore, QtGui
from PySide6.QtCore import (
    Qt,
    Slot,
    QSettings,
    QDir,
    QThreadPool,
    QSize,
    QRunnable,
)
from PySide6.QtGui import (
    QUndoStack,
    QStandardItemModel,
    QIcon,
    QMoveEvent,
    QPixmap,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QComboBox,
    QButtonGroup,
    QWidget,
    QMenu,
)
from compel import Compel
from qt_material import QtStyleTools

from gui.modules.PurDiCanvas import PurDiCanvasView, UndoRedoItemMoved
from gui.purDi_Actions import PurDiActions
from gui.ui_form import Ui_BasePurDi
from scripts.VQFR.predict import Predictor
from scripts.diffusers.stable_diffusion import StableDiffusion


class PurDiMainWindow(QMainWindow, QtStyleTools):
    """
    Main PurDi window. Connects the QGraphicsScene/QGraphicsView, QDockWidgets,
    Image Browser, etc. Also, mainly handles PySide's Signal() and Slots()
    related to the right dock widget slider bar and text field value changes.
    """

    def __init__(self):
        super().__init__()
        self.ui_loader = QUiLoader()
        self.ui_loader.load("gui/form.ui", self)
        self.ui = Ui_BasePurDi()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool(self)
        # self.sd_inference = StableDiffusion(self)
        self.pa = PurDiActions()
        self.settings = QSettings("PurDi", "PurDi")
        self.setWindowIcon(QIcon("gui/icons/app_icon.png"))
        self.setWindowOpacity(1)
        # self.m_widgets = {}

        # add PurDiCanvasView to main layout
        self.image_viewer = PurDiCanvasView(self)
        self.image_viewer.setStyleSheet("border-color: rgba(0, 0, 0, 0);")
        self.image_viewer.setParent(self.centralWidget())

        # toolbox widget
        # self.toolbox_dock_widget = PurDiToolBoxWidget(self)
        # self.toolbox_dock_widget.setParent(self.centralWidget())
        # self.toolbox_dock_widget.setVisible(False)  # hide toolbox
        # toggle_toolbox = self.toolbox_dock_widget.toggleViewAction()
        # self.ui.menu_bar.addAction(toggle_toolbox)

        # resizes image_viewer on window/widget move/updates
        self.image_viewer.scene.items_moved.connect(self.items_moved)

        # add icons to QTabWidgets' QTabs
        self.add_ui_icons()

        # TODO: add model selection to somewhere else
        # add model/textual inversion to the file menu bar
        self.select_model_drop_down_box = QComboBox()
        select_model_q_item_model = QStandardItemModel()
        self.select_model_drop_down_box.setModel(select_model_q_item_model)
        self.add_models_to_top_right_window()

        # status bar changes
        self.ui.status_bar.setVisible(False)
        self.ui.status_bar.setFixedHeight(30)

        # right sidebar settings
        self.ui.right_top_dock_widget.setTitleBarWidget(QWidget())

        # left sidebar settings
        self.ui.left_dock_widget.setTitleBarWidget(QWidget())
        self.ui.left_dock_widget.setMinimumWidth(325)

        self.menu_file = QMenu()
        self.menu_file_button = self.pa.create_toolbox_buttons(
            icon_path="gui/icons/feather/align-justify.svg",
            icon_txt="",
            icon_tool_tip="",
        )
        self.menu_file_button.setStyleSheet(
            """
            QPushButton::menu-indicator {
              width: 0px;
              height: 0px
            }
            
            QPushButton {
              border: 0px;
              icon-size: 50px 50px;
              padding-top: 20px;
            }
            """
        )
        self.ui.toolbar_left.addWidget(self.menu_file_button)
        self.ui.toolbar_left.setContentsMargins(0, 0, 0, 0)
        self.ui.toolbar_left.setFixedWidth(60)
        self.menu_file_button.setMenu(self.menu_file)
        # self.menu_file_button.setPopupMode(
        #     QToolButton.ToolButtonPopupMode.InstantPopup
        # )

        # self.menu_file.addAction('test', lambda: print('test'))
        self.menu_file.addAction(self.ui.actionOpen)
        self.menu_file.addAction(self.ui.actionSave)
        self.menu_file.addAction(self.ui.actionSettings)

        self.menu_edit = QMenu("Edit")
        self.undoStack = QUndoStack()
        self.menu_edit.addAction(
            self.undoStack.createUndoAction(self.image_viewer.scene)
        )
        self.menu_edit.addAction(
            self.undoStack.createRedoAction(self.image_viewer.scene)
        )

        self.menu_file.addMenu(self.menu_edit)

        self.ui.edit_theme_button.clicked.connect(lambda: self.show_dock_theme(self))

        # prompt widget overrides
        self.ui.prompt_field.setStyleSheet(
            """
            QTabBar, QPlainTextEdit {
                background-color: white; 
                border-color: white;  
                border: 0px; 
                border-radius: 0px
            }
            QWidget#right_bottom_dock_content{
                background-color: transparent;  
                border: 0px;
            }
            QTabBar::tab {color: gray;}
            QTabBar:selected {color: green }
            """
        )
        self.ui.prompt_field.setFixedHeight(100)

        # optimization tab group widget
        self.ui.optimization_options.setStyleSheet("border-color: rgba(0, 0, 0, 0);")

        self.ui.generate_img_progress.setVisible(False)

        # updates text fields upon slider bar value changes
        self.ui.width_slider_bar.valueChanged.connect(self.width_slider_value_changed)
        self.ui.height_slider_bar.valueChanged.connect(self.height_slider_value_changed)
        self.ui.cfg_slider_bar.valueChanged.connect(self.cfg_slider_value_changed)
        self.ui.steps_slider_bar.valueChanged.connect(self.steps_slider_value_changed)
        self.ui.img2img_strength_slider_bar.valueChanged.connect(
            self.i2i_strength_slider_value_changed
        )
        self.ui.img_guidance_slider_bar.valueChanged.connect(
            self.img_guidance_slider_value_changed
        )

        # updates slider bar values based on text fields upon "Enter" key press
        self.ui.width_field.returnPressed.connect(self.width_field_value_changed)
        self.ui.height_field.returnPressed.connect(self.height_field_value_changed)
        self.ui.cfg_field.returnPressed.connect(self.cfg_field_value_changed)
        self.ui.steps_field.returnPressed.connect(self.steps_field_value_changed)
        self.ui.img2img_strength_field.returnPressed.connect(
            self.i2i_strength_field_value_changed
        )
        self.ui.img_guidance_scale_field.returnPressed.connect(
            self.img_guidance_field_value_changed
        )

        try:
            from scripts.diffusers.available_schedulers import (
                euler,
                euler_a,
                dpm_multi,
                dpm_single,
                dpm_karras,
                dpm_karras_a,
                ddim,
                heun,
                lms,
                pndm,
                uni_pc_multistep,
            )
        except ModuleNotFoundError:
            print("Unable to import schedule modules")
        else:
            self.scheduler_options = [
                euler,
                euler_a,
                dpm_multi,
                dpm_single,
                dpm_karras,
                dpm_karras_a,
                ddim,
                heun,
                lms,
                pndm,
                uni_pc_multistep,
            ]

        # add diffuser sampler/schedulers to right side dock
        self.add_scheduler_to_drop_down_box()

        # generates random seed when random button is pressed in ui
        self.ui.random_seed.clicked.connect(
            lambda: self.ui.select_seed.setProperty(
                "text", torch.Generator("cuda").seed()
            )
        )

        # QButtonGroups for exclusive toggle per group
        self.cpu_offload_group = QButtonGroup()
        self.cpu_offload_group.addButton(self.ui.model_cpu_offload_checkbox)
        self.cpu_offload_group.addButton(self.ui.sequential_cpu_offload_checkbox)
        self.cpu_offload_group.addButton(self.ui.cpu_offload_disable)
        self.txt2img_option_group = QButtonGroup()
        self.txt2img_option_group.addButton(self.ui.txt2img_checkbox)
        self.txt2img_option_group.addButton(self.ui.attend_excite_checkbox)
        self.txt2img_option_group.addButton(self.ui.multidiffusion_panorama_checkbox)
        self.txt2img_option_group.addButton(self.ui.self_attention_guidance_checkbox)
        self.img2img_option_group = QButtonGroup()
        self.img2img_option_group.addButton(self.ui.img2img_checkbox)
        self.img2img_option_group.addButton(self.ui.cycle_diffusion_checkbox)
        self.img2img_option_group.addButton(self.ui.img2img_image_variation_checkbox)
        self.img2img_option_group.addButton(self.ui.instruct_pix2pix_checkbox)
        self.img2img_option_group.addButton(self.ui.inpaint_checkbox)
        self.img2img_option_group.addButton(self.ui.depth_to_image_checkbox)
        self.img2img_option_group.addButton(self.ui.pix2pix_zero_checkbox)
        self.img2img_option_group.addButton(self.ui.controlnet_checkbox)

        # right sidebar img2img box.
        self.ui.img2img_clear_btn.clicked.connect(
            lambda: self.ui.img2img_select_box.clear()
        )
        self.ui.img2img_container.setVisible(True)

        self.ui.generate_button.clicked.connect(self.inference)
        self.ui.image_browser.cache_updated.connect(
            self.ui.image_browser.append_items_to_view
        )
        self.image_viewer.image_processed.connect(self.ui.image_browser.generate_cache)

        self.full_screen = False

        attend_excite_pixmap = QPixmap("gui/images/txt2img/attend-excite.png")
        self.ui.attend_excite_pixmap.setPixmap(attend_excite_pixmap)
        multi_diffusion_pixmap = QPixmap("gui/images/txt2img/multi_diffusion.png")
        self.ui.multi_diffusion_pixmap.setPixmap(multi_diffusion_pixmap)
        vqfr_comparision_pixmap = QPixmap("gui/images/vqfr/comparison-small.jpg")
        self.ui.vqfr_pixmap.setPixmap(vqfr_comparision_pixmap)
        cycle_diffusion_pixmap = QPixmap("gui/images/img2img/cycle_diffusion.png")
        self.ui.cycle_diffusion_pixmap.setPixmap(cycle_diffusion_pixmap)
        image_variation_pixmap = QPixmap("gui/images/img2img/image-variations.jpg")
        self.ui.image_variations_pixmap.setPixmap(image_variation_pixmap)
        instruct_pix2pix_pixmap = QPixmap("gui/images/img2img/instruct_pix2pix.png")
        self.ui.instruct_pix2pix_pixmap.setPixmap(instruct_pix2pix_pixmap)
        zero_pix2pix_pixmap = QPixmap("gui/images/img2img/zero-pix2pix.png")
        self.ui.zero_pix2pix_pixmap.setPixmap(zero_pix2pix_pixmap)

        if os.path.exists("my_theme.xml"):
            self.apply_stylesheet(self, "my_theme.xml")
        else:
            self.apply_stylesheet(self, "dark_teal.xml")

    @Slot()
    def inference(self):
        inference_thread = StableDiffusionRunnable(self)
        if self.ui.generate_button.isChecked():
            self.threadpool.globalInstance().start(inference_thread)

    @Slot()
    def disable_generate_img_button(self):
        self.ui.generate_button.setChecked(True)
        self.ui.generate_button.setProperty("text", "Cancel")
        self.ui.generate_img_progress.setVisible(True)

    @Slot()
    def re_enable_generate_img_button(self):
        self.ui.generate_button.setChecked(False)
        self.ui.generate_button.setProperty("text", "Generate")
        self.ui.generate_img_progress.setVisible(False)

    def add_models_to_top_right_window(self) -> None:
        """
        Loops through diffuser models in models/diffusers path
        and adds their base name as selectable items in the QComboBox
        that is assigned to the top right of the main window.
        """
        model_dir = QDir("models")

        for index, model in enumerate(
            model_dir.entryInfoList(
                QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot, QDir.SortFlag.Name
            )
        ):
            file_path = model.absoluteFilePath()
            model_name = (
                model.baseName()
                .replace("--", " ")
                .replace("-", " ")
                .strip("models")
                .lower()
            )
            display_name = f"{model_name}"
            icon = QIcon("gui/icons/select_rect.svg")
            self.select_model_drop_down_box.addItem(icon, display_name)
            self.select_model_drop_down_box.setItemData(
                index, file_path, Qt.ItemDataRole.UserRole
            )

        # TODO: remove?
        excluded_models = ["controlnet", "lambdalabs sd image variations", "timbrooks"]
        for model in excluded_models:
            folder = self.select_model_drop_down_box.findText(
                model, Qt.MatchFlag.MatchContains
            ).__index__()
            self.select_model_drop_down_box.removeItem(folder)

    # TODO: pipe_line.scheduler.compatibles.
    #  In the future, replace with diffuser's own builtin. Previously it did not exist?
    def add_scheduler_to_drop_down_box(self) -> None:
        """
        Add available schedulers from Diffusers to a QComboBox with QIcon
        images that were generated per scheduler as an example

        PurDiDiffuserSchedulers('display_name', 'tool_tip', 'icon', 'module')
        """
        self.ui.scheduler_drop_down_box.setIconSize(QSize(75, 75))
        self.ui.scheduler_drop_down_box.setFixedHeight(100)
        self.ui.scheduler_drop_down_box.setMaxVisibleItems(5)

        for index, scheduler in enumerate(self.scheduler_options):
            self.ui.scheduler_drop_down_box.addItem(
                QIcon(scheduler.icon),
                scheduler.display_name,
            )
            self.ui.scheduler_drop_down_box.setItemData(
                index, scheduler.tool_tip, Qt.ItemDataRole.ToolTipRole
            )
            self.ui.scheduler_drop_down_box.setItemData(
                index, scheduler.module, Qt.ItemDataRole.UserRole
            )

        default = self.ui.scheduler_drop_down_box.findText("UniPC").__index__()
        self.ui.scheduler_drop_down_box.setCurrentIndex(default)

    @Slot()
    def img_guidance_field_value_changed(self) -> None:
        t_field = self.ui.img_guidance_scale_field.text()
        self.ui.img_guidance_slider_bar.setValue(int(t_field))

    @Slot()
    def img_guidance_slider_value_changed(self) -> None:
        s_field = self.ui.img_guidance_slider_bar.value()
        self.ui.img_guidance_scale_field.setProperty("text", s_field)

    @Slot()
    def i2i_strength_field_value_changed(self) -> None:
        t_field = self.ui.img2img_strength_field.text()
        self.ui.img2img_strength_slider_bar.setValue(int(t_field))

    @Slot()
    def i2i_strength_slider_value_changed(self) -> None:
        s_field = self.ui.img2img_strength_slider_bar.value()
        self.ui.img2img_strength_field.setProperty("text", s_field)

    @Slot()
    def width_field_value_changed(self) -> None:
        t_field = self.ui.width_field.text()
        self.ui.width_slider_bar.setValue(int(t_field))

    @Slot()
    def width_slider_value_changed(self) -> None:
        s_value = self.ui.width_slider_bar.value()
        self.ui.width_field.setProperty("text", s_value)

    @Slot()
    def height_field_value_changed(self) -> None:
        t_field = self.ui.height_field.text()
        self.ui.height_slider_bar.setValue(int(t_field))

    @Slot()
    def height_slider_value_changed(self) -> None:
        s_value = self.ui.height_slider_bar.value()
        self.ui.height_field.setProperty("text", s_value)

    @Slot()
    def cfg_field_value_changed(self) -> None:
        t_field = self.ui.cfg_field.text()
        self.ui.cfg_slider_bar.setValue(int(t_field))

    @Slot()
    def cfg_slider_value_changed(self) -> None:
        s_value = self.ui.cfg_slider_bar.value()
        self.ui.cfg_field.setProperty("text", s_value)

    @Slot()
    def steps_field_value_changed(self) -> None:
        t_field = self.ui.steps_field.text()
        self.ui.steps_slider_bar.setValue(int(t_field))

    @Slot()
    def steps_slider_value_changed(self) -> None:
        s_value = self.ui.steps_slider_bar.value()
        self.ui.steps_field.setProperty("text", s_value)

    @Slot()
    def items_moved(self, old_positions, new_positions) -> None:
        """
        Slot for undoing/redoing QGraphicsPixmapItem that were moved in the QGraphicsScene
        """
        self.undoStack.push(UndoRedoItemMoved(old_positions, new_positions))

    @Slot()
    def update_window_on_ui_changes(self) -> None:
        self.image_viewer.resize(self.centralWidget().size())
        # self.align_widget_to_canvas()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F11:
            if not self.full_screen:
                self.showFullScreen()
                self.full_screen = True
                return
            self.showNormal()
            self.full_screen = False

    def resizeEvent(self, event) -> None:
        self.update_window_on_ui_changes()

    def moveEvent(self, event: QMoveEvent) -> None:
        self.update_window_on_ui_changes()

    # possibly not needed anymore as the prompt field was moved back to the sidebar
    # instead of aligning to the bottom right of the canvas/central widget.

    # def add_fixed_widget_to_window(self, widget, alignment) -> None:
    #     """
    #     Set widgets' parent to centralWidget()
    #     """
    #     try:
    #         widget.setParent(self.centralWidget())
    #         self.m_widgets[widget] = alignment
    #     except ValueError:
    #         print("No widget to align")

    # def align_widget_to_canvas(self) -> None:
    #     """
    #     Any widget added with add_fixed_widget_to_window() will be aligned
    #     to its parent - self.centralWidget().size()
    #     """
    #     parent_widget = self.centralWidget().size()
    #     for widget, alignment in self.m_widgets.items():
    #         point = QtCore.QPoint()
    #
    #         if alignment & QtCore.Qt.AlignmentFlag.AlignHCenter:
    #             point.setX((parent_widget.width() - widget.width()) / 2)
    #         elif alignment & QtCore.Qt.AlignmentFlag.AlignRight:
    #             point.setX(parent_widget.width() - widget.width())
    #
    #         if alignment & QtCore.Qt.AlignmentFlag.AlignVCenter:
    #             point.setY((parent_widget.height() - widget.height()) / 2)
    #         elif alignment & QtCore.Qt.AlignmentFlag.AlignBottom:
    #             point.setY(parent_widget.height() - widget.height())
    #         widget.move(point)

    def add_ui_icons(self):
        inference_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/aperture.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_tab_widget.setTabIcon(0, inference_tab_icon)
        train_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/cpu.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_tab_widget.setTabIcon(1, train_tab_icon)
        chat_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/message-square.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_tab_widget.setTabIcon(2, chat_tab_icon)
        general_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/settings.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_tab_widget.setTabIcon(3, general_tab_icon)
        txt_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/align-right.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_inference_tab.setTabIcon(0, txt_tab_icon)
        image_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/image.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_inference_tab.setTabIcon(1, image_tab_icon)
        inf_general_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/battery-charging.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.right_dock_inference_tab.setTabIcon(2, inf_general_tab_icon)
        image_browser_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/grid.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.left_tab_widget.setTabIcon(0, image_browser_tab_icon)
        prompt_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/activity.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.left_tab_widget.setTabIcon(1, prompt_tab_icon)
        history_tab_icon = self.pa.set_icon_color(
            icon_path="gui/icons/feather/list.svg",
            replace_color="black",
            new_color="white",
        )
        self.ui.left_tab_widget.setTabIcon(2, history_tab_icon)


class StableDiffusionRunnable(QRunnable):
    """
    SD QRunnable used for QThreadpool to manage multi-threading so
    GUI does not freeze up when running inference.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.pipeline = StableDiffusion(parent)

        # User params from GUI
        self.positive = "a award winning painting of a house by the ocean"
        self.negative = ""
        self.width = 512
        self.height = 512
        self.n_images = 1
        self.n_batch = 1
        self.n_steps = 20
        self.scheduler = diffusers.DDIMScheduler
        self.cfg = 6
        self.i2i_list = []
        self.img2img_strength = 7.5

        self._base_dir = os.path.abspath("models")
        self.upscaler_dir = os.path.join(self._base_dir, "upscalers")
        self.output_dir = os.path.abspath("output")

        self.pipeline.img_started.connect(self.parent.disable_generate_img_button)
        self.pipeline.img_finished.connect(self.parent.re_enable_generate_img_button)
        self.pipeline.img_finished.connect(self.parent.ui.image_browser.generate_cache)
        self.pipeline.img_finished.connect(
            self.parent.image_viewer.scene.delete_latents_from_scene
        )

    def run(self):
        self.update_user_params()
        images = self.get_images()

        restore_face = Predictor(
            model_dir=self.upscaler_dir, output_dir=self.output_dir
        )

        for img in images:
            image = img[0]
            seed = img[1]
            if self.parent.ui.latent_upscale_2x.isChecked():
                image = self.latent_upscaler_2x(
                    prompt=self.positive, latent=img[0], steps=self.n_steps, seed=seed
                )

            self.parent.image_viewer.scene.show_image(image)
            image_name = f"I2I_{self.positive[:60]}"
            img_uri = self.save_images(image=image, seed=seed, name=image_name)

            restored_image = restore_face.predict(image=img_uri)
            self.parent.image_viewer.scene.show_image(restored_image)
            self.save_images(
                image=restored_image, seed=seed, name=image_name, suffix="vqfr"
            )

    def get_images(self):
        """
        Flow control for Stable Diffusion inference mode. Prioritize image-to-image methods first
        then falls back to text-to-image.
        """
        model_id = "stabilityai/stable-diffusion-2-1-base"
        pipe = diffusers.DiffusionPipeline.from_pretrained(model_id, cache_dir=self._base_dir)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=self.positive, negative=self.negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)
            _ = i

        if (
            self.parent.ui.img2img_select_box.count() >= 1
            or len(self.parent.image_viewer.scene.selectedItems()) >= 1
        ):
            if self.parent.ui.controlnet_checkbox.isChecked():
                controlnet_current_selection = (
                    self.parent.ui.controlnet_method_combobox.currentText()
                )
                canny = "Canny Edge Detection"
                depth_map = "Depth Map Detection"
                hed = "HED Edge Detection"
                mlsd = "M-LSD Line Detection"
                open_pose = "OpenPose Bone Detection"
                scribble = "Scribble"
                seg = "Semantic Segmentation"

                user_params = (
                    pos_prompt,
                    neg_prompt,
                    pos_emb,
                    neg_emb,
                    self.width,
                    self.height,
                    self.n_images,
                    self.n_batch,
                    self.n_steps,
                    self.scheduler,
                    self.cfg,
                    self.i2i_list
                )

                if controlnet_current_selection == canny:
                    self.pipeline.controlnet_canny(
                        user_params, callback=live_img_preview
                    )
                elif controlnet_current_selection == depth_map:
                    self.pipeline.controlnet_depth(
                        user_params, callback=live_img_preview
                    )
                elif controlnet_current_selection == hed:
                    self.pipeline.controlnet_hed(
                        user_params, callback=live_img_preview
                    )
                elif controlnet_current_selection == mlsd:
                    self.pipeline.controlnet_mlsd(
                        user_params, callback=live_img_preview
                    )
                elif controlnet_current_selection == open_pose:
                    self.pipeline.controlnet_openpose(
                        user_params, callback=live_img_preview
                    )
                elif controlnet_current_selection == scribble:
                    self.pipeline.controlnet_scribble(
                        user_params, callback=live_img_preview
                    )
                elif controlnet_current_selection == seg:
                    self.pipeline.controlnet_seg(
                        user_params, callback=live_img_preview
                    )

            elif self.parent.ui.img2img_image_variation_checkbox.isChecked():
                pipe = diffusers.StableDiffusionImageVariationPipeline.from_pretrained(
                    "lambdalabs/sd-image-variations-diffusers",
                    revision="v2.0",
                    cache_dir=self._base_dir,
                )

                return self.pipeline.img2img_variation(
                    width=self.width,
                    height=self.height,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    scheduler=self.scheduler,
                    cfg=self.cfg,
                    i2i_list=self.i2i_list,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            elif self.parent.ui.cycle_diffusion_checkbox.isChecked():
                model_id = "stabilityai/stable-diffusion-2-1-base"
                pipe = diffusers.CycleDiffusionPipeline.from_pretrained(
                    model_id, torch_dtype=torch.float16, cache_dir=self._base_dir
                )

                return self.pipeline.cycle_diffusion(
                    positive=self.positive,
                    negative=self.negative,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    cfg=self.cfg,
                    i2i_list=self.i2i_list,
                    strength=self.img2img_strength,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            elif self.parent.ui.instruct_pix2pix_checkbox.isChecked():
                img_guidance_scale = float(
                    self.parent.ui.img_guidance_scale_field.text()
                )
                pipe = diffusers.StableDiffusionInstructPix2PixPipeline.from_pretrained(
                    "timbrooks/instruct-pix2pix",
                    torch_dtype=torch.float16,
                    cache_dir=self._base_dir,
                )

                return self.pipeline.instruct_pix2pix(
                    pos_prompt=pos_prompt,
                    neg_prompt=neg_prompt,
                    pos_emb=pos_emb,
                    neg_emb=neg_emb,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    cfg=self.cfg,
                    i2i_list=self.i2i_list,
                    img_guidance=img_guidance_scale,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            elif self.parent.ui.pix2pix_zero_checkbox.isChecked():
                import transformers
                captioner_id = "Salesforce/blip-image-captioning-base"
                processor = transformers.BlipProcessor.from_pretrained(captioner_id)
                model = transformers.BlipForConditionalGeneration.from_pretrained(
                    captioner_id, torch_dtype=torch.float16, low_cpu_mem_usage=True
                )

                pipe = diffusers.StableDiffusionPix2PixZeroPipeline.from_pretrained(
                    "CompVis/stable-diffusion-v1-4",
                    torch_dtype=torch.float16,
                    caption_generator=model,
                    caption_processor=processor,
                    cache_dir=self._base_dir,
                )

                self.pipeline.pix2pix_zero_image(
                    width=self.width,
                    height=self.height,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    cfg=self.cfg,
                    i2i_list=self.i2i_list,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            elif self.parent.ui.inpaint_checkbox.isChecked():
                model_id = "stabilityai/stable-diffusion-2-inpainting"
                pipe = diffusers.StableDiffusionInpaintPipeline.from_pretrained(
                    model_id, torch_dtype=torch.float16, cache_dir=self._base_dir
                )

                return self.pipeline.inpaint(
                    pos_prompt=pos_prompt,
                    neg_prompt=neg_prompt,
                    pos_emb=pos_emb,
                    neg_emb=neg_emb,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    scheduler=self.scheduler,
                    cfg=self.cfg,
                    i2i_list=self.i2i_list,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            else:
                model_id = "stabilityai/stable-diffusion-2-1-base"
                pipe = diffusers.StableDiffusionImg2ImgPipeline.from_pretrained(
                    model_id, torch_dtype=torch.float16, cache_dir=self._base_dir
                )

                return self.pipeline.img2img(
                    pos_prompt=pos_prompt,
                    neg_prompt=neg_prompt,
                    pos_emb=pos_emb,
                    neg_emb=neg_emb,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    scheduler=self.scheduler,
                    cfg=self.cfg,
                    i2i_list=self.i2i_list,
                    strength=self.img2img_strength,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
        else:
            if self.parent.ui.multidiffusion_panorama_checkbox.isChecked():
                model_id = "CompVis/stable-diffusion-v1-4"
                pipe = diffusers.StableDiffusionPanoramaPipeline.from_pretrained(
                    model_id, torch_dtype=torch.float16, cache_dir=self._base_dir
                )
                pipe.scheduler = diffusers.DDIMScheduler.from_pretrained(
                    model_id, subfolder="scheduler"
                )

                return self.pipeline.multi_diffusion_panorama(
                    pos_prompt=pos_prompt,
                    neg_prompt=neg_prompt,
                    pos_emb=pos_emb,
                    neg_emb=neg_emb,
                    width=self.width,
                    height=self.height,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    cfg=self.cfg,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            elif self.parent.ui.self_attention_guidance_checkbox.isChecked():
                pipe = diffusers.StableDiffusionSAGPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-2-1-base",
                    torch_dtype=torch.float16,
                    cache_dir=self._base_dir,
                )

                return self.pipeline.self_attention_guidance(
                    positive=self.positive,
                    negative=self.negative,
                    width=self.width,
                    height=self.height,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    scheduler=self.scheduler,
                    cfg=self.cfg,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            elif self.parent.ui.attend_excite_checkbox.isChecked():
                model_id = "CompVis/stable-diffusion-v1-4"
                pipe = diffusers.StableDiffusionAttendAndExcitePipeline.from_pretrained(
                    model_id, torch_dtype=torch.float16, cache_dir=self._base_dir
                )
                max_alteration = int(self.parent.ui.max_iter_to_alter_field.text())

                self.pipeline.attend_and_excite(
                    pos_prompt=pos_prompt,
                    neg_prompt=neg_prompt,
                    pos_emb=pos_emb,
                    neg_emb=neg_emb,
                    width=self.width,
                    height=self.height,
                    n_image=self.n_images,
                    n_steps=self.n_steps,
                    scheduler=self.scheduler,
                    cfg=self.cfg,
                    max_alteration=max_alteration,
                    pipe=pipe,
                    live_preview=live_img_preview
                )
            else:
                # TODO: fix......
                base_path = os.path.abspath("models")
                full_path = os.path.join(base_path, "stable-diffusion-2-1")

                pipe = diffusers.StableDiffusionPipeline.from_pretrained(
                    full_path, torch_dtype=torch.float16
                )

                self.pipeline.txt2img(
                    pos_prompt=pos_prompt,
                    neg_prompt=neg_prompt,
                    pos_emb=pos_emb,
                    neg_emb=neg_emb,
                    width=self.width,
                    height=self.height,
                    n_image=self.n_images,
                    n_batch=self.n_batch,
                    n_steps=self.n_steps,
                    scheduler=self.scheduler,
                    cfg=self.cfg,
                    pipe=pipe,
                    live_preview=live_img_preview
                )

    def save_images(
        self, image, seed: int, name, suffix="", image_format=".png"
    ) -> str:
        """
        Utility method for saving images from Diffuser pipelines
        :param image: list[PIL.Image]
        :param seed: int from random_or_manual_seed()
        :param name: string variable
        :param suffix: additional text before file extension
        :param image_format:
        """
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        path = f"{self.output_dir}/{name.replace(' ', '_').replace(',', '')}_{seed}_{suffix}{image_format}"
        Image.Image.save(image, path)
        return path

    @staticmethod
    def latent_upscaler_2x(prompt, latent, steps, seed):
        upscaler = diffusers.StableDiffusionLatentUpscalePipeline.from_pretrained(
            "stabilityai/sd-x2-latent-upscaler", torch_dtype=torch.float16
        ).to("cuda")

        output_img = upscaler(
            prompt=prompt, image=latent, num_inference_steps=steps, generator=seed
        ).images
        return output_img

    def prompt_weight_embedding(self, pipe_line, positive, negative):
        """
        Generates text embeddings for use in most diffuser pipelines
        if prompt weighting is enabled in UI settings.
        """
        generate_embed = Compel(
            tokenizer=pipe_line.tokenizer, text_encoder=pipe_line.text_encoder
        )

        prompt_weight_enabled = self.parent.ui.prompt_weight_checkbox.isChecked()

        positive_text = positive if not prompt_weight_enabled else None
        negative_text = negative if not prompt_weight_enabled else None
        positive_emb = (
            generate_embed.build_conditioning_tensor(positive)
            if prompt_weight_enabled
            else None
        )
        negative_emb = (
            generate_embed.build_conditioning_tensor(negative)
            if prompt_weight_enabled
            else None
        )

        return positive_text, negative_text, positive_emb, negative_emb

    def update_user_params(self) -> None:
        """
        Returns a list of all user defined parameters from the right side dock of the main window.
        If a field is left blank, it will use the default value.
        """

        if len(self.parent.ui.prompt_positive_field.property("plainText")) != 0:
            self.positive = self.parent.ui.prompt_positive_field.property("plainText")

        if len(self.parent.ui.prompt_negative_field.property("plainText")) != 0:
            self.negative = self.parent.ui.prompt_negative_field.property("plainText")

        self.width = int(self.parent.ui.width_field.text())
        self.height = int(self.parent.ui.height_field.text())
        self.cfg = float(self.parent.ui.cfg_field.text())
        self.n_steps = int(self.parent.ui.steps_field.text())
        self.scheduler = self.parent.ui.scheduler_drop_down_box.currentData(
            Qt.ItemDataRole.UserRole
        )
        self.n_images = (
            int(self.parent.ui.select_n_sample.text())
            if len(self.parent.ui.select_n_sample.text()) >= 1
            else 1
        )
        self.n_batch = (
            int(self.parent.ui.select_batch_size.text())
            if len(self.parent.ui.select_batch_size.text()) >= 1
            else 1
        )

        # images selected in QGraphicsScene
        if len(self.parent.image_viewer.scene.selectedItems()) >= 1:
            for item in self.parent.image_viewer.scene.selectedItems():
                img = Image.fromqpixmap(item.pixmap())
                self.i2i_list.append(img)

        # images in top-right side img2img box
        elif self.parent.ui.img2img_select_box.count() >= 1:
            for index in range(self.parent.ui.img2img_select_box.count()):
                self.i2i_list.append(
                    self.parent.ui.img2img_select_box.item(index).text()
                )

        # images selected from left side image browser
        # elif len(self.parent.ui.image_browser.selectedIndexes()) >= 1:
        #     for index in self.parent.ui.image_browser.selectedIndexes():
        #         img = index.data(Qt.ItemDataRole.DisplayRole)
        #         image_list.append(img)

        self.img2img_strength = (
            float(self.parent.ui.img2img_strength_field.text()) / 100
        )


def main():
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)
    window = PurDiMainWindow()

    window.ui.right_top_dock_widget.setFixedWidth(400)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
