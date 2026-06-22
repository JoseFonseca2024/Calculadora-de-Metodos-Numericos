import sympy as sp
import re

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)


def validar_y_preparar_funcion_integral(
    funcion_str
):

    if not funcion_str or not funcion_str.strip():

        return (
            False,
            "Debe ingresar una expresión.",
            None
        )

    if "=" in funcion_str:

        return (
            False,
            "Formato incorrecto: ingrese solo la función sin ninguna igualdad.",
            None
        )

    try:

        texto_original = funcion_str.replace(
            " ",
            ""
        )

        # ======================================
        # NORMALIZACIÓN
        # ======================================

        f_prep = texto_original.lower()

        f_prep = f_prep.replace(
            ",",
            "."
        )

        # trigonométricas

        f_prep = (
            f_prep.replace("sen", "sin")
                  .replace("tg", "tan")
                  .replace("ctg", "cot")
                  .replace("cosec", "csc")
        )

        # π

        f_prep = f_prep.replace(
            "π",
            "pi"
        )

        # potencias

        f_prep = (
            f_prep.replace(
                "²",
                "**2"
            )
            .replace(
                "³",
                "**3"
            )
        )

        # constante e

        f_prep = re.sub(
            r'\be\b',
            'E',
            f_prep
        )

        # exponenciales

        f_prep = re.sub(
            r'E\*\*\((.*?)\)',
            r'exp(\1)',
            f_prep
        )

        f_prep = re.sub(
            r'E\*\*([a-zA-Z0-9]+)',
            r'exp(\1)',
            f_prep
        )

        # ======================================
        # RAÍCES
        # ======================================

        f_prep = re.sub(
            r'√\((.*?)\)',
            r'sqrt(\1)',
            f_prep
        )

        f_prep = re.sub(
            r'√([a-zA-Z0-9]+)',
            r'sqrt(\1)',
            f_prep
        )

        f_prep = re.sub(
            r'raiz\((.*?)\)',
            r'sqrt(\1)',
            f_prep
        )

        f_prep = re.sub(
            r'raiz(\d+)\((.*?)\)',
            r'(\2)**(1/\1)',
            f_prep
        )

        f_prep = re.sub(
            r'∛\((.*?)\)',
            r'(\1)**(1/3)',
            f_prep
        )

        f_prep = re.sub(
            r'∛([a-zA-Z0-9]+)',
            r'(\1)**(1/3)',
            f_prep
        )

        # ======================================
        # TRANSFORMACIONES
        # ======================================

        transformaciones = (
            standard_transformations
            +
            (
                implicit_multiplication_application,
                convert_xor
            )
        )

        # ======================================
        # VARIABLES
        # ======================================

        x, y = sp.symbols(
            "x y"
        )

        local_dict = {

            "x": x,
            "y": y,

            "pi": sp.pi,

            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "cot": sp.cot,
            "sec": sp.sec,
            "csc": sp.csc,

            "log": sp.log,
            "ln": sp.log,

            "sqrt": sp.sqrt,
            "exp": sp.exp
        }

        # ======================================
        # PARSEO
        # ======================================

        f_sym = parse_expr(
            f_prep,
            transformations=transformaciones,
            local_dict=local_dict
        )

        # ======================================
        # VALIDACIÓN
        # ======================================

        if not (
            f_sym.has(x)
            or
            f_sym.has(y)
        ):

            return (
                False,
                "La función debe depender de x o y.",
                None
            )

        # ======================================
        # VISUAL
        # ======================================

        f_visual = sp.latex(
            f_sym
        )

        f_visual = re.sub(
            r'\^([\-\+]?[a-zA-Z0-9\(\)]+)',
            r'^{\1}',
            f_visual
        )

        f_visual = f_visual.replace(
            "*",
            ""
        )

        # ======================================
        # RETORNO
        # ======================================

        return (
            True,
            "",
            (
                f_sym,
                x,
                y,
                f_visual
            )
        )

    except (
        sp.SympifyError,
        TypeError,
        ValueError
    ) as e:

        return (
            False,
            f"Error: {str(e)}",
            None
        )