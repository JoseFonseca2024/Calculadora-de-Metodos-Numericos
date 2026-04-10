import sympy as sp

def ejecutar_newton_raphson(f, f_deriv, C0, tol):
    iteraciones = []

    Ci = C0
    i = 0

    while True:
        try:
            f_Ci = f(Ci)
            f_deriv_Ci = f_deriv(Ci)

            if f_deriv_Ci == 0:
                return False, "La derivada es cero. No se puede continuar.", None

            Ci_next = Ci - (f_Ci / f_deriv_Ci)

            if i == 0:
                error = None
            else:
                if abs(Ci_next) < 1e-12:
                    error = 0
                else:
                    error = abs((Ci_next - Ci) / Ci_next) * 100

            iteraciones.append({
                "i": i,
                "Ci": Ci,
                "f(Ci)": f_Ci,
                "f'(Ci)": f_deriv_Ci,
                "Ci+1": Ci_next,
                "Error%": error
            })

            if error is not None and error < tol:
                break

            Ci = Ci_next
            i += 1

            if i > 100:
                return False, "El método no converge.", None

        except (sp.SympifyError, TypeError):
            return False, "Error en la evaluación numérica.", None

    return True, "", iteraciones