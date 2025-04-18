from pydantic import BaseModel, Field
from typing import List

class PIDController(BaseModel):
    Kp: float
    Ki: float
    Kd: float

    def get_params(self):
        return self.Kp, self.Ki, self.Kd

class GuessPIDControllers(BaseModel):
    reasoning: str = Field(description = "Your reasoninng for suggesting these PID Parameters.")
    controllers: List[PIDController] = Field(description = "List of PID Candidates to evaulate")