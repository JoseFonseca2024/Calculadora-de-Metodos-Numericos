import numpy as np
import matplotlib.pyplot as plt

def _configurar_grafica_base(f, iteraciones, incluir_prev=False, factor_margen=0.5):
    fig, ax = plt.subplots(figsize=(10, 6))

    xs_all = []
    for it in iteraciones:
        xs_all.append(it["Ci"])
        xs_all.append(it["Ci+1"])
        if incluir_prev or "Ci-1" in it:
            xs_all.append(it.get("Ci-1", it["Ci"]))

    xmin_real, xmax_real = min(xs_all), max(xs_all)

    # Margen dinámico mejorado
    rango = abs(xmax_real - xmin_real)
    margen_x = max(rango * factor_margen, 0.5)
    if rango < 1:
        margen_x += 1.5

    x_vals = np.linspace(xmin_real - margen_x, xmax_real + margen_x, 500)

    # Evaluación segura
    y_vals = []
    for x in x_vals:
        try:
            y = f(x)
            y_vals.append(y if np.isfinite(y) else np.nan)
        except (ValueError, ZeroDivisionError, TypeError):
            y_vals.append(np.nan)

    ax.plot(x_vals, y_vals, linewidth=2, label="f(x)", zorder=2, color='royalblue')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    return fig, ax, xmin_real, xmax_real, margen_x


def graficar_newton(f, iteraciones):
    fig, ax, xmin_real, xmax_real, margen_x = _configurar_grafica_base(
        f, iteraciones, factor_margen=0.8
    )

    for i, it in enumerate(iteraciones):
        Ci = it["Ci"]
        Ci_next = it["Ci+1"]
        fCi = it["f(Ci)"]

        # Punto
        ax.scatter(Ci, fCi, s=45, zorder=5, color='black')

        # Tangente (aproximación visual)
        label = "Tangentes" if i == 0 else ""
        ax.plot(
            [Ci, Ci_next],
            [fCi, 0],
            linestyle='--',
            linewidth=1.5,
            color='green',
            alpha=0.7,
            label=label
        )

        # Proyección vertical
        try:
            f_next = f(Ci_next)
            if np.isfinite(f_next):
                ax.plot(
                    [Ci_next, Ci_next],
                    [0, f_next],
                    linestyle=':',
                    color='gray',
                    alpha=0.6
                )
        except (ValueError, ZeroDivisionError, TypeError):
            pass

        # Etiqueta mejor posicionada
        ax.text(Ci, fCi, f'$x_{i}$', fontsize=9, ha='right', va='bottom')

    # Raíz final
    raiz = iteraciones[-1]["Ci+1"]
    ax.scatter(
        raiz, 0,
        marker='*',
        s=200,
        color='gold',
        edgecolor='orange',
        label=f"Raíz: {raiz:.4f}",
        zorder=10
    )

    # Ajuste eje Y
    ys = [it["f(Ci)"] for it in iteraciones] + [0]
    ymin, ymax = min(ys), max(ys)
    margen_y = max(abs(ymax - ymin) * 0.3, 1.0)

    ax.set_xlim(xmin_real - margen_x, xmax_real + margen_x)
    ax.set_ylim(ymin - margen_y, ymax + margen_y)

    ax.set_title("Método de Newton-Raphson")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend()

    return fig


def graficar_secante(f, iteraciones):
    fig, ax, xmin_real, xmax_real, margen_x = _configurar_grafica_base(
        f, iteraciones, incluir_prev=True, factor_margen=0.6
    )

    for i, it in enumerate(iteraciones):
        Ci = it["Ci"]
        Ci_prev = it["Ci-1"]
        Ci_next = it["Ci+1"]

        fCi = it["f(Ci)"]
        fCi_prev = it["f(Ci-1)"]

        # Secante (visual didáctica)
        label_sec = "Secantes" if i == 0 else ""
        ax.plot(
            [Ci_prev, Ci, Ci_next],
            [fCi_prev, fCi, 0],
            linestyle='--',
            linewidth=1.5,
            color='red',
            alpha=0.6,
            label=label_sec
        )

        # Puntos
        ax.scatter([Ci_prev, Ci], [fCi_prev, fCi], color='black', s=30, zorder=5)

        # Proyección vertical
        try:
            f_next = f(Ci_next)
            if np.isfinite(f_next):
                ax.plot(
                    [Ci_next, Ci_next],
                    [0, f_next],
                    linestyle=':',
                    color='gray',
                    alpha=0.5
                )
        except (ValueError, ZeroDivisionError, TypeError):
            pass
        # Etiqueta
        ax.text(Ci, fCi, f'$x_{i}$', fontsize=9, ha='right', va='bottom')

    # Raíz final
    raiz = iteraciones[-1]["Ci+1"]
    ax.scatter(
        raiz, 0,
        marker='*',
        s=200,
        color='gold',
        edgecolor='orange',
        label=f"Raíz aprox: {raiz:.4f}",
        zorder=10
    )

    # Ajuste eje Y
    ys = [it["f(Ci)"] for it in iteraciones] + [0]
    ymin, ymax = min(ys), max(ys)
    margen_y = max(abs(ymax - ymin) * 0.3, 1.0)

    ax.set_xlim(xmin_real - margen_x, xmax_real + margen_x)
    ax.set_ylim(ymin - margen_y, ymax + margen_y)

    ax.set_title("Método de la Secante (Visualización de Convergencia)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()

    return fig

def graficar_punto_fijo(gs, x_min, x_max):

    fig, ax = plt.subplots(figsize=(8,8))

    x_vals = np.linspace(x_min, x_max, 500)

    # Línea y=x
    ax.plot(
        x_vals,
        x_vals,
        '--',
        linewidth=2,
        label='y = x'
    )

    # Graficar todas las g(x)
    for g_data in gs:

        try:

            g_num = g_data["num"]

            y_vals = []

            for x in x_vals:

                try:
                    y_vals.append(g_num(x))
                except:
                    y_vals.append(np.nan)

            ax.plot(
                x_vals,
                y_vals,
                linewidth=2,
                label=g_data["nombre"]
            )

        except:
            continue

    ax.grid()
    ax.legend()

    ax.set_title("Funciones g(x) del Método de Punto Fijo")
    ax.set_xlabel("x")
    ax.set_ylabel("g(x)")

    return fig

def graficar_metodo_cerrado(f, iteraciones, titulo):
   
    iter_adaptadas = []
    for it in iteraciones:
        iter_adaptadas.append({
            "Ci": it["a"], 
            "Ci+1": it["b"]
        })

    fig, ax, xmin_real, xmax_real, margen_x = _configurar_grafica_base(
        f, iter_adaptadas, factor_margen=0.6
    )

    # 2. Dibujar el intervalo final (el más preciso)
    a_final = iteraciones[-1]["a"]
    b_final = iteraciones[-1]["b"]
    raiz = iteraciones[-1]["Ci"]

    # Sombreado del intervalo final
    ax.axvspan(a_final, b_final, color='green', alpha=0.1, label='Intervalo Final')
    
    # Líneas verticales de los límites
    ax.axvline(a_final, color='green', linestyle='--', alpha=0.6, label='Límite a')
    ax.axvline(b_final, color='orange', linestyle='--', alpha=0.6, label='Límite b')

    # Marca la raíz 
    ax.scatter(
        raiz, 0,
        marker='*',
        s=200,
        color='gold',
        edgecolor='orange',
        label=f"Raíz aprox: {raiz:.4f}",
        zorder=10
    )

    # Ajustes finales de ejes
    ax.set_title(titulo)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()

    return fig