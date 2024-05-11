from base import GLOBAL_CATEGORY, BaseNode

import comfy
import comfy.samplers

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/conditioning"


class HelperNodes_CLIPSkip(BaseNode):
    """
    Core implementation of this is basically the same as ComfyUI's node
    for CLIPSetLastLayer, but making it a positive number like A1111 does
    for user understanding.

    Functions otherwise identical, converting the positive number to negative
    before passing into CLIP object.
    """
    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "clip": ("CLIP", ),
                "skip_layers": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 24,
                    "step": 1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("CLIP",)

    CATEGORY = f"{MODULE_CATEGORY}"

    def process(self, clip, skip_layers) -> tuple:
        clip = clip.clone()
        clip.clip_layer(skip_layers * -1)
        return (clip,)
