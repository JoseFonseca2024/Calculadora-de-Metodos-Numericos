import numpy as np

def ejecutar_punto_fijo(g, x0, tol):

    iteraciones = []

    i = 0

    ultimo_error = None

    while True:

        try:

            x_eval = g(x0)

            # ==========================================
            # COMPLEJOS
            # ==========================================

            if np.iscomplexobj(x_eval):

                if abs(x_eval.imag) > 1e-10:
                    return False, "La función produjo valores complejos.", None

                x_eval = x_eval.real

            # ==========================================
            # FINITOS
            # ==========================================

            if not np.isfinite(x_eval):
                return False, "La función produjo valores no finitos.", None

            x_next = float(x_eval)

            # ==========================================
            # DIVERGENCIA
            # ==========================================

            if abs(x_next) > 1e6:
                return False, "El método diverge (valores muy grandes).", None

            # ==========================================
            # ERROR
            # ==========================================

            if x_next != 0:

                error = abs((x_next - x0) / x_next) * 100

            else:

                error = abs(x_next - x0) * 100

            iteraciones.append({
                "i": i,
                "Ci": x0,
                "Ci+1": x_next,
                "Error%": error
            })

            # ==========================================
            # CONVERGENCIA
            # ==========================================

            if error < tol:
                break

            # ==========================================
            # ESTANCAMIENTO REAL
            # ==========================================

            if ultimo_error is not None:

                if abs(error - ultimo_error) < 1e-14:

                    if i > 10:
                        return False, "El método se estancó.", None

            ultimo_error = error

            # ==========================================
            # SIGUIENTE ITERACIÓN
            # ==========================================

            x0 = x_next

            i += 1

            # ==========================================
            # MÁX ITERACIONES
            # ==========================================

            if i > 200:
                return False, "El método no converge.", None

        except (
            ValueError,
            ZeroDivisionError,
            TypeError,
            OverflowError
        ) as e:

            return False, f"Error en evaluación numérica: {str(e)}", None

    return True, "", iteraciones