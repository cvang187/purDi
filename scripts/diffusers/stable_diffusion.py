import os.path

import cv2
import diffusers
import numpy as np
import torch
import transformers
from PIL import Image
from PySide6.QtCore import Signal, QObject
from controlnet_aux import OpenposeDetector, HEDdetector, MLSDdetector
from diffusers import DDIMScheduler, DiffusionPipeline, SchedulerMixin, StableDiffusionAttendAndExcitePipeline, \
    StableDiffusionPanoramaPipeline, StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, \
    StableDiffusionInpaintPipeline, StableDiffusionInstructPix2PixPipeline, StableDiffusionImageVariationPipeline, \
    CycleDiffusionPipeline, StableDiffusionSAGPipeline, StableDiffusionPix2PixZeroPipeline
from torchvision.transforms import transforms
from typing import Union


class StableDiffusion(QObject):
    img_started = Signal()
    img_finished = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self._model_dir = os.path.abspath("models")
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._output_type = (
            "latent"
            if self.parent.ui.latent_upscale_checkbox.isChecked()
            or self.parent.ui.live_preview_checkbox.isChecked()
            else "pil"
        )
        torch.backends.cuda.matmul.allow_tf32 = (
            True if self.parent.ui.tf32_item_checkbox.isChecked() else False
        )
        self.results = []
        self._callback_step = 1

    @property
    def output_type(self):
        return self._output_type

    @property
    def device(self):
        return self._device

    def _controlnet(
        self,
        user_params: tuple,
        callback,
        network,
        processed_img,
        file_name: str,
        img_map_suffix="",
    ):
        """
        Controlnet
        """
        self.img_started.emit()
        self.results = []
        (
            pos_prompt,
            neg_prompt,
            pos_emb,
            neg_emb,
            width,
            height,
            n_image,
            n_batch,
            n_steps,
            scheduler,
            cfg,
            i2i_list,
        ) = user_params

        model_id = "runwayml/stable-diffusion-v1-5"
        pipe = diffusers.StableDiffusionControlNetPipeline.from_pretrained(
            model_id,
            controlnet=network,
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}",
        )
        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)
        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.sliced_vae_check(pipe)
        self.nsfw_check(pipe)

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)
            input_img = processed_img(initial_img)

            # saves image to be processed
            if self.parent.ui.save_controlnet_input_maps_checkbox.isChecked():
                # name = f"CN_{pos_prompt[:60]}"
                self.parent.save_images(
                    image=[input_img],
                    seed=0,
                    name=file_name,
                    suffix=img_map_suffix,
                )

            for n in range(n_image):
                seed = self.random_or_manual_seed("cpu")

                # TODO: replace width/height with conditionals
                image = pipe(
                    prompt=pos_prompt,
                    negative_prompt=neg_prompt,
                    prompt_embeds=pos_emb,
                    negative_prompt_embeds=neg_emb,
                    image=input_img,
                    width=None,
                    height=None,
                    num_inference_steps=n_steps,
                    num_images_per_prompt=n_batch,
                    generator=seed[0],
                    guidance_scale=cfg,
                    # output_type=self.output_type,
                    output_type="pil",
                    callback=None,
                    # callback=callback,
                    callback_steps=self._callback_step,
                    controlnet_conditioning_scale=1.0,
                ).images[0]
                self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def controlnet_canny(self, user_param: tuple, callback, img_file_name):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __image_prep(img):
            low_threshold = (
                int(self.parent.ui.canny_low_threshold.text())
                if len(self.parent.ui.canny_low_threshold.text()) >= 1
                else 100
            )
            high_threshold = (
                int(self.parent.ui.canny_high_threshold.text())
                if len(self.parent.ui.canny_high_threshold.text()) >= 1
                else 200
            )

            canny_img = np.array(img)
            canny_img = cv2.Canny(canny_img, low_threshold, high_threshold)
            canny_img = canny_img[:, :, None]
            canny_img = np.concatenate([canny_img, canny_img, canny_img], axis=2)
            output_img = Image.fromarray(canny_img)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__image_prep,
            file_name=img_file_name,
            img_map_suffix="_canny",
        )

    def controlnet_openpose(self, user_param: tuple, callback, img_file_name):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-openpose",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __image_prep(img):
            img_processor = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__image_prep,
            file_name=img_file_name,
            img_map_suffix="_openpose",
        )

    def controlnet_depth(self, user_param: tuple, callback, img_file_name):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-depth",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = transformers.pipeline("depth-estimation")
            depth_img = img_processor(img)["depth"]
            depth_img = np.array(depth_img)
            depth_img = depth_img[:, :, None]
            depth_img = np.concatenate([depth_img, depth_img, depth_img], axis=2)
            output_img = Image.fromarray(depth_img)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__img_prep,
            file_name=img_file_name,
            img_map_suffix="_depth",
        )

    def controlnet_hed(self, user_param: tuple, callback, img_file_name):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-hed",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = HEDdetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__img_prep,
            file_name=img_file_name,
            img_map_suffix="hed",
        )

    def controlnet_mlsd(self, user_param: tuple, callback, img_file_name):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-mlsd",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = MLSDdetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__img_prep,
            file_name=img_file_name,
            img_map_suffix="mlsd",
        )

    def controlnet_scribble(self, user_param: tuple, callback, img_file_name):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-scribble",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = HEDdetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__img_prep,
            file_name=img_file_name,
            img_map_suffix="scribble",
        )

    def controlnet_seg(self, user_param: tuple, callback, img_file_name):
        from scripts.diffusers.controlnet_utils import ade_palette

        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-seg",
            torch_dtype=torch.float16,
            cache_dir=f"{self._model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = transformers.AutoImageProcessor.from_pretrained(
                "openmmlab/upernet-convnext-small"
            )
            img_segmentor = transformers.UperNetForSemanticSegmentation.from_pretrained(
                "openmmlab/upernet-convnext-small"
            )
            pixel_values = img_processor(img, return_tensors="pt").pixel_values

            with torch.no_grad():
                outputs = img_segmentor(pixel_values)

            seg = img_processor.post_process_semantic_segmentation(
                outputs, target_sizes=[img.size[::-1]]
            )[0]
            color_seg = np.zeros(
                (seg.shape[0], seg.shape[1], 3), dtype=np.uint8
            )  # height, width, 3
            palette = np.array(ade_palette())

            for label, color in enumerate(palette):
                color_seg[seg == label, :] = color

            color_seg = color_seg.astype(np.uint8)

            output_img = Image.fromarray(color_seg)
            return output_img

        return self._controlnet(
            user_params=user_param,
            callback=callback,
            network=network_model,
            processed_img=__img_prep,
            file_name=img_file_name,
            img_map_suffix="seg",
        )

    def generate_embed_captions(self, sentences, tokenizer, text_encoder):
        """
        Utility method for generating embed captions for use with Pix2Pix-Zero
        :param sentences:
        :param tokenizer:
        :param text_encoder:
        """
        with torch.inference_mode():
            embeddings = []
            for sentence in sentences:
                text_inputs = tokenizer(
                    sentence,
                    padding="max_length",
                    max_length=tokenizer.model_max_length,
                    truncation=True,
                    return_tensors="pt",
                )
                text_input_ids = text_inputs.input_ids
                prompt_embeds = text_encoder(
                    text_input_ids.to(self.device), attention_mask=None
                )[0]
                embeddings.append(prompt_embeds)
        return torch.concatenate(embeddings, dim=0).mean(dim=0).unsqueeze(0)

    @staticmethod
    def generate_captions(input_prompt):
        """
        Utility method for generating captions for Pix2Pix-Zero
        :param input_prompt:
        """
        tokenizer = transformers.AutoTokenizer.from_pretrained("google/flan-t5-base")
        model = transformers.T5ForConditionalGeneration.from_pretrained(
            "google/flan-t5-base", device_map="auto", torch_dtype=torch.float16
        )

        with torch.inference_mode():
            input_ids = tokenizer(input_prompt, return_tensors="pt").input_ids.to(
                "cuda"
            )
            outputs = model.generate(
                input_ids,
                temperature=0.8,
                num_return_sequences=16,
                do_sample=True,
                max_new_tokens=128,
                top_k=10,
            )
        return tokenizer.batch_decode(outputs, skip_special_tokens=True)

    def pix2pix_zero_image(
        self,
        width: int = 512,
        height: int = 512,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        cfg: Union[int, float] = 6.5,
        i2i_list: list[str] = None,
        pipe: type[DiffusionPipeline] = StableDiffusionPix2PixZeroPipeline,
        live_preview=None,
    ):
        """
        Semi-working pix2pix
        TODO: fix or improve?
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = diffusers.DDIMScheduler.from_config(pipe.scheduler.config)
        pipe.inverse_scheduler = diffusers.DDIMInverseScheduler.from_config(
            pipe.scheduler.config
        )

        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.nsfw_check(pipe)

        w = width if not self.parent.ui.width_field == "" else None
        h = height if not self.parent.ui.height_field == "" else None

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)

            caption = pipe.generate_caption(initial_img)

            source_concept = self.parent.ui.pix2pix_source_field.text()
            target_concept = self.parent.ui.pix2pix_target_field.text()

            # source_caption = [caption]
            # target_caption = [caption.replace(source_concept, target_concept) for caption in source_caption]

            source_text = (
                f"Provide a caption for {caption}. "
                f"The captions should be in English and should be no longer than 150 characters"
            ).lower()
            source_caption = self.generate_captions(source_text)
            target_caption = [
                caption.replace(source_concept, target_concept).lower()
                for caption in source_caption
            ]

            source_embeddings = self.generate_embed_captions(
                source_caption, pipe.tokenizer, pipe.text_encoder
            )
            target_embeddings = self.generate_embed_captions(
                target_caption, pipe.tokenizer, pipe.text_encoder
            )
            # source_embeddings = pipe.get_embeds(source_caption, batch_size=2)
            # target_embeddings = pipe.get_embeds(target_caption, batch_size=2)

            print(f"caption: {caption}")
            print(f"source_caption: {source_caption}")
            print(f"target_caption: {target_caption}")

            generator = self.random_or_manual_seed("cpu")
            inverted_latent = pipe.invert(
                prompt=caption,
                image=initial_img,
                generator=generator[0][0],
                lambda_auto_corr=40.0,
                lambda_kl=20.0,
                num_reg_steps=5,
                num_auto_corr_rolls=5,
            ).latents

            for n in range(n_image):
                seed = self.random_or_manual_seed("cpu")
                image = pipe(
                    prompt=caption,
                    negative_prompt=caption,
                    source_embeds=source_embeddings,
                    target_embeds=target_embeddings,
                    width=w,
                    height=h,
                    num_inference_steps=n_steps,
                    guidance_scale=cfg,
                    num_images_per_prompt=n_batch,
                    cross_attention_guidance_amount=0.15,
                    generator=seed[0],
                    latents=inverted_latent,
                    output_type=self.output_type,
                    callback=live_preview,
                    callback_steps=self._callback_step,
                ).images[0]
                self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def self_attention_guidance(
        self,
        pos_prompt: str,
        neg_orompt: str,
        width: int = 512,
        height: int = 512,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        scheduler: type[SchedulerMixin] = DDIMScheduler,
        cfg: Union[int, float] = 6.5,
        pipe: type[DiffusionPipeline] = StableDiffusionSAGPipeline,
        live_preview=None,
    ):
        """
        Stable Diffusion - Self-Attention Guidance
        Does not work with prompt weighting
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)
        self.sliced_vae_check(pipe)
        self.sequential_cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        sag_scale = float(self.parent.ui.sag_scale_field.text())
        for n in range(n_image):
            seed = self.random_or_manual_seed(self.device)

            with torch.inference_mode():
                image = pipe(
                    prompt=pos_prompt,
                    negative_prompt=neg_orompt,
                    width=width,
                    height=height,
                    num_images_per_prompt=n_batch,
                    num_inference_steps=n_steps,
                    guidance_scale=cfg,
                    sag_scale=sag_scale if sag_scale <= 1.0 else 0.75,
                    generator=seed[0],
                    output_type=self.output_type,
                    latents=None,
                    callback=live_preview,
                    callback_steps=self._callback_step,
                ).images[0]
                self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def cycle_diffusion(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        cfg: Union[int, float] = 6.5,
        i2i_list: list[str] = None,
        strength: Union[int, float] = 0.75,
        pipe: type[DiffusionPipeline] = CycleDiffusionPipeline,
        live_preview=None,
    ):
        """
        Cycle Diffusion - text guided image-to-image variation pipe_line
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = diffusers.DDIMScheduler.from_config(pipe.scheduler.config)
        self.cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)

            for n in range(n_image):
                seed = self.random_or_manual_seed(self.device)

                # TODO: Use BLIP to generate source_prompt
                with torch.inference_mode():
                    image = pipe(
                        prompt=pos_prompt,
                        source_prompt=neg_prompt,
                        image=initial_img,
                        num_inference_steps=n_steps,
                        num_images_per_prompt=n_batch,
                        generator=seed[0],
                        strength=strength,
                        guidance_scale=cfg,
                        source_guidance_scale=1,
                        output_type="pil",
                        callback=live_preview,
                        callback_steps=self._callback_step,
                    ).images[0]
                self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def img2img_variation(
        self,
        width: int = 512,
        height: int = 512,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        scheduler: type[SchedulerMixin] = DDIMScheduler,
        cfg: Union[int, float] = 6.5,
        i2i_list: list[str] = None,
        pipe: type[DiffusionPipeline] = StableDiffusionImageVariationPipeline,
        live_preview=None,
    ):
        """
        Stable Diffusion image-to-image variation pipe_line.
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.sequential_cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Resize(
                    (224, 224),
                    interpolation=transforms.InterpolationMode.BICUBIC,
                    antialias=False,
                ),
                transforms.Normalize(
                    [0.48145466, 0.4578275, 0.40821073],
                    [0.26862954, 0.26130258, 0.27577711],
                ),
            ]
        )

        for img in i2i_list:
            initial_img = self.img2pillow(file=img).resize((width, height))

            for n in range(n_image):
                seed = self.random_or_manual_seed(self.device)

                with torch.inference_mode():
                    image_transformed = transform(initial_img).to("cuda").unsqueeze(0)
                    image = pipe(
                        image=image_transformed,
                        width=width if width <= 512 else None,
                        height=height if height <= 512 else None,
                        guidance_scale=cfg,
                        generator=seed[0],
                        num_images_per_prompt=n_batch,
                        num_inference_steps=n_steps,
                        output_type=self.output_type,
                        callback=live_preview,
                        callback_steps=self._callback_step,
                    ).images[0]
                    self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def instruct_pix2pix(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        pos_emb: torch.Tensor = None,
        neg_emb: torch.Tensor = None,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 29,
        cfg: Union[int, float] = 6.5,
        i2i_list: list[str] = None,
        img_guidance: Union[int, float] = 1.5,
        pipe: type[DiffusionPipeline] = StableDiffusionInstructPix2PixPipeline,
        live_preview=None
    ):
        """
        InstructPix2Pix human instruction image-to-image variations
        """
        self.img_started.emit()
        self.results = []

        self.cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        for n in range(n_image):
            for img in i2i_list:
                seed = self.random_or_manual_seed(self.device)
                initial_img = self.img2pillow(file=img)

                with torch.inference_mode():
                    image = pipe(
                        prompt=pos_prompt,
                        negative_prompt=neg_prompt,
                        prompt_embeds=pos_emb,
                        negative_prompt_embeds=neg_emb,
                        image=initial_img,
                        num_inference_steps=n_steps,
                        num_images_per_prompt=n_batch,
                        image_guidance_scale=img_guidance,
                        guidance_scale=cfg,
                        generator=seed[0],
                        output_type=self.output_type,
                        callback=live_preview,
                        callback_steps=self._callback_step,
                    ).images[0]
                    self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def inpaint(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        pos_emb: torch.Tensor = None,
        neg_emb: torch.Tensor = None,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        scheduler: type[SchedulerMixin] = DDIMScheduler,
        cfg: Union[int, float] = 6.5,
        i2i_list: list[str] = None,
        pipe: type[DiffusionPipeline] = StableDiffusionInpaintPipeline,
        live_preview=None,
    ):
        """
        Stable Diffusion image-to-image pipe_line. Images are saved in /output.
        """
        self.img_started.emit()
        self.results = []

        try:
            image_path = self.parent.ui.img2img_select_box.item(0).text()
            mask_img = Image.open(image_path).convert("RGB")
        except ValueError:
            raise ValueError("Inpainting needs a mask image")

        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.nsfw_check(pipe)

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)

            for n in range(n_image):
                seed = self.random_or_manual_seed(self.device)

                with torch.inference_mode():
                    image = pipe(
                        prompt=pos_prompt,
                        negative_prompt=neg_prompt,
                        prompt_embeds=pos_emb,
                        negative_prompt_embeds=neg_emb,
                        image=initial_img,
                        mask_image=mask_img,
                        width=mask_img.width,
                        height=mask_img.height,
                        num_images_per_prompt=n_batch,
                        num_inference_steps=n_steps,
                        guidance_scale=cfg,
                        generator=seed[0],
                        output_type=self.output_type,
                        callback=live_preview,
                        callback_steps=self._callback_step,
                    ).images[0]
                    self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def img2img(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        pos_emb: torch.Tensor = None,
        neg_emb: torch.Tensor = None,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        scheduler: type[SchedulerMixin] = DDIMScheduler,
        cfg: Union[int, float] = 6.5,
        i2i_list: list[str] = None,
        strength: float = 0.75,
        pipe: type[DiffusionPipeline] = StableDiffusionImg2ImgPipeline,
        live_preview=None,
    ):
        """
        Stable Diffusion image-to-image pipe_line. Images are saved in /output.
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.nsfw_check(pipe)

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)

            for n in range(n_image):
                seed = self.random_or_manual_seed(self.device)

                with torch.inference_mode():
                    image = pipe(
                        prompt=pos_prompt,
                        negative_prompt=neg_prompt,
                        prompt_embeds=pos_emb,
                        negative_prompt_embeds=neg_emb,
                        image=initial_img,
                        strength=strength,
                        num_images_per_prompt=n_batch,
                        num_inference_steps=n_steps,
                        guidance_scale=cfg,
                        generator=seed[0],
                        output_type=self.output_type,
                        callback=live_preview,
                        callback_steps=self._callback_step,
                    ).images[0]
                    self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def attend_and_excite(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        pos_emb: torch.Tensor = None,
        neg_emb: torch.Tensor = None,
        width: int = 512,
        height: int = 512,
        n_image: int = 1,
        n_steps: int = 20,
        scheduler: type[SchedulerMixin] = DDIMScheduler,
        cfg: Union[int, float] = 6.5,
        max_alteration: int = 20,
        pipe: type[DiffusionPipeline] = StableDiffusionAttendAndExcitePipeline,
        live_preview=None,
    ):
        """
        Attend & Excite, prompt emphasis for Stable Diffusion. Any word wrapped with
        single quotes '' will be attended and excited.
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.sequential_cpu_offload_check(pipe)
        self.sliced_vae_check(pipe)
        self.nsfw_check(pipe)

        # finds any words wrapped with single quote
        import re

        token_words = re.findall('"(.+?)"', pos_prompt)
        prompt = pos_prompt.replace('"', "")
        token_list = []
        indices = pipe.get_indices(prompt)
        for index, token in indices.items():
            for word in token_words:
                if word in token:
                    token_list.append(index)
        print(f"Indices: {indices}")
        print(f"Selected tokens: {token_list}")

        for n in range(n_image):
            seed = self.random_or_manual_seed(self.device)

            image = pipe(
                prompt=pos_prompt,
                negative_prompt=neg_prompt,
                prompt_embeds=pos_emb,
                negative_prompt_embeds=neg_emb,
                width=width if width <= 512 else None,
                height=height if height <= 512 else None,
                token_indices=token_list,
                guidance_scale=cfg,
                generator=seed[0],
                num_inference_steps=n_steps,
                max_iter_to_alter=max_alteration,
                output_type=self.output_type,
                callback=live_preview,
                callback_steps=self._callback_step,
            ).images[0]
            self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    def multi_diffusion_panorama(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        pos_emb: torch.Tensor = None,
        neg_emb: torch.Tensor = None,
        width: int = 512,
        height: int = 512,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        cfg: Union[int, float] = 6.5,
        pipe: type[DiffusionPipeline] = StableDiffusionPanoramaPipeline,
        live_preview=None,
    ):
        """
        Stable Diffusion Multi-Diffusion Panorama
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = DDIMScheduler.from_pretrained(
            pipe.model_id, subfolder="scheduler"
        )

        self.sequential_cpu_offload_check(pipe)
        self.sliced_vae_check(pipe)
        self.nsfw_check(pipe)

        for n in range(n_image):
            seed = self.random_or_manual_seed(self.device)

            with torch.inference_mode():
                image = pipe(
                    prompt=pos_prompt,
                    negative_prompt=neg_prompt,
                    prompt_embeds=pos_emb,
                    negative_prompt_embeds=neg_emb,
                    width=width,
                    height=height,
                    num_inference_steps=n_steps,
                    num_images_per_prompt=n_batch,
                    generator=seed[0],
                    guidance_scale=cfg,
                    output_type=self.output_type,
                    callback=live_preview,
                    callback_steps=self._callback_step,
                ).images[0]
                self.results.append([image, seed[1]])
        self.img_finished.emit()
        return self.results

    def txt2img(
        self,
        pos_prompt: str = "",
        neg_prompt: str = "",
        pos_emb: torch.Tensor = None,
        neg_emb: torch.Tensor = None,
        width: int = 512,
        height: int = 512,
        n_image: int = 1,
        n_batch: int = 1,
        n_steps: int = 20,
        scheduler: type[SchedulerMixin] = DDIMScheduler,
        cfg: Union[int, float] = 6.5,
        pipe: type[DiffusionPipeline] = StableDiffusionPipeline,
        live_preview=None,
    ):
        """
        Stable Diffusion text-to-image pipe_line. Images are saved in /output.
        """
        self.img_started.emit()
        self.results = []

        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.cpu_offload_check(pipe)
        self.sliced_vae_check(pipe)
        self.attention_slicing_check(pipe)
        self.nsfw_check(pipe)

        for n in range(n_image):
            seed = self.random_or_manual_seed(self.device)
            with torch.inference_mode():
                image = pipe(
                    prompt=pos_prompt,
                    negative_prompt=neg_prompt,
                    prompt_embeds=pos_emb,
                    negative_prompt_embeds=neg_emb,
                    width=width,
                    height=height,
                    num_images_per_prompt=n_batch,
                    num_inference_steps=n_steps,
                    guidance_scale=cfg,
                    generator=seed[0],
                    output_type=self.output_type,
                    callback=live_preview,
                    callback_steps=self._callback_step,
                ).images[0]
                self.results.append([image, seed[1]])

        self.img_finished.emit()
        return self.results

    @staticmethod
    def img2pillow(file):
        if isinstance(file, str):
            initial_img = Image.open(file)
        else:
            initial_img = file
        return initial_img

    def nsfw_check(self, pipe_line):
        if self.parent.ui.nsfw_checkbox.isChecked():
            pipe_line.register_to_config(safety_checker=None)

    def random_or_manual_seed(self, device) -> [list[torch.Generator], list[int]]:
        """
        Helper method to check if the seed text field is empty.
        If it is, implement workaround for random seed to return
        a torch.Generator as it is required by Diffusers pipelines
        instead of just INT
        :return: list[torch.Generator, int] int is appended to end of image file name
        """
        batch_size = (
            int(self.parent.ui.select_batch_size.text())
            if len(self.parent.ui.select_batch_size.text()) >= 1
            else 1
        )
        seed_generator_list = []
        seed_int_list = []

        # if seed is provided in GUI, use this - manual seed
        if len(self.parent.ui.select_seed.property("text")) >= 1:
            manual_seed = int(self.parent.ui.select_seed.property("text"))

            for index in range(batch_size):
                seed_int_list.append(manual_seed + index)
                seed_generator_list.append(
                    torch.Generator(device).manual_seed(manual_seed + index)
                )
            return seed_generator_list, seed_int_list

        # otherwise, generate a random seed per image in batch_size
        for _ in range(batch_size):
            random_seed = torch.Generator(device).seed()
            seed_int_list.append(random_seed)
            seed_generator_list.append(torch.Generator(device).manual_seed(random_seed))
        return seed_generator_list, seed_int_list

    @staticmethod
    def image_grid(
        images: list[Image], rows: int, columns: int, spacing: int = 20
    ) -> Image:
        """
        Arranges images into a user defined grid
        :param images: list consisting of PIL.Image(s)
        :param rows: number of images per row
        :param columns: number of images per column
        :param spacing: spacing between images in row/column
        """
        assert len(images) == rows * columns

        width, height = images[0].size
        grid = Image.new(
            "RGBA",
            size=(
                columns * width + (columns - 1) * spacing,
                rows * height + (rows - 1) * spacing,
            ),
            color=(255, 255, 255, 0),
        )
        for index, img in enumerate(images):
            grid.paste(
                img,
                box=(
                    index // rows * (width + spacing),
                    index % rows * (height + spacing),
                ),
            )
            print((index // rows * width, index % rows * height))
        return grid

    def cpu_offload_check(self, pipe_line: type[DiffusionPipeline]) -> None:
        """
        For additional memory savings, you can offload the weights to CPU and only load
        them to GPU when performing the forward pass.
        """
        if self.parent.ui.model_cpu_offload_checkbox.isChecked():
            pipe_line.enable_model_cpu_offload()
        elif self.parent.ui.sequential_cpu_offload_checkbox.isChecked():
            pipe_line.enable_sequential_cpu_offload()
        else:
            pipe_line.to(self.device)

    def sequential_cpu_offload_check(self, pipe_line: type[DiffusionPipeline]) -> None:
        """
        Some pipelines do not support enable_model_cpu_offload so,
        this method will cover those specific pipelines
        """
        if (
            self.parent.ui.sequential_cpu_offload_checkbox.isChecked()
            or self.parent.ui.model_cpu_offload_checkbox.isChecked()
        ):
            pipe_line.enable_sequential_cpu_offload()
        else:
            pipe_line.to(self.device)

    def sliced_vae_check(self, pipe_line: type[DiffusionPipeline]) -> None:
        """
        To decode large batches of images with limited V-RAM, or to enable batches with
        32 images or more, you can use sliced VAE decode that decodes the batch latents
        one image at a time.

        You likely want to couple this with enable_attention_slicing() or
        enable_xformers_memory_efficient_attention() to further minimize memory use.
        """
        if self.parent.ui.sliced_vae_decode_checkbox.isChecked():
            pipe_line.enable_vae_slicing()
        else:
            pipe_line.disable_vae_slicing()

    def attention_slicing_check(self, pipe_line: type[DiffusionPipeline]) -> None:
        """
        For even additional memory savings, you can use a sliced version of attention
        that performs the computation in steps instead of all at once.
        """
        if self.parent.ui.attention_slicing_checkbox.isChecked():
            pipe_line.enable_attention_slicing()
        else:
            pipe_line.disable_attention_slicing()
