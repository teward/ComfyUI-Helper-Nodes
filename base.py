"""Base functionality and nodes are incorporated here.

Primarily contains base class declarations inherited elsewhere.

Also has some global declarations."""


GLOBAL_CATEGORY = "ComfyUI-Helper-Nodes"


class BaseNode:
    """
    Base class for all custom ComfyUI nodes in this repository.

    Mostly done to makes sure that things're defined properly in
    any inherited functions during development.
    """
    def __init__(self, **kwargs) -> None:
        pass

    # noinspection PyPep8Naming
    @classmethod
    def INPUT_TYPES(cls) -> dict:
        raise NotImplementedError

    RETURN_TYPES: tuple = None
    RETURN_NAMES: tuple = None

    CATEGORY: str = GLOBAL_CATEGORY

    FUNCTION: str = "process"

    def process(self, **kwargs) -> tuple:
        raise NotImplementedError
