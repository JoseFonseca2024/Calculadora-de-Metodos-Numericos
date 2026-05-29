import numpy as np
import plotly.graph_objects as go

# =========================================================
# CONFIGURACIÓN GLOBAL
# =========================================================

LIMITE_ABSURDO = 1e12
MUESTRAS_GRAFICA = 6000

COLOR_FUNCION = 'royalblue'
COLOR_RAIZ = 'gold'
COLOR_NEWTON = 'green'
COLOR_SECANTE = 'red'
COLOR_VERTICAL = 'red'
COLOR_HORIZONTAL = 'blue'

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
        with np.errstate(all='ignore'):
            y = f(x)

        # 1. Manejo de complejos de Python y de NumPy
        if np.iscomplexobj(y):
            if abs(np.imag(y)) < 1e-10:
                y = np.real(y)
            else:
                return np.nan

        if np.isnan(y):
            return np.nan

        if not np.isfinite(y) or abs(y) > LIMITE_ABSURDO:
            return np.nan

        return float(y)
    except:
        return np.nan

def _filtrar_datos(y_vals):

    y_filtrado = np.copy(y_vals)

    mask = (
        np.isfinite(y_filtrado)
        & (np.abs(y_filtrado) < LIMITE_ABSURDO)
    )

    y_filtrado[~mask] = np.nan

    return y_filtrado


# =========================================================
# VIEWPORT INTELIGENTE
# =========================================================

def _crear_viewport(f, x_centrales):

    if not x_centrales:
        x_centrales = [-1, 1]

    xmin = min(x_centrales)
    xmax = max(x_centrales)

    rango = max(abs(xmax - xmin), 1)

    margen = rango * 0.5

    x_min = xmin - margen
    x_max = xmax + margen

    x_vals = np.linspace(
        x_min,
        x_max,
        MUESTRAS_GRAFICA
    )

    y_vals = np.array([
        _evaluar_funcion_segura(f, x)
        for x in x_vals
    ])

    y_vals = _filtrar_datos(y_vals)

    # =====================================================
    # ESCALADO ROBUSTO
    # =====================================================

    y_validos = y_vals[np.isfinite(y_vals)]

    if len(y_validos) == 0:

        ymin, ymax = -10, 10

    else:

        # percentiles robustos
        p2 = np.percentile(y_validos, 2)
        p98 = np.percentile(y_validos, 98)

        # región matemática útil
        mask_util = (
            (y_vals >= p2)
            & (y_vals <= p98)
        )

        y_util = y_vals[mask_util]
        y_util = y_util[np.isfinite(y_util)]

        if len(y_util) == 0:
            y_util = y_validos

        ymin = np.min(y_util)
        ymax = np.max(y_util)

        # evitar rango cero
        if abs(ymax - ymin) < 1e-10:
            ymin -= 1
            ymax += 1

    yrange = ymax - ymin
    if yrange < 0.1: yrange = 2        

    ymin = np.clip(ymin, -5, 5) 
    ymax = np.clip(ymax, -5, 5)

    y_vals = np.where(
        (
            y_vals < ymin - yrange * 3
        ) | (
            y_vals > ymax + yrange * 3
        ),
        np.nan,
        y_vals
    )

    return (
        x_vals,
        y_vals,
        x_min,
        x_max,
        ymin,
        ymax
    )


# =========================================================
# FIGURA BASE
# =========================================================

