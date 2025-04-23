from models.state import ToTState
from models.feedback import Candidate
from typing import Dict, List
from langchain_core.runnables import RunnableConfig
from agent.utils import _ensure_configurable

def prune(state: ToTState, config: RunnableConfig) -> Dict[str, List[Candidate]]:
    ''' Prune The Tree Candidates '''

    # Log the Current Node
    print("\n--🌲 Pruning candidate pool using beam search...--")

    # Access The Necessary State and Configuration Attributes
    scored_candidates = state["scored_candidates"]
    beam_size = _ensure_configurable(config)["beam_size"]

    # Sort the Candidates Based On The Score
    organized = sorted(
    scored_candidates, key=lambda candidate: candidate.score or 0.0, reverse=True
)
    # Prune The Candidate Leaves
    pruned = organized[:beam_size]

    # Return the new state
    return {
        "candidates" : pruned,
        "scored_candidates" : "clear",
        "depth" : 1
    }