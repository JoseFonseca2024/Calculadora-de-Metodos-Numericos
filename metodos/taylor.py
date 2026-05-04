import sympy as sp
import math

def ejecutar_taylor(f_simbolica, x, a, n, x_eval):
    try:
        iteraciones = []
        polinomio_acumulado_expr = sp.Integer(0)

        valor_real = float(f_simbolica.subs(x, x_eval).evalf())

        for i in range(n + 1):

            derivada = sp.diff(f_simbolica, x, i)
            f_i_a = derivada.subs(x, a)

            denominador = math.factorial(i)

            termino = (f_i_a / denominador) * (x - a)**i

            polinomio_acumulado_expr += termino

            aprox_actual = float(polinomio_acumulado_expr.subs(x, x_eval).evalf())
            error_abs = abs(valor_real - aprox_actual)

            iteraciones.append({
                "i": i,
                "derivada_sym": derivada,   # 🔥 AQUÍ ESTABA EL PROBLEMA
                "f^(i)(a)": float(f_i_a.evalf()),
                "Termino": sp.latex(sp.simplify(termino)),
                "Aproximacion": aprox_actual,
                "Error_Abs": error_abs
            })

        poly_func_num = sp.lambdify(x, polinomio_acumulado_expr, "numpy")

        return True, "", {
            "iteraciones": iteraciones,
            "polinomio_final_latex": sp.latex(sp.simplify(polinomio_acumulado_expr)),
            "poly_func_num": poly_func_num,
            "valor_real": valor_real
        }

    except Exception as e:
        return False, f"Error en el cálculo de Taylor: {str(e)}", None