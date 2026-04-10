import streamlit as st
import sympy as sp
import pandas as pd
import re

from utils.funciones import validar_y_preparar_funcion
from utils.formateo import fmt
from metodos.regla_falsa import ejecutar_regla_falsa
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_metodo_cerrado
from Services.exportar_excel import exportar_excel_newton as exportar_excel_bytes

def mostrar_regla_falsa():
    st.title("Método de la Regla Falsa")
    st.markdown("Este método utiliza la interpolación lineal para aproximar la raíz en un intervalo cerrado.")

    funcion_str = st.text_input("Introduzca una función f(x):", placeholder="Ej: e^-x - x")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Límite inferior (a):", value=0.0, format="%.6f")
    with col2:
        b = st.number_input("Límite superior (b):", value=1.0, format="%.6f")
        
    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.6f")

    if st.button("Calcular"):
        try:
            # 1. Validación (Asegúrate que funciones.py retorne 5 valores)
            valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

            if not valido:
                st.error(f"Error de validación: {error_msg}")
                return

            f_sym, x_sym, f_num, f_der_num, texto_visual = datos
            
            # 2. Ejecución del método
            ok, msg, iteraciones = ejecutar_regla_falsa(f_num, a, b, tol)

            if not ok:
                st.error(f"Error en el método: {msg}")
                return

            # --- RENDERIZADO VISUAL ---
            st.subheader("Función analizada:")
            # Regex corregida para no "comerse" toda la expresión
            f_rep = texto_visual.replace("**", "^")
            f_render = re.sub(r'\^([\-\+]?[a-zA-Z0-9\(\)]+)', r'^{\1}', f_rep)
            f_render = f_render.replace("*", "") 
            st.latex(f"f(x) = {f_render}")

            # --- PROCEDIMIENTO PASO A PASO ---
            st.subheader("Procedimiento Paso a Paso")
            with st.expander("Ver cálculos detallados", expanded=False):
                st.markdown("### Desarrollo")
                for i, it in enumerate(iteraciones):
                    st.write(f"#### Iteración {it['i']}")
                    st.latex(f"c_{{{it['i']}}} = {it['b']:.6f} - \\frac{{f({it['b']:.4f})({it['a']:.6f} - {it['b']:.6f})}}{{f({it['a']:.4f}) - f({it['b']:.4f})}}")
                    st.latex(f"c_{{{it['i']}}} = {it['Ci']:.6f}")
                    st.markdown("---")

            # --- TABLA Y EXCEL ---
            for it in iteraciones:
                it["Ci+1"] = it["Ci"]
                it["f(a)"] = float(f_num(it["a"]))
                it["f(b)"] = float(f_num(it["b"]))

            iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
            df = pd.DataFrame(iteraciones_visibles)
            
            st.subheader("Tabla de Iteraciones")
            st.dataframe(df.style.format({
                "a": fmt, "b": fmt, "f(a)": fmt, "f(b)": fmt, 
                "Ci": fmt, "f(Ci)": fmt, "Error%": fmt
            }))

            st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci']:.6f}")
            
            # Gráfica
            fig = graficar_metodo_cerrado(f_num, iteraciones_visibles, "Convergencia: Regla Falsa")
            st.pyplot(fig)

            # Exportación
            excel_bytes = exportar_excel_bytes(df, f_num, iteraciones_visibles)
            st.download_button(label="📊 Descargar Excel", data=excel_bytes, file_name="Regla_Falsa.xlsx")

        except Exception as e:
            # Si algo falla, esto te dirá EXACTAMENTE qué línea y qué error es
            st.error(f"Se produjo un error inesperado: {str(e)}")
            st.info("Revisa si el archivo utils/funciones.py devuelve 5 valores.")