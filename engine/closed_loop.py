import numpy as np
import control as ctrl
from models.controller import PIDController


def simulate_closed_loop(Kp, Ki, Kd, G, t: np.ndarray = None, target: float = 1.0):
    """
    Simulates the closed loop step response for a given PID controller and plant G(s).
    Returns the time vector and output response.
    """
    # Default Time Vector
    if t is None:
        t = np.linspace(0,10,1000)
    
    # Build the PID controller C(s)
    P = ctrl.TransferFunction([Kp], [1])
    I = ctrl.TransferFunction([Ki], [1,0]) if Ki != 0 else 0
    D = ctrl.TransferFunction([Kd, 0], [1]) if Kd != 0 else 0
    C = P + I + D

    # Closed-loop system: T(s) = C(s) * G(s) / (1 + C(s) * G(s))
    T = ctrl.feedback(C * G)

    # Step resonse 
    t, y = ctrl.step_response(T, T=t)

    return t, y