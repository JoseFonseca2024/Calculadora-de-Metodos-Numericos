import numpy as np


def ordenar_matriz_diagonalmente(A, B):

    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    n = len(A)

    A_ordenada = np.zeros_like(A)
    B_ordenado = np.zeros_like(B)

    filas_usadas = set()

    # ==========================================
    # BUSCAR FILAS DOMINANTES
    # ==========================================

    for i in range(n):

        encontrada = False

        for fila in range(n):

            if fila in filas_usadas:
                continue

            diagonal = abs(A[fila][i])

            suma = sum(
                abs(A[fila][j])
                for j in range(n)
                if j != i
            )

            # Dominancia diagonal
            if diagonal >= suma:

                A_ordenada[i] = A[fila]
                B_ordenado[i] = B[fila]

                filas_usadas.add(fila)

                encontrada = True
                break

        if not encontrada:

            return (
                False,
                "No fue posible reordenar la matriz para obtener dominancia diagonal.",
                None,
                None
            )

    return (
        True,
        "",
        A_ordenada.tolist(),
        B_ordenado.tolist()
    )