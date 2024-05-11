from base import GLOBAL_CATEGORY, BaseNode

import comfy
import comfy.samplers

MODULE_CATEGORY = f"{GLOBAL_CATEGORY}/scheduler"


class HelperNodes_SchedulerSelector(BaseNode):
    """
    Simple Selector node that allows selection of a Scheduler from
    known schedulers in the environment.
    """
    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "scheduler_name": (comfy.samplers.KSampler.SCHEDULERS,)
            }
        }

    RETURN_TYPES = (comfy.samplers.KSampler.SCHEDULERS,)
    RETURN_NAMES = ("scheduler",)

    CATEGORY = f"{MODULE_CATEGORY}"

    def process(self, scheduler_name):
        return (scheduler_name,)
