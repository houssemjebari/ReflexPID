import matplotlib.pyplot as plt

def plot_response(t, y, title="Step Response", target=1.0, tol=0.02, settling_time=None):
    plt.figure(figsize=(8, 4))
    plt.plot(t, y, label='System Output', linewidth=2)

    # Add ±2% band
    upper = target * (1 + tol)
    lower = target * (1 - tol)
    plt.hlines([upper, lower], xmin=t[0], xmax=t[-1], colors='gray', linestyles='dashed', label='±2% Band')

    # Settling time line
    if settling_time is not None:
        plt.axvline(settling_time, color='red', linestyle='--', label=f'Settling Time: {settling_time:.2f}s')

    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Output")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
