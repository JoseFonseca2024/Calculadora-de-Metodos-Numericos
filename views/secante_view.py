import streamlit as st
import pandas as pd
from utils.funciones import validar_y_preparar_funcion
from metodos.secante import ejecutar_secante
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_secante
from Services.exportar_excel import exportar_excel_newton as exportar_excel_bytes

def mostrar_secante():
    st.title("Método de la Secante")
    
    funcion_str = st.text_input("Introduzca f(x):", placeholder="Ej: x^2 - 4")
    col1, col2 = st.columns(2)
    with col1: x0 = st.number_input("C₀:", value=0.0, format="%.6f")
    with col2: x1 = st.number_input("C₋₁", value=1.0, format="%.6f")
    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.6f")

    if st.button("Calcular"):
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)
        if not valido:
            st.error(error_msg); return

        _, _, f_num, _, f_visual = datos
        ok, msg, iteraciones = ejecutar_secante(f_num, x0, x1, tol)

        if not ok:
            st.error(msg); return

        st.subheader("Función:")
        st.latex(f"f(x) = {f_visual}")

        # --- PROCEDIMIENTO PASO A PASO ---
        with st.expander("Ver procedimiento detallado", expanded=False):
            for it in iteraciones:
                idx = it.get('i', it.get('iter', 0))
                x_act = it.get('xn', it.get('Ci', 0))
                x_prev = it.get('xn-1', it.get('Ci-1', 0))
                x_sig = it.get('xn+1', it.get('Ci+1', 0))
                st.write(f"**Iteración {idx}:**")
                st.latex(f"x_{{{idx+1}}} = {x_act:.6f} - \\frac{{f({x_act:.6f})({x_prev:.6f} - {x_act:.6f})}}{{f({x_prev:.6f}) - f({x_act:.6f})}} = {x_sig:.6f}")

        # Mapeo seguro para evitar KeyError
        for it in iteraciones:
            it["Ci-1"] = it.get('xn-1', it.get('Ci-1', 0))
            it["Ci"] = it.get('xn', it.get('Ci', 0))
            it["Ci+1"] = it.get('xn+1', it.get('Ci+1', 0))
            it["f(Ci)"] = float(f_num(it["Ci"]))
            it["f(Ci-1)"] = float(f_num(it["Ci-1"]))

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
        st.subheader("Tabla de Iteraciones")
        st.dataframe(pd.DataFrame(iteraciones_visibles))

        st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci+1']:.6f}")
        st.pyplot(graficar_secante(f_num, iteraciones_visibles))
        
        excel_bytes = exportar_excel_bytes(pd.DataFrame(iteraciones_visibles), f_num, iteraciones_visibles)
        st.download_button(label="📊 Descargar Excel", data=excel_bytes, file_name="Secante.xlsx")