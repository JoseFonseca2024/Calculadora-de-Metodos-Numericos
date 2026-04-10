import numpy as np

def evaluar_seguro(f, x):
    try:
        y = f(x)

        if isinstance(y, (list, tuple, np.ndarray)):
            y = y[0]

        y = float(y)

        if np.isnan(y) or np.isinf(y):
            return None

        return y

    except Exception:
        return None