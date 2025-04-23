from models.state import ToTState
from models.feedback import Candidate
from typing import Dict, List
from langchain_core.runnables import RunnableConfig
from agent.candidate_generator import _ensure_configurable

def prune(state: ToTState, config: RunnableConfig) -> Dict[str, List[Candidate]]:
    """Prune The Tree Candidates"""
    scored_candidates = state["scored_candidates"]
    beam_size = _ensure_configurable(config)["beam_size"]
    organized = sorted(
    scored_candidates, key=lambda candidate: candidate.score or 0.0, reverse=True
)
    pruned = organized[:beam_size]

    return {
        "candidates" : pruned,
        "scored_candidates" : "clear",
        "depth" : 1
    }