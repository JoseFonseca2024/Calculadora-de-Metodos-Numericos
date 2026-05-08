import numpy as np
import matplotlib.pyplot as plt

LIMITE_X = 80
LIMITE_Y = 30
LIMITE_FILTRO = 1000

# =========================================================
# UTILIDADES
# =========================================================

def _convertir_real(valor):
    if isinstance(valor, complex):
        if abs(valor.imag) < 1e-10:
            return float(valor.real)
        return None
    try:
        return float(valor)
    except:
        return None


def _evaluar_funcion_segura(f, x):
    try:
        y = f(x)

        if isinstance(y, complex):
            if abs(y.imag) < 1e-10:
                y = y.real
            else:
                return np.nan

        return float(y) if np.isfinite(y) else np.nan

    except:
        return np.nan


# =========================================================
# CONFIGURACIÓN BASE
# =========================================================

def _configurar_grafica_base(f, iteraciones, incluir_prev=False, factor_margen=0.5):

    fig, ax = plt.subplots(figsize=(10, 6))

    xs_all = []

    for it in iteraciones:
        valores = [it.get("Ci"), it.get("Ci+1")]

        if incluir_prev:
            valores.append(it.get("Ci-1"))

        for val in valores:
            real = _convertir_real(val)
            if real is not None:
                xs_all.append(real)

    if not xs_all:
        xs_all = [-10, 10]

    xmin, xmax = min(xs_all), max(xs_all)

    rango = max(xmax - xmin, 1)
    margen = max(rango * factor_margen, 5)

    x_min = xmin - margen
    x_max = xmax + margen

    x_vals = np.linspace(x_min, x_max, 5000)

    y_vals = np.array([_evaluar_funcion_segura(f, x) for x in x_vals])

    ax.plot(x_vals, y_vals, 'royalblue', linewidth=2.5)
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')

    ax.set_xlim(max(x_min, -LIMITE_X), min(x_max, LIMITE_X))
    ax.set_ylim(-LIMITE_Y, LIMITE_Y)

    ax.relim()
    ax.autoscale_view()

    return fig, ax, xmin, xmax, margen


# =========================================================
# NEWTON
# =========================================================

def graficar_newton(f, iteraciones):

    fig, ax, xmin, xmax, _ = _configurar_grafica_base(f, iteraciones)

    for it in iteraciones:
        Ci = it["Ci"]
        Ci_next = it["Ci+1"]

        fCi = _evaluar_funcion_segura(f, Ci)

        if np.isfinite(fCi):
            ax.scatter(Ci, fCi, color='black')
            ax.plot([Ci, Ci_next], [fCi, 0], '--', color='green')

    raiz = iteraciones[-1]["Ci+1"]
    ax.scatter(raiz, 0, marker='*', s=200, color='gold')

    ax.set_title("Newton")
    ax.grid(True)

    return fig


# =========================================================
# SECANTE
# =========================================================

def graficar_secante(f, iteraciones):

    fig, ax, xmin, xmax, _ = _configurar_grafica_base(
        f, iteraciones, incluir_prev=True
    )

    for it in iteraciones:
        Ci = it["Ci"]
        Cp = it["Ci-1"]

        f1 = _evaluar_funcion_segura(f, Ci)
        f0 = _evaluar_funcion_segura(f, Cp)

        if np.isfinite(f1) and np.isfinite(f0):
            ax.plot([Cp, Ci], [f0, f1], '--', color='red')

    raiz = iteraciones[-1]["Ci+1"]
    ax.scatter(raiz, 0, marker='*', s=200, color='gold')

    ax.set_title("Secante")
    ax.grid(True)

    return fig


# =========================================================
# PUNTO FIJO
# =========================================================

def graficar_punto_fijo(g, iteraciones, x_min, x_max):

    fig, ax = plt.subplots(figsize=(8, 8))

    x_vals = np.linspace(x_min, x_max, 4000)
    y_vals = np.array([_evaluar_funcion_segura(g, x) for x in x_vals])

    ax.plot(x_vals, x_vals, '--')
    ax.plot(x_vals, y_vals)

    x = iteraciones[0]["Ci"]

    for it in iteraciones:
        y = g(x)
        if not np.isfinite(y):
            break

        ax.plot([x, x], [x, y], 'r--')
        ax.plot([x, y], [y, y], 'b--')
        ax.scatter(x, y)

        x = y

    raiz = iteraciones[-1]["Ci+1"]
    ax.scatter(raiz, raiz, marker='*', s=200, color='gold')

    ax.set_xlim(max(x_min, -LIMITE_X), min(x_max, LIMITE_X))
    ax.set_ylim(-LIMITE_Y, LIMITE_Y)

    return fig


# =========================================================
# MÉTODO CERRADO
# =========================================================

def graficar_metodo_cerrado(f, iteraciones, titulo):

    fig, ax, xmin, xmax, _ = _configurar_grafica_base(f, iteraciones)

    a_final = iteraciones[-1]["a"]
    b_final = iteraciones[-1]["b"]

    raiz = iteraciones[-1]["Ci"]

    ax.axvspan(a_final, b_final, alpha=0.12)
    ax.scatter(raiz, 0, marker='*', s=220, color='gold')

    ax.set_title(titulo)
    ax.grid(True)

    return fig


# =========================================================
# MULLER (arreglado scope)
# =========================================================

def graficar_muller(f, iteraciones):

    fig, ax, xmin, xmax, _ = _configurar_grafica_base(f, iteraciones)

    raiz = _convertir_real(iteraciones[-1]["x3"])

    if raiz is not None:
        ax.scatter(raiz, 0, marker='*', s=200, color='gold')

    ax.set_title("Muller")
    ax.grid(True)

    return fig


# =========================================================
# TAYLOR (ARREGLADO)
# =========================================================

def graficar_taylor(f_num, poly_num, x_eval, a, titulo):

    centro = (a + x_eval) / 2
    rango = max(abs(x_eval - a) * 2, 4)

    x_vals = np.linspace(centro - rango, centro + rango, 3000)

    fig, ax = plt.subplots()

    y_f = np.array([_evaluar_funcion_segura(f_num, x) for x in x_vals])
    y_p = np.array([_evaluar_funcion_segura(poly_num, x) for x in x_vals])

    ax.plot(x_vals, y_f)
    ax.plot(x_vals, y_p, '--')

    ax.set_xlim(max(centro - rango, -LIMITE_X), min(centro + rango, LIMITE_X))
    ax.set_ylim(-LIMITE_Y, LIMITE_Y)

    ax.set_title(titulo)

    return fig