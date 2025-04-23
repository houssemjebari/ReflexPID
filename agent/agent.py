from agent.candidate_generator import expand
from agent.pruner import prune
from agent.score import score
from agent.termination import should_terminate
from models.state import ToTState
from models.configuration import Configuration
from langgraph.graph import StateGraph
from typing import Generator



def create_agent():
    ''' Create A Tree Of Thoughts Agent For Controller Tuning '''

    # Instantiate The Graph 
    builder = StateGraph(state_schema=ToTState, config_schema=Configuration)

    # Add Nodes
    builder.add_node(expand)
    builder.add_node(score)
    builder.add_node(prune)

    # Add Edges
    builder.add_edge("expand", "score")
    builder.add_edge("score", "prune")
    builder.add_conditional_edges("prune", should_terminate, path_map=["expand","__end__"])

    # Set Entry Point
    builder.add_edge("__start__", "expand")

    # Compile the graph
    agent = builder.compile()

    return agent

def run_agent(agent, initial_state: ToTState, config: dict) -> Generator:
    ''' Run The Agent '''

    for step in agent.stream(initial_state, {"configurable": config}):
        print("🔁 Agent Step")
        print("🧠 State:", step)
        print("-" * 50)
