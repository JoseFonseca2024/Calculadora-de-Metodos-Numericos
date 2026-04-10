from utils.evaluacion_segura import evaluar_seguro

def ejecutar_biseccion(f, a, b, tol):
    iteraciones = [] 
    i = 0
    xr_viejo = 0

    f_a = evaluar_seguro(f, a)
    f_b = evaluar_seguro(f, b)

    if f_a is None or f_b is None:
        return False, "No se puede evaluar la función en el intervalo.", None

    if f_a * f_b >= 0:
        return False, "f(a) y f(b) deben tener signos opuestos.", None

    while True:
        xr = (a + b) / 2

        f_xr = evaluar_seguro(f, xr)
        if f_xr is None:
            return False, "Error al evaluar la función durante las iteraciones.", None

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

        if error < tol:
            break

        if f_a * f_xr < 0:
            b = xr
            f_b = f_xr
        else:
            a = xr
            f_a = f_xr

        xr_viejo = xr
        i += 1

        if i > 100:
            return False, "El método no converge.", None

    return True, "", iteraciones