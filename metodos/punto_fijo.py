def ejecutar_punto_fijo(g, x0, tol):
    iteraciones = []

    i = 0

    while True:
        try:
            x_next = float(g(x0))

            error = abs((x_next - x0) / x_next) * 100 if x_next != 0 else 0

            iteraciones.append({
                "i": i,
                "Ci": x0,
                "Ci+1": x_next,
                "Error%": error
            })

            if error < tol:
                break

            x0 = x_next
            i += 1

            if i > 100:
                return False, "El método no converge.", None

        except:
            return False, "Error en evaluación numérica.", None

    return True, "", iteraciones