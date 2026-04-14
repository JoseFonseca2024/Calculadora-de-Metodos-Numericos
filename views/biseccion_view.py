import streamlit as st
import pandas as pd

from utils.funciones import validar_y_preparar_funcion
from utils.formateo import fmt
from metodos.biseccion import ejecutar_biseccion
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_metodo_cerrado
from Services.exportar_excel import exportar_excel_biseccion
from utils.evaluacion_segura import evaluar_seguro

def mostrar_biseccion():
    st.title("Método de Bisección")
    st.markdown("Este método divide el intervalo a la mitad en cada iteración para encontrar la raíz.")

    funcion_str = st.text_input("Introduzca una función f(x):", placeholder="Ej: x^2 - 10*cos(x) - 2", key="bis_input")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Límite inferior (a):", value=0.0, format="%.8f", key="bis_a")
    with col2:
        b = st.number_input("Límite superior (b):", value=1.0, format="%.8f", key="bis_b")
        
    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.8f", key="bis_tol")

    if st.button("Calcular"):
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error_msg)
            return

        # Desempaquetado de 5 valores
        _, _, f_num, _, f_visual = datos

        st.subheader("Función analizada:")
        st.latex(f"f(x) = {f_visual}")

        # Verificar existencia de Raiz
        fa_init = evaluar_seguro(f_num, a)
        fb_init = evaluar_seguro(f_num, b)

        if fa_init is None or fb_init is None:
            st.error("La función no se puede evaluar en el intervalo.")
            return

        st.subheader("Verificación de existencia de raíz")
        st.latex(f"f(a) = f({a:.4f}) = {fa_init:.8f}")
        st.latex(f"f(b) = f({b:.4f}) = {fb_init:.8f}")

        if fa_init * fb_init > 0:
            st.error("No hay cambio de signo en el intervalo. No existe una raiz")
            return
        else:
            st.success(r"Existe al menos una raíz en el intervalo ($f(a) \cdot f(b) < 0$).")
        
        ok, msg, iteraciones = ejecutar_biseccion(f_num, a, b, tol)

        if not ok:
            st.error(msg)
            return

        # --- PROCEDIMIENTO PASO A PASO ---
        st.subheader("Procedimiento Paso a Paso")
        with st.expander("Ver cálculos detallados", expanded=False):

            st.markdown("---")
            st.markdown("### 2. Desarrollo de Iteraciones")
            for i, it in enumerate(iteraciones):
                idx = it.get('i', i + 1)
                actual_a = it['a']
                actual_b = it['b']
                c = it['Ci']
                fc = it['f(Ci)']
                
                st.write(f"#### Iteración {idx}")
                st.latex(rf"c_{{{idx}}} = \frac{{{actual_a:.8f} + {actual_b:.8f}}}{{2}} = {c:.8f}")
                st.latex(f"f(c_{{{idx}}}) = {fc:.8f}")
                
                if i < len(iteraciones) - 1:
                    proxima = iteraciones[i+1]
                    if proxima['a'] == c:
                        st.info(f"Como $f(a) \cdot f(c) > 0$, la raíz está en $[c, b]$. Nuevo intervalo: $[{proxima['a']:.8f}, {proxima['b']:.8f}]$")
                    else:
                        st.info(f"Como $f(a) \cdot f(c) < 0$, la raíz está en $[a, c]$. Nuevo intervalo: $[{proxima['a']:.8f}, {proxima['b']:.8f}]$")
                st.markdown("---")

        # Preparación de datos para tabla
        for it in iteraciones:
            it["Ci+1"] = it["Ci"]
            it["f(a)"] = evaluar_seguro(f_num, it["a"])
            it["f(b)"] = evaluar_seguro(f_num, it["b"])

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
        df = pd.DataFrame(iteraciones_visibles)
        
        st.subheader("Tabla de Iteraciones")
        st.dataframe(df.style.format(fmt))

        st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci']:.8f}")

        # Gráfica
        st.subheader("Visualización del Método")
        fig = graficar_metodo_cerrado(f_num, iteraciones_visibles, "Convergencia: Bisección")
        st.pyplot(fig)

        excel_bytes = exportar_excel_biseccion(df, f_num, iteraciones_visibles)
        st.download_button(label="📊 Descargar Excel", data=excel_bytes, file_name="Biseccion.xlsx")