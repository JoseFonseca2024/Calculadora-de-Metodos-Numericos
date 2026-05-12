import sympy as sp
import numpy as np

def generar_gs_algebraicas(expr):

    x = sp.Symbol('x')

    gs = []
    candidatos = []

    # =========================================================
    # FUNCIONES INVERSAS TRIGONOMÉTRICAS
    # =========================================================

    TRIG_INVERSAS = {
        sp.sin: sp.asin,
        sp.cos: sp.acos,
        sp.tan: sp.atan
    }

    # =========================================================
    # DESPEJE LINEAL
    # =========================================================

    if expr.coeff(x) != 0:

        try:

            coef_x = expr.coeff(x)

            otros = expr - coef_x * x

            g_lineal = sp.simplify(-otros / coef_x)

            candidatos.append(g_lineal)

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError
        ):
            pass

    # =========================================================
    # EXPONENCIALES
    # =========================================================

    for exp_expr in expr.atoms(sp.exp):

        try:

            despeje = sp.solve(
                sp.Eq(expr, 0),
                exp_expr
            )

            if despeje:

                rhs = despeje[0]

                argumento = exp_expr.args[0]

                eq = sp.Eq(
                    argumento,
                    sp.log(rhs)
                )

                soluciones_x = sp.solve(eq, x)

                for sol in soluciones_x:

                    candidatos.append(
                        sp.simplify(sol)
                    )

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError
        ):
            continue

    # =========================================================
    # LOGARITMOS
    # =========================================================

    for log_expr in expr.atoms(sp.log):

        try:

            despeje = sp.solve(
                sp.Eq(expr, 0),
                log_expr
            )

            if despeje:

                rhs = despeje[0]

                argumento = log_expr.args[0]

                eq = sp.Eq(
                    argumento,
                    sp.exp(rhs)
                )

                soluciones_x = sp.solve(eq, x)

                for sol in soluciones_x:

                    candidatos.append(
                        sp.simplify(sol)
                    )

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError
        ):
            continue

    # =========================================================
    # RAÍCES
    # =========================================================

    for raiz in expr.atoms(sp.sqrt):

        try:

            despeje = sp.solve(
                sp.Eq(expr, 0),
                raiz
            )

            if despeje:

                rhs = despeje[0]

                interior = raiz.args[0]

                eq = sp.Eq(
                    interior,
                    rhs**2
                )

                soluciones_x = sp.solve(eq, x)

                for sol in soluciones_x:

                    candidatos.append(
                        sp.simplify(sol)
                    )

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError
        ):
            continue

    # =========================================================
    # TRIGONOMÉTRICAS
    # =========================================================

    for trig_func, inv_func in TRIG_INVERSAS.items():

        for trig_expr in expr.atoms(trig_func):

            try:

                despeje = sp.solve(
                    sp.Eq(expr, 0),
                    trig_expr
                )

                if despeje:

                    rhs = despeje[0]

                    argumento = trig_expr.args[0]

                    eq = sp.Eq(
                        argumento,
                        inv_func(rhs)
                    )

                    soluciones_x = sp.solve(eq, x)

                    for sol in soluciones_x:

                        candidatos.append(
                            sp.simplify(sol)
                        )

            except (
                ValueError,
                TypeError,
                NotImplementedError,
                ZeroDivisionError
            ):
                continue

    # =========================================================
    # POTENCIAS
    # =========================================================

    for potencia in range(2, 15):

        if expr.has(x**potencia):

            try:

                coef = expr.coeff(x**potencia)

                if coef != 0:

                    resto = expr - coef * x**potencia

                    base = -resto / coef

                    g1 = base**sp.Rational(1, potencia)

                    candidatos.append(
                        sp.simplify(g1)
                    )

                    # raíz negativa si potencia par
                    if potencia % 2 == 0:

                        g2 = -base**sp.Rational(1, potencia)

                        candidatos.append(
                            sp.simplify(g2)
                        )

            except (
                ValueError,
                TypeError,
                NotImplementedError,
                ZeroDivisionError
            ):
                continue

    # =========================================================
    # FILTRO
    # =========================================================

    candidatos_validos = []

    for g in candidatos:

        try:

            # complejos o infinitos
            if (
                g.has(sp.I)
                or g.has(sp.zoo)
                or g.has(sp.oo)
            ):
                continue

            # debe depender de x
            if not g.has(x):
                continue

            # evitar x = x
            if sp.simplify(g - x) == 0:
                continue

            # evitar expresiones monstruosas
            if sp.count_ops(g) > 80:
                continue

            # prueba numérica rápida
            test = g.subs(x, 1)

            if test.has(sp.I):
                continue

            candidatos_validos.append(
                sp.simplify(g)
            )

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError
        ):
            continue

    # =========================================================
    # ELIMINAR DUPLICADOS
    # =========================================================

    candidatos_unicos = []

    for g in candidatos_validos:

        if g not in candidatos_unicos:

            candidatos_unicos.append(g)

    # =========================================================
    # FORMATO FINAL (CON EVALUADOR DE RAÍZ REAL)
    # =========================================================
    for i, g in enumerate(candidatos_unicos):
        g_num = sp.lambdify(
            x, 
            g, 
            modules=[
                'numpy', 
                {
                    'Pow': lambda b, e: np.sign(b) * np.abs(b)**e if (isinstance(e, float) and e < 1 and e != 0) or (isinstance(e, (int, float)) and e % 1 != 0) else b**e
                }
            ]
        )

        gs.append({
            "nombre": f"g{i+1}(x)",
            "expr": g,
            "num": g_num,  # Guardamos la versión numérica ya corregida
            "latex": sp.latex(g)
        })

    return gs