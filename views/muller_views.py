import streamlit as st
import cmath
import pandas as pd
from utils.polinomios import validar_y_preparar_polinomio
from metodos.muller import ejecutar_muller
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_muller
from Services.exportar_excel import exportar_excel_muller


def mostrar_muller():

    st.title("Método de Muller")

    st.markdown("""
    Este método encuentra raíces mediante una aproximación parabólica
    a través de tres puntos.

    Es ideal para encontrar raíces reales y complejas.
    """)

    polinomio_str = st.text_input(
        "Introduzca P(x):",
        placeholder="Ej: x^3 - x - 1"
    )

    st.subheader("Intervalo de búsqueda")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input(
            "Límite inferior (a):",
            value=0.0,
            format="%.4f"
        )

    with col2:
        b = st.number_input(
            "Límite superior (b):",
            value=2.0,
            format="%.4f"
        )

    tol = st.number_input(
        "Tolerancia (%)",
        value=0.00001,
        format="%.5f"
    )

    if st.button("Calcular"):

        # =========================================================
        # VALIDACIÓN
        # =========================================================

        valido, error_msg, datos = validar_y_preparar_polinomio(
            polinomio_str
        )

        if not valido:
            st.error(error_msg)
            return

        _, _, _, _, f_num, f_visual = datos

        # =========================================================
        # PUNTOS INICIALES
        # =========================================================

        x0 = a
        x1 = (a + b) / 2
        x2 = b

        st.subheader("Puntos iniciales generados automáticamente")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.latex(f"x_0 = {x0:.6f}")

        with col_b:
            st.latex(f"x_1 = {x1:.6f}")

        with col_c:
            st.latex(f"x_2 = {x2:.6f}")

        # =========================================================
        # EJECUTAR MÉTODO
        # =========================================================

        ok, msg, iteraciones = ejecutar_muller(
            f_num,
            x0,
            x1,
            x2,
            tol
        )

        if not ok:
            st.error(msg)
            return

        # =========================================================
        # FUNCIÓN
        # =========================================================

        st.subheader("Polinimio:")
        st.latex(f"P(x) = {f_visual}")

        # =========================================================
        # EVALUACIÓN INICIAL
        # =========================================================

        st.subheader("Evaluación inicial")

        f_x0 = f_num(x0)
        f_x1 = f_num(x1)
        f_x2 = f_num(x2)

        func_x0 = (
            f_visual.replace("x", f"({x0:.6f})")
        )

        func_x1 = (
            f_visual.replace("x", f"({x1:.6f})")
        )

        func_x2 = (
            f_visual.replace("x", f"({x2:.6f})")
        )

        # =====================================================
        # f(x0)
        # =====================================================

        st.latex(r"P(x_0)")

        st.latex(
            f"= {func_x0}"
        )

        st.latex(
            f"= {f_x0:.8f}"
        )

        # =====================================================
        # f(x1)
        # =====================================================

        st.latex(r"P(x_1)")

        st.latex(
            f"= {func_x1}"
        )

        st.latex(
            f"= {f_x1:.8f}"
        )

        # =====================================================
        # f(x2)
        # =====================================================

        st.latex(r"P(x_2)")

        st.latex(
            f"= {func_x2}"
        )

        st.latex(
            f"= {f_x2:.8f}"
        )

        # =========================================================
        # PROCEDIMIENTO
        # =========================================================

        with st.expander(
            "Ver procedimiento detallado paso a paso",
            expanded=False
        ):

            for it in iteraciones:

                idx = it["i"]

                st.markdown(f"## Iteración {idx+1}")

                x0 = it["x0"]
                x1 = it["x1"]
                x2 = it["x2"]

                fx0 = it["f(x0)"]
                fx1 = it["f(x1)"]
                fx2 = it["f(x2)"]

                x3 = it["x3"]

                a_coef = it["a"]
                b_coef = it["b"]
                c_coef = it["c"]

                # =====================================================
                # PASO 1
                # =====================================================

                st.write("### 1. Valores iniciales")

                st.latex(
                    f"x_0 = {x0:.8f}, \\quad "
                    f"x_1 = {x1:.8f}, \\quad "
                    f"x_2 = {x2:.8f}"
                )

                st.latex(
                    f"P(x_0) = {fx0:.8f}, \\quad "
                    f"P(x_1) = {fx1:.8f}, \\quad "
                    f"P(x_2) = {fx2:.8f}"
                )

                # =====================================================
                # PASO 2
                # =====================================================

                h1 = x1 - x0
                h2 = x2 - x1

                d1 = (fx1 - fx0) / h1
                d2 = (fx2 - fx1) / h2

                st.write("### 2. Diferencias y pendientes")

                st.latex(r"h_1 = x_1 - x_0")

                st.latex(
                    f"h_1 = {x1:.8f} - ({x0:.8f})"
                )

                st.latex(
                    f"h_1 = {h1:.8f}"
                )

                st.latex(r"h_2 = x_2 - x_1")

                st.latex(
                    f"h_2 = {x2:.8f} - ({x1:.8f})"
                )

                st.latex(
                    f"h_2 = {h2:.8f}"
                )

                st.latex(
                    r"d_1 = \frac{P(x_1)-P(x_0)}{h_1}"
                )

                st.latex(
                    f"d_1 = "
                    f"\\frac{{{fx1:.8f}-({fx0:.8f})}}"
                    f"{{{h1:.8f}}}"
                )

                st.latex(
                    f"d_1 = {d1:.8f}"
                )

                st.latex(
                    r"d_2 = \frac{P(x_2)-P(x_1)}{h_2}"
                )

                st.latex(
                    f"d_2 = "
                    f"\\frac{{{fx2:.8f}-({fx1:.8f})}}"
                    f"{{{h2:.8f}}}"
                )

                st.latex(
                    f"d_2 = {d2:.8f}"
                )

                # =====================================================
                # PASO 3
                # =====================================================

                st.write("### 3. Coeficientes de la parábola")

                st.latex(
                    r"a = \frac{d_2-d_1}{h_2+h_1}"
                )

                st.latex(
                    f"a = "
                    f"\\frac{{{d2:.8f}-({d1:.8f})}}"
                    f"{{{h2:.8f}+{h1:.8f}}}"
                )

                st.latex(
                    f"a = {a_coef:.8f}"
                )

                st.latex(
                    r"b = ah_2+d_2"
                )

                st.latex(
                    f"b = "
                    f"({a_coef:.8f})"
                    f"({h2:.8f})"
                    f"+({d2:.8f})"
                )

                st.latex(
                    f"b = {b_coef:.8f}"
                )

                st.latex(
                    r"c = f(x_2)"
                )

                st.latex(
                    f"c = {fx2:.8f}"
                )

                # PASO 4

                st.write("### 4. Fórmula de Muller")

                st.latex(
                    r"x_3 = x_2 + \frac{-2c}{b \pm \sqrt{b^2-4ac}}"
                )

                # DISCRIMINANTE

                discriminante = (
                    b_coef**2 - 4*a_coef*c_coef
                )

                sqrt_disc = cmath.sqrt(discriminante)

                st.write("### 4.1 Discriminante")

                st.latex(
                    r"\Delta = b^2 - 4ac"
                )

                st.latex(
                    f"\\Delta = "
                    f"({b_coef:.8f})^2 "
                    f"-4({a_coef:.8f})({c_coef:.8f})"
                )

                st.latex(
                    f"\\Delta = {discriminante:.8f}"
                )

                # RAÍZ DEL DISCRIMINANTE

                if isinstance(sqrt_disc, complex):
                    # Si la parte imaginaria es prácticamente 0
                    if abs(sqrt_disc.imag) < 1e-12:

                        sqrt_disc = sqrt_disc.real
                        sqrt_text = f"{sqrt_disc:.8f}"

                    else:

                        signo_sqrt = (
                            "+"
                            if sqrt_disc.imag >= 0
                            else "-"
                        )

                        sqrt_text = (
                            f"{sqrt_disc.real:.8f}"
                            f"{signo_sqrt}"
                            f"{abs(sqrt_disc.imag):.8f}i"
                        )

                else:

                    sqrt_text = f"{sqrt_disc:.8f}"

                st.write("### 4.2 Raíz del discriminante")

                st.latex(
                    r"\sqrt{\Delta}"
                )

                st.latex(
                    f"\\sqrt{{{discriminante:.8f}}}"
                )

                st.latex(
                    f"= {sqrt_text}"
                )

                # DENOMINADORES
                den1 = b_coef + sqrt_disc
                den2 = b_coef - sqrt_disc

                if isinstance(den1, complex):

                    signo_den1 = (
                        "+"
                        if den1.imag >= 0
                        else "-"
                    )

                    den1_text = (
                        f"{den1.real:.8f}"
                        f"{signo_den1}"
                        f"{abs(den1.imag):.8f}i"
                    )

                else:

                    den1_text = f"{den1:.8f}"

                if isinstance(den2, complex):

                    signo_den2 = (
                        "+"
                        if den2.imag >= 0
                        else "-"
                    )

                    den2_text = (
                        f"{den2.real:.8f}"
                        f"{signo_den2}"
                        f"{abs(den2.imag):.8f}i"
                    )

                else:

                    den2_text = f"{den2:.8f}"

                st.write("### 4.3 Denominadores")

                st.latex(
                    r"D_1 = b + \sqrt{\Delta}"
                )

                st.latex(
                    f"D_1 = "
                    f"({b_coef:.8f}) + ({sqrt_text})"
                )

                st.latex(
                    f"D_1 = {den1_text}"
                )

                st.latex(
                    r"D_2 = b - \sqrt{\Delta}"
                )

                st.latex(
                    f"D_2 = "
                    f"({b_coef:.8f}) - ({sqrt_text})"
                )

                st.latex(
                    f"D_2 = {den2_text}"
                )

                # =====================================================
                # SELECCIÓN
                # =====================================================
                den_usado_text = (
                    den1_text
                    if abs(den1) > abs(den2)
                    else den2_text
                )

                st.write("### 4.4 Selección del denominador")

                st.latex(
                    f"|D_1| = {abs(den1):.8f}"
                )

                st.latex(
                    f"|D_2| = {abs(den2):.8f}"
                )

                st.latex(
                    f"D = {den_usado_text}"
                )

                # =====================================================
                # SUSTITUCIÓN FINAL
                # =====================================================

                st.write("### 4.5 Sustitución en la fórmula")

                st.latex(
                    r"x_3 = x_2 + \frac{-2c}{D}"
                )

                st.latex(
                    f"x_3 = "
                    f"{x2:.8f}"
                    f"+"
                    f"\\frac{{-2({c_coef:.8f})}}"
                    f"{{{den_usado_text}}}"
                )

                st.latex(
                    f"x_3 = {x3}"
                )
                # =====================================================
                # RESULTADO
                # =====================================================

                st.write("### 5. Resultado")

                if isinstance(x3, complex):

                    signo = (
                        "+"
                        if x3.imag >= 0
                        else "-"
                    )

                    st.latex(
                        f"x_3 = "
                        f"{x3.real:.8f}"
                        f"{signo}"
                        f"{abs(x3.imag):.8f}i"
                    )

                else:

                    st.latex(
                        f"x_3 = {x3:.8f}"
                    )

                st.latex(
                    f"Error = {it['Error%']:.8f}\\%"
                )

                st.divider()

        # =========================================================
        # TABLA
        # =========================================================

        iteraciones_visibles = filtrar_iteraciones(
            iteraciones,
            tol
        )

        st.subheader("Tabla de Iteraciones")

        df_mostrar = pd.DataFrame(
            iteraciones_visibles
        )

        st.dataframe(df_mostrar)

        # =========================================================
        # RESULTADO FINAL
        # =========================================================

        raiz_final = iteraciones_visibles[-1]["x3"]

        st.success(
            f"Raíz aproximada: {raiz_final}"
        )

        # =========================================================
        # GRÁFICA
        # =========================================================

        st.subheader("Visualización del Método")

        fig = graficar_muller(
            f_num,
            iteraciones_visibles
        )

        st.plotly_chart(fig, use_container_width=True)

        # =========================================================
        # EXPORTAR EXCEL
        # =========================================================

        excel_bytes = exportar_excel_muller(
            df_mostrar,
            f_num,
            iteraciones_visibles
        )

        st.download_button(
            label="📊 Descargar Excel",
            data=excel_bytes,
            file_name="Reporte_Muller.xlsx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )