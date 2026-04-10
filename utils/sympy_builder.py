import sympy as sp

def construir_funcion(funcion_str):
    x = sp.symbols('x')

    funcion = sp.sympify(funcion_str)

    if not funcion.has(x):
        raise ValueError("La función debe depender de x")

    derivada = sp.diff(funcion, x)

    f = sp.lambdify(x, funcion)
    f_deriv = sp.lambdify(x, derivada)

    return funcion, derivada, f, f_deriv