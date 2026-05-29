import sympy as sp

def ejecutar_secante(f, C0, C_1, tol):
    iteraciones = []

    Ci = C0   # C₀
    Ci_prev = C_1   # C-₁
    i = 0

    while True:
        try:
            f_ci = f(Ci)
            f_Ci_prev = f(Ci_prev)

            #Evitar division entre 0
            if abs(f_ci-f_Ci_prev) < 1e-12:
                return False, "División por cero en la fórmula de la secante.", None
            
            
            #Calculo de siguiente valor
            Ci_next = Ci - (f_ci * (Ci - Ci_prev)) / (f_ci - f_Ci_prev)
            
            #Calculo de error
            error = abs(1 -(Ci / Ci_next)) * 100

            iteraciones.append({
                "i": i,
                "Ci": Ci,
                "Ci-1": Ci_prev,
                "f(Ci)": f_ci,
                "f(Ci-1)": f_Ci_prev,
                "Ci+1": Ci_next,
                "Error%": error
            })

            # Verificar criterio de pago
            if error < tol:
                break

            Ci_prev = Ci
            Ci = Ci_next
            i += 1

            if i > 100:
                return False, "El metodo no converge", None
            
        except (sp.SympifyError, TypeError):
            return False, "Error en la evaluación numérica.", None

    return True, "", iteraciones