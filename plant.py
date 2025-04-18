import control as ctrl

def get_default_plant():
    """
    Returns a simple first-order transfer function:
        G(s) = 1 / (s + 1)
    """
    numerator = [1]
    denominator = [1, 1]
    return ctrl.TransferFunction(numerator, denominator)
