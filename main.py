from dotenv import load_dotenv
load_dotenv()
import os
import getpass
import operator
from agent.candidate_generator import expand
from agent.score import score
from models.feedback import Candidate
from models.controller import PIDController
from engine.evaluate import compute_pid_metrics
from engine.closed_loop import simulate_closed_loop
from plant import get_default_plant  
from plot import plot_response
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.config import RunnableConfig


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

    plant = get_default_plant()
    G = plant.get_tf()
    metrics = compute_pid_metrics(pid, G)
    candidate = Candidate(candidate=pid, metrics=metrics)
    requirements = {
        "rise_time": 2.0,
        "settling_time": 3.0,
        "overshoot": 0.1,
        "steady_state_error": 0.01,
        "IAE": 1.0
    }
    state = {
        "plant": plant,
        "requirements": requirements,
        "seed": candidate,
        "candidates": [],
        "scored_candidates": [],
        "depth": 0
    }

    # 7. Call the expander
    print("\n🧪 Testing expander node...")
    expand_node = RunnableLambda(expand)
    out = expand_node.invoke(state, config=RunnableConfig(configurable={"k": 3}))
    print(out)

    # 8. Call the scorer
    print("\n🧪 Testing Scorer node...")
    expand_node = RunnableLambda(score)
    state = {
        "plant": plant,
        "requirements": requirements,
        "candidates": out["candidates"],
        "scored_candidates": [],
        "depth": 0
    }
    out = expand_node.invoke(state, config=RunnableConfig(configurable={"k": 3}))
    print(out)


if __name__ == "__main__":
    main()
