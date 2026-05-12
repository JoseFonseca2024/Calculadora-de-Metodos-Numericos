import math

def inicializar(a):

    n = len(a) - 1

    r_peq = a[1] / a[2] if a[2] != 0 else 0
    s_peq = a[0] / a[2] if a[2] != 0 else 0

    r_grd = a[n - 1] / a[n] if a[n] != 0 else 0
    s_grd = a[n - 2] / a[n] if a[n] != 0 else 0

    return (r_peq, s_peq), (r_grd, s_grd)


def resolver_cuadratica(r, s):

    disc = r * r + 4 * s

    if disc < 0 and abs(disc) < 1e-12:
        disc = 0.0

    if disc >= 0:

        sqrt_disc = math.sqrt(disc)

        x1 = (r + sqrt_disc) / 2
        x2 = (r - sqrt_disc) / 2

    else:

        real = r / 2
        imag = math.sqrt(-disc) / 2

        x1 = complex(real, imag)
        x2 = complex(real, -imag)

    return x1, x2


def ejecutar_bairstow(coeficientes, tol, max_iter=100):

    try:

        a = [float(c) for c in coeficientes][::-1]

        historial_total = []

        raices = []

        while True:

            n = len(a) - 1

            # ============================================
            # LINEAL
            # ============================================

            if n == 1:

                raiz = -a[0] / a[1]

                raices.append(raiz)

                break

            # ============================================
            # CUADRÁTICA
            # ============================================

            if n == 2:

                r = -a[1] / a[2]
                s = -a[0] / a[2]

                x1, x2 = resolver_cuadratica(r, s)

                raices.extend([x1, x2])

                break

            # ============================================
            # BAIRSTOW
            # ============================================

            (r_peq, s_peq), (r_grd, s_grd) = inicializar(a)

            # raíces grandes
            r = r_grd
            s = s_grd

            x1_old = None
            x2_old = None

            historial_local = []

            for it in range(max_iter):

                b = [0.0] * (n + 1)
                c = [0.0] * (n + 1)

                r_old = r
                s_old = s

                # ========================================
                # b
                # ========================================

                b[n] = a[n]

                b[n - 1] = (
                    a[n - 1]
                    + r_old * b[n]
                )

                for i in range(n - 2, -1, -1):

                    b[i] = (
                        a[i]
                        + r_old * b[i + 1]
                        + s_old * b[i + 2]
                    )

                # ========================================
                # c
                # ========================================

                c[n] = b[n]

                c[n - 1] = (
                    b[n - 1]
                    + r_old * c[n]
                )

                for i in range(n - 2, -1, -1):

                    c[i] = (
                        b[i]
                        + r_old * c[i + 1]
                        + s_old * c[i + 2]
                    )

                det = (
                    c[2] * c[2]
                    - c[1] * c[3]
                )

                if abs(det) < 1e-12:

                    r += 0.5
                    s += 0.5

                    continue

                dr = (
                    b[0] * c[3]
                    - b[1] * c[2]
                ) / det

                ds = (
                    b[1] * c[1]
                    - b[0] * c[2]
                ) / det

                r += dr
                s += ds

                x1, x2 = resolver_cuadratica(r, s)

                # ========================================
                # ERRORES
                # ========================================

                if x1_old is not None:

                    error_x1 = abs(
                        (x1_old - x1) / x1
                    ) * 100

                    error_x2 = abs(
                        (x2_old - x2) / x2
                    ) * 100

                else:

                    error_x1 = None
                    error_x2 = None

                historial_local.append({

                    "iter": it,

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

                x1_old = x1
                x2_old = x2

                if abs(dr) < tol and abs(ds) < tol:
                    break

            historial_total.append({

                "iteraciones": historial_local,

                "factor_r": r,
                "factor_s": s,

                "cociente": b[2:].copy()
            })

            # ============================================
            # GUARDAR RAÍCES
            # ============================================

            raices.extend([x1, x2])

            # ============================================
            # NUEVO POLINOMIO
            # ============================================

            a = b[2:]

        # ============================================
        # SOLO REALES
        # ============================================

        raices_reales = []

        for r in raices:

            if isinstance(r, complex):

                if abs(r.imag) < 1e-10:

                    raices_reales.append(
                        float(r.real)
                    )

            else:

                raices_reales.append(
                    float(r)
                )

        return True, "", {

            "raices": raices_reales,

            "raices_completas": raices,

            "iteraciones": historial_total
        }

    except (ValueError, ZeroDivisionError) as e:

        return (
            False,
            f"Error en Bairstow: {str(e)}",
            None
        )