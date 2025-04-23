from dotenv import load_dotenv
load_dotenv()
import os
import getpass
import operator
from models.feedback import Candidate
from models.controller import PIDController
from engine.evaluate import compute_pid_metrics
from engine.closed_loop import simulate_closed_loop
from plant import get_default_plant  
from plot import plot_response
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig
from agent.agent import create_agent, run_agent


def main():
    # 1. Instantiate a test PID controller
    pid = PIDController(Kp=1.0, Ki=0.5, Kd=0.1)

    # 2. Get your test plant
    plant = get_default_plant()
    G = plant.get_tf()
    # 3. Simulate using raw simulate_closed_loop
    t, y = simulate_closed_loop(*pid.get_params(), G)
    plot_response(t, y, title="Closed-Loop Response")

    # 4. Compute metrics using the evaluation bridge
    metrics = compute_pid_metrics(pid, G)
    print("\n✅ Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Create The Plant
    plant = get_default_plant()
    G = plant.get_tf()
    # Compute Initial Metrics with Initial Controller
    metrics = compute_pid_metrics(pid, G)
    candidate = Candidate(candidate=pid, metrics=metrics)
    requirements = {
        "rise_time": 2.0,
        "settling_time": 3.0,
        "overshoot": 0.1,
        "steady_state_error": 0.01,
        "IAE": 1.0
    }
    # Initialize the State
    initial_state = {
        "plant": plant,
        "requirements": requirements,
        "seed": candidate,
        "candidates": [],
        "scored_candidates": [],
        "depth": 0
    }

    # Create The Agent
    agent = create_agent()
    
    # Run The Agent
    run_agent(agent, initial_state, config=RunnableConfig(configurable={}))


if __name__ == "__main__":
    main()
