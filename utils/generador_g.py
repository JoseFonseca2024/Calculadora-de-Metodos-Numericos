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
            ZeroDivisionError,
            RecursionError
        ):
            pass

    # =========================================================
    # DESPEJE RACIONAL SIMPLE
    # =========================================================

    try:

        if expr.has(1/x):

            # aislar 1/x
            despeje = sp.solve(
                sp.Eq(expr, 0),
                1/x
            )

            if despeje:

                rhs = sp.simplify(despeje[0])

                g_racional = sp.simplify(
                    1 / rhs
                )

                candidatos.append(g_racional)

    except (
        ValueError,
        TypeError,
        NotImplementedError,
        ZeroDivisionError,
        RecursionError
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

                rhs = sp.simplify(despeje[0])

                argumento = sp.expand(exp_expr.args[0])

                coef_x = argumento.coeff(x)

                resto = sp.simplify(argumento - coef_x * x)

                # solo si argumento es lineal
                if coef_x != 0 and not resto.has(x):

                    sol = sp.simplify(
                        (sp.log(rhs) - resto) / coef_x
                    )

                    candidatos.append(sol)

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError,
            RecursionError
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

                rhs = sp.simplify(despeje[0])

                argumento = sp.expand(log_expr.args[0])

                coef_x = argumento.coeff(x)

                resto = sp.simplify(argumento - coef_x * x)

                # solo si argumento es lineal
                if coef_x != 0 and not resto.has(x):

                    sol = sp.simplify(
                        (sp.exp(rhs) - resto) / coef_x
                    )

                    candidatos.append(sol)

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError,
            RecursionError
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

                rhs = sp.simplify(despeje[0])

                interior = sp.expand(raiz.args[0])

                coef_x = interior.coeff(x)

                resto = sp.simplify(interior - coef_x * x)

                # solo si interior es lineal
                if coef_x != 0 and not resto.has(x):

                    sol = sp.simplify(
                        (rhs**2 - resto) / coef_x
                    )

                    candidatos.append(sol)

        except (
            ValueError,
            TypeError,
            NotImplementedError,
            ZeroDivisionError,
            RecursionError
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

                    rhs = sp.simplify(despeje[0])

                    argumento = sp.expand(trig_expr.args[0])

                    coef_x = argumento.coeff(x)

                    resto = sp.simplify(argumento - coef_x * x)

                    # solo si argumento es lineal
                    if coef_x != 0 and not resto.has(x):

                        sol = sp.simplify(
                            (inv_func(rhs) - resto) / coef_x
                        )

                        candidatos.append(sol)

            except (
                ValueError,
                TypeError,
                NotImplementedError,
                ZeroDivisionError,
                RecursionError
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

                    g1 = sp.simplify(
                        base**sp.Rational(1, potencia)
                    )

                    candidatos.append(g1)

                    # raíz negativa si potencia par
                    if potencia % 2 == 0:

                        g2 = sp.simplify(
                            -base**sp.Rational(1, potencia)
                        )

                        candidatos.append(g2)

            except (
                ValueError,
                TypeError,
                NotImplementedError,
                ZeroDivisionError,
                RecursionError
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
            if sp.count_ops(g) > 40:
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
            ZeroDivisionError,
            RecursionError
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
    # FORMATO FINAL
    # =========================================================

    for i, g in enumerate(candidatos_unicos):

        try:

            g_num = sp.lambdify(
                x,
                g,
                modules=["numpy"]
            )

            gs.append({
                "nombre": f"g{i+1}(x)",
                "expr": g,
                "num": g_num,
                "latex": sp.latex(g)
            })

        except Exception:
            continue

    return gs