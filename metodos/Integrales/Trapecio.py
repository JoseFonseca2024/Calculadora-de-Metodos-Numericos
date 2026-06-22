import sympy as sp


def ejecutarTrapecio(
    expr,
    tipo_integral,
    n,
    a=None,
    b=None,
    ax=None,
    bx=None,
    ay=None,
    by=None
):

    try:

        # ==========================================
        # VARIABLES SIMBÓLICAS
        # ==========================================

        x = sp.Symbol("x")
        y = sp.Symbol("y")

        # ==========================================
        # INTEGRAL SIMPLE
        # ==========================================

        if tipo_integral == "Integral simple":

            # --------------------------------------
            # h
            # --------------------------------------

            h = (b - a) / n

            # --------------------------------------
            # xi
            # --------------------------------------

            xi = []

            for i in range(n + 1):

                xi.append(
                    a + i * h
                )

            # --------------------------------------
            # f(xi)
            # --------------------------------------

            f_num = sp.lambdify(
                x,
                expr,
                "numpy"
            )

            fi = []

            for valor in xi:

                fi.append(
                    float(
                        f_num(valor)
                    )
                )

            # --------------------------------------
            # fórmula trapecio
            # --------------------------------------

            suma_interna = sum(
                fi[1:-1]
            )

            resultado = (
                h / 2
            ) * (
                fi[0]
                +
                2 * suma_interna
                +
                fi[-1]
            )

            return (
                True,
                "",
                {
                    "tipo": "simple",

                    "expr": expr,

                    "h": h,

                    "xi": xi,

                    "fi": fi,

                    "suma_interna":
                        suma_interna,

                    "resultado":
                        resultado
                }
            )

        # ==========================================
        # INTEGRAL DOBLE
        # ==========================================

        else:

            # --------------------------------------
            # Integral indefinida respecto a y
            # --------------------------------------

            integral_indefinida = sp.integrate(
                expr,
                y
            )

            # --------------------------------------
            # Validar si Sympy resolvió
            # --------------------------------------

            if isinstance(
                integral_indefinida,
                sp.Integral
            ):

                return (
                    False,
                    "No fue posible resolver la integral interna de forma analítica.",
                    None
                )

            # --------------------------------------
            # Aplicar límites a la integral interna
            # --------------------------------------

            integral_superior = (
                integral_indefinida.subs(
                    y,
                    by
                )
            )

            integral_inferior = (
                integral_indefinida.subs(
                    y,
                    ay
                )
            )

            integral_interna = sp.simplify(
                integral_superior
                -
                integral_inferior
            )

            # --------------------------------------
            # h
            # --------------------------------------

            h = (
                bx - ax
            ) / n

            # --------------------------------------
            # xi
            # --------------------------------------

            xi = []

            for i in range(n + 1):

                xi.append(
                    ax + i * h
                )

            # --------------------------------------
            # F(xi)
            # --------------------------------------

            f_num = sp.lambdify(
                x,
                integral_interna,
                "numpy"
            )

            fi = []

            for valor in xi:

                fi.append(
                    float(
                        f_num(valor)
                    )
                )

            # --------------------------------------
            # Trapecio
            # --------------------------------------

            suma_interna = sum(
                fi[1:-1]
            )

            resultado = (
                h / 2
            ) * (
                fi[0]
                +
                2 * suma_interna
                +
                fi[-1]
            )

            return (
                True,
                "",
                {
                    "tipo": "doble",

                    "expr": expr,

                    "integral_indefinida":
                        integral_indefinida,

                    "integral_superior":
                        integral_superior,

                    "integral_inferior":
                        integral_inferior,

                    "integral_interna":
                        integral_interna,

                    "h": h,

                    "xi": xi,

                    "fi": fi,

                    "suma_interna":
                        suma_interna,

                    "resultado":
                        resultado
                }
            )

    except Exception as e:

        return (
            False,
            f"Error: {str(e)}",
            None
        )