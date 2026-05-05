import pandas as pd

def filtrar_iteraciones(iteraciones, tol):
    resultado = []

    for it in iteraciones:
        resultado.append(it)
        if it["Error%"] is not None and it["Error%"] < tol:
            break

    return resultado

def convertir_biseccion_a_tabla(iteraciones):
    data = []
    xr_anterior = None

    for it in iteraciones:
        xr = it["Ci"]

        if xr_anterior is None:
            ea = float('nan')
        else:
            ea = abs((xr - xr_anterior) / xr) * 100

        data.append({
            "Iteración": it["i"] + 1,
            "a": it["a"],
            "c": xr,
            "b": it["b"],
            "f(a)": it["f(a)"],
            "f(c)": it["f(Ci)"],
            "f(b)": it["f(b)"],
            "f(a)*f(c)": it["f(a)"] * it["f(Ci)"],
            "Ea%": ea
        })

        xr_anterior = xr

    return pd.DataFrame(data)