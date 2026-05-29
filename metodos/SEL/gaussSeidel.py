import numpy as np


def ejecutarGaussSeidel(A, B, tol, max_iter=100):

    # ==========================================
    # CONVERTIR A NUMPY
    # ==========================================

    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    n = len(B)

    # ==========================================
    # VECTOR INICIAL
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

    for i in range(n):

        if abs(A[i][i]) < 1e-14:

            return (
                False,
                f"El elemento diagonal A[{i+1},{i+1}] es cero.",
                None
            )

    # ==========================================
    # DETERMINANTE
    # ==========================================

    detA = np.linalg.det(A)

    if abs(detA) < 1e-14:

        return (
            False,
            "La matriz A es singular.",
            None
        )

    # ==========================================
    # ITERACIONES
    # ==========================================

    for k in range(max_iter):

        X_viejo = X.copy()

        # ======================================
        # RECORRER VARIABLES
        # ======================================

        for i in range(n):

            suma = 0

            for j in range(n):

                if i != j:

                    suma += A[i][j] * X[j]

            X[i] = (
                B[i] - suma
            ) / A[i][i]

        # ======================================
        # ERRORES
        # ======================================

        errores = []

        for i in range(n):

            if abs(X[i]) < 1e-14:

                err = 0

            else:

                err = abs(
                    (X[i] - X_viejo[i])
                    / X[i]
                ) * 100

            errores.append(err)

        error_max = max(errores)

        # ======================================
        # GUARDAR ITERACION
        # ======================================

        iteraciones.append({

            "i": k,

            "Xi": X_viejo.tolist(),

            "Xi+1": X.tolist(),

            "Errores": errores,

            "Error%": error_max
        })

        # ======================================
        # CONVERGENCIA
        # ======================================

        if error_max < tol:

            break

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
    