def crear_grafica_base(f, x_centrales):

    (
        x_vals,
        y_vals,
        x_min,
        x_max,
        ymin,
        ymax
    ) = _crear_viewport(f, x_centrales)

    fig = go.Figure()

    span = x_max - x_min

    if span <= 5:
        dtick = 0.5
    elif span <= 20:
        dtick = 1
    else:
        dtick = 5

    fig.update_layout(
        template='plotly_white', 
        plot_bgcolor='white',    
        paper_bgcolor='white',   
        
        xaxis=dict(
            range=[x_min, x_max],
            gridcolor='lightgray',
            showgrid=True,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            tickmode='linear',
            tickangle=0,
            dtick = 1,
            ##tickmode='auto',
            tickfont=dict(color='black', size=12),
            showticklabels=True  
        ),
        yaxis=dict(
            range=[ymin, ymax],
            gridcolor='lightgray',
            showgrid=True,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
            scaleanchor="x",
            ##scaleratio=1,
            tickmode='linear',
            tickangle=0,
            dtick=1, 
            ##tickmode='auto',
            tickfont=dict(color='black', size=12),
            showticklabels=True  
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name='f(x)',

            line=dict(
                color=COLOR_FUNCION,
                width=2
            ),

            connectgaps=False
        )
    )

    fig.add_hline(
        y=0,
        line_color='black',
        line_width=1
    )

    fig.add_vline(
        x=0,
        line_color='black',
        line_width=1
    )

    fig.update_layout(

        template='plotly_white',

        hovermode='closest',

        dragmode='zoom',

        showlegend=False,

        margin=dict(
            l=30,
            r=30,
            t=50,
            b=30
        ),

    )

    return fig


# =========================================================
# NEWTON
# =========================================================

def graficar_newton(f, iteraciones):

    # =====================================================
    # 1. RECOLECTAR PUNTOS (con filtro seguro)
    # =====================================================
    puntos_x = []

    for it in iteraciones:
        puntos_x.append(it["Ci"])
        puntos_x.append(it["Ci+1"])

    puntos_x = np.array(puntos_x, dtype=float)
    puntos_x = puntos_x[np.isfinite(puntos_x)]

    # =====================================================
    # 2. PROTECCIÓN CONTRA CASOS RAROS
    # =====================================================
    if len(puntos_x) == 0:
        x_min, x_max = -2, 2
    else:
        # =================================================
        # 3. QUITAR OUTLIERS (CLAVE)
        # =================================================
        x_min = np.percentile(puntos_x, 10)
        x_max = np.percentile(puntos_x, 90)

        # si quedó degenerado
        if abs(x_max - x_min) < 1e-6:
            x_min -= 2
            x_max += 2

    # =====================================================
    # 4. ZOOM ROBUSTO (no dependiente de explosiones)
    # =====================================================
    centro = (x_max + x_min) / 2
    ancho = max((x_max - x_min) * 2, 4)

    x_centrales = [centro - ancho, centro + ancho]

    # =====================================================
    # 5. FIGURA BASE
    # =====================================================
    fig = crear_grafica_base(f, x_centrales)

    ymin, ymax = fig.layout.yaxis.range

    # =====================================================
    # 6. DIBUJO NEWTON
    # =====================================================
    for it in iteraciones:

        Ci = it["Ci"]
        Ci_next = it["Ci+1"]

        fCi = _evaluar_funcion_segura(f, Ci)
        fNext = _evaluar_funcion_segura(f, Ci_next)

        if not np.isfinite(fCi):
            continue

        fig.add_trace(go.Scatter(
            x=[Ci],
            y=[fCi],
            mode='markers',
            marker=dict(color='black', size=7),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[Ci, Ci_next],
            y=[fCi, 0],
            mode='lines',
            line=dict(color=COLOR_NEWTON, dash='dash', width=2),
            showlegend=False
        ))

        if np.isfinite(fNext):
            fig.add_trace(go.Scatter(
                x=[Ci_next, Ci_next],
                y=[0, fNext],
                mode='lines',
                line=dict(color='gray', dash='dot'),
                showlegend=False
            ))

    # =====================================================
    # 7. RAÍZ FINAL
    # =====================================================
    raiz = iteraciones[-1]["Ci+1"]

    fig.add_trace(go.Scatter(
        x=[raiz],
        y=[0],
        mode='markers',
        marker=dict(
            symbol='star',
            size=16,
            color=COLOR_RAIZ,
            line=dict(color='black', width=1)
        ),
        showlegend=False
    ))

    # =====================================================
    # 8. RESTAURAR ESCALA Y EVITAR "APLASTAMIENTO"
    # =====================================================
    fig.update_yaxes(range=[ymin, ymax])

    fig.update_layout(title='Método de Newton-Raphson')

    return fig


