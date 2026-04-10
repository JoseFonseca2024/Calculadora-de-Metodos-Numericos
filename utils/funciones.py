import sympy as sp
from utils.parsers import normalizar_funcion
from utils.sympy_builder import construir_funcion

def validar_y_preparar_funcion(funcion_str):

    if funcion_str.strip() == "":
        return False, "Debe ingresar una función", None
    
    try:
        funcion_str = normalizar_funcion(funcion_str)
        datos = construir_funcion(funcion_str)

        return True, "", datos

    except (sp.SympifyError, TypeError):
        return False, "Formato inválido", None

    except ValueError as e:
        return False, str(e), None