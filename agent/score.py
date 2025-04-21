from losses import compute_weighted_loss 
from engine.evaluate import compute_pid_metrics
from models.feedback import ScoredCandidate, Candidate
from typing import Dict, List
from models.state import ToTState

def compute_score(candidate: Candidate, plant, requirements, weights, loss_type="L1") -> ScoredCandidate:
    # Simulate the Plant + PID 
    metrics = compute_pid_metrics(candidate.candidate, plant.get_tf())
    # Compute Loss
    loss = compute_weighted_loss(metrics, requirements, weights, loss=loss_type)
    # Compute Score 
    score = 1 / (1 + loss)
    
    return ScoredCandidate(
        candidate=candidate.candidate,
        metrics=metrics,
        score=score,
        feedback=f"Score based on {loss_type} loss: {score:.4f}"
    )


def score(state: ToTState) -> Dict[str, List[ScoredCandidate]]:
    candidates = state["candidates"]
    plant = state["plant"]
    requirements = state["requirements"]

    weights = {
        "rise_time": 1.0,
        "settling_time": 1.0,
        "overshoot": 1.0,
        "steady_state_error": 1.0,
        "IAE": 1.0
    }

    scored = [
        compute_score(candidate, plant, requirements, weights)
        for candidate in candidates
    ]

    return {
        "scored_candidates" : scored,
        "candidates" : "clear"
    }
