import numpy as np 

def compute_rise_time(t, y, final_value):
    indices = np.where((y >= 0.1 * final_value) & (y <= 0.9 * final_value))[0]
    return t[indices[-1]] - t[indices[0]] if len(indices) > 0 else None

def compute_settling_time(t, y, final_value, tol=0.02):
    band = tol * final_value
    out_of_bounds = np.where(np.abs(y - final_value) > band)[0]
    if len(out_of_bounds) == 0:
        return 0
    last_out = out_of_bounds[-1]
    return t[last_out + 1] if last_out + 1 < len(t) else t[-1]

def compute_overshoot(y, final_value):
    return max(((np.max(y) - final_value) / final_value) * 100, 0)

def compute_steady_state_error(y, target):
    return abs(target - y[-1])

def compute_IAE(t, y, target):
    error = target - y
    return np.trapz(np.abs(error), t)

def compute_metrics(t, y, target=1.0, tol=0.02):
    final_value = y[-1]
    return {
        'rise_time': round(float(compute_rise_time(t, y, final_value)), 4),
        'settling_time': round(float(compute_settling_time(t, y, final_value, tol)), 4),
        'overshoot': round(float(compute_overshoot(y, final_value)), 4),
        'steady_state_error': round(float(compute_steady_state_error(y, target)), 4),
        'IAE': round(float(compute_IAE(t, y, target)), 4)
    }
