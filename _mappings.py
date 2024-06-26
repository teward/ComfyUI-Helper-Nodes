from .util import HelperNodes_MultilineStringLiteral, HelperNodes_StringLiteral
from .util import HelperNodes_Steps, HelperNodes_CfgScale, HelperNodes_WidthHeight

from .scheduler import HelperNodes_SchedulerSelector

from .sampler import HelperNodes_SamplerSelector, HelperNodes_SeedSelector

from .conditioning import HelperNodes_CLIPSkip   # Not currently provided while we refine this.

from .models import HelperNodes_VAESelector, HelperNodes_CheckpointSelector

from .prompt import HelperNodes_Prompt

from .sdxl import HelperNodes_SDXLCommonResolutions

from .image import HelperNodes_SaveImage


NODE_CLASS_MAPPINGS = {
    "HelperNodes_MultilineStringLiteral": HelperNodes_MultilineStringLiteral,
    "HelperNodes_StringLiteral": HelperNodes_StringLiteral,
    "HelperNodes_Steps": HelperNodes_Steps,
    "HelperNodes_CfgScale": HelperNodes_CfgScale,
    "HelperNodes_WidthHeight": HelperNodes_WidthHeight,
    "HelperNodes_SchedulerSelector": HelperNodes_SchedulerSelector,
    "HelperNodes_SamplerSelector": HelperNodes_SamplerSelector,
    "HelperNodes_SeedSelector": HelperNodes_SeedSelector,
    "HelperNodes_CheckpointSelector": HelperNodes_CheckpointSelector,
    "HelperNodes_VAESelector": HelperNodes_VAESelector,
    "HelperNodes_Prompt": HelperNodes_Prompt,
    "HelperNodes_SDXLCommonResolutions": HelperNodes_SDXLCommonResolutions,
    "HelperNodes_SaveImage": HelperNodes_SaveImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HelperNodes_MultilineStringLiteral": "String Literal (multi-line)",
    "HelperNodes_StringLiteral": "String Literal",
    "HelperNodes_Steps": "Steps",
    "HelperNodes_CfgScale": "CFG Scale",
    "HelperNodes_WidthHeight": "Image Dimensions",
    "HelperNodes_SchedulerSelector": "Scheduler Selector",
    "HelperNodes_SamplerSelector": "Sampler Selector",
    "HelperNodes_SeedSelector": "Seed",
    "HelperNodes_CheckpointSelector": "Checkpoint Selector",
    "HelperNodes_VAESelector": "VAE Selector",
    "HelperNodes_Prompt": "Positive/Negative Prompts",
    "HelperNodes_SDXLCommonResolutions": "Common SDXL Resolutions",
    "HelperNodes_SaveImage": "Save Image",
}