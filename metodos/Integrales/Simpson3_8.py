import sympy as sp


def ejecutarSimpson38(
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
        # VALIDAR n MÚLTIPLO DE 3
        # ==========================================

        if n % 3 != 0:

            return (
                False,
                "Para Simpson 3/8 el número de subintervalos debe ser múltiplo de 3.",
                None
            )

        # ==========================================
        # VARIABLES
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
            # SUMAS SIMPSON 3/8
            # --------------------------------------

            suma_3 = 0
            suma_2 = 0

            pesos = []

            for i in range(n + 1):

                if i == 0 or i == n:

                    pesos.append(1)

                elif i % 3 == 0:

                    pesos.append(2)

                    suma_2 += fi[i]

                else:

                    pesos.append(3)

                    suma_3 += fi[i]

            # --------------------------------------
            # SIMPSON 3/8
            # --------------------------------------

            resultado = (

                (3 * h) / 8

            ) * (

                fi[0]

                +

                3 * suma_3

                +

                2 * suma_2

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

                    "pesos": pesos,

                    "suma_3":
                        suma_3,

                    "suma_2":
                        suma_2,

                    "resultado":
                        resultado
                }
            )

        # ==========================================
        # INTEGRAL DOBLE
        # ==========================================

        else:

            # --------------------------------------
            # INTEGRAL INDEFINIDA
            # --------------------------------------

            integral_indefinida = sp.integrate(
                expr,
                y
            )

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
            # LÍMITE SUPERIOR
            # --------------------------------------

            integral_superior = (

                integral_indefinida.subs(
                    y,
                    by
                )

            )

            # --------------------------------------
            # LÍMITE INFERIOR
            # --------------------------------------

            integral_inferior = (

                integral_indefinida.subs(
                    y,
                    ay
                )

            )

            # --------------------------------------
            # INTEGRAL INTERNA
            # --------------------------------------

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
            # SUMAS SIMPSON 3/8
            # --------------------------------------

            suma_3 = 0
            suma_2 = 0

            pesos = []

            for i in range(n + 1):

                if i == 0 or i == n:

                    pesos.append(1)

                elif i % 3 == 0:

                    pesos.append(2)

                    suma_2 += fi[i]

                else:

                    pesos.append(3)

                    suma_3 += fi[i]

            # --------------------------------------
            # SIMPSON 3/8
            # --------------------------------------

            resultado = (

                (3 * h) / 8

            ) * (

                fi[0]

                +

                3 * suma_3

                +

                2 * suma_2

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

                    "pesos": pesos,

                    "suma_3":
                        suma_3,

                    "suma_2":
                        suma_2,

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