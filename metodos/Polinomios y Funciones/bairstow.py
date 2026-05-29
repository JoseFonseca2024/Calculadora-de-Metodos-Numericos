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

    if abs(disc) < 1e-12:
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


def bairstow_core(a, r, s, tol, max_iter):

    if len(a) < 4:
        return False, [], [], a

    n = len(a) - 1
    historial_local = []

    x1_old = None
    x2_old = None

    for it in range(max_iter):

        b = [0.0] * (n + 1)
        c = [0.0] * (n + 1)

        r_old = r
        s_old = s

        b[n] = a[n]
        b[n - 1] = a[n - 1] + r_old * b[n]

        for i in range(n - 2, -1, -1):
            b[i] = a[i] + r_old * b[i + 1] + s_old * b[i + 2]

        c[n] = b[n]
        c[n - 1] = b[n - 1] + r_old * c[n]

        for i in range(n - 2, -1, -1):
            c[i] = b[i] + r_old * c[i + 1] + s_old * c[i + 2]

        det = c[2] * c[2] - c[1] * c[3]

        if abs(det) < 1e-12:
            r += 0.5
            s += 0.5
            continue

        dr = (b[0] * c[3] - b[1] * c[2]) / det
        ds = (b[1] * c[1] - b[0] * c[2]) / det

        r += dr
        s += ds

        x1, x2 = resolver_cuadratica(r, s)

        error_x1 = None
        error_x2 = None

        if x1_old is not None:
            if x1 != 0:
                error_x1 = abs((x1_old - x1) / x1) * 100
            if x2 != 0:
                error_x2 = abs((x2_old - x2) / x2) * 100

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

        x1_old, x2_old = x1, x2

        if abs(dr) < tol and abs(ds) < tol:
            break

    return True, historial_local, [x1, x2], b


def ejecutar_bairstow(coeficientes, tol, max_iter=100):

    try:

        # ⚠️ IMPORTANTE: orden ascendente (constante → mayor grado)
        a = [float(c) for c in coeficientes][::-1]

        historial_total = []
        raices = []

        while True:

            n = len(a) - 1

            if n == 1:
                raices.append(-a[0] / a[1])
                break

            if n == 2:
                r = -a[1] / a[2]
                s = -a[0] / a[2]
                x1, x2 = resolver_cuadratica(r, s)
                raices.extend([x1, x2])
                break

            # ==========================
            # INICIALIZACIÓN
            # ==========================
            (r_peq, s_peq), (r_grd, s_grd) = inicializar(a)

            candidatos = [
                ("peque", r_peq, s_peq),
                ("grande", r_grd, s_grd)
            ]

            mejor_historial = None
            mejor_raices = None
            mejor_score = float("inf")
            mejor_b = None
            mejor_r0 = None
            mejor_s0 = None
            mejor_tipo = None

            for tipo, r0, s0 in candidatos:

                ok, hist, roots, b = bairstow_core(
                    a.copy(), r0, s0, tol, max_iter
                )

                if not ok or len(hist) == 0:
                    continue

                last = hist[-1]
                score = abs(last["dr"]) + abs(last["ds"])

                if score < mejor_score:
                    mejor_score = score
                    mejor_historial = hist
                    mejor_raices = roots
                    mejor_b = b
                    mejor_r0 = r0
                    mejor_s0 = s0
                    mejor_tipo = tipo

            if mejor_b is None:
                return False, "No convergió", None

            ultimo = mejor_historial[-1]

            historial_total.append({
                "iteraciones": mejor_historial,
                "factor_r": ultimo["r"],
                "factor_s": ultimo["s"],
                "cociente": mejor_b[2:],
                "r_inicial": mejor_r0,
                "s_inicial": mejor_s0,
                "tipo_inicial": mejor_tipo
            })

            raices.extend(mejor_raices)

            # 🔥 AQUÍ ESTÁ EL FIX CRÍTICO
            a = mejor_b[2:].copy()

        raices_reales = []

        for r in raices:
            if isinstance(r, complex):
                if abs(r.imag) < 1e-10:
                    raices_reales.append(float(r.real))
            else:
                raices_reales.append(float(r))

        return True, "", {
            "raices": raices_reales,
            "raices_completas": raices,
            "iteraciones": historial_total
        }

    except Exception as e:
        return False, f"Error: {str(e)}", None