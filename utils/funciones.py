import sympy as sp
import re
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

def validar_y_preparar_funcion(funcion_str):
    if not funcion_str or not funcion_str.strip():
        return False, "Debe ingresar una expresión.", None
    
    if "=" in funcion_str:
        return False, "Formato incorrecto: ingrese solo la función sin ninguna igualdad.", None
    try:
        texto_original = funcion_str.replace(" ", "")

        # Normalización base
        f_prep = texto_original.lower()
        f_prep = f_prep.replace(",", ".")

        # Trigonométricas
        f_prep = (
            f_prep.replace("sen", "sin")
                .replace("tg", "tan")
                .replace("ctg", "cot")
                .replace("cosec", "csc")
        )

        # Símbolos
        f_prep = f_prep.replace("π", "pi")

        # Potencias 
        f_prep = f_prep.replace("²", "**2").replace("³", "**3")

        # 🔹 Constante e
        f_prep = re.sub(r'\be\b', 'E', f_prep)

        # EXPONENCIAL
        f_prep = re.sub(r'E\*\*\((.*?)\)', r'exp(\1)', f_prep)
        f_prep = re.sub(r'E\*\*([a-zA-Z0-9]+)', r'exp(\1)', f_prep)

        # RAÍCES

        # √(expresión)
        f_prep = re.sub(r'√\((.*?)\)', r'sqrt(\1)', f_prep)

        # √x
        f_prep = re.sub(r'√([a-zA-Z0-9]+)', r'sqrt(\1)', f_prep)

        # raiz(x)
        f_prep = re.sub(r'raiz\((.*?)\)', r'sqrt(\1)', f_prep)

        # raiz3(x) → x^(1/3)
        f_prep = re.sub(r'raiz(\d+)\((.*?)\)', r'(\2)**(1/\1)', f_prep)

        # ∛(x+1)
        f_prep = re.sub(r'∛\((.*?)\)', r'(\1)**(1/3)', f_prep)

        # ∛x
        f_prep = re.sub(r'∛([a-zA-Z0-9]+)', r'(\1)**(1/3)', f_prep)


        # 🔹 Transformaciones
        transformaciones = standard_transformations + (
            implicit_multiplication_application,
            convert_xor
        )

        x = sp.symbols('x')

        local_dict = {
            "e": sp.E,
            "pi": sp.pi,

            # trig
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "cot": sp.cot,
            "sec": sp.sec,
            "csc": sp.csc,

            # otras
            "log": sp.log,
            "ln": sp.log,
            "sqrt": sp.sqrt,
            "exp": sp.exp
        }

        # 🔹 Parseo
        f_sym = parse_expr(
            f_prep,
            transformations=transformaciones,
            local_dict=local_dict
        )

        # 🔹 Numérico
        f_num = sp.lambdify(x, f_sym, 'numpy')

        # 🔹 Derivada
        f_der_sym = sp.diff(f_sym, x)
        f_der_num = sp.lambdify(x, f_der_sym, 'numpy')

        # 🔹 Visual
        f_visual = texto_original.replace("**", "^")
        f_visual = re.sub(r'\^([\-\+]?[a-zA-Z0-9\(\)]+)', r'^{\1}', f_visual)
        f_visual = f_visual.replace("*", "")

        return True, "", (f_sym, x, f_num, f_der_num, f_visual)

    except (sp.SympifyError, TypeError, ValueError) as e:
        return False, f"Error: {str(e)}", None