from .base import GLOBAL_CATEGORY, BaseNode

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}"


class HelperNodes_Prompt(BaseNode):
    """
    This is a multi-field TEXT node that allows entering a positive and negative
    prompt and pass them both out.

    Contains two multiline text input fields, neg_prompt is optional.
    """

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("PROMPT", "NEGPROMPT")

    CATEGORY = MODULE_CATEGORY

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True})
            },
            "optional": {
                "neg_prompt": ("STRING", {"multiline": True})
            }
        }

    def process(self, prompt, neg_prompt) -> tuple:
        if not neg_prompt:
            neg_prompt = ""

        return prompt, neg_prompt