# =========================================================
# SECANTE
# =========================================================

def graficar_secante(f, iteraciones):

    # =====================================================
    # 1. RECOLECTAR PUNTOS DE FORMA SEGURA
    # =====================================================
    puntos_x = []

    for it in iteraciones:
        puntos_x.extend([it["Ci-1"], it["Ci"], it["Ci+1"]])

    puntos_x = np.array(puntos_x, dtype=float)
    puntos_x = puntos_x[np.isfinite(puntos_x)]

    # =====================================================
    # 2. PROTECCIÓN CONTRA CASOS VACÍOS
    # =====================================================
    if len(puntos_x) == 0:
        x_min, x_max = -2, 2
    else:
        # =================================================
        # 3. ELIMINAR OUTLIERS (CLAVE)
        # =================================================
        x_min = np.percentile(puntos_x, 10)
        x_max = np.percentile(puntos_x, 90)

        if abs(x_max - x_min) < 1e-6:
            x_min -= 2
            x_max += 2

    # =====================================================
    # 4. ZOOM ESTABLE
    # =====================================================
    centro = (x_max + x_min) / 2
    ancho = max((x_max - x_min) * 2, 4)

    x_centrales = [centro - ancho, centro + ancho]

    # =====================================================
    # 5. FIGURA BASE
    # =====================================================
    fig = crear_grafica_base(f, x_centrales)

    # =====================================================
    # 6. DIBUJO DE SECANTE
    # =====================================================
    for it in iteraciones:

        Ci = it["Ci"]
        Cp = it["Ci-1"]

        f1 = _evaluar_funcion_segura(f, Ci)
        f0 = _evaluar_funcion_segura(f, Cp)

        if np.isfinite(f1) and np.isfinite(f0):

            fig.add_trace(go.Scatter(
                x=[Cp, Ci],
                y=[f0, f1],
                mode='lines+markers',
                line=dict(color=COLOR_SECANTE, dash='dash'),
                marker=dict(color='black', size=7),
                showlegend=False
            ))

    # =====================================================
    # 7. RAÍZ FINAL
    # =====================================================
    raiz = iteraciones[-1]["Ci+1"]

    fig.add_trace(go.Scatter(
        x=[raiz],
        y=[0],
        mode='markers',
        marker=dict(
            symbol='star',
            size=16,
            color=COLOR_RAIZ
        ),
        showlegend=False
    ))

    fig.update_layout(title='Método de la Secante')

    return fig

# =========================================================
# PUNTO FIJO
# =========================================================

