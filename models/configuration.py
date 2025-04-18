from typing_extensions import TypedDict

class Configuration(TypedDict, total=False):
    max_depth: int
    threshold: float
    k: int
    beam_size: int
