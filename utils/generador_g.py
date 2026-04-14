import sympy as sp


def generar_gs_algebraicas(expr):
    x = sp.Symbol('x')

    gs = []
    candidatos = []

    # -------- DESPEJE LINEAL --------
    if expr.coeff(x) != 0:

        coef_x = expr.coeff(x)

        otros = expr - coef_x*x

        g_lineal = sp.simplify(-otros / coef_x)

        candidatos.append(g_lineal)


    # -------- DESPEJE CUADRÁTICO --------
    if expr.has(x**2):

        try:
            despeje = sp.solve(sp.Eq(expr, 0), x**2)

            if despeje:
                candidatos.append(
                    sp.simplify(
                        sp.sqrt(despeje[0])
                    )
                )

        except:
            pass


    # -------- DESPEJE EXPONENCIAL --------
    if expr.has(sp.exp(x)):

        try:
            despeje = sp.solve(sp.Eq(expr, 0), sp.exp(x))

            if despeje:
                candidatos.append(
                    sp.simplify(
                        sp.log(despeje[0])
                    )
                )

        except:
            pass


    # -------- DESPEJE LOG --------
    if expr.has(sp.log(x)):

        try:
            despeje = sp.solve(sp.Eq(expr, 0), sp.log(x))

            if despeje:
                candidatos.append(
                    sp.simplify(
                        sp.exp(despeje[0])
                    )
                )

        except:
            pass


    # Eliminar repetidos
    candidatos_unicos = []

    for g in candidatos:

        if g not in candidatos_unicos:
            candidatos_unicos.append(g)


    # Formato final
    for i, g in enumerate(candidatos_unicos):

        gs.append({
            "nombre": f"g{i+1}(x)",
            "expr": g,
            "latex": sp.latex(g)
        })

    return gs