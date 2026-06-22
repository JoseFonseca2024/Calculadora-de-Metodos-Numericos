import sympy as sp


def ejecutarSimpson13(
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
        # VALIDAR n PAR
        # ==========================================

        if n % 2 != 0:

            return (
                False,
                "Para Simpson 1/3 el número de subintervalos debe ser par.",
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

            h = (b - a) / n

            xi = []

            for i in range(n + 1):

                xi.append(
                    a + i * h
                )

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
            # SUMAS
            # --------------------------------------

            suma_impares = 0
            suma_pares = 0

            pesos = []

            for i in range(n + 1):

                if i == 0 or i == n:

                    pesos.append(1)

                elif i % 2 == 1:

                    pesos.append(4)

                    suma_impares += fi[i]

                else:

                    pesos.append(2)

                    suma_pares += fi[i]

            # --------------------------------------
            # SIMPSON 1/3
            # --------------------------------------

            resultado = (

                h / 3

            ) * (

                fi[0]

                +

                4 * suma_impares

                +

                2 * suma_pares

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

                    "suma_impares":
                        suma_impares,

                    "suma_pares":
                        suma_pares,

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
            # SUMAS
            # --------------------------------------

            suma_impares = 0
            suma_pares = 0

            pesos = []

            for i in range(n + 1):

                if i == 0 or i == n:

                    pesos.append(1)

                elif i % 2 == 1:

                    pesos.append(4)

                    suma_impares += fi[i]

                else:

                    pesos.append(2)

                    suma_pares += fi[i]

            # --------------------------------------
            # SIMPSON 1/3
            # --------------------------------------

            resultado = (

                h / 3

            ) * (

                fi[0]

                +

                4 * suma_impares

                +

                2 * suma_pares

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

                    "suma_impares":
                        suma_impares,

                    "suma_pares":
                        suma_pares,

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