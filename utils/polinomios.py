import sympy as sp 
import re 
from sympy.parsing.sympy_parser import ( parse_expr, standard_transformations, implicit_multiplication_application, convert_xor )

def validar_Y_preparar_polinomio(polinomio_str):

    if not polinomio_str or not polinomio_str.strip():
        return False, "Debe ingresar una expresión", None

    try: 
        texto_original = polinomio_str.replace(" ", "")

        if "=" in texto_original:
            izquierda, derecha = texto_original.split("=")
            expr_str = f"({izquierda})-({derecha})"
        else:
            expr_str = texto_original

        # 🔹 ESTO VA FUERA DEL ELSE
        p_prep = expr_str.lower()
        p_prep = p_prep.replace(",", ".")
        p_prep = p_prep.replace("π", "pi")
        p_prep = p_prep.replace("²", "**2").replace("³", "**3")

        transformaciones = standard_transformations + (
            implicit_multiplication_application,
            convert_xor
        )

        x = sp.symbols("x")

        # 🔹 Parseo
        p_sym = parse_expr(
            p_prep,
            transformations=transformaciones
        )

        if not p_sym.is_polynomial(x):
            return False, "La expresión no es un polinomio en x.", None
        
        polinomio = sp.Poly(p_sym, x)
        grado = polinomio.degree()
        coeficientes = polinomio.all_coeffs()

        p_num = sp.lambdify(x, p_sym, "numpy")

        p_visual = texto_original.replace("**", "^")
        p_visual = re.sub(r'\^([\-\+]?[a-zA-Z0-9\(\)]+)', r'^{\1}', p_visual)

        return True, "", (p_sym, x, grado, coeficientes, p_num, p_visual)

    except (sp.SympifyError, TypeError, ValueError) as e:
        return False, f"Error: {str(e)}", None

