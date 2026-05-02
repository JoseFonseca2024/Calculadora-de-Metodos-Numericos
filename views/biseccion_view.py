import streamlit as st
import sympy as sp
import pandas as pd
from utils.funciones import validar_y_preparar_funcion
from utils.formateo import fmt
from metodos.biseccion import ejecutar_biseccion
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_metodo_cerrado
from Services.exportar_excel import exportar_excel_newton as exportar_excel_bytes

def mostrar_biseccion():
    st.title("Método de Bisección")
    st.markdown("Este método divide el intervalo a la mitad en cada iteración para encontrar la raíz.")

    funcion_str = st.text_input("Introduzca una función f(x):", placeholder="Ej: x^2 - 10*cos(x) - 2", key="bis_input")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Límite inferior (a):", value=0.0, format="%.6f", key="bis_a")
    with col2:
        b = st.number_input("Límite superior (b):", value=1.0, format="%.6f", key="bis_b")
        
    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.6f", key="bis_tol")

    if st.button("Calcular"):
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error_msg)
            return

        # Desempaquetado de 5 valores
        f_sym, x_sym, f_num, f_der_num, f_visual = datos
        
        ok, msg, iteraciones = ejecutar_biseccion(f_num, a, b, tol)

        if not ok:
            st.error(msg)
            return

        st.subheader("Función analizada:")
        st.latex(f"f(x) = {f_visual}")

        # --- PROCEDIMIENTO PASO A PASO ---
        st.subheader("Procedimiento Paso a Paso")
        with st.expander("Ver cálculos detallados", expanded=False):
            st.markdown("### 1. Evaluación Inicial")
            fa_init = float(f_num(a))
            fb_init = float(f_num(b))
            st.latex(f"f(a) = f({a:.4f}) = {fa_init:.6f}")
            st.latex(f"f(b) = f({b:.4f}) = {fb_init:.6f}")
            
            if fa_init * fb_init > 0:
                st.error("No hay cambio de signo en el intervalo inicial.")
            else:
                st.success("Cambio de signo detectado ($f(a) \cdot f(b) < 0$).")

            st.markdown("---")
            st.markdown("### 2. Desarrollo de Iteraciones")
            for i, it in enumerate(iteraciones):
                idx = it.get('i', i + 1)
                actual_a = it['a']
                actual_b = it['b']
                c = it['Ci']
                fc = it['f(Ci)']
                
                st.write(f"#### Iteración {idx}")
                st.latex(f"c_{{{idx}}} = \\frac{{{actual_a:.6f} + {actual_b:.6f}}}{{2}} = {c:.6f}")
                st.latex(f"f(c_{{{idx}}}) = {fc:.6f}")
                
                if i < len(iteraciones) - 1:
                    proxima = iteraciones[i+1]
                    if proxima['a'] == c:
                        st.info(f"Como $f(a) \cdot f(c) > 0$, la raíz está en $[c, b]$. Nuevo intervalo: $[{proxima['a']:.6f}, {proxima['b']:.6f}]$")
                    else:
                        st.info(f"Como $f(a) \cdot f(c) < 0$, la raíz está en $[a, c]$. Nuevo intervalo: $[{proxima['a']:.6f}, {proxima['b']:.6f}]$")
                st.markdown("---")

        # Preparación de datos para tabla
        for it in iteraciones:
            it["Ci+1"] = it["Ci"]
            it["f(a)"] = float(f_num(it["a"]))
            it["f(b)"] = float(f_num(it["b"]))

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
        df = pd.DataFrame(iteraciones_visibles)
        
        st.subheader("Tabla de Iteraciones")
        st.dataframe(df.style.format(fmt))

        st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci']:.6f}")

        # Gráfica
        st.subheader("Visualización del Método")
        fig = graficar_metodo_cerrado(f_num, iteraciones_visibles, "Convergencia: Bisección")
        st.pyplot(fig)

        excel_bytes = exportar_excel_bytes(df, f_num, iteraciones_visibles)
        st.download_button(label="📊 Descargar Excel", data=excel_bytes, file_name="Biseccion.xlsx")