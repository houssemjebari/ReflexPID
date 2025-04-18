from typing import NamedTuple, Optional
from models.controller import PIDController

class Candidate(NamedTuple):
    candidate: PIDController
    metrics: Optional[dict] = None
    feedback: Optional[str] = None
    score: Optional[float] = None

    def __str__(self):
        values = f"Kp={self.candidate.Kp}, Ki={self.candidate.Ki}, Kd={self.candidate.Kd}"
        metrics_str = f"Metrics: {self.metrics}" if self.metrics else ""
        score_str = f"Score: {self.score:.4f}" if self.score is not None else ""
        feedback_str = f"Feedback: {self.feedback}" if self.feedback else ""

        parts = ["PID(" + values + ")"]
        if metrics_str: parts.append(metrics_str)
        if score_str: parts.append(score_str)
        if feedback_str: parts.append(feedback_str)

        return " | ".join(parts)

class ScoredCandidate(Candidate):
    metrics: dict
    feedback: str

