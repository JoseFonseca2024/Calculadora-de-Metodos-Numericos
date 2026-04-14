import streamlit as st
import sympy as sp
import pandas as pd
from utils.funciones import validar_y_preparar_funcion
from metodos.newton_raphson import ejecutar_newton_raphson
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_newton
from Services.exportar_excel import exportar_excel_newton as exportar_excel_bytes

def mostrar_newton_raphson():
    st.title("Método de Newton-Raphson")
    
    funcion_str = st.text_input("Introduzca una función f(x):", placeholder="Ej: x^3 - x - 1")
    x0 = st.number_input("Punto inicial (C₀):", value=0.0, format="%.8f")
    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.8f")

    if st.button("Calcular"):
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)
        if not valido:
            st.error(error_msg); return

        f_sym, x_sym, f_num, f_der_num, f_visual = datos
        ok, msg, iteraciones = ejecutar_newton_raphson(f_num, f_der_num, x0, tol)

        if not ok:
            st.error(msg); return

        st.subheader("Análisis de la Función:")
        st.latex(f"f(x) = {f_visual}")
        st.latex(f"f'(x) = {sp.latex(sp.diff(f_sym, x_sym))}")

        with st.expander("Ver procedimiento paso a paso", expanded=False):
            for it in iteraciones:
                idx = it.get('i', it.get('iter', 0))
                actual = it.get('xn', it.get('Ci', 0))
                siguiente = it.get('xn+1', it.get('Ci+1', 0))
                st.write(f"**Iteración {idx}:**")
                st.latex(f"x_{{{idx+1}}} = {actual:.8f} - \\frac{{f({actual:.8f})}}{{f'({actual:.8f})}} = {siguiente:.8f}")

        # Mapeo seguro para la gráfica
        for it in iteraciones:
            it["Ci"] = it.get('xn', it.get('Ci', 0))
            it["Ci+1"] = it.get('xn+1', it.get('Ci+1', 0))
            it["f(Ci)"] = it.get('f(xn)', it.get('f(Ci)', 0))

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
        st.subheader("Tabla de Iteraciones")
        st.dataframe(pd.DataFrame(iteraciones_visibles))

        st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci+1']:.8f}")
        st.pyplot(graficar_newton(f_num, iteraciones_visibles))
        
        excel_bytes = exportar_excel_bytes(pd.DataFrame(iteraciones_visibles), f_num, iteraciones_visibles)
        st.download_button(label="📊 Descargar Excel", data=excel_bytes, file_name="Newton.xlsx")