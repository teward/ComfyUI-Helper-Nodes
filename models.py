from .base import BaseNode, GLOBAL_CATEGORY

import comfy.utils
import folder_paths

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/models"


class HelperNodes_CheckpointSelector(BaseNode):
    """
    Simple selector node that allows the selection of Checkpoint/Model.

    This should then be passed into either a conditioner or into a LoRA loader.

    Does not include LoRA selection, which is done in the standard Load LoRA nodes.
    """
    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "chkpt_name": (folder_paths.get_filename_list("checkpoints"),)
            }
        }

    CATEGORY = MODULE_CATEGORY

    RETURN_TYPES = (folder_paths.get_filename_list("checkpoints"),)
    RETURN_NAMES = ("chkpt_name",)

    def process(self, chkpt_name) -> tuple:
        return (chkpt_name,)


class HelperNodes_VAESelector(BaseNode):
    """
    Simple selector node that allows the selection of VAEs.

    This should then be passed to a VAE decoder node as it returns a VAE.
    """

    @staticmethod
    def vae_list():
        # Borrowed verbatim from comfyui's implementations.
        vaes = folder_paths.get_filename_list("vae")
        approx_vaes = folder_paths.get_filename_list("vae_approx")
        sdxl_taesd_enc = False
        sdxl_taesd_dec = False
        sd1_taesd_enc = False
        sd1_taesd_dec = False

        for v in approx_vaes:
            if v.startswith("taesd_decoder."):
                sd1_taesd_dec = True
            elif v.startswith("taesd_encoder."):
                sd1_taesd_enc = True
            elif v.startswith("taesdxl_decoder."):
                sdxl_taesd_dec = True
            elif v.startswith("taesdxl_encoder."):
                sdxl_taesd_enc = True
        if sd1_taesd_dec and sd1_taesd_enc:
            vaes.append("taesd")
        if sdxl_taesd_dec and sdxl_taesd_enc:
            vaes.append("taesdxl")
        return vaes

    @staticmethod
    def load_taesd(name):
        # Borrowed verbatim from comfyui's implementations
        sd = {}
        approx_vaes = folder_paths.get_filename_list("vae_approx")

        encoder = next(filter(lambda a: a.startswith("{}_encoder.".format(name)), approx_vaes))
        decoder = next(filter(lambda a: a.startswith("{}_decoder.".format(name)), approx_vaes))

        enc = comfy.utils.load_torch_file(folder_paths.get_full_path("vae_approx", encoder))
        for k in enc:
            sd["taesd_encoder.{}".format(k)] = enc[k]

        dec = comfy.utils.load_torch_file(folder_paths.get_full_path("vae_approx", decoder))
        for k in dec:
            sd["taesd_decoder.{}".format(k)] = dec[k]

        if name == "taesd":
            sd["vae_scale"] = torch.tensor(0.18215)
        elif name == "taesdxl":
            sd["vae_scale"] = torch.tensor(0.13025)
        return sd

    CATEGORY = f"{MODULE_CATEGORY}"

    RETURN_TYPES = ("VAE",)
    RETURN_NAMES = ("VAE",)

    def process(self, vae_name) -> tuple:
        if vae_name in ["taesd", "taesdxl"]:
            sd = self.load_taesd(vae_name)
        else:
            vae_path = folder_paths.get_full_path("vae", vae_name)
            sd = comfy.utils.load_torch_file(vae_path)
        vae = comfy.sd.VAE(sd=sd)
        return (vae,)
