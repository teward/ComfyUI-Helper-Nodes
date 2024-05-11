from .util import HelperNodes_MultilineStringLiteral, HelperNodes_StringLiteral
from .util import HelperNodes_Steps, HelperNodes_CfgScale, HelperNodes_WidthHeight

from .scheduler import HelperNodes_SchedulerSelector

from .sampler import HelperNodes_SamplerSelector, HelperNodes_SeedSelector


NODE_CLASS_MAPPINGS = {
    "HelperNodes_MultilineStringLiteral": HelperNodes_MultilineStringLiteral,
    "HelperNodes_StringLiteral": HelperNodes_StringLiteral,
    "HelperNodes_Steps": HelperNodes_Steps,
    "HelperNodes_CfgScale": HelperNodes_CfgScale,
    "HelperNodes_WidthHeight": HelperNodes_WidthHeight,
    "HelperNodes_SchedulerSelector": HelperNodes_SchedulerSelector,
    "HelperNodes_SamplerSelector": HelperNodes_SamplerSelector,
    "HelperNodes_SeedSelector": HelperNodes_SeedSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HelperNodes_MultilineStringLiteral": "String Literal (multi-line)",
    "HelperNodes_StringLiteral": "String Literal",
    "HelperNodes_Steps": "Steps",
    "HelperNodes_CfgScale": "CFG Scale",
    "HelperNodes_WidthHeight": "Image Dimensions",
    "HelperNodes_SchedulerSelector": "Scheduler",
    "HelperNodes_SamplerSelector": "Sampler",
    "HelperNodes_SeedSelector": "Seed",
}