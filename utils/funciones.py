import sympy as sp
import re
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, 
    implicit_multiplication_application, convert_xor
)

def validar_y_preparar_funcion(funcion_str):
    if not funcion_str or not funcion_str.strip():
        return False, "Debe ingresar una expresión.", None
    try:
        texto_original = funcion_str.replace(" ", "")
        f_prep = texto_original.lower().replace(",", ".").replace("sen", "sin").replace("tg", "tan")
        
        transformaciones = standard_transformations + (implicit_multiplication_application, convert_xor)
        x = sp.symbols('x')
        local_dict = {"e": sp.E, "pi": sp.pi}
        
        f_sym = parse_expr(f_prep, transformations=transformaciones, local_dict=local_dict)
        f_num = sp.lambdify(x, f_sym, 'numpy')
        f_der_sym = sp.diff(f_sym, x)
        f_der_num = sp.lambdify(x, f_der_sym, 'numpy')

        # Formateo visual para que e^-x no se desarme
        f_visual = texto_original.replace("**", "^")
        f_visual = re.sub(r'\^([\-\+]?[a-zA-Z0-9\(\)]+)', r'^{\1}', f_visual)
        f_visual = f_visual.replace("*", "")

        return True, "", (f_sym, x, f_num, f_der_num, f_visual)
    except Exception as e:
        return False, f"Error: {str(e)}", None