import numpy as np

def ejecutar_punto_fijo(g, x0, tol):
    iteraciones = []
    i = 0

    while True:
        try:
            x_eval = g(x0)

            if np.iscomplexobj(x_eval):
                if abs(x_eval.imag) > 1e-12:
                    return False, "La función produjo valores complejos.", None
                x_eval = x_eval.real

            x_next = float(x_eval)

            if abs(x_next) > 1e6:
                return False, "El método diverge (valores muy grandes).", None

            error = abs((x_next - x0) / x_next) * 100 if x_next != 0 else 0

            iteraciones.append({
                "i": i,
                "Ci": x0,
                "Ci+1": x_next,
                "Error%": error
            })

            if error < tol:
                break

            if abs(x_next - x0) < 1e-12:
                return False, "El método se estancó.", None

            x0 = x_next
            i += 1

            if i > 100:
                return False, "El método no converge.", None

        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as e:
            return False, f"Error en evaluación numérica: {str(e)}", None

    return True, "", iteraciones