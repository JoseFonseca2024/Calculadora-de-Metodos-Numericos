def formatear_numero(valor, decimales=8):

    # Si es entero
    if abs(valor - int(valor)) < 1e-12:

        return str(int(valor))

    # Redondear
    texto = f"{valor:.{decimales}f}"

    # Eliminar ceros sobrantes
    texto = texto.rstrip("0").rstrip(".")

    return texto