def ejecutar_regla_falsa(f, a, b, tol):
    iteraciones = []
    i = 0
    xr_viejo = 0

    try:
        f_a = float(f(a))
        f_b = float(f(b))
    except Exception as e:
        return False, f"Error al evaluar la función: {e}", None

    # Validación de Bolzano
    if f_a * f_b >= 0:
        return False, "f(a) y f(b) deben tener signos opuestos.", None

    while True:
        # Fórmula de la Regla Falsa (Posición Falsa)
        xr = b - (f_b * (a - b)) / (f_a - f_b)
        f_xr = float(f(xr))
        
        error = abs((xr - xr_viejo) / xr) * 100 if i > 0 else 100
        
        iteraciones.append({
            "i": i,
            "a": a,
            "b": b,
            "Ci": xr,
            "f(Ci)": f_xr,
            "Error%": error
        })

        if error < tol:
            break
        
        # Cambio de intervalo
        if f_a * f_xr < 0:
            b = xr
            f_b = f_xr
        else:
            a = xr
            f_a = f_xr

        xr_viejo = xr
        i += 1
        
        if i > 100:
            return False, "El método no converge en 100 iteraciones.", None

    return True, "", iteraciones