import streamlit as st
import pandas as pd
import sympy as sp
import numpy as np

from utils.funciones import validar_y_preparar_funcion
from utils.generador_g import generar_gs_algebraicas
from utils.intervalos import encontrar_intervalos_raiz

from metodos.punto_fijo import ejecutar_punto_fijo

from plot.graficas import graficar_punto_fijo
from Services.exportar_excel import exportar_excel_punto_fijo


def mostrar_punto_fijo():

    st.title("Método del Punto Fijo")

    funcion_str = st.text_input(
        "Introduzca una función f(x):",
        placeholder="Ej: x²-3x+e^x-2"
    )

    tol = st.number_input(
        "Tolerancia (%)",
        value=0.0001,
        format="%.8f"
    )

    # 🔍 CONFIGURACIÓN DE INTERVALOS
    st.subheader("Búsqueda de Intervalos")

    col1, col2, col3 = st.columns(3)

    with col1:
        inicio_busqueda = st.number_input("Desde", value=-10.0)

    with col2:
        fin_busqueda = st.number_input("Hasta", value=10.0)

    with col3:
        paso_busqueda = st.number_input("Paso", value=0.01, min_value=0.01)

    if st.button("Calcular"):

        # VALIDACIÓN
        if inicio_busqueda >= fin_busqueda:
            st.error("El valor 'Desde' debe ser menor que 'Hasta'.")
            return

        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error_msg)
            return

        f_sym, x, f_num, _, _ = datos

        # GENERAR g(x)
        gs = generar_gs_algebraicas(f_sym)

        if not gs:
            st.error("No se pudieron generar funciones g(x).")
            return

        # BUSCAR INTERVALOS
        intervalos = encontrar_intervalos_raiz(
            f_num,
            inicio_busqueda,
            fin_busqueda,
            paso_busqueda
        )

        if not intervalos:
            st.error("No se encontraron intervalos con raíz.")
            return

        # MOSTRAR FUNCIÓN
        st.subheader("Función Original:")
        st.latex(f"f(x) = {sp.latex(f_sym)}")

        # MOSTRAR g(x)
        st.subheader("Funciones g(x) Generadas:")
        for g_data in gs:
            st.latex(f"{g_data['nombre']} = {g_data['latex']}")

        st.divider()

        resultados_globales = []

        # 🔁 RECORRER INTERVALOS
        for idx, intervalo in enumerate(intervalos):

            a, b = intervalo
            x0 = (a + b) / 2

            st.header(f"Raíz #{idx+1} detectada en ({a}, {b})")
            st.success(f"Valor inicial automático X₀ = {x0:.8f}")

            # FILTRO DE CONVERGENCIA
            gs_validas = []

            for g_data in gs:

                try:

                    g_expr = g_data["expr"]

                    g_deriv = sp.diff(g_expr, x)

                    g_num = g_data["num"]

                    g_deriv_num = sp.lambdify(
                        x,
                        g_deriv,
                        modules=["numpy"]
                    )

                    # =====================================================
                    # VALIDAR g(x) EN EL INTERVALO
                    # =====================================================

                    eps = 1e-4

                    xs_test = np.linspace(
                        a + eps,
                        b - eps,
                        25
                    )

                    derivadas = []

                    valido = True

                    for xt in xs_test:

                        try:

                            val = g_num(xt)

                            if np.iscomplexobj(val):

                                if abs(val.imag) > 1e-10:
                                    valido = False
                                    break

                                val = val.real

                            if not np.isfinite(val):
                                valido = False
                                break

                            if abs(val) > 1e6:
                                valido = False
                                break

                            dv = g_deriv_num(xt)

                            if np.iscomplexobj(dv):

                                if abs(dv.imag) > 1e-10:
                                    valido = False
                                    break

                                dv = dv.real

                            if not np.isfinite(dv):
                                valido = False
                                break

                            derivadas.append(
                                abs(float(dv))
                            )

                        except:
                            valido = False
                            break

                    if not valido:
                        continue

                    # =====================================================
                    # CRITERIO DE CONVERGENCIA
                    # =====================================================

                    max_deriv = max(derivadas)

                    # ❌ demasiado divergente
                    if max_deriv >= 2:
                        continue

                    # ⚠️ advertencia convergencia lenta
                    if max_deriv > 0.9:

                        st.warning(
                            f"{g_data['nombre']} puede converger lento "
                            f"(max |g'(x)| ≈ {max_deriv:.4f})"
                        )

                    gs_validas.append({
                        "nombre": g_data["nombre"],
                        "expr": g_expr,
                        "num": g_num
                    })

                except (
                    ValueError,
                    ZeroDivisionError,
                    TypeError,
                    OverflowError,
                    RecursionError
                ):
                    continue

            if not gs_validas:
                st.warning("Ninguna función g(x) converge en este intervalo.")
                continue

            # 🔁 ITERAR CADA g(x)
            for g in gs_validas:

                st.subheader(f"Resolviendo con {g['nombre']}")

                try:
                    ok, msg, iteraciones = ejecutar_punto_fijo(
                        g["num"],
                        x0,
                        tol
                    )

                    if not ok:
                        st.error(msg)
                        continue

                    st.success("Método convergente.")

                    with st.expander(f"Ver procedimiento paso a paso ({g['nombre']})", expanded=False):

                        g_expr = g["expr"]
                        g_latex = sp.latex(g_expr)

                        for it in iteraciones:
                            i = it["i"]
                            xi = it["Ci"]
                            xi1 = it["Ci+1"]

                            st.write(f"**Iteración {i}:**")

                            # 🔹 Forma general
                            st.latex(f"x_{{{i+1}}} = g(x_{{{i}}})")

                            # 🔹 Sustitución simbólica
                            valor_latex = f"({xi:.6f})"
                            g_sust = g_latex.replace("x", valor_latex)

                            st.latex(f"x_{{{i+1}}} = {g_sust}")

                            # 🔹 Evaluación numérica
                            st.latex(f"x_{{{i+1}}} = {xi1:.8f}")

                            # 🔹 Error
                            st.latex(f"Error = {it['Error%']:.8f}\\%")

                    # 📊 GRÁFICA (CORRECTAMENTE UBICADA)
                    st.plotly_chart(
                        graficar_punto_fijo(
                            g["num"],
                            iteraciones
                        ),
                        use_container_width=True
                    )

                    # TABLA
                    df = pd.DataFrame(iteraciones)
                    st.dataframe(df)

                    # RESULTADO FINAL
                    st.success(
                        f"Raíz aproximada: {iteraciones[-1]['Ci+1']:.8f}"
                    )

                    resultados_globales.append({
                        "intervalo": (a, b),
                        "g": g["nombre"],
                        "iteraciones": iteraciones
                    })

                except Exception as e:
                    st.error(f"Error en {g['nombre']}: {str(e)}")

            st.divider()

        # 📥 EXPORTACIÓN
        st.subheader("Exportación")

        excel_bytes = exportar_excel_punto_fijo(resultados_globales)

        st.download_button(
            label="📊 Descargar Excel Completo",
            data=excel_bytes,
            file_name="PuntoFijo_Unificado.xlsx"
        )