from typing import List, Optional, Dict, Any
from typing import Literal, Union
from typing_extensions import Annotated, TypedDict
import operator
from models.feedback import Candidate, ScoredCandidate

def update_candidates(
    existing: Optional[list] = None,
    updates: Optional[Union[list, Literal["clear"]]] = None,
) -> List[str]:
    if existing is None:
        existing = []
    if updates is None:
        return existing
    if updates == "clear":
        return []
    # Concatenate the lists
    return existing + updates


class ToTState(TypedDict):
    plant: str
    requirements: str
    candidates: Annotated[List[Candidate], update_candidates]
    scored_candidates: Annotated[List[ScoredCandidate], update_candidates]
    depth: Annotated[int, operator.add]

class ExpansionState(ToTState):
    seed: Optional[Candidate]
