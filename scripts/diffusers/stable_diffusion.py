import os.path

# import re

import cv2
import numpy as np
import torch
from PIL import Image
from PIL.ImageQt import fromqpixmap
from PySide6.QtCore import Qt, Signal, Slot, QObject
from compel import Compel
from controlnet_aux import OpenposeDetector, HEDdetector, MLSDdetector
from torchvision.transforms import transforms
import diffusers
import transformers


class StableDiffusion(QObject):
    img_started = Signal()
    img_finished = Signal()

    def __init__(self, parent=None):
        super(StableDiffusion, self).__init__()
        self.parent = parent
        self.model_dir = os.path.join(
            os.path.abspath(os.path.dirname("purDi")), "models"
        )
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_type = (
            "pil" if not self.parent.ui.latent_upscale_2x.isChecked() else "latent"
        )
        self.callback_step = 1

        torch.backends.cudnn.benchmark = (
            True if self.parent.ui.cudnn_checkbox.isChecked() else False
        )
        torch.backends.cuda.matmul.allow_tf32 = (
            True if self.parent.ui.tf32_item_checkbox.isChecked() else False
        )

    @property
    def current_model_selected(self):
        return self.parent.select_model_drop_down_box.currentData(
            Qt.ItemDataRole.UserRole
        )

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

    def _controlnet(self, network, processed_img, img_map_suffix=""):
        """
        Controlnet
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline("img2img")

        pipe = diffusers.StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=network,
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
        )
        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)
        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.sliced_vae_check(pipe)
        self.xformer_check(pipe)
        self.nsfw_check(pipe)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)
            input_img = processed_img(initial_img)

            # saves image to be processed
            if self.parent.ui.save_controlnet_input_maps_checkbox.isChecked():
                name = f"CN_{positive[:60]}"
                self.save_images(
                    image_list=[input_img],
                    seed_list=[0],
                    filename=name,
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
                    num_inference_steps=steps,
                    num_images_per_prompt=batch,
                    generator=seed[0],
                    guidance_scale=cfg,
                    output_type=self.output_type,
                    callback=live_img_preview,
                    callback_steps=self.callback_step,
                    controlnet_conditioning_scale=1.0,
                ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"CN_{positive[:60]}"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def controlnet_canny(self):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
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

        self._controlnet(
            network=network_model, processed_img=__image_prep, img_map_suffix="_canny"
        )

    @Slot()
    def controlnet_openpose(self):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-openpose",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
        )

        def __image_prep(img):
            img_processor = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        self._controlnet(
            network=network_model,
            processed_img=__image_prep,
            img_map_suffix="_openpose",
        )

    @Slot()
    def controlnet_depth(self):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-depth",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = transformers.pipeline("depth-estimation")
            depth_img = img_processor(img)["depth"]
            depth_img = np.array(depth_img)
            depth_img = depth_img[:, :, None]
            depth_img = np.concatenate([depth_img, depth_img, depth_img], axis=2)
            output_img = Image.fromarray(depth_img)
            return output_img

        self._controlnet(
            network=network_model, processed_img=__img_prep, img_map_suffix="_depth"
        )

    @Slot()
    def controlnet_hed(self):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-hed",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = HEDdetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        self._controlnet(
            network=network_model, processed_img=__img_prep, img_map_suffix="hed"
        )

    @Slot()
    def controlnet_mlsd(self):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-mlsd",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = MLSDdetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        self._controlnet(
            network=network_model, processed_img=__img_prep, img_map_suffix="mlsd"
        )

    @Slot()
    def controlnet_scribble(self):
        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-scribble",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
        )

        def __img_prep(img):
            img_processor = HEDdetector.from_pretrained("lllyasviel/ControlNet")
            output_img = img_processor(img)
            return output_img

        self._controlnet(
            network=network_model, processed_img=__img_prep, img_map_suffix="scribble"
        )

    @Slot()
    def controlnet_seg(self):
        from scripts.diffusers.controlnet_utils import ade_palette

        network_model = diffusers.ControlNetModel.from_pretrained(
            "fusing/stable-diffusion-v1-5-controlnet-seg",
            torch_dtype=torch.float16,
            cache_dir=f"{self.model_dir}/controlnet",
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

        self._controlnet(
            network=network_model, processed_img=__img_prep, img_map_suffix="seg"
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

    @Slot()
    def pix2pix_zero_image(self):
        """
        Semi-working pix2pix
        TODO: fix or improve?
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline(inference_type="img2img")

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
            cache_dir=self.model_dir,
        )
        pipe.scheduler = diffusers.DDIMScheduler.from_config(pipe.scheduler.config)
        pipe.inverse_scheduler = diffusers.DDIMInverseScheduler.from_config(
            pipe.scheduler.config
        )

        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.nsfw_check(pipe)

        w = width if not self.parent.ui.width_field == "" else None
        h = height if not self.parent.ui.height_field == "" else None

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

        for img in i2i_list:
            # initial_img = self.img2pillow(file=img).resize((width, height))
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
                    num_inference_steps=steps,
                    guidance_scale=cfg,
                    num_images_per_prompt=batch,
                    cross_attention_guidance_amount=0.15,
                    generator=seed[0],
                    latents=inverted_latent,
                    output_type=self.output_type,
                    callback=live_img_preview,
                    callback_steps=self.callback_step,
                ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"P2P_{caption[:60]}"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def self_attention_guidance(self):
        """
        Stable Diffusion - Self-Attention Guidance
        Does not work with prompt weighting
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
        ) = self.user_params_for_pipeline()

        pipe = diffusers.StableDiffusionSAGPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1-base",
            torch_dtype=torch.float16,
            cache_dir=self.model_dir,
        )
        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)
        self.sliced_vae_check(pipe)
        self.sequential_cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

        sag_scale = float(self.parent.ui.sag_scale_field.text())
        for n in range(n_image):
            seed = self.random_or_manual_seed(self.device)

            with torch.inference_mode():
                image = pipe(
                    prompt=positive,
                    negative_prompt=negative,
                    width=width,
                    height=height,
                    num_images_per_prompt=batch,
                    num_inference_steps=steps,
                    guidance_scale=cfg,
                    sag_scale=sag_scale if sag_scale <= 1.0 else 0.75,
                    generator=seed[0],
                    output_type=self.output_type,
                    latents=None,
                    callback=live_img_preview,
                    callback_steps=self.callback_step,
                ).images

            if self.parent.ui.latent_upscale_2x.isChecked():
                image = self.latent_upscaler_2x(
                    prompt=positive, latent=image, steps=steps, seed=seed[0]
                )

            name = f"SAG_{positive[:60]}"
            self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def cycle_diffusion(self):
        """
        Cycle Diffusion - text guided image-to-image variation pipe_line
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline(inference_type="img2img")

        # TODO: should works with any version of Stable Diffusion but 2-1-768 gets OOM Error on 3080
        model_id = "stabilityai/stable-diffusion-2-1-base"
        pipe = diffusers.CycleDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, cache_dir=self.model_dir
        )
        pipe.scheduler = diffusers.DDIMScheduler.from_config(pipe.scheduler.config)
        self.cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

        for img in i2i_list:
            initial_img = self.img2pillow(file=img)

            for n in range(n_image):
                seed = self.random_or_manual_seed(self.device)

                # TODO: Use BLIP to generate source_prompt
                with torch.inference_mode():
                    image = pipe(
                        prompt=positive,
                        source_prompt=negative,
                        image=initial_img,
                        num_inference_steps=steps,
                        num_images_per_prompt=batch,
                        generator=seed[0],
                        strength=strength,
                        guidance_scale=cfg,
                        source_guidance_scale=1,
                        output_type=self.output_type,
                        callback=live_img_preview,
                        callback_steps=self.callback_step,
                    ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"CD_{positive[:60]}"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def img2img_variation(self):
        """
        Stable Diffusion image-to-image variation pipe_line.
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline(inference_type="img2img")

        pipe = diffusers.StableDiffusionImageVariationPipeline.from_pretrained(
            "lambdalabs/sd-image-variations-diffusers",
            revision="v2.0",
            cache_dir=self.model_dir,
        )
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

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

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
                        num_images_per_prompt=batch,
                        num_inference_steps=steps,
                        output_type=self.output_type,
                        callback=live_img_preview,
                        callback_steps=self.callback_step,
                    ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"IV"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def instruct_pix2pix(self):
        """
        InstructPix2Pix human instruction image-to-image variations
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline(inference_type="img2img")
        img_guidance_scale = float(self.parent.ui.img_guidance_scale_field.text())

        pipe = diffusers.StableDiffusionInstructPix2PixPipeline.from_pretrained(
            "timbrooks/instruct-pix2pix",
            torch_dtype=torch.float16,
            cache_dir=self.model_dir,
        )

        self.cpu_offload_check(pipe)
        self.nsfw_check(pipe)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

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
                        num_inference_steps=steps,
                        num_images_per_prompt=batch,
                        image_guidance_scale=img_guidance_scale,
                        guidance_scale=cfg,
                        generator=seed[0],
                        output_type=self.output_type,
                        callback=live_img_preview,
                        callback_steps=self.callback_step,
                    ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"IP2P_{positive[:60]}"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def inpaint(self):
        """
        Stable Diffusion image-to-image pipe_line. Images are saved in /output.
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline(inference_type="img2img")

        try:
            mask_img = self.parent.ui.img2img_select_box.item(0).text()
            print(mask_img)
            mask_img = Image.open(mask_img).convert("RGB")
            print(mask_img.size)
        except ValueError:
            raise ValueError("Inpainting needs a mask image")

        model_id = "stabilityai/stable-diffusion-2-inpainting"
        # model_id = "runwayml/stable-diffusion-inpainting"
        pipe = diffusers.StableDiffusionInpaintPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, cache_dir=self.model_dir
        )
        # pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.xformer_check(pipe)
        self.nsfw_check(pipe)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

        for img in i2i_list:
            # TODO: fix issue
            # initial_img = self.img2pillow(file=img)
            dir = os.path.abspath("output")
            initial_img = Image.open(os.path.join(dir, "init.png"))

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
                        num_images_per_prompt=batch,
                        num_inference_steps=steps,
                        guidance_scale=cfg,
                        generator=seed[0],
                        output_type=self.output_type,
                        callback=live_img_preview,
                        callback_steps=self.callback_step,
                    ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"I2I_{positive[:60]}"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def img2img(self):
        """
        Stable Diffusion image-to-image pipe_line. Images are saved in /output.
        """
        self.img_started.emit()
        (
            positive,
            negative,
            _,
            _,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
            i2i_list,
            strength,
        ) = self.user_params_for_pipeline(inference_type="img2img")

        model_id = "stabilityai/stable-diffusion-2-1-base"
        pipe = diffusers.StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, cache_dir=self.model_dir
        )
        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.cpu_offload_check(pipe)
        self.attention_slicing_check(pipe)
        self.xformer_check(pipe)
        self.nsfw_check(pipe)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

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
                        num_images_per_prompt=batch,
                        num_inference_steps=steps,
                        guidance_scale=cfg,
                        generator=seed[0],
                        output_type=self.output_type,
                        callback=live_img_preview,
                        callback_steps=self.callback_step,
                    ).images

                if self.parent.ui.latent_upscale_2x.isChecked():
                    image = self.latent_upscaler_2x(
                        prompt=positive, latent=image, steps=steps, seed=seed[0]
                    )

                name = f"I2I_{positive[:60]}"
                self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def attend_and_excite(self):
        """
        Attend & Excite, prompt emphasis for Stable Diffusion. Any word wrapped with
        single quotes '' will be attended and excited.
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
        ) = self.user_params_for_pipeline()
        max_alteration = int(self.parent.ui.max_iter_to_alter_field.text())

        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = diffusers.StableDiffusionAttendAndExcitePipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, cache_dir=self.model_dir
        )
        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.sequential_cpu_offload_check(pipe)
        self.sliced_vae_check(pipe)
        self.nsfw_check(pipe)

        # finds any words wrapped with single quote
        import re

        token_words = re.findall('"(.+?)"', positive)
        prompt = positive.replace('"', "")
        token_list = []
        indices = pipe.get_indices(prompt)
        for index, token in indices.items():
            for word in token_words:
                if word in token:
                    token_list.append(index)
        print(f"Indices: {indices}")
        print(f"Selected tokens: {token_list}")

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

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
                num_inference_steps=steps,
                max_iter_to_alter=max_alteration,
                output_type=self.output_type,
                callback=live_img_preview,
                callback_steps=self.callback_step,
            ).images

            if self.parent.ui.latent_upscale_2x.isChecked():
                image = self.latent_upscaler_2x(
                    prompt=positive, latent=image, steps=steps, seed=seed[0]
                )

            strip_quotes = positive.replace('"', "")
            name = f"AE_{strip_quotes[:60]}"
            self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def multi_diffusion_panorama(self):
        """
        Stable Diffusion Multi-Diffusion Panorama
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
        ) = self.user_params_for_pipeline()

        model_id = "CompVis/stable-diffusion-v1-4"
        pipe = diffusers.StableDiffusionPanoramaPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, cache_dir=self.model_dir
        )
        pipe.scheduler = diffusers.DDIMScheduler.from_pretrained(
            model_id, subfolder="scheduler"
        )

        self.sequential_cpu_offload_check(pipe)
        self.sliced_vae_check(pipe)
        self.nsfw_check(pipe)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

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
                    num_inference_steps=steps,
                    num_images_per_prompt=batch,
                    generator=seed[0],
                    guidance_scale=cfg,
                    output_type=self.output_type,
                    callback=live_img_preview,
                    callback_steps=self.callback_step,
                ).images

            if self.parent.ui.latent_upscale_2x.isChecked():
                image = self.latent_upscaler_2x(
                    prompt=positive, latent=image, steps=steps, seed=seed[0]
                )

            name = f"MD_{positive[:60]}"
            self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @Slot()
    def txt2img(self):
        """
        Stable Diffusion text-to-image pipe_line. Images are saved in /output.
        """
        self.img_started.emit()
        (
            positive,
            negative,
            width,
            height,
            n_image,
            batch,
            scheduler,
            cfg,
            steps,
        ) = self.user_params_for_pipeline()

        # TODO: fix......
        base_path = os.path.abspath("models")
        full_path = os.path.join(base_path, "stable-diffusion-2-1")

        pipe = diffusers.StableDiffusionPipeline.from_pretrained(
            full_path, torch_dtype=torch.float16
        )
        pipe.scheduler = scheduler.from_config(pipe.scheduler.config)

        self.cpu_offload_check(pipe)
        self.sliced_vae_check(pipe)
        self.attention_slicing_check(pipe)
        self.xformer_check(pipe)
        self.nsfw_check(pipe)

        pos_prompt, neg_prompt, pos_emb, neg_emb = self.prompt_weight_embedding(
            pipe_line=pipe, positive=positive, negative=negative
        )

        def live_img_preview(i, t, latents):
            img = pipe.decode_latents(latents)
            img = img.squeeze()
            self.parent.ui.generate_img_progress.setValue(t)
            self.parent.image_viewer.scene.show_image(img, is_latent=True)

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
                    num_images_per_prompt=batch,
                    num_inference_steps=steps,
                    guidance_scale=cfg,
                    generator=seed[0],
                    output_type=self.output_type,
                    callback=live_img_preview,
                    callback_steps=self.callback_step,
                ).images

            if self.parent.ui.latent_upscale_2x.isChecked():
                image = self.latent_upscaler_2x(
                    prompt=positive, latent=image, steps=steps, seed=seed[0]
                )

            name = f"t2i_{positive[:60]}"
            self.save_images(image_list=image, seed_list=seed[1], filename=name)

        self.img_finished.emit()

    @staticmethod
    def latent_upscaler_2x(prompt, latent, steps, seed):
        upscaler = diffusers.StableDiffusionLatentUpscalePipeline.from_pretrained(
            "stabilityai/sd-x2-latent-upscaler", torch_dtype=torch.float16
        ).to("cuda")

        output_img = upscaler(
            prompt=prompt, image=latent, num_inference_steps=steps, generator=seed
        ).images
        return output_img

    @staticmethod
    def img2pillow(file):
        if isinstance(file, str):
            initial_img = Image.open(file).convert("RGB")
        else:
            initial_img = file.convert("RGB")
        return initial_img

    def nsfw_check(self, pipe_line):
        if self.parent.ui.nsfw_checkbox.isChecked():
            pipe_line.register_to_config(safety_checker=None)

    def save_images(
        self, image_list: list[Image], seed_list: list[int], filename, suffix=""
    ) -> None:
        """
        Utility method for saving images from Diffuser pipelines
        :param image_list: list[PIL.Image]
        :param seed_list: int from random_or_manual_seed()
        :param filename: string variable
        :param suffix: additional text before file extension
        """
        image_format = ".png"
        for image, seed in zip(image_list, seed_list):
            self.parent.image_viewer.scene.show_image(image)
            path = f"output/{filename.replace(' ', '_').replace(',', '')}_{seed}_{suffix}{image_format}"
            Image.Image.save(image, path)
            # print(f"Image saved as: {path}")

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

    def cpu_offload_check(self, pipe_line):
        """
        For additional memory savings, you can offload the weights to CPU and only load
        them to GPU when performing the forward pass.
        """
        if self.parent.ui.model_cpu_offload_checkbox.isChecked():
            pipe_line.enable_model_cpu_offload()
        elif self.parent.ui.sequential_cpu_offload_checkbox.isChecked():
            pipe_line.enable_sequential_cpu_offload()
        else:
            pipe_line.to("cuda")

    def sequential_cpu_offload_check(self, pipe_line):
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
            pipe_line.to("cuda")

    def sliced_vae_check(self, pipe_line):
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

    def attention_slicing_check(self, pipe_line):
        """
        For even additional memory savings, you can use a sliced version of attention
        that performs the computation in steps instead of all at once.
        """
        if self.parent.ui.attention_slicing_checkbox.isChecked():
            pipe_line.enable_attention_slicing()
        else:
            pipe_line.disable_attention_slicing()

    def xformer_check(self, pipe_line):
        """
        Conditional checks to enable memory efficient attention or if able,
        xformers memory efficient attention
        """
        # if "2.1.0" not in torch.version.__version__:
        #     try:
        #         import xformers
        #         from xformers.ops import MemoryEfficientAttentionFlashAttentionOp
        #     except ModuleNotFoundError:
        #         print("xformers library not found. Please try installing xformers again")
        #     else:
        #         if self.parent.ui.memory_efficient_attention_checkbox.isChecked():
        #             pipe_line.enable_xformers_memory_efficient_attention(
        #                 attention_op=MemoryEfficientAttentionFlashAttentionOp
        #             )
        #             pipe_line.vae.enable_xformers_memory_efficient_attention(
        #                 attention_op=None
        #             )
        #             print("xFormers Memory Efficient Attention")
        #         elif (
        #                 self.parent.ui.memory_efficient_attention_checkbox.isChecked()
        #                 and self.parent.ui.attention_slicing_checkbox.isChecked()
        #         ):
        #             pipe_line.enable_xformers_memory_efficient_attention()
        #             print("Memory Efficient Attention")
        #         else:
        #             pipe_line.disable_xformers_memory_efficient_attention()
        pass

    def user_params_for_pipeline(self, inference_type: str = None) -> list:
        """
        Returns a list of all user defined parameters from the right side dock of the main window.
        If a field is left blank, it will use the default value.
        :param inference_type: 'img2img' else None defaults to txt2img
        """

        if len(self.parent.ui.prompt_positive_field.property("plainText")) == 0:
            user_positive_prompt = "a award winning painting of a house by the ocean"
        else:
            user_positive_prompt = self.parent.ui.prompt_positive_field.property(
                "plainText"
            )

        if len(self.parent.ui.prompt_negative_field.property("plainText")) == 0:
            user_negative_prompt = ""
        else:
            user_negative_prompt = self.parent.ui.prompt_negative_field.property(
                "plainText"
            )

        user_img_width = int(self.parent.ui.width_field.text())
        user_img_height = int(self.parent.ui.height_field.text())
        user_cfg = float(self.parent.ui.cfg_field.text())
        user_n_steps = int(self.parent.ui.steps_field.text())
        user_scheduler = self.parent.ui.scheduler_drop_down_box.currentData(
            Qt.ItemDataRole.UserRole
        )
        user_number_of_images = (
            int(self.parent.ui.select_n_sample.text())
            if len(self.parent.ui.select_n_sample.text()) >= 1
            else 1
        )
        user_batch_size = (
            int(self.parent.ui.select_batch_size.text())
            if len(self.parent.ui.select_batch_size.text()) >= 1
            else 1
        )

        if inference_type is None:
            return [
                user_positive_prompt,
                user_negative_prompt,
                user_img_width,
                user_img_height,
                user_number_of_images,
                user_batch_size,
                user_scheduler,
                user_cfg,
                user_n_steps,
            ]
        elif inference_type == "img2img":
            image_list = []

            # stores images from the img2img selection box on the right sidebar into a list
            if self.parent.ui.img2img_select_box.count() >= 1:
                for index in range(self.parent.ui.img2img_select_box.count()):
                    image_list.append(
                        self.parent.ui.img2img_select_box.item(index).text()
                    )

            # takes selected images from the QGraphicsScene a.k.a Canvas
            elif len(self.parent.image_viewer.scene.selectedItems()) >= 1:
                for item in self.parent.image_viewer.scene.selectedItems():
                    img = fromqpixmap(item.pixmap())
                    image_list.append(img)

            # uses images that are selected from the left sidebar image browser
            # elif len(self.parent.ui.image_browser.selectedIndexes()) >= 1:
            #     for index in self.parent.ui.image_browser.selectedIndexes():
            #         img = index.data(Qt.ItemDataRole.DisplayRole)
            #         image_list.append(img)

            img2img_strength = float(self.parent.ui.img2img_strength_field.text()) / 100
            return [
                user_positive_prompt,
                user_negative_prompt,
                user_img_width,
                user_img_height,
                user_number_of_images,
                user_batch_size,
                user_scheduler,
                user_cfg,
                user_n_steps,
                image_list,
                img2img_strength,
            ]
