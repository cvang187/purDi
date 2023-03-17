from dataclasses import dataclass

import torch
from diffusers import StableDiffusionPipeline, schedulers, UniPCMultistepScheduler


@dataclass
class PurDiDiffuserSchedulers:
    display_name: str
    tool_tip: str
    icon: str
    module: schedulers


euler = PurDiDiffuserSchedulers(
    display_name="Euler",
    tool_tip="Euler scheduler",
    icon="gui/images/Euler.png",
    module=schedulers.EulerDiscreteScheduler,
)
euler_a = PurDiDiffuserSchedulers(
    display_name="Euler_A",
    tool_tip="Euler Ancestral scheduler",
    icon="gui/images/Euler_A.png",
    module=schedulers.EulerAncestralDiscreteScheduler,
)
dpm_single = PurDiDiffuserSchedulers(
    display_name="DPM Single-Step",
    tool_tip="Singlestep DPM-Solver",
    icon="gui/images/DPM Single-Step.png",
    module=schedulers.DPMSolverSinglestepScheduler,
)
dpm_multi = PurDiDiffuserSchedulers(
    display_name="DPM Multi-Step",
    tool_tip="Multistep DPM-Solver",
    icon="gui/images/DPM Multi-Step.png",
    module=schedulers.DPMSolverMultistepScheduler,
)
dpm_karras = PurDiDiffuserSchedulers(
    display_name="DPM Karras",
    tool_tip="DPM Discrete Scheduler",
    icon="gui/images/DPM Karras.png",
    module=schedulers.KDPM2DiscreteScheduler,
)
dpm_karras_a = PurDiDiffuserSchedulers(
    display_name="DPM Karras Ancestral",
    tool_tip="DPM Discrete Scheduler with ancestral sampling ",
    icon="gui/images/DPM Karras Ancestral.png",
    module=schedulers.KDPM2AncestralDiscreteScheduler,
)
ddim = PurDiDiffuserSchedulers(
    display_name="DDIM",
    tool_tip="Denoising diffusion implicit models",
    icon="gui/images/DDIM.png",
    module=schedulers.DDIMScheduler,
)
heun = PurDiDiffuserSchedulers(
    display_name="HEUN",
    tool_tip="Heun scheduler",
    icon="gui/images/HEUN.png",
    module=schedulers.HeunDiscreteScheduler,
)
lms = PurDiDiffuserSchedulers(
    display_name="LMS",
    tool_tip="Linear Multi-Step",
    icon="gui/images/LMS.png",
    module=schedulers.LMSDiscreteScheduler,
)
pndm = PurDiDiffuserSchedulers(
    display_name="PNDM",
    tool_tip="Pseudo numerical methods for diffusion models",
    icon="gui/images/PNDM.png",
    module=schedulers.PNDMScheduler,
)
uni_pc_multistep = PurDiDiffuserSchedulers(
    display_name="UniPC",
    tool_tip="UniPC Multi-Step",
    icon="gui/images/UniPC",
    module=UniPCMultistepScheduler,
)


def main():
    """
    Run this script to generate your own icons for the side dock
    drop down scheduler list in the main window ui.
    """

    scheduler_list = [
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

    model_id = "stabilityai/stable-diffusion-2-1-base"
    # model_id = "../../models/diffusers/stable-diffusion-21-768"
    # model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
    )
    pipe.enable_vae_slicing()
    pipe.enable_attention_slicing()
    pipe.enable_xformers_memory_efficient_attention()
    pipe.enable_model_cpu_offload()

    seed = torch.Generator(device="cuda").manual_seed(3453123547)

    # for idx in scheduler_list:
    #     pipe.scheduler = idx.module.from_config(pipe.scheduler.config)
    #
    #     with torch.inference_mode():
    #         image = pipe(
    #             prompt="a painting of a house by the ocean",
    #             negative_prompt=None,
    #             width=512,
    #             height=512,
    #             num_images_per_prompt=1,
    #             num_inference_steps=30,
    #             guidance_scale=6,
    #             generator=seed,
    #             output_type="pil",
    #             callback=None,
    #             callback_steps=1,
    #         ).images[0]
    #         image.save(f"../../gui/images/{idx.display_name}.png")

    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    with torch.inference_mode():
        image = pipe(
            prompt="a painting of a house by the ocean",
            negative_prompt=None,
            width=512,
            height=512,
            num_images_per_prompt=1,
            num_inference_steps=30,
            guidance_scale=6,
            generator=seed,
            output_type="pil",
            callback=None,
            callback_steps=1,
        ).images[0]
        image.save(f"../../gui/images/UniPC.png")


if __name__ == "__main__":
    main()
