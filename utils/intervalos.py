import numpy as np


def encontrar_intervalos_raiz(
    f,
    inicio=-10,
    fin=10,
    paso=1
):

    intervalos = []

    x_vals = np.arange(
        inicio,
        fin + paso,
        paso
    )

    for i in range(len(x_vals)-1):

        a = x_vals[i]
        b = x_vals[i+1]

        try:

            fa = f(a)
            fb = f(b)

            # Cambio de signo
            if fa * fb < 0:
                intervalos.append((a, b))

            # Si toca exactamente cero
            elif fa == 0:
                intervalos.append((a, a))

        except:
            continue

    return intervalos