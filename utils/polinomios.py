import sympy as sp
import re

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)


def validar_y_preparar_polinomio(polinomio_str):

    if not polinomio_str or not polinomio_str.strip():
        return False, "Debe ingresar una expresión.", None

    try:

        texto_original = polinomio_str.replace(" ", "")

        # =====================================================
        # MANEJO DE ECUACIONES
        # =====================================================

        if "=" in texto_original:

            izquierda, derecha = texto_original.split("=")

            expr_str = f"({izquierda})-({derecha})"

        else:

            expr_str = texto_original

        # =====================================================
        # NORMALIZACIÓN
        # =====================================================

        p_prep = expr_str.lower()

        p_prep = p_prep.replace(",", ".")

        # π
        p_prep = p_prep.replace("π", "pi")

        # potencias unicode
        p_prep = (
            p_prep
            .replace("²", "**2")
            .replace("³", "**3")
        )

        # trigonométricas en español
        p_prep = (
            p_prep
            .replace("sen", "sin")
            .replace("tg", "tan")
            .replace("ctg", "cot")
            .replace("cosec", "csc")
        )

        # constante e
        p_prep = re.sub(r'\be\b', 'E', p_prep)

        # =====================================================
        # EXPONENCIALES
        # =====================================================

        p_prep = re.sub(
            r'E\*\*\((.*?)\)',
            r'exp(\1)',
            p_prep
        )

        p_prep = re.sub(
            r'E\*\*([a-zA-Z0-9]+)',
            r'exp(\1)',
            p_prep
        )

        # =====================================================
        # RAÍCES
        # =====================================================

        # √(...)
        p_prep = re.sub(
            r'√\((.*?)\)',
            r'sqrt(\1)',
            p_prep
        )

        # √x
        p_prep = re.sub(
            r'√([a-zA-Z0-9]+)',
            r'sqrt(\1)',
            p_prep
        )

        # raiz(...)
        p_prep = re.sub(
            r'raiz\((.*?)\)',
            r'sqrt(\1)',
            p_prep
        )

        # raiz3(x)
        p_prep = re.sub(
            r'raiz(\d+)\((.*?)\)',
            r'(\2)**(1/\1)',
            p_prep
        )

        # ∛(...)
        p_prep = re.sub(
            r'∛\((.*?)\)',
            r'(\1)**(1/3)',
            p_prep
        )

        # =====================================================
        # TRANSFORMACIONES
        # =====================================================

        transformaciones = standard_transformations + (
            implicit_multiplication_application,
            convert_xor
        )

        x = sp.symbols("x")

        local_dict = {

            "pi": sp.pi,
            "E": sp.E,

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

        # =====================================================
        # PARSEO
        # =====================================================

        p_sym = parse_expr(
            p_prep,
            transformations=transformaciones,
            local_dict=local_dict
        )

        # =====================================================
        # VALIDAR VARIABLE
        # =====================================================

        if not p_sym.has(x):

            return (
                False,
                "La expresión debe depender de x.",
                None
            )

        # =====================================================
        # VALIDAR POLINOMIO
        # =====================================================

        if not p_sym.is_polynomial(x):

            return (
                False,
                "La expresión no es un polinomio en x.",
                None
            )

        # =====================================================
        # POLINOMIO
        # =====================================================

        polinomio = sp.Poly(p_sym, x)

        grado = polinomio.degree()

        coeficientes = polinomio.all_coeffs()

        # =====================================================
        # NUMÉRICO
        # =====================================================

        p_num = sp.lambdify(
            x,
            p_sym,
            "numpy"
        )

        # =====================================================
        # VISUAL LATEX
        # =====================================================

        p_visual = sp.latex(p_sym)

        p_visual = re.sub(
            r'\^([\-\+]?[a-zA-Z0-9\(\)]+)',
            r'^{\1}',
            p_visual
        )

        p_visual = p_visual.replace("*", "")

        return True, "", (
            p_sym,
            x,
            grado,
            coeficientes,
            p_num,
            p_visual
        )

    except (
        sp.SympifyError,
        TypeError,
        ValueError
    ) as e:

        return False, f"Error: {str(e)}", None