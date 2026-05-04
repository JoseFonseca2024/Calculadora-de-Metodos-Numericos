import streamlit as st
import pandas as pd
import math
import sympy as sp

from metodos.taylor import ejecutar_taylor
from utils.funciones import validar_y_preparar_funcion
from plot.graficas import graficar_taylor
from Services.exportar_excel import exportar_excel_taylor


def mostrar_taylor():
    st.title("Serie de Taylor - Reporte Académico")
    st.markdown("Calcula el polinomio de aproximación y el error mediante el desarrollo de Taylor.")

    funcion_str = st.text_input("Introduzca una función f(x):", placeholder="Ej: e^x")

    col1, col2, col3 = st.columns(3)

    with col1:
        a = st.number_input("Punto de expansión (a):", value=0.0, format="%.4f")

    with col2:
        n_max = st.number_input("Grado máximo (n)", min_value=0, max_value=20, value=0)

    with col3:
        x_eval = st.number_input("Valor a evaluar (x)", value=0.0, format="%.4f")

    tol = st.number_input("Tolerancia (Epsilon)", value=0.0001, format="%.8f")

    if st.button("Calcular Desarrollo Detallado"):

        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error_msg)
            return

        f_sym, x, f_num, f_deriv, f_visual = datos

        ok, msg, res = ejecutar_taylor(f_sym, x, a, n_max, x_eval)

        if not ok:
            st.error(msg)
            return

        st.success("✅ Desarrollo generado exitosamente")

        # 🔹 Función
        st.subheader("Función analizada")
        st.latex(f"f(x) = {sp.latex(f_sym)}")

        # =====================================================
        # PROCEDIMIENTO PASO A PASO
        # =====================================================
        st.subheader("1. Procedimiento y Construcción")

        polinomio_acumulado = ""

        for i, it in enumerate(res["iteraciones"]):

            with st.expander(f"Paso para grado n = {i}", expanded=(i == 0)):

                derivada_sym = it["derivada_sym"]

                # 🔹 1. Derivada simbólica
                st.markdown("**Derivada:**")
                st.latex(rf"f^{{({i})}}(x) = {sp.latex(derivada_sym)}")

                # 🔹 2. Sustitución
                st.markdown("**Evaluando en a:**")
                derivada_sust = sp.latex(derivada_sym).replace("x", f"({a})")
                st.latex(rf"f^{{({i})}}({a}) = {derivada_sust}")

                # 🔹 3. Resultado numérico
                st.latex(rf"f^{{({i})}}({a}) = {it['f^(i)(a)']:.8f}")

                # 🔹 4. Construcción del término
                fact = math.factorial(i)
                distancia = x_eval - a

                st.markdown("**Construcción del término:**")
                st.latex(
                    rf"T_{{{i}}} = \frac{{{it['f^(i)(a)']:.8f}}}{{{fact}}} ({distancia:.4f})^{{{i}}}"
                )

                # 🔹 5. Resultado término
                st.latex(rf"T_{{{i}}} = {it['Termino']}")

                # 🔹 6. Polinomio acumulado
                term_str = str(it["Termino"])

                if i == 0:
                    polinomio_acumulado = term_str
                else:
                    signo = " + " if not term_str.startswith("-") else " "
                    polinomio_acumulado += f"{signo}{term_str}"

                st.markdown("**Polinomio acumulado:**")
                st.latex(rf"P_{{{i}}}(x) = {polinomio_acumulado}")

        # =====================================================
        # TABLA
        # =====================================================
        st.subheader("2. Tabla de Aproximaciones")

        data_tabla = []

        for it in res["iteraciones"]:
            cumple = "CUMPLE" if it["Error_Abs"] < tol else "NO CUMPLE"

            data_tabla.append({
                "Grado (n)": it["i"],
                "Aproximación Pn(x)": it["Aproximacion"],
                "Error (Rn)": it["Error_Abs"],
                "Decisión": cumple
            })

        df_final = pd.DataFrame(data_tabla)

        st.dataframe(
            df_final.style.format({
                "Aproximación Pn(x)": "{:.8f}",
                "Error (Rn)": "{:.8f}"
            }).map(
                lambda v: 'background-color: #d4edda' if v == "CUMPLE" else 'background-color: #f8d7da',
                subset=["Decisión"]
            ),
            use_container_width=True
        )

        # =====================================================
        # GRÁFICA
        # =====================================================
        st.subheader("3. Comportamiento Gráfico")
        st.pyplot(graficar_taylor(f_num, res["poly_func_num"], x_eval, a))

        # =====================================================
        # EXPORTAR
        # =====================================================
        df_excel = df_final.rename(columns={
            "Grado (n)": "i",
            "Aproximación Pn(x)": "aprox",
            "Error (Rn)": "error",
            "Decisión": "decision"
        })

        excel_bytes = exportar_excel_taylor(
            df_excel,
            f_num,
            res["poly_func_num"],
            x_eval,
            a
        )

        st.download_button(
            "📥 Descargar Reporte Excel",
            excel_bytes,
            "Taylor.xlsx",
            use_container_width=True
        )