from langchain_core.prompts import ChatPromptTemplate
from agent.agent import get_llm
from models.controller import GuessPIDControllers
from langchain_core.runnables import RunnableConfig
from models.feedback import Candidate
from models.controller import PIDController
from typing import Dict, List
from models.state import ToTState
from agent.agent import _ensure_configurable

system_prompt = """
You are a control systems expert. Your task is to propose well-tuned PID controllers for a given plant.
If the current controller is slow (long rise or settling time), you're encouraged to make aggressive improvements.
If the system is oscillating or unstable, tune conservatively to regain stability.

You will be given:
- A plant transfer function (in LaTeX or human-readable form)
- Performance requirements (rise time, settling time, overshoot, etc.)
- A previous candidate (optional)

A PID controller consists of:
- Kp: proportional gain — increases response speed but can cause overshoot
- Ki: integral gain — eliminates steady-state error but may introduce oscillation
- Kd: derivative gain — dampens the response and reduces overshoot

Always explain your reasoning, and return exactly {k} PID configurations that improve the system toward the requirements.
"""

user_prompt = """
Plant: {plant_description}\n\n
Requirements: {requirements}\n\n
Previous candidate: {candidate}\n\n
Please return a list of {k} PID candidates using the previous candidate parameters along with the feedback (if it is available) to meet the requirements.
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", user_prompt)
])

# Get the shared LLM instance
llm = get_llm()

# Structured output binding
pid_solver = prompt | llm.with_structured_output(GuessPIDControllers)

def get_pid_solver():
    return pid_solver

def expand(state: ToTState, *, config: RunnableConfig) -> Dict[str, List[Candidate]]:
    '''
    Generate the next set of PID controller candidates from the current state.
    '''
    # Log the Current Node
    print("\n--🧠 Invoking PID generation chain...--")

    # Get the Configurations
    configurable = _ensure_configurable(config)
    k = configurable["k"]

    # Check for Previous Candiadates
    if not state.get("seed"):
        candidate_str = ""
    else:
        candidate_str = str(state["seed"])

    # Call the Chain
    try:
        result = pid_solver.invoke({
            "requirements" : state["requirements"],
            "candidate" : candidate_str,
            "plant_description": state["plant"].to_latex(),
            "k" : k
        })
    except Exception as e:
        print(f"[Expand Node Error] {e}")
        return {"candidates": []}

    # Wrap each controller in a Candidate object
    new_candidates = [
        Candidate(candidate=pid) for pid in result.controllers
    ]

    return {"candidates" : new_candidates}
