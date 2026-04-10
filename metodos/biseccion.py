def ejecutar_biseccion(f, a, b, tol):
    iteraciones = [] 
    i = 0
    xr_viejo = 0

    try:
        f_a = float(f(a))
        f_b = float(f(b))
    except Exception as e:
        return False, f"Error al evaluar la función: {e}", None

    if f_a * f_b >= 0:
        return False, "f(a) y f(b) deben tener signos opuestos.", None

    while True:
        xr = (a + b) / 2
        f_xr = float(f(xr)) 
        error = abs((xr - xr_viejo) / xr) * 100 if i > 0 else 100
        
        iteraciones.append({
            "i": i,
            "a": a,
            "b": b,
            "f(a)": f_a,   
            "f(b)": f_b,   
            "Ci": xr,
            "f(Ci)": f_xr,
            "Error%": error
        })

        if error < tol: break
        if f_a * f_xr < 0:
            b = xr
        else:
            a = xr
            f_a = f_xr

        xr_viejo = xr
        i += 1
        if i > 100: return False, "El método no converge.", None

    return True, "", iteraciones