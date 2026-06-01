import sympy as sp


def ejecutarPolNewton(x_vals, y_vals, grado):

    try:

        n = len(x_vals)

        if n != len(y_vals):

            return (
                False,
                "La cantidad de valores x y f(x) debe coincidir.",
                None
            )

        if len(set(x_vals)) != len(x_vals):

            return (
                False,
                "Existen valores de x repetidos.",
                None
            )

        # ==========================================
        # TABLA DE DIFERENCIAS DIVIDIDAS
        # ==========================================

        tabla = [
            [None] * n
            for _ in range(n)
        ]

        for i in range(n):

            tabla[i][0] = float(
                y_vals[i]
            )

        for j in range(1, n):

            for i in range(j, n):

                tabla[i][j] = (
                    tabla[i][j - 1]
                    -
                    tabla[i - 1][j - 1]
                ) / (
                    x_vals[i]
                    -
                    x_vals[i - j]
                )

        # ==========================================
        # COEFICIENTES
        # ==========================================

        coeficientes = []

        for i in range(grado + 1):

            coeficientes.append(
                tabla[i][i]
            )

        # ==========================================
        # POLINOMIO
        # ==========================================

        x = sp.Symbol("x")

        polinomio = coeficientes[0]

        producto = 1

        terminos_expr = [
            sp.Float(coeficientes[0])
        ]

        for i in range(1, grado + 1):

            producto *= (
                x - x_vals[i - 1]
            )

            termino = (
                coeficientes[i]
                * producto
            )

            terminos_expr.append(
                sp.expand(
                    sp.simplify(
                        termino
                    )
                )
            )

            polinomio += termino

        return (
            True,
            "",
            {
                "grado": grado,
                "tabla": tabla,
                "coeficientes": coeficientes,
                "terminos_expr": terminos_expr,
                "polinomio": sp.simplify(
                    polinomio
                ),
                "polinomio_expandido":
                    sp.expand(
                        polinomio
                    )
            }
        )

    except Exception as e:

        return (
            False,
            str(e),
            None
        )