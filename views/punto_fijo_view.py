import streamlit as st
import pandas as pd
import sympy as sp

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

    # CONFIGURACIÓN DE BÚSQUEDA
    st.subheader("Búsqueda de Intervalos")

    col1, col2, col3 = st.columns(3)

    with col1:
        inicio_busqueda = st.number_input(
            "Desde",
            value=-10.0
        )

    with col2:
        fin_busqueda = st.number_input(
            "Hasta",
            value=10.0
        )

    with col3:
        paso_busqueda = st.number_input(
            "Paso",
            value=1.0,
            min_value=0.01
        )

    if st.button("Calcular"):

        # VALIDACIÓN INTERVALO
        if inicio_busqueda >= fin_busqueda:
            st.error("El valor 'Desde' debe ser menor que 'Hasta'.")
            return

        # VALIDAR FUNCIÓN
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error_msg)
            return

        f_sym, x, f_num, _, f_visual = datos

        # GENERAR g(x)
        gs = generar_gs_algebraicas(f_sym)

        if not gs:
            st.error("No se pudieron generar funciones g(x).")
            return

        # ENCONTRAR INTERVALOS
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
        st.latex(f"f(x)={sp.latex(f_sym)}")

        # MOSTRAR g(x)
        st.subheader("Funciones g(x) Generadas:")

        for g_data in gs:
            st.latex(f"{g_data['nombre']} = {g_data['latex']}")

        st.divider()

        resultados_globales = []

        # RECORRER INTERVALOS
        for idx, intervalo in enumerate(intervalos):

            a, b = intervalo
            x0 = (a + b) / 2

            st.header(f"Raíz #{idx+1} detectada en ({a}, {b})")

            st.success(f"Valor inicial automático X₀ = {x0:.8f}")

            # PREPARAR GS PARA GRÁFICA
            gs_grafica = []

            for g_data in gs:
                gs_grafica.append({
                    "nombre": g_data["nombre"],
                    "num": sp.lambdify(x, g_data["expr"], "numpy")
                })

            # ITERAR g(x)
            for g_data, g_eval in zip(gs, gs_grafica):

                st.subheader(f"Resolviendo con {g_data['nombre']}")

                try:

                    ok, msg, iteraciones = ejecutar_punto_fijo(
                        g_eval["num"],
                        x0,
                        tol
                    )

                    if not ok:
                        st.error(msg)
                        continue

                    st.success("Método convergente.")

                    # PROCEDIMIENTO
                    with st.expander(f"Ver procedimiento {g_data['nombre']}"):

                        for it in iteraciones:
                            st.latex(
                                f"x_{{{it['i']+1}}}=g(x_{{{it['i']}}})={it['Ci+1']:.8f}"
                            )

                    # TABLA
                    df = pd.DataFrame(iteraciones)

                    st.dataframe(df)

                    # RESULTADO
                    st.success(
                        f"Raíz aproximada: {iteraciones[-1]['Ci+1']:.8f}"
                    )

                    # GUARDAR PARA EXCEL UNIFICADO
                    resultados_globales.append({
                        "intervalo": (a, b),
                        "g": g_data["nombre"],
                        "iteraciones": iteraciones
                    })

                except Exception as e:
                    st.error(f"Error en {g_data['nombre']}: {str(e)}")

            # 🔥 UNA SOLA GRÁFICA POR INTERVALO
            st.subheader("Gráfica de g(x)")

            st.pyplot(
                graficar_punto_fijo(
                    gs_grafica,
                    inicio_busqueda,
                    fin_busqueda
                )
            )

            st.divider()

        # 🔥 EXCEL UNIFICADO (UNA SOLA DESCARGA)
        st.subheader("Exportación")

        excel_bytes = exportar_excel_punto_fijo(resultados_globales)

        st.download_button(
            label="📊 Descargar Excel Completo",
            data=excel_bytes,
            file_name="PuntoFijo_Unificado.xlsx"
        )