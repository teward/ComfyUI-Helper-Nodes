import os
import json

from .base import BaseNode, GLOBAL_CATEGORY

# noinspection PyUnresolvedReferences
import folder_paths
# noinspection PyUnresolvedReferences,PyPackageRequirements
from nodes import MAX_RESOLUTION

# noinspection PyUnresolvedReferences,PyPackageRequirements
import comfy.samplers

from PIL import Image, ExifTags
from PIL.PngImagePlugin import PngInfo
import piexif
import piexif.helper
import numpy as np

from ._image_util import *

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/image"


class HelperNodes_SaveImage(BaseNode):
    """
    Essentially, this does the same function as ImageSaveWithMetadata from
    https://github.com/giriss/comfy-image-saver.git but allows us to
    greatly REDUCE runtime by not serializing the ComfyUI workflow into the metadata.

    That is controlled by multiple boolean values to control whether we output metadata
    and if we do what we include.

    This is designed to work with other nodes in this library, which provide aspect_ratio and orientation.

    Orientation can be calculated based on width and height, if not provided otherwise.
    """
    def __init__(self):
        super().__init__()
        self.output_dir = folder_paths.output_directory

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        # This relies heavily on components that're from comfy-image-saver by
        # https://github.com/giriss/comfy-image-saver.git - but with differences
        # in actual implementation
        #
        # We decide whether to write to individual files for metadata, or add to image,
        # or both, or neither.  Yes, we allow just saving the image directly.

        inputs = {
            "required": {
                "images": ("IMAGE", {"forceInput": True}),
                "filename": ("STRING", {"default": f'%time_%seed', "multiline": False}),
                "path": ("STRING", {"default": '', "multiline": False}),
                "extension": (['png', 'jpeg', 'webp'], {"default": "png"}),
                "steps": ("INT", {"forceInput": True}),
                "cfg": ("FLOAT", {"forceInput": True}),
                "model_name": (folder_paths.get_filename_list("checkpoints"), {"forceInput": True}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"forceInput": True}),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"forceInput": True}),
            },
            "optional": {
                "positive_prompt": ("STRING", {"default": "unknown", "multiline": True, "forceInput": True}),
                "negative_prompt": ("STRING", {"default": "unknown", "multiline": True, "forceInput": True}),
                "seed_value": ("INT", {"default": 0, "min": 0, "max": 18446744073709551615, "step": 1}),
                "width": ("INT", {"default": 1024, "min": 8, "max": MAX_RESOLUTION, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 8, "max": MAX_RESOLUTION, "step": 8}),
                "aspect_ratio": ("STRING", {"default": "unknown", "forceInput": True}),
                "orientation": ("STRING", {"default": "unknown", "forceInput": True}),
                "lossless_webp": ("BOOLEAN", {"default": True}),
                "quality_jpeg_or_webp": ("INT", {"default": 100, "min": 1, "max": 100}),
                "counter": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "time_format": ("STRING", {"default": "%Y-%m-%d-%H%M%S", "multiline": False}),
                "include_metadata": ("BOOLEAN", {"default": True}),
                "save_prompt_with_metadata": ("BOOLEAN", {"default": False}),
                "save_extra_pnginfo_with_metadata": ("BOOLEAN", {"default": True})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

        return inputs

    RETURN_TYPES = ()  # We don't return anything here
    OUTPUT_NODE = True  # We are an OUTPUT node.

    FUNCTION = "save_files"

    # noinspection PyShadowingNames
    def save_files(self, images, filename: str, path: str, extension: str, steps: int, cfg: float,
                   model_name: str, sampler_name: str, scheduler: str, positive_prompt: str, negative_prompt: str,
                   seed_value: int, width: int, height: int, lossless_webp: bool,
                   quality_jpeg_or_webp: str, counter: int, time_format: str, include_metadata: bool,
                   save_prompt_with_metadata: bool, save_extra_pnginfo_with_metadata: bool, prompt=None,
                   extra_pnginfo=None, aspect_ratio: str = None, orientation: str = None):
        filename = make_filename(filename, seed_value, model_name, counter, time_format)
        path = make_pathname(path, seed_value, model_name, counter, time_format)
        ckpt_path = folder_paths.get_full_path("checkpoints", model_name)
        basemodelname = parse_name(model_name)
        modelhash = calculate_sha256(ckpt_path)[:10]
        comment = (f"{handle_whitespace(positive_prompt)}\n{handle_whitespace(negative_prompt)}\nSteps: {steps}, "
                   f"Sampler: {sampler_name}\nSampler: {sampler_name}, ")
        if scheduler != "normal":
            comment += f"Scheduler: {scheduler}, "

        comment += f"CFG Scale: {cfg}, Seed: {seed_value}, Size: {width}x{height}, "

        if aspect_ratio:
            comment += f"Aspect Ratio: {aspect_ratio}, "

        if orientation:
            comment += f"Orientation: {orientation},"
        else:
            if width == height:
                comment += f"Orientation: square, "
            elif width > height:
                comment += f"Orientation: landscape, "
            else:
                comment += f"Orientation: portrait, "

        comment += f"Model: {basemodelname}, Model Hash: {modelhash}, Version: ComfyUI"

        output_path = os.path.join(self.output_dir, path)

        if output_path.strip() != '':
            if not os.path.exists(output_path.strip()):
                print(f"The specified path `{output_path.strip()}` does not exist. Creating directory.")
                os.makedirs(output_path, exist_ok=True)

        filenames = self.save_images(images, output_path, filename, comment, extension, quality_jpeg_or_webp,
                                     lossless_webp, prompt=prompt, extra_pnginfo=extra_pnginfo,
                                     include_metadata=include_metadata,
                                     include_prompt_in_metadata=save_prompt_with_metadata,
                                     include_extra_pnginfo=save_extra_pnginfo_with_metadata)

        subfolder = os.path.normpath(path)
        return {"ui": {"images": map(
            lambda filename: {"filename": filename, "subfolder": subfolder if subfolder != '.' else '',
                              "type": 'output'}, filenames)}}

    @staticmethod
    def save_images(images, output_path, filename_prefix, comment, extension, quality_jpeg_or_webp, lossless_webp,
                    prompt=None, extra_pnginfo=None, include_metadata=True, include_prompt_in_metadata=True,
                    include_extra_pnginfo=False) -> list[str]:
        img_count = 1
        paths = []

        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            if images.size()[0] > 1:
                filename_prefix += "{:02d}".format(img_count)

            if extension == "png":
                metadata = PngInfo()
                if include_metadata:
                    metadata.add_text("parameters", comment)

                    if prompt is not None and include_prompt_in_metadata:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None and include_extra_pnginfo:
                        print(extra_pnginfo.keys())
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                filename = f"{filename_prefix}.png"
                img.save(os.path.join(output_path, filename), pnginfo=metadata, optimize=True)
            else:
                filename = f"{filename_prefix}.{extension}"
                file = os.path.join(output_path, filename)
                img.save(file, optimize=True, quality=quality_jpeg_or_webp, lossless=lossless_webp)
                if include_metadata:
                    exif_bytes = piexif.dump({
                        "Exif": {
                            piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(comment, encoding="unicode")
                        },
                    })
                    piexif.insert(exif_bytes, file)

            paths.append(filename)
            img_count += 1

        return paths
