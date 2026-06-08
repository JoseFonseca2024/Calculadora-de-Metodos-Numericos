import sympy as sp
import numpy as np

from metodos.SEL.jacobi import ejecutarJacobi
from metodos.SEL.gaussSeidel import ejecutarGaussSeidel


def ejecutarTrazadoresCubicos(
    x_vals,
    y_vals,
    metodo="Directo",
    tol=0.001
):

    try:

        # ==========================================
        # VALIDACIONES
        # ==========================================

        n_puntos = len(x_vals)

        if n_puntos != len(y_vals):

            return (
                False,
                "La cantidad de x y f(x) debe coincidir.",
                None
            )

        if n_puntos < 2:

            return (
                False,
                "Debe ingresar al menos dos puntos.",
                None
            )

        if len(set(x_vals)) != n_puntos:

            return (
                False,
                "Existen valores x repetidos.",
                None
            )

        # ==========================================
        # VARIABLES
        # ==========================================

        x = sp.Symbol("x")

        n_splines = n_puntos - 1

        splines = []

        variables = []

        # ==========================================
        # CREAR SPLINES
        # ==========================================

        for i in range(n_splines):

            a = sp.Symbol(f"a{i+1}")
            b = sp.Symbol(f"b{i+1}")
            c = sp.Symbol(f"c{i+1}")
            d = sp.Symbol(f"d{i+1}")

            variables.extend(
                [a, b, c, d]
            )

            spline = (
                a * x**3
                + b * x**2
                + c * x
                + d
            )

            splines.append(spline)

        # ==========================================
        # ECUACIONES
        # ==========================================

        condiciones_ajuste = []

        condiciones_derivada1 = []

        condiciones_derivada2 = []

        condiciones_naturales = []

        ecuaciones = []

        # ==========================================
        # AJUSTE
        # ==========================================

        for i in range(n_splines):

            xi = x_vals[i]
            xi1 = x_vals[i + 1]

            yi = y_vals[i]
            yi1 = y_vals[i + 1]

            eq1 = sp.Eq(
                splines[i].subs(x, xi),
                yi
            )

            eq2 = sp.Eq(
                splines[i].subs(x, xi1),
                yi1
            )

            condiciones_ajuste.append(eq1)
            condiciones_ajuste.append(eq2)

            ecuaciones.append(eq1)
            ecuaciones.append(eq2)

        # ==========================================
        # CONTINUIDAD PRIMERA DERIVADA
        # ==========================================

        for i in range(n_splines - 1):

            deriv1 = sp.diff(
                splines[i],
                x
            )

            deriv2 = sp.diff(
                splines[i + 1],
                x
            )

            nodo = x_vals[i + 1]

            eq = sp.Eq(
                deriv1.subs(x, nodo),
                deriv2.subs(x, nodo)
            )

            condiciones_derivada1.append(eq)

            ecuaciones.append(eq)

        # ==========================================
        # CONTINUIDAD SEGUNDA DERIVADA
        # ==========================================

        for i in range(n_splines - 1):

            deriv1 = sp.diff(
                splines[i],
                x,
                2
            )

            deriv2 = sp.diff(
                splines[i + 1],
                x,
                2
            )

            nodo = x_vals[i + 1]

            eq = sp.Eq(
                deriv1.subs(x, nodo),
                deriv2.subs(x, nodo)
            )

            condiciones_derivada2.append(eq)

            ecuaciones.append(eq)

        # ==========================================
        # CONDICIONES NATURALES
        # ==========================================

        deriv2_ini = sp.diff(
            splines[0],
            x,
            2
        )

        deriv2_fin = sp.diff(
            splines[-1],
            x,
            2
        )

        eq_ini = sp.Eq(
            deriv2_ini.subs(
                x,
                x_vals[0]
            ),
            0
        )

        eq_fin = sp.Eq(
            deriv2_fin.subs(
                x,
                x_vals[-1]
            ),
            0
        )

        condiciones_naturales.append(eq_ini)
        condiciones_naturales.append(eq_fin)

        ecuaciones.append(eq_ini)
        ecuaciones.append(eq_fin)

        # ==========================================
        # MATRIZ
        # ==========================================

        A, B = sp.linear_eq_to_matrix(
            ecuaciones,
            variables
        )

        A_np = np.array(
            A,
            dtype=float
        )

        B_np = np.array(
            B,
            dtype=float
        ).flatten()

        # ==========================================
        # RESOLVER SISTEMA
        # ==========================================

        iteraciones = None

        if metodo == "Directo":

            solucion = np.linalg.solve(
                A_np,
                B_np
            )

        elif metodo == "Jacobi":

            ok, msg, iteraciones = (
                ejecutarJacobi(
                    A_np,
                    B_np,
                    tol
                )
            )

            if not ok:

                return (
                    False,
                    msg,
                    None
                )

            solucion = (
                iteraciones[-1]["Xi+1"]
            )

        elif metodo == "Gauss-Seidel":

            ok, msg, iteraciones = (
                ejecutarGaussSeidel(
                    A_np,
                    B_np,
                    tol
                )
            )

            if not ok:

                return (
                    False,
                    msg,
                    None
                )

            solucion = (
                iteraciones[-1]["Xi+1"]
            )

        else:

            return (
                False,
                "Método inválido.",
                None
            )

        # ==========================================
        # MAPEAR SOLUCION
        # ==========================================

        mapa = {}

        for i, var in enumerate(
            variables
        ):

            mapa[var] = solucion[i]

        # ==========================================
        # SPLINES FINALES
        # ==========================================

        splines_finales = []

        for spline in splines:

            spline_final = spline.subs(
                mapa
            )

            spline_final = sp.expand(
                spline_final
            )

            splines_finales.append(
                spline_final
            )

        # ==========================================
        # RETORNO
        # ==========================================

        return (
            True,
            "",
            {
                "splines": splines,
                "variables": variables,
                "condiciones_ajuste":
                    condiciones_ajuste,
                "condiciones_derivada1":
                    condiciones_derivada1,
                "condiciones_derivada2":
                    condiciones_derivada2,
                "condiciones_naturales":
                    condiciones_naturales,
                "ecuaciones": ecuaciones,
                "A": A_np,
                "B": B_np,
                "solucion": solucion,
                "splines_finales":
                    splines_finales,
                "iteraciones":
                    iteraciones
            }
        )

    except Exception as e:

        return (
            False,
            f"Error: {str(e)}",
            None
        )
