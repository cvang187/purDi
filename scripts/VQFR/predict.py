import os.path
import cv2
import numpy as np
import torch.cuda
from basicsr.archs.rrdbnet_arch import RRDBNet
from cog import BasePredictor
from realesrgan import RealESRGANer
from scripts.VQFR.vqfr.demo_util import VQFR_Demo


class Predictor(BasePredictor):
    def __init__(
        self,
        model_dir: os.path = os.path.abspath("models"),
        output_dir: os.path = os.path.abspath("output"),
        upscale: bool = False
    ):
        self.restorer = None
        self.output_dir = output_dir
        self.model_dir = model_dir
        self.vqfr_name = "VQFR_v2"
        self.real_esrgan_name = "RealESRGAN_x2plus.pth"

        self.upscale_bg = upscale
        self.bg_upsampler = None
        self.scale = 2 if self.upscale_bg else 1
        self.arch = "v2"

        self.setup()

    def setup(
        self,
    ):
        # bg_upsampler = "realesrgan"
        bg_tile = 400
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=2,
        )

        if self.upscale_bg:
            real_esrgan_model_path = os.path.join(self.model_dir, self.real_esrgan_name)
            self.bg_upsampler = RealESRGANer(
                scale=self.scale,
                model_path=real_esrgan_model_path,
                model=model,
                tile=bg_tile,
                tile_pad=10,
                pre_pad=0,
                half=True if torch.cuda.is_available() else False,
            )

        model_path = os.path.join(self.model_dir, self.vqfr_name + ".pth")
        if not os.path.isfile(model_path):
            raise ValueError(f"Model {self.vqfr_name} does not exist.")

        self.restorer = VQFR_Demo(
            model_path=model_path, upscale=self.scale, arch=self.arch, bg_upsampler=self.bg_upsampler
        )

    def predict(self, image: str, fidelity_ratio: int = 0) -> np.ndarray:
        only_center_face = False
        input_img = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)

        cropped_faces, restored_faces, restored_img = self.restorer.enhance(
            input_img,
            fidelity_ratio=fidelity_ratio,
            has_aligned=False,
            only_center_face=only_center_face,
            paste_back=True,
        )
        return restored_img
