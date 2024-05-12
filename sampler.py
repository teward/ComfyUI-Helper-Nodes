from datetime import timezone, datetime
import random

from .base import GLOBAL_CATEGORY, BaseNode

# noinspection PyUnresolvedReferences,PyPackageRequirements
import comfy
# noinspection PyUnresolvedReferences,PyPackageRequirements
import comfy.samplers

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/sampler"

# Initialize the random system anew. This is because some extensions may alter
# this seed generation process and cause problems.
initial_random_state = random.getstate()
random.seed(datetime.now().timestamp())
seed_random_state = random.getstate()
random.setstate(initial_random_state)


def new_random_seed():
    """ Gets a new random seed from the rgthree_seed_random_state and resetting the previous state."""
    global seed_random_state
    prev_random_state = random.getstate()
    random.setstate(seed_random_state)
    seed = random.randint(1, 18446744073709551615)
    seed_random_state = random.getstate()
    random.setstate(prev_random_state)
    return seed


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


class HelperNodes_SeedSelector(BaseNode):
    """
    Integer value node that has a Random Number Generator component in it.

    -1 makes a new random seed every time.
    """

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 18446744073709551615,   # equivalent to 0xffffffffffffffff - 64-bit integer max
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)

    CATEGORY = f"{MODULE_CATEGORY}"

    def process(self, seed) -> tuple:
        if seed == -1:
            # When seed value is -1, we generate a random value.
            original_seed = seed
            seed = new_random_seed()

        return (seed,)
