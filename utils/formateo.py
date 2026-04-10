def fmt(x):
    if x is None:
        return "-"
    if abs(x) < 1e-6 or abs(x) > 1e6:
        return f"{x:.6E}"
    return f"{x:.6f}"