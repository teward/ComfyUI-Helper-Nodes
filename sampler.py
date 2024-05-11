from datetime import timezone, datetime
import random

from base import GLOBAL_CATEGORY, BaseNode

import comfy
import comfy.samplers

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/sampler"


# noinspection PyUnresolvedReferences
class HelperNodes_SamplerSelector(BaseNode):
    """
    Simple Selector node that allows selection of a Sampler from
    known samplers in the environment.
    """
    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,)
            }
        }

    RETURN_TYPES = (comfy.samplers.KSampler.SAMPLERS,)
    RETURN_NAMES = ("sampler",)

    CATEGORY = f"{MODULE_CATEGORY}"

    def process(self, sampler_name) -> tuple:
        return (sampler_name,)