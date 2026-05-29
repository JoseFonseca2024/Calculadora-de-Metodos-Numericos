import numpy as np


def ejecutarJacobi(A, B, tol, max_iter=100):

    # ==========================================
    # CONVERTIR A NUMPY
    # ==========================================

    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    n = len(B)

    # ==========================================
    # VECTOR INICIAL AUTOMATICO
    # ==========================================

    X = np.zeros(n)

    iteraciones = []

    # ==========================================
    # VALIDACIONES
    # ==========================================

    if A.shape[0] != A.shape[1]:

        return (
            False,
            "La matriz A debe ser cuadrada.",
            None
        )

    if len(B) != A.shape[0]:

        return (
            False,
            "Dimensiones incompatibles.",
            None
        )

    # ==========================================
    # DETERMINANTE
    # ==========================================

    detA = np.linalg.det(A)

    if abs(detA) < 1e-14:

        return (
            False,
            "La matriz A es singular (det(A)=0).",
            None
        )

    # ==========================================
    # ITERACIONES
    # ==========================================

    for k in range(max_iter):

        X_nuevo = np.zeros(n)

        # ======================================
        # CALCULO DE VARIABLES
        # ======================================

        for i in range(n):

            suma = 0

            for j in range(n):

                if i != j:

                    suma += A[i][j] * X[j]

            X_nuevo[i] = (
                B[i] - suma
            ) / A[i][i]

        # ======================================
        # ERRORES
        # ======================================

        errores = []

        for i in range(n):

            if abs(X_nuevo[i]) < 1e-14:

                err = 0

            else:

                err = abs(
                    (X_nuevo[i] - X[i])
                    / X_nuevo[i]
                ) * 100

            errores.append(err)

        error_max = max(errores)

        # ======================================
        # GUARDAR ITERACION
        # ======================================

        iteraciones.append({

            "i": k,

            "Xi": X.tolist(),

            "Xi+1": X_nuevo.tolist(),

            "Errores": errores,

            "Error%": error_max
        })

        # ======================================
        # CONVERGENCIA
        # ======================================

        if error_max < tol:

            break

        X = X_nuevo.copy()

    # ==========================================
    # MAX ITERACIONES
    # ==========================================

    if len(iteraciones) >= max_iter:

        return (
            False,
            "El método alcanzó el máximo de iteraciones.",
            iteraciones
        )

    return (
        True,
        "",
        iteraciones
    )