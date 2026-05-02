import sympy as sp
import math

def ejecutar_taylor(funcion_str, a, n, x_eval):
    try:
        x = sp.symbols('x')
        # Usamos sympify para obtener la expresión matemática del string
        f_simbolica = sp.sympify(funcion_str)
        
        iteraciones = []
        polinomio_acumulado_expr = sp.Integer(0)
        valor_real = float(f_simbolica.subs(x, x_eval).evalf())

        for i in range(n + 1):
            # 1. Derivada de orden i
            derivada = sp.diff(f_simbolica, x, i)
            # 2. Evaluar f^(i)(a)
            f_i_a = derivada.subs(x, a)
            
            # 3. Construir el término simbólico: [f^(i)(a) / i!] * (x - a)**i
            denominador = math.factorial(i)
            termino = (f_i_a / denominador) * (x - a)**i
            
            # 4. Acumular en el polinomio expresado simbólicamente
            polinomio_acumulado_expr += termino
            
            # 5. Evaluación numérica para la tabla
            aprox_actual = float(polinomio_acumulado_expr.subs(x, x_eval).evalf())
            error_abs = abs(valor_real - aprox_actual)
            
            iteraciones.append({
                "i": i,
                "f^(i)(a)": float(f_i_a.evalf()),
                "Termino": sp.latex(sp.simplify(termino)),
                "Aproximacion": aprox_actual,
                "Error_Abs": error_abs
            })

        # Creamos la función numérica del polinomio para la gráfica
        poly_func_num = sp.lambdify(x, polinomio_acumulado_expr, "numpy")

        return True, "", {
            "iteraciones": iteraciones,
            "polinomio_final_latex": sp.latex(sp.simplify(polinomio_acumulado_expr)),
            "poly_func_num": poly_func_num,
            "valor_real": valor_real
        }
    except Exception as e:
        return False, f"Error en el cálculo de Taylor: {str(e)}", None  