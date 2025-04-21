import control as ctrl

def get_default_plant():
    """
    Returns a simple first-order transfer function:
        G(s) = 1 / (s + 1)
    """
    numerator = [1]
    denominator = [1, 1]
    return Plant(numerator, denominator)

def parse_tf_equation(coeffs):
    terms = []
    degree = len(coeffs) - 1

    for i, coef in enumerate(coeffs):
        power = degree - i
        # Skip 0 Coefficients
        if coef == 0:
            continue
        # Format coefficient
        abs_coef = abs(coef)
        sign = "-" if coef < 0 else "+"
        # Format term
        if power == 0:
            term = f"{abs_coef}"
        elif power == 1:
            term = f"{'' if abs_coef == 1 else abs_coef}s"
        else:
            term = f"{'' if abs_coef == 1 else abs_coef}s^{power}"
        # Add sign (no leading '+' for first term)
        if not terms:
            terms.append(f"{'-' if coef < 0 else ''}{term}")
        else:
            terms.append(f" {sign} {term}")
    return "".join(terms) if terms else "0"


class Plant:

    def __init__(self, numerator=None, denominator=None):
        self.numerator = numerator or [1]
        self.denominator = denominator or [1, 1]
        self.tf = ctrl.TransferFunction(numerator, denominator)

    def get_tf(self):
        return self.tf
    
    def __str__(self):
        output_str = "G(s) = "
        numerator_str = parse_tf_equation(self.numerator)
        denominator_str = parse_tf_equation(self.denominator)
        return f"G(s) = " + numerator_str + " / " + denominator_str

    def to_latex(self):
        num_str = parse_tf_equation(self.numerator)
        den_str = parse_tf_equation(self.denominator)
        return f"$$\\frac{{{num_str}}}{{{den_str}}}$$"

