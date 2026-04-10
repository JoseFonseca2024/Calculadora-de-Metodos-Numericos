import streamlit as st
import sympy as sp
import pandas as pd

from utils.formateo import fmt
from utils.funciones import validar_y_preparar_funcion
from metodos.secante import ejecutar_secante
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_secante
from Services.exportar_excel import exportar_excel_secante

def mostrar_secante():
    st.title("Metodo de la Secante")
        
    funcion_str = st.text_input(
        "Introduzca una función f(x):",
        placeholder="Ej: x² - 4x - 12"
    )

    C0 = st.number_input("Valor inicial (C₀):", value=0.0, format="%.6f")

    C_1 = st.number_input("Valor inicial (C-₁):", value=0.0, format="%.6f")

    tol = st.number_input("Tolerancia (%)", value=0.01, format="%.6f")

    if st.button("Calcular"):

        valido, error, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error)
            return
        
        funcion, _, f, _ = datos

        st.subheader("Función insertada:")
        st.latex(sp.latex(funcion))

        ok, msg, iteraciones = ejecutar_secante(f, C0, C_1, tol)

        if not ok:
            st.error(msg)
            return
        
        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)

        # Paso a paso
        st.subheader("Cálculo paso a paso")
        for it in iteraciones_visibles:
            Ci = fmt(it["Ci"])
            Ci_1 = fmt(it["Ci-1"])
            fCi = fmt(it["f(Ci)"])
            fCi_1 = fmt(it["f(Ci-1)"])
            Ci_next = fmt(it["Ci+1"])

            st.latex(
                fr"C_{{{it['i']+1}}} = {Ci} - \frac{{{fCi}({Ci} - {Ci_1})}}{{{fCi} - {fCi_1}}} = {Ci_next}"
            )
        # Tabla
        st.subheader("Tabla")
        df = pd.DataFrame(iteraciones_visibles)

        st.dataframe(
            df.style.format({
                "Ci": fmt,
                "Ci-1": fmt,
                "f(Ci)": fmt,
                "f(Ci-1)": fmt,
                "Ci+1": fmt,
                "Error%": fmt
            })
        )

        # Resultado
        raiz = iteraciones_visibles[-1]["Ci+1"]
        st.success(f"Raíz aproximada: {raiz:.6f}")

        #Grafica
        st.subheader("Grafica")
        fig = graficar_secante(f, iteraciones_visibles)
        st.pyplot(fig)

        excel_bytes = exportar_excel_secante(df, f, iteraciones_visibles)

        st.download_button(
                label="📊 Descargar Excel con Gráfico Nativo",
                data=excel_bytes,
                file_name="Metodo_Secante.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

