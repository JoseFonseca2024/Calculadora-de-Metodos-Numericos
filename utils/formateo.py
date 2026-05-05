def fmt(x):
    if x is None:
        return "-"
    if isinstance(x, int):
        return str(x)  
    if abs(x) < 1e-6 or abs(x) > 1e6:
        return f"{x:.8E}"
    return f"{x:.8f}"