def graficar_punto_fijo(g, iteraciones):
    # 1. Recolectar todos los valores de X que tocó el método
    puntos_x = [it["Ci"] for it in iteraciones] + [it["Ci+1"] for it in iteraciones]

    x_min_it = min(puntos_x)
    x_max_it = max(puntos_x)

    # 2. Calcular ancho y centro para el Viewport
    ancho = x_max_it - x_min_it
    ancho_vista = max(ancho * 2, 4) 
    centro = (x_max_it + x_min_it) / 2

    # 🔹 Añadir margen dinámico y rango fijo alrededor de 0
    x_lims = [min(x_min_it - ancho_vista, -5), max(x_max_it + ancho_vista, 5)]

    # 3. Usar tu función base para mantener estilos y el viewport inteligente
    fig = crear_grafica_base(g, x_lims)

    # Línea identidad y=x
    x_vals = np.linspace(fig.layout.xaxis.range[0], fig.layout.xaxis.range[1], 4000)
    fig.add_trace(go.Scatter(
        x=x_vals, y=x_vals,
        mode='lines',
        name='y=x',
        line=dict(dash='dash', color='gray', width=1),
        showlegend=False
    ))

    # 4. Dibujar la telaraña
    x_actual = iteraciones[0]["Ci"]
    for it in iteraciones:
        y_siguiente = _evaluar_funcion_segura(g, x_actual)
        if not np.isfinite(y_siguiente): break

        fig.add_trace(go.Scatter(
            x=[x_actual, x_actual], y=[x_actual, y_siguiente],
            mode='lines',
            line=dict(color=COLOR_VERTICAL, width=1, dash='dot'),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[x_actual, y_siguiente], y=[y_siguiente, y_siguiente],
            mode='lines',
            line=dict(color=COLOR_HORIZONTAL, width=1, dash='dot'),
            showlegend=False
        ))
        x_actual = y_siguiente

    # 5. Marcar la raíz
    raiz = iteraciones[-1]["Ci+1"]
    fig.add_trace(go.Scatter(
        x=[raiz], y=[raiz],
        mode='markers',
        marker=dict(symbol='star', size=15, color=COLOR_RAIZ, line=dict(width=1, color='black')),
        showlegend=False
    ))

    fig.update_layout(title='Método de Punto Fijo - Diagrama de Telaraña')
    return fig


# MÉTODOS CERRADOS
# =========================================================

def graficar_metodo_cerrado(
    f,
    iteraciones,
    titulo
):

    # =====================================================
    # 1. RECOLECTAR PUNTOS
    # =====================================================

    puntos_x = []

    for it in iteraciones:

        for clave in ["a", "b", "Ci"]:

            val = _convertir_real(it.get(clave))

            if val is not None and np.isfinite(val):
                puntos_x.append(val)

    puntos_x = np.array(puntos_x, dtype=float)

    # =====================================================
    # 2. PROTECCIÓN
    # =====================================================

    if len(puntos_x) == 0:

        x_min, x_max = -2, 2

    else:

        # eliminar extremos absurdos
        x_min = np.percentile(puntos_x, 10)
        x_max = np.percentile(puntos_x, 90)

        if abs(x_max - x_min) < 1e-6:
            x_min -= 2
            x_max += 2

    # =====================================================
    # 3. ZOOM ROBUSTO
    # =====================================================

    centro = (x_min + x_max) / 2

    ancho = max(
        (x_max - x_min) * 2,
        4
    )

    x_centrales = [
        centro - ancho,
        centro + ancho
    ]

    # =====================================================
    # 4. FIGURA BASE
    # =====================================================

    fig = crear_grafica_base(
        f,
        x_centrales
    )

    ymin, ymax = fig.layout.yaxis.range

    # =====================================================
    # 5. RECTÁNGULO FINAL
    # =====================================================

    a_final = iteraciones[-1]["a"]
    b_final = iteraciones[-1]["b"]

    raiz = iteraciones[-1]["Ci"]

    fig.add_vrect(
        x0=a_final,
        x1=b_final,
        fillcolor='orange',
        opacity=0.12,
        line_width=0
    )

    # =====================================================
    # 6. RAÍZ
    # =====================================================

    fig.add_trace(
        go.Scatter(
            x=[raiz],
            y=[0],
            mode='markers',
            marker=dict(
                symbol='star',
                size=16,
                color=COLOR_RAIZ
            ),
            showlegend=False
        )
    )

    # mantener viewport original
    fig.update_yaxes(
        range=[ymin, ymax]
    )

    fig.update_layout(
        title=titulo
    )

    return fig

# =========================================================
# MÜLLER
# =========================================================

