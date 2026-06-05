import sympy as sp


def ejecutarLagrange(x_vals, y_vals, x_prueba=None):

    try:

        # ==========================================
        # VALIDACIONES
        # ==========================================

        n = len(x_vals)

        if n != len(y_vals):

            return (
                False,
                "La cantidad de x y f(x) debe coincidir.",
                None
            )

        if n < 2:

            return (
                False,
                "Debe ingresar al menos dos puntos.",
                None
            )

        if len(set(x_vals)) != n:

            return (
                False,
                "Existen valores de x repetidos.",
                None
            )

        # ==========================================
        # VARIABLE SIMBÓLICA
        # ==========================================

        x = sp.Symbol("x")

        # ==========================================
        # CONSTRUIR Li
        # ==========================================

        Li_lista = []

        polinomio = 0

        for i in range(n):

            numerador = 1
            denominador = 1

            for j in range(n):

                if i != j:

                    numerador *= (
                        x - x_vals[j]
                    )

                    denominador *= (
                        x_vals[i]
                        - x_vals[j]
                    )

            Li = numerador / denominador

            termino = y_vals[i] * Li

            polinomio += termino

            Li_lista.append({

                "i": i,

                "Li": sp.simplify(Li),

                "termino": sp.expand(
                    sp.simplify(termino)
                ),

                "denominador": denominador
            })

        # ==========================================
        # POLINOMIO FINAL
        # ==========================================

        polinomio_expandido = sp.expand(
            sp.simplify(polinomio)
        )

        # ==========================================
        # VERIFICACIÓN
        # ==========================================

        verificaciones = []

        for i in range(n):

            valor = polinomio_expandido.subs(
                x,
                x_vals[i]
            )

            verificaciones.append({

                "x": x_vals[i],

                "esperado": y_vals[i],

                "obtenido": float(valor)
            })

        # ==========================================
        # PUNTO DE PRUEBA
        # ==========================================

        valor_prueba = None

        if x_prueba is not None:

            valor_prueba = float(
                polinomio_expandido.subs(
                    x,
                    x_prueba
                )
            )

        # ==========================================
        # RETORNO
        # ==========================================

        return (
            True,
            "",
            {

                "Li": Li_lista,

                "polinomio": sp.simplify(
                    polinomio
                ),

                "polinomio_expandido":
                    polinomio_expandido,

                "verificaciones":
                    verificaciones,

                "x_prueba":
                    x_prueba,

                "valor_prueba":
                    valor_prueba
            }
        )

    except Exception as e:

        return (
            False,
            f"Error: {str(e)}",
            None
        )