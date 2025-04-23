from typing import Dict, List, Union, Literal
from models.state import ToTState
from langchain_core.runnables import RunnableConfig
from langgraph.constants import Send
from agent.agent import _ensure_configurable


def should_terminate(state: ToTState, config: RunnableConfig) -> Union[Literal["__end__"], Send]:
    ''' Termination Conditional Edge '''

    # Log The Current Node
    print("\n--🛑 Evaluating termination condition...--")

    # Extract All The  Necessary Config and State Attributes 
    config = _ensure_configurable(config)
    threshold = config["threshold"]
    max_depth = config["max_depth"]
    candidates = state["candidates"]
    depth = state["depth"]

    # Check if the Problem is solved 
    solved = candidates[0].score >= threshold

    # Terminate The Graph or Return New Candidates
    if solved or depth >= max_depth:
        return "__end__"
    return [
        Send("expand", {**state, "seed": candidate})
        for candidate in candidates
    ]