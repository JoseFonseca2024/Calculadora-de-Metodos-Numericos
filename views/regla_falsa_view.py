import streamlit as st
import pandas as pd
import re

from utils.funciones import validar_y_preparar_funcion
from utils.formateo import fmt
from metodos.regla_falsa import ejecutar_regla_falsa
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_metodo_cerrado
from Services.exportar_excel import exportar_excel_regla_falsa
from utils.evaluacion_segura import evaluar_seguro


def mostrar_regla_falsa():
    st.title("Método de la Regla Falsa")
    st.markdown("Este método utiliza interpolación lineal para aproximar la raíz en un intervalo cerrado.")

    # 🔹 Entrada
    funcion_str = st.text_input(
        "Introduzca una función f(x):",
        placeholder="Ej: e^-x - x"
    )

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Límite inferior (a):", value=0.0, format="%.6f")
    with col2:
        b = st.number_input("Límite superior (b):", value=1.0, format="%.6f")

    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.6f")

    if st.button("Calcular"):

        # 🔹 1. Validación
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(f"Error: {error_msg}")
            return

        _, _, f_num, _, texto_visual = datos

        # 🔹 Mostrar función
        st.subheader("Función analizada:")
        f_rep = texto_visual.replace("**", "^")
        f_render = re.sub(r'\^([\-\+]?[a-zA-Z0-9\(\)]+)', r'^{\1}', f_rep)
        f_render = f_render.replace("*", "")
        st.latex(f"f(x) = {f_render}")

        # 🔹 2. Verificación de raíz
        fa_init = evaluar_seguro(f_num, a)
        fb_init = evaluar_seguro(f_num, b)

        if fa_init is None or fb_init is None:
            st.error("La función no se puede evaluar en el intervalo.")
            return

        st.subheader("Verificación de existencia de raíz")
        st.latex(f"f(a) = f({a:.4f}) = {fa_init:.6f}")
        st.latex(f"f(b) = f({b:.4f}) = {fb_init:.6f}")

        if fa_init * fb_init > 0:
            st.error("No hay cambio de signo en el intervalo.")
            return
        else:
            st.success(r"Existe al menos una raíz en el intervalo ($f(a)\cdot f(b) < 0$)")

        # 🔹 3. Ejecutar método
        ok, msg, iteraciones = ejecutar_regla_falsa(f_num, a, b, tol)

        if not ok:
            st.error(msg)
            return

        # 🔹 4. Procedimiento
        st.subheader("Procedimiento Paso a Paso")
        with st.expander("Ver cálculos detallados", expanded=False):

            for it in iteraciones:
                st.write(f"#### Iteración {it['i']}")

                st.latex(
                    rf"c_{{{it['i']}}} = {it['b']:.6f} - "
                    rf"\frac{{({it['f(b)']:.6f})({it['a']:.6f} - {it['b']:.6f})}}"
                    rf"{{({it['f(a)']:.6f}) - ({it['f(b)']:.6f})}}"
                )

                st.latex(rf"c_{{{it['i']}}} = {it['Ci']:.6f}")
                st.latex(rf"f(c_{{{it['i']}}}) = {it['f(Ci)']:.6f}")

                if it["Error%"] is not None:
                    st.latex(rf"Error = {it['Error%']:.6f}\%")

                st.markdown("---")

        # 🔹 5. Tabla
        for it in iteraciones:
            it["Ci+1"] = it["Ci"]
            it["f(a)"] = evaluar_seguro(f_num, it["a"])
            it["f(b)"] = evaluar_seguro(f_num, it["b"])

        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
        df = pd.DataFrame(iteraciones_visibles)

        st.subheader("Tabla de Iteraciones")
        st.dataframe(df.style.format({
            "a": fmt,
            "b": fmt,
            "f(a)": fmt,
            "f(b)": fmt,
            "Ci": fmt,
            "f(Ci)": fmt,
            "Error%": fmt
        }))

        # 🔹 6. Resultado
        st.success(f"Raíz aproximada: {iteraciones_visibles[-1]['Ci']:.6f}")

        # 🔹 7. Gráfica
        st.subheader("Visualización del Método")
        fig = graficar_metodo_cerrado(
            f_num,
            iteraciones_visibles,
            "Convergencia: Regla Falsa"
        )
        st.pyplot(fig)

        # 🔹 8. Exportar
        excel_bytes = exportar_excel_regla_falsa(
            df,
            f_num,
            iteraciones_visibles
        )

        st.download_button(
            "📊 Descargar Excel",
            excel_bytes,
            "Regla_Falsa.xlsx"
        )