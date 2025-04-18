import numpy as np
from models.controller import PIDController
from engine.closed_loop import simulate_closed_loop
from metrics import compute_metrics

def compute_pid_metrics(pid: PIDController, G, t=None, target=1.0, tol=0.02):
    """
    Simulate the closed loop using external engine and return performance metrics
    """
    Kp, Ki, Kd = pid.get_params()
    t, y = simulate_closed_loop(Kp, Ki, Kd, G, t=t, target=target)
    return compute_metrics(t, y, target=target, tol=tol)