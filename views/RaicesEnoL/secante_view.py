import streamlit as st
import pandas as pd
from utils.funciones import validar_y_preparar_funcion
from metodos.secante import ejecutar_secante
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_secante
from Services.exportar_excel import exportar_excel_secante


def mostrar_secante():
    st.title("Método de la Secante")
    
    funcion_str = st.text_input("Introduzca f(x):", placeholder="Ej: x^2 - 4")
    
    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("C₀:", value=0.0, format="%.4f")
    with col2:
        x1 = st.number_input("C₋₁:", value=1.0, format="%.4f")

    tol = st.number_input("Tolerancia (%)", value=0.00001, format="%.5f")

    if st.button("Calcular"):

        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)
        if not valido:
            st.error(error_msg)
            return

        _, _, f_num, _, f_visual = datos

        ok, msg, iteraciones = ejecutar_secante(f_num, x0, x1, tol)
        if not ok:
            st.error(msg)
            return

        st.subheader("Función:")
        st.latex(f"f(x) = {f_visual}")

        # 🔹 Evaluación inicial (NUEVO)
        st.subheader("Evaluación inicial")

        f_x0_sust = f_visual.replace("x", f"({x0:.6f})")
        f_x1_sust = f_visual.replace("x", f"({x1:.6f})")

        f_x0 = f_num(x0)
        f_x1 = f_num(x1)

        st.latex(f"f(C_0) = {f_visual}")
        st.latex(f"f(C_0) = {f_x0_sust}")
        st.latex(f"f(C_0) = {f_x0:.8f}")

        st.latex(f"f(C_{{-1}}) = {f_visual}")
        st.latex(f"f(C_{{-1}}) = {f_x1_sust}")
        st.latex(f"f(C_{{-1}}) = {f_x1:.8f}")

        # 🔹 PROCEDIMIENTO DETALLADO
        with st.expander("Ver procedimiento detallado", expanded=False):

            for it in iteraciones:

                idx = it["i"]
                xi = it["Ci"]
                xi_prev = it["Ci-1"]
                xi_next = it["Ci+1"]

                f_xi = it["f(Ci)"]
                f_xi_prev = it["f(Ci-1)"]

                st.write(f"### Iteración {idx + 1}")

                # 🔹 Fórmula general
                st.latex(
                    f"x_{{{idx+1}}} = {xi:.8f} - "
                    f"\\frac{{f({xi:.8f})({xi_prev:.8f} - {xi:.8f})}}"
                    f"{{f({xi_prev:.8f}) - f({xi:.8f})}}"
                )

                # 🔹 Sustitución en f(xi)
                f_sust_xi = f_visual.replace("x", f"({xi:.6f})")
                st.latex(f"f({xi:.6f}) = {f_sust_xi}")
                st.latex(f"f({xi:.6f}) = {f_xi:.8f}")

                # 🔹 Sustitución en f(xi-1)
                f_sust_prev = f_visual.replace("x", f"({xi_prev:.6f})")
                st.latex(f"f({xi_prev:.6f}) = {f_sust_prev}")
                st.latex(f"f({xi_prev:.6f}) = {f_xi_prev:.8f}")

                # 🔹 Sustitución en la fórmula
                st.latex(
                    f"x_{{{idx+1}}} = {xi:.8f} - "
                    f"\\frac{{({f_xi:.8f})({xi_prev:.8f} - {xi:.8f})}}"
                    f"{{({f_xi_prev:.8f}) - ({f_xi:.8f})}}"
                )

                # 🔹 Resultado final
                st.latex(f"x_{{{idx+1}}} = {xi_next:.8f}")

                # 🔹 Error
                st.latex(f"Error = {it['Error%']:.8f}\\%")

                st.markdown("---")

        # 🔹 TABLA
        for it in iteraciones:
            it["Ci"] = it["Ci"]
            it["Ci+1"] = it["Ci+1"]
            it["f(Ci)"] = f_num(it["Ci"])

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)

        st.subheader("Tabla de Iteraciones")
        st.dataframe(pd.DataFrame(iteraciones_visibles))

        # 🔹 RESULTADO
        st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci+1']:.8f}")

        # 🔹 GRÁFICA
        st.plotly_chart(graficar_secante(f_num, iteraciones_visibles), use_container_width=True)

        # 🔹 EXPORTAR
        excel_bytes = exportar_excel_secante(
            pd.DataFrame(iteraciones_visibles),
            f_num,
            iteraciones_visibles
        )

        st.download_button(
            label="📊 Descargar Excel",
            data=excel_bytes,
            file_name="Secante.xlsx"
        )