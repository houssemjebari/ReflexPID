import matplotlib.pyplot as plt
import control as ctrl 
import numpy as np 
from metrics import compute_metrics
from losses import compute_weighted_loss
from plot import plot_response

"""
open_loop_sim.py

This script simulates the open-loop step response of a first-order system,
representing a simplified DC motor speed control system.

The transfer function is:
    G(s) = K / (tau * s + 1)

Where:
    - K   = 1     (system gain)
    - tau = 1     (time constant)

This is part of a small proof-of-concept (POC) for motor control using PID tuning.
Future steps will wrap this system with a PID controller in closed-loop configuration
and use an agent to tune PID parameters for optimal performance.
"""

def create_pid_controller(Kp, Ki, Kd):
    """
    Returns a PID controller transfer function.
    C(s) = Kp + Ki/s + Kd*s
    """
    # Proportional, Integral, Derivative terms
    P = ctrl.TransferFunction([Kp], [1])
    I = ctrl.TransferFunction([Ki], [1, 0]) if Ki != 0 else 0
    D = ctrl.TransferFunction([Kd, 0], [1]) if Kd != 0 else 0

    return P + I + D



# System parameters
K = 1       
tau = 1  

# Controller Parameters
Kp, Ki, Kd = 20.0, 20, 1


# Transfer function: G(s) = K / (tau*s + 1)
numerator = [K]
denominator = [tau, 1]
G = ctrl.TransferFunction(numerator, denominator)

# Define Controller 
C = create_pid_controller(Kp, Ki, Kd)
T = ctrl.feedback(C * G)
t = np.linspace(0, 10, 1000)

# Time vector for simulation
t = np.linspace(0, 10, 1000)

# Step response
t, y = ctrl.step_response(T, T=t)

# Compute metrics
metrics = compute_metrics(t, y)
print(metrics)

# Score the response
requirements = {
    'overshoot': 5.0,
    'settling_time': 2.0,
    'IAE': 0.5,
}
weights = {
    'overshoot': 0.3,
    'settling_time': 0.4,
    'IAE': 0.3,
}
loss = compute_weighted_loss(metrics, requirements, weights, loss='L2')
print("L2 Loss on Metrics Yields: ",loss)

# Plot
plot_response(t, y, title="Open-Loop Step Response", settling_time=metrics["settling_time"])
