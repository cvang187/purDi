import os.path

import cv2
import numpy as np
from PIL.Image import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from cog import BasePredictor
from realesrgan import RealESRGANer

from scripts.VQFR.vqfr.demo_util import VQFR_Demo


class Predictor(BasePredictor):
    def __init__(
            self,
            model_dir: os.path = os.path.abspath('models'),
            output_dir: os.path = os.path.abspath('output'),
    ):
        self.restorer = None
        self.output_dir = output_dir
        self.model_dir = model_dir
        self.vqfr_name = "VQFR_v2"
        self.real_esrgan_name = "RealESRGAN_x2plus.pth"

        self.setup()

    def setup(self,):
        # bg_upsampler = "realesrgan"
        real_esrgan_model_path = os.path.join(self.model_dir, self.real_esrgan_name)
        bg_tile = 400
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=2,
        )
        bg_upsampler = RealESRGANer(
            scale=2,
            model_path=real_esrgan_model_path,
            model=model,
            tile=bg_tile,
            tile_pad=10,
            pre_pad=0,
            half=True,
        )  # need to set False in CPU mode

        arch = "v2"

        model_path = os.path.join(self.model_dir, self.vqfr_name + ".pth")
        if not os.path.isfile(model_path):
            raise ValueError(f"Model {self.vqfr_name} does not exist.")

        upscale = 2
        self.restorer = VQFR_Demo(
            model_path=model_path, upscale=upscale, arch=arch, bg_upsampler=bg_upsampler
        )

    # def predict(self, image: str, fidelity_ratio: int = 0):
    def predict(self, image: str, fidelity_ratio: int = 0) -> np.ndarray:
        only_center_face = False
        # input_img = cv2.imread(image, cv2.IMREAD_COLOR)
        # input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        input_img = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGBA)

        cropped_faces, restored_faces, restored_img = self.restorer.enhance(
            input_img,
            fidelity_ratio=fidelity_ratio,
            has_aligned=False,
            only_center_face=only_center_face,
            paste_back=True,
        )
        return restored_img