def graficar_muller(f, iteraciones):

    # =====================================================
    # 1. RECOLECTAR PUNTOS
    # =====================================================

    puntos_x = []

    for it in iteraciones:

        for clave in [
            "x0",
            "x1",
            "x2",
            "x3"
        ]:

            val = _convertir_real(
                it.get(clave)
            )

            if (
                val is not None
                and np.isfinite(val)
            ):
                puntos_x.append(val)

    puntos_x = np.array(
        puntos_x,
        dtype=float
    )

    # =====================================================
    # 2. PROTECCIÓN
    # =====================================================

    if len(puntos_x) == 0:

        x_min, x_max = -2, 2

    else:

        # eliminar outliers
        x_min = np.percentile(
            puntos_x,
            10
        )

        x_max = np.percentile(
            puntos_x,
            90
        )

        # evitar degeneración
        if abs(x_max - x_min) < 1e-6:

            x_min -= 2
            x_max += 2

    # =====================================================
    # 3. ZOOM ROBUSTO
    # =====================================================

    centro = (
        x_min + x_max
    ) / 2

    ancho = max(
        (x_max - x_min) * 2,
        4
    )

    x_centrales = [
        centro - ancho,
        centro + ancho
    ]

    # =====================================================
    # 4. FIGURA BASE
    # =====================================================

    fig = crear_grafica_base(
        f,
        x_centrales
    )

    ymin, ymax = fig.layout.yaxis.range

    # =====================================================
    # 5. RAÍZ FINAL
    # =====================================================

    raiz = _convertir_real(
        iteraciones[-1]["x3"]
    )

    if raiz is not None:

        fig.add_trace(
            go.Scatter(
                x=[raiz],
                y=[0],
                mode='markers',
                marker=dict(
                    symbol='star',
                    size=16,
                    color=COLOR_RAIZ
                ),
                showlegend=False
            )
        )

    # =====================================================
    # 6. MANTENER VIEWPORT
    # =====================================================

    fig.update_yaxes(
        range=[ymin, ymax]
    )

    fig.update_layout(
        title='Método de Müller'
    )

    return fig

# =========================================================
# TAYLOR
# =========================================================

def graficar_taylor(
    f_num,
    poly_num,
    x_eval,
    a,
    titulo
):

    # =====================================================
    # 1. VIEWPORT ROBUSTO
    # =====================================================

    puntos_x = np.array(
        [a, x_eval],
        dtype=float
    )

    puntos_x = puntos_x[np.isfinite(puntos_x)]

    if len(puntos_x) == 0:
        x_min, x_max = -2, 2

    else:

        x_min = np.percentile(puntos_x, 10)
        x_max = np.percentile(puntos_x, 90)

        if abs(x_max - x_min) < 1e-6:
            x_min -= 2
            x_max += 2

    centro = (x_max + x_min) / 2
    ancho = max((x_max - x_min) * 3, 6)

    x_centrales = [
        centro - ancho,
        centro + ancho
    ]

    # =====================================================
    # 2. FIGURA BASE (f(x))
    # =====================================================

    fig = crear_grafica_base(
        f_num,
        x_centrales
    )

    fig.update_layout(
        height=650, # Aumenta este valor si la quieres más grande
        margin=dict(l=50, r=50, t=80, b=50) # Un poco más de margen para los números
    )

    ymin, ymax = fig.layout.yaxis.range

    # =====================================================
    # 3. GENERAR TAYLOR
    # =====================================================

    x_vals = np.linspace(
        centro - ancho,
        centro + ancho,
        4000
    )

    y_p = np.array([
        _evaluar_funcion_segura(poly_num, x)
        for x in x_vals
    ])

    y_p = _filtrar_datos(y_p)

    # =====================================================
    # 4. CURVA TAYLOR
    # =====================================================

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_p,
            mode='lines',
            name='Taylor',
            line=dict(
                dash='dash',
                width=2,
                color='red'
            )
        )
    )

    # =====================================================
    # 5. PUNTO DE EXPANSIÓN
    # =====================================================

    y_aprox = _evaluar_funcion_segura(poly_num, x_eval)

    if np.isfinite(y_aprox):
        fig.add_trace(
            go.Scatter(
                x=[x_eval],      # <--- Cambiado de 'a' a 'x_eval'
                y=[y_aprox],    # <--- Cambiado de 'y_a' a 'y_aprox'
                mode='markers',
                name='Aproximación',
                marker=dict(
                    symbol='star',
                    size=14,
                    color=COLOR_RAIZ, # O el color que prefieras para el resultado
                    line=dict(color='black', width=1)
                ),
                showlegend=True # Ahora sí conviene mostrar qué es en la leyenda
            )
    )

    # =====================================================
    # 6. RESTAURAR ESCALA
    # =====================================================

    fig.update_yaxes(
        range=[ymin, ymax]
    )

    fig.update_layout(
        title=titulo
    )

    return fig

