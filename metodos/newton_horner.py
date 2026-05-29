import numpy as np


def ejecutar_newton_horner(coeficientes, Ci, tol):

    iteraciones = []

    max_iter = 100

    i = 0

    while i < max_iter:

        n = len(coeficientes)

        # =====================================
        # HORNER PARA P(x)
        # =====================================

        b = [0] * n

        b[0] = coeficientes[0]

        for j in range(1, n):

            b[j] = coeficientes[j] + Ci * b[j - 1]

        fx = b[-1]

        # =====================================
        # HORNER PARA P'(x)
        # =====================================

        d = [0] * (n - 1)

        d[0] = b[0]

        for j in range(1, n - 1):

            d[j] = b[j] + Ci * d[j - 1]

        dfx = d[-1]

        # =====================================
        # VALIDAR DERIVADA
        # =====================================

        if abs(dfx) < 1e-14:

            return False, "La derivada es cero.", None

        # =====================================
        # NEWTON-RAPHSON
        # =====================================

        Ci_next = Ci - (fx / dfx)

        # =====================================
        # ERROR
        # =====================================

        if abs(Ci_next) < 1e-14:

            error = 0

        else:

            error = abs((Ci_next - Ci) / Ci_next) * 100

        # =====================================
        # GUARDAR ITERACION
        # =====================================

        iteraciones.append({

            "i": i,

            "Ci": float(Ci),

            "coeficientes": [float(c) for c in coeficientes],

            "b": [float(v) for v in b],

            "d": [float(v) for v in d],

            "Residuo": float(fx),

            "Funcion": float(fx),

            "Derivada": float(dfx),

            "Ci+1": float(Ci_next),

            "Error%": float(error)
        })

        # =====================================
        # CONVERGENCIA
        # =====================================

        if error < tol:

            break

        Ci = Ci_next

        i += 1

    return True, "", iteraciones

