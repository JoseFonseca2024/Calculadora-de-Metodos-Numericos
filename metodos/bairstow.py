import math

def inicializar(a):
    n = len(a) - 1

    # 🔹 evitar división por cero
    r_peq = a[1] / a[2] if a[2] != 0 else 0
    s_peq = a[0] / a[2] if a[2] != 0 else 0

    r_grd = a[n-1] / a[n] if a[n] != 0 else 0
    s_grd = a[n-2] / a[n] if a[n] != 0 else 0

    return (r_peq, s_peq), (r_grd, s_grd)


def ejecutar_bairstow(coeficientes, tol, max_iter=100):
    try:
        a = [float(c) for c in coeficientes][::-1]
        n = len(a) - 1

        if n < 2:
            return False, "El polinomio debe ser de grado >= 2", None

        raices = []
        historial = []

        factor_actual = 1
        while n > 2:

            (r_peq, s_peq), (r_grd, s_grd) = inicializar(a)

            # 🔹 evaluar pequeñas
            b_test = [0.0]*(n+1)
            b_test[n] = a[n]
            b_test[n-1] = a[n-1] + r_peq*b_test[n]
            for i in range(n-2, -1, -1):
                b_test[i] = a[i] + r_peq*b_test[i+1] + s_peq*b_test[i+2]
            residuo_peq = max(abs(b_test[0]), abs(b_test[1]))

            # 🔹 evaluar grandes
            b_test = [0.0]*(n+1)
            b_test[n] = a[n]
            b_test[n-1] = a[n-1] + r_grd*b_test[n]
            for i in range(n-2, -1, -1):
                b_test[i] = a[i] + r_grd*b_test[i+1] + s_grd*b_test[i+2]
            residuo_grd = max(abs(b_test[0]), abs(b_test[1]))

            if residuo_peq < residuo_grd:
                r, s = r_peq, s_peq
                modo = "pequeñas"
            else:
                r, s = r_grd, s_grd
                modo = "grandes"

            x1_old = None
            x2_old = None

            for it in range(max_iter):
                b = [0.0]*(n+1)
                c = [0.0]*(n+1)

                r_old, s_old = r, s

                # 🔹 cálculo de b
                b[n] = a[n]
                b[n-1] = a[n-1] + r_old*b[n]
                for i in range(n-2, -1, -1):
                    b[i] = a[i] + r_old*b[i+1] + s_old*b[i+2]

                # 🔹 cálculo de c
                c[n] = b[n]
                c[n-1] = b[n-1] + r_old*c[n]
                for i in range(n-2, -1, -1):
                    c[i] = b[i] + r_old*c[i+1] + s_old*c[i+2]

                # protección de índices
                if len(c) <= 3:
                    return False, "Error interno: tamaño insuficiente en c", None

                det = c[2]*c[2] - c[1]*c[3]

                # manejo robusto de det ≈ 0
                if abs(det) < 1e-12:
                    r += 0.5
                    s += 0.5
                    continue

                dr = (b[0]*c[3] - b[1]*c[2]) / det
                ds = (b[1]*c[1] - b[0]*c[2]) / det

                r += dr
                s += ds

                # 🔹 cálculo de raíces del factor
                disc = r*r + 4*s

                if disc >= 0:
                    x1 = (r + math.sqrt(disc)) / 2
                    x2 = (r - math.sqrt(disc)) / 2
                else:
                    real = r / 2
                    imag = math.sqrt(-disc) / 2
                    x1 = complex(real, imag)
                    x2 = complex(real, -imag)

                # 🔹 error relativo
                if x1_old is not None:
                    error_x1 = abs((x1_old - x1)/x1)*100 if x1 != 0 else abs(x1_old - x1)*100
                    error_x2 = abs((x2_old - x2)/x2)*100 if x2 != 0 else abs(x2_old - x2)*100
                else:
                    error_x1 = error_x2 = None

                historial.append({
                    "factor": factor_actual,
                    "iter": it,
                    "modo": modo,
                    "r_old": r_old,
                    "s_old": s_old,
                    "r": r,
                    "s": s,
                    "dr": dr,
                    "ds": ds,
                    "b": b.copy(),
                    "c": c.copy(),
                    "x1": x1,
                    "x2": x2,
                    "error_x1": error_x1,
                    "error_x2": error_x2
                })

                x1_old, x2_old = x1, x2

                if abs(dr) < tol and abs(ds) < tol:
                    break

            raices.extend([x1, x2])
            factor_actual += 1
            # 🔹 deflación
            a = b[2:]
            n = len(a) - 1

        # resolver grado 2 correctamente
        if n == 2:
            a0, a1, a2 = a[0], a[1], a[2]

            disc = a1*a1 - 4*a2*a0

            if disc >= 0:
                x1 = (-a1 + math.sqrt(disc)) / (2*a2)
                x2 = (-a1 - math.sqrt(disc)) / (2*a2)
            else:
                real = -a1 / (2*a2)
                imag = math.sqrt(-disc) / (2*a2)
                x1 = complex(real, imag)
                x2 = complex(real, -imag)

            raices.extend([x1, x2])

        elif n == 1:
            raices.append(-a[0] / a[1])

        return True, "", {"raices": raices, "iteraciones": historial}

    except (ValueError, ZeroDivisionError) as e:
        return False, f"Error en Bairstow: {str(e)}", None