# =========================================================
# NEWTON-HORNER
# =========================================================

def graficar_newton_horner(f, iteraciones):

    # =====================================================
    # 1. RECOLECTAR PUNTOS
    # =====================================================

    puntos_x = []

    for it in iteraciones:

        if "Ci" in it:
            puntos_x.append(it["Ci"])

        if "Ci+1" in it:
            puntos_x.append(it["Ci+1"])

    puntos_x = np.array(puntos_x, dtype=float)
    puntos_x = puntos_x[np.isfinite(puntos_x)]

    # =====================================================
    # 2. PROTECCIÓN
    # =====================================================

    if len(puntos_x) == 0:

        x_min, x_max = -2, 2

    else:

        x_min = np.percentile(puntos_x, 10)
        x_max = np.percentile(puntos_x, 90)

        if abs(x_max - x_min) < 1e-6:
            x_min -= 2
            x_max += 2

    # =====================================================
    # 3. ZOOM ROBUSTO
    # =====================================================

    centro = (x_max + x_min) / 2
    ancho = max((x_max - x_min) * 2, 4)

    x_centrales = [
        centro - ancho,
        centro + ancho
    ]

    # =====================================================
    # 4. FIGURA BASE
    # =====================================================

    fig = crear_grafica_base(
        f,
        x_centrales
    )

    ymin, ymax = fig.layout.yaxis.range

    # =====================================================
    # 5. DIBUJAR ITERACIONES
    # =====================================================

    for it in iteraciones:

        Ci = it["Ci"]
        Ci_next = it["Ci+1"]

        fCi = _evaluar_funcion_segura(f, Ci)
        fNext = _evaluar_funcion_segura(f, Ci_next)

        if not np.isfinite(fCi):
            continue

        # Punto sobre la función
        fig.add_trace(
            go.Scatter(
                x=[Ci],
                y=[fCi],
                mode='markers',
                marker=dict(
                    color='black',
                    size=7
                ),
                showlegend=False
            )
        )

        # Tangente
        fig.add_trace(
            go.Scatter(
                x=[Ci, Ci_next],
                y=[fCi, 0],
                mode='lines',
                line=dict(
                    color='purple',
                    dash='dash',
                    width=2
                ),
                showlegend=False
            )
        )

        # Línea vertical
        if np.isfinite(fNext):

            fig.add_trace(
                go.Scatter(
                    x=[Ci_next, Ci_next],
                    y=[0, fNext],
                    mode='lines',
                    line=dict(
                        color='gray',
                        dash='dot'
                    ),
                    showlegend=False
                )
            )

    # =====================================================
    # 6. RAÍZ FINAL
    # =====================================================

    raiz = iteraciones[-1]["Ci+1"]

    fig.add_trace(
        go.Scatter(
            x=[raiz],
            y=[0],
            mode='markers',
            marker=dict(
                symbol='star',
                size=16,
                color=COLOR_RAIZ,
                line=dict(
                    color='black',
                    width=1
                )
            ),
            showlegend=False
        )
    )

    # =====================================================
    # 7. RESTAURAR ESCALA
    # =====================================================

    fig.update_yaxes(
        range=[ymin, ymax]
    )

    fig.update_layout(
        title='Método de Newton-Horner'
    )

    return fig