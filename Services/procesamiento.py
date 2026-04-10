def filtrar_iteraciones(iteraciones, tol):
    resultado = []

    for it in iteraciones:
        resultado.append(it)
        if it["Error%"] is not None and it["Error%"] < tol:
            break

    return resultado