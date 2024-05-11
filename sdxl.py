from .base import BaseNode, GLOBAL_CATEGORY

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/sdxl"


class HelperNodes_SDXLCommonResolutions(BaseNode):
    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "dimensions": ([
                    "640 x 1536 (5:12 Portrait)",
                    "768 x 1344 (4:7 Portrait)",
                    "832 x 1216 (13:19 Portrait)",
                    "896 x 1152 (7:9 Portrait)",
                    "1024 x 1024 (1:1 Square)",
                    "1152 x 896 (9:7 Landscape)",
                    "1216 x 832 (19:13 Landscape)",
                    "1344 x 768 (7:4 Landscape)",
                    "1536 x 640 (12:5 Landscape)"
                ],)
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING", "STRING",)
    RETURN_NAMES = ("width", "height", "aspect ratio", "orientation",)

    CATEGORY = MODULE_CATEGORY

    def process(self, dimensions: str) -> tuple:
        dim, asp = dimensions.split(' (', 1)
        sasp: str = asp.strip('()')
        aspect = sasp.split(' ', 1)[0]
        orient = sasp.split(' ', 1)[1]
        dims: str = dim.lower().split(' x ')
        fwidth = float(dims[0])
        fheight = float(dims[1])
        width = int(fwidth) if fwidth.is_integer() else round(fwidth, 2)
        height = int(fheight) if fheight.is_integer() else round(fheight, 2)

        return width, height, aspect, orient.lower()
