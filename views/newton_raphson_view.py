import streamlit as st
import sympy as sp
import pandas as pd

from utils.funciones import validar_y_preparar_funcion
from utils.formateo import fmt
from metodos.newton_raphson import ejecutar_newton_raphson
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_newton
from Services.exportar_excel import exportar_excel_newton

def mostrar_newton_raphson():
    st.title("Metodo Newton-Raphson")

    funcion_str = st.text_input(
        "Introduzca una función f(x):",
        placeholder="Ej: x² - 4x - 12"
    )

    C0 = st.number_input("Valor inicial (C₀):", value=0.0, format="%.6f")

    tol = st.number_input("Tolerancia (%)", value=0.01, format="%.6f")

    if st.button("Calcular"):

        valido, error, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error)
            return

        funcion, derivada, f, f_deriv = datos

        st.subheader("Función insertada:")
        st.latex(sp.latex(funcion))
        st.subheader("Derivada:")
        st.latex(sp.latex(derivada))

        ok, msg, iteraciones = ejecutar_newton_raphson(f, f_deriv, C0, tol)

        if not ok:
            st.error(msg)
            return

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)

        # Paso a paso
        st.subheader("Cálculo paso a paso")
        for it in iteraciones_visibles:
            Ci = fmt(it["Ci"])
            fCi = fmt(it["f(Ci)"])
            fDeriv = fmt(it["f'(Ci)"])
            Ci_next = fmt(it["Ci+1"])

            st.latex(
                fr"C_{{{it['i']+1}}} = {Ci} - \frac{{{fCi}}}{{{fDeriv}}} = {Ci_next}"
            )
        # Tabla
        st.subheader("Tabla")
        df = pd.DataFrame(iteraciones_visibles)

        st.dataframe(
            df.style.format({
                "Ci": fmt,
                "f(Ci)": fmt,
                "f'(Ci)": fmt,
                "Ci+1": fmt,
                "Error%": fmt
            })
        )

        # Resultado
        raiz = iteraciones_visibles[-1]["Ci+1"]
        st.success(f"Raíz aproximada: {raiz:.6f}")

        # Gráfica
        st.subheader("Gráfica")
        fig = graficar_newton(f, iteraciones_visibles)
        st.pyplot(fig)

        excel_bytes = exportar_excel_newton(df, f, iteraciones_visibles)

        st.download_button(
                label="📊 Descargar Excel con Gráfico Nativo",
                data=excel_bytes,
                file_name="Metodo_Newton_Raphson.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    