
def l1_loss(actual, target):
    return abs(actual - target)

def l2_loss(actual, target):
    return (actual - target) ** 2

def huber_loss(actual, target, delta=1.0):
    error = actual - target
    if abs(error) <= delta:
        return 0.5 * error ** 2
    else:
        return delta * (abs(error) - 0.5 * delta)

loss_registry = {
    'L1': l1_loss,
    'L2': l2_loss,
    'Huber': huber_loss,
}

def compute_weighted_loss(metrics, requirements, weights, loss='L1', epsilon=1e-6, verbose=False):
    """
    Compute a weighted score based on how far each metric is from its requirement.
    
    Lower score = better.
    """
    score = 0

    for name in requirements:
        actual = metrics[name]
        target = requirements[name]
        normalized_actual = actual / (target + epsilon)
        weight = weights.get(name, 1.0)
        # Select the appropriate loss function
        if isinstance(loss, str):
            loss_fn = loss_registry[loss]
        elif isinstance(loss, dict):
            loss_type = loss.get(name, 'L1')
            loss_fn = loss_registry[loss_type]
        else:
            raise ValueError("loss must be a string or a dict of metric:loss_type")
        normalized_loss = loss_fn(normalized_actual, 1.0)
        # Print Output if Verbose
        if verbose:
            print(f"{name}: actual={actual}, norm={normalized_actual:.4f}, loss={normalized_loss:.4f}, weight={weight}")
        # Normalize the score 
        score += weight * normalized_loss

    return round(score, 4)
