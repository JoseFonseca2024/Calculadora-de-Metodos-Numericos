import sympy as sp

def generar_gs_algebraicas(expr):
    x = sp.Symbol('x')

    gs = []
    candidatos = []

    # -------- DESPEJE GENERAL --------
    try:
        soluciones = sp.solve(sp.Eq(expr, 0), x)
        for sol in soluciones:
            candidatos.append(sp.simplify(sol))
    except (sp.SympifyError, ValueError, TypeError):
        pass

    # -------- DESPEJE LINEAL --------
    if expr.coeff(x) != 0:
        try:
            coef_x = expr.coeff(x)
            otros = expr - coef_x * x
            g_lineal = sp.simplify(-otros / coef_x)
            candidatos.append(g_lineal)
        except:
            pass

    # -------- EXPONENCIAL --------
    if expr.has(sp.exp(x)):
        try:
            despeje = sp.solve(sp.Eq(expr, 0), sp.exp(x))
            if despeje:
                g_exp = sp.log(despeje[0])
                candidatos.append(sp.simplify(g_exp))
        except:
            pass

    # -------- LOG --------
    if expr.has(sp.log(x)):
        try:
            despeje = sp.solve(sp.Eq(expr, 0), sp.log(x))
            if despeje:
                g_log = sp.exp(despeje[0])
                candidatos.append(sp.simplify(g_log))
        except:
            pass

    # -------- DESPEJE POR POTENCIAS (CLAVE) --------
    for potencia in range(2, 15):
        if expr.has(x**potencia):
            try:
                coef = expr.coeff(x**potencia)

                if coef != 0:
                    resto = expr - coef * x**potencia
                    base = -resto / coef

                    g1 = base**(1/potencia)
                    candidatos.append(sp.simplify(g1))

                    # considerar negativo si potencia es par
                    if potencia % 2 == 0:
                        g2 = -base**(1/potencia)
                        candidatos.append(sp.simplify(g2))

            except:
                continue

    # -------- FILTRO --------
    candidatos_validos = []

    for g in candidatos:
        try:
            if g.has(sp.I) or g.has(sp.zoo) or g.has(sp.oo):
                continue

            if g.free_symbols != {x}:
                continue

            candidatos_validos.append(sp.simplify(g))
        except:
            continue

    # eliminar duplicados
    candidatos_unicos = []
    for g in candidatos_validos:
        if g not in candidatos_unicos:
            candidatos_unicos.append(g)

    # FORMATO FINAL
    for i, g in enumerate(candidatos_unicos):
        gs.append({
            "nombre": f"g{i+1}(x)",
            "expr": g,
            "latex": sp.latex(g)
        })

    return gs