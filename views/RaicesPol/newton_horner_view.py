import streamlit as st
import pandas as pd
import sympy as sp

from utils.polinomios import validar_y_preparar_polinomio

from metodos.Polinomios_y_Funciones.newton_horner import ejecutar_newton_horner

from plot.graficas import graficar_newton_horner

from Services.exportar_excel import exportar_excel_newton_horner

from Services.procesamiento import filtrar_iteraciones


def mostrar_newton_horner():

    st.title("Método de Newton-Horner")

    st.markdown("""
    Este método utiliza Horner para evaluar el polinomio
    y Newton-Raphson para aproximar raíces.
    """)

    polinomio_str = st.text_input(
        "Introduzca P(x):",
        placeholder="Ej: x^3 - 6x^2 + 11x - 6"
    )

    col1, col2 = st.columns(2)

    with col1:

        Ci = st.number_input(
            "Valor inicial C₀:",
            value=1.0,
            format="%.6f"
        )

    with col2:

        tol = st.number_input(
            "Tolerancia (%)",
            value=0.0001,
            format="%.6f"
        )

    if st.button("Calcular"):

        valido, error_msg, datos = validar_y_preparar_polinomio(
            polinomio_str
        )

        if not valido:

            st.error(error_msg)

            return

        p_sym, x, grado, coeficientes, p_num, p_visual = datos

        ok, msg, iteraciones = ejecutar_newton_horner(
            coeficientes,
            Ci,
            tol
        )

        if not ok:

            st.error(msg)

            return

        # ==========================================
        # INFORMACION GENERAL
        # ==========================================

        st.subheader("Polinomio")

        st.latex(
            f"P(x) = {p_visual}"
        )

        st.write(
            f"Grado detectado: {grado}"
        )

        # ==========================================
        # PROCEDIMIENTO
        # ==========================================

        with st.expander(
            "Ver procedimiento detallado paso a paso",
            expanded=False
        ):

            mostrar_horner = True

            for it in iteraciones:

                idx = it["i"]

                st.markdown(
                    f"# Iteración {idx + 1}"
                )

                # ==========================================
                # VALOR ACTUAL
                # ==========================================

                st.write(
                    "## 1. Valor actual de la raíz"
                )

                st.latex(
                    f"C_{{{idx}}} = {it['Ci']:.8f}"
                )

                if mostrar_horner: 

                    # ==========================================
                    # COEFICIENTES
                    # ==========================================

                    st.write(
                        "## 2. Coeficientes del polinomio"
                    )

                    coeficientes_actuales = it["coeficientes"]

                    grado_coef = grado

                    for j in range(len(coeficientes_actuales)):

                        subindice = grado_coef - j

                        st.latex(
                            f"A_{{{subindice}}} = "
                            f"{coeficientes_actuales[j]:.8f}"
                        )

                    # ==========================================
                    # HORNER
                    # ==========================================

                    st.write(
                        "## 3. División sintética de Horner"
                    )

                    b = it["b"]

                    grado_actual = grado

                    for j in range(len(b)):

                        subindice = grado_actual - j

                        if j == 0:

                            st.latex(
                                f"b_{{{subindice}}} = "
                                f"A_{{{subindice}}} = "
                                f"{b[j]:.8f}"
                            )

                        else:

                            coef_actual = it["coeficientes"][j]

                            anterior_subindice = (
                                grado_actual - (j - 1)
                            )

                            anterior = b[j - 1]

                            st.latex(
                                f"b_{{{subindice}}} = "
                                f"A_{{{subindice}}} + "
                                f"({it['Ci']:.8f})"
                                f"(b_{{{anterior_subindice}}})"
                            )

                            st.latex(
                                f"b_{{{subindice}}} = "
                                f"{coef_actual:.8f} + "
                                f"({it['Ci']:.8f})"
                                f"({anterior:.8f})"
                            )

                            st.latex(
                                f"b_{{{subindice}}} = "
                                f"{b[j]:.8f}"
                            )

                    # ==========================================
                    # EVALUAR P(C)
                    # ==========================================

                    st.write(
                        "## 4. Evaluación de la raíz en P(x)"
                    )

                    expr_original = sp.expand(p_sym)

                    st.latex(
                        f"P(x) = {sp.latex(expr_original)}"
                    )
                   ## expr_sustituida = expr_original.subs( x, it["Ci"] )
                    st.latex(
                        f"P({it['Ci']:.8f}) = " f"{it['Funcion']:.8f}"
                    )

                    st.latex(
                        f"Residuo = b_0 = " f"{it['Residuo']:.8f}"
                    )

                    # ==========================================
                    # Q(X)
                    # ==========================================

                    st.write(
                        "## 5. Construcción de Q(x)"
                    )

                    q_coef = b[:-1]

                    partes_q = []

                    grado_q = grado - 1

                    for j in range(len(q_coef)):

                        coef = q_coef[j]

                        exponente = grado_q - j

                        if exponente > 1:

                            partes_q.append(
                                f"({coef:.8f})x^{exponente}"
                            )

                        elif exponente == 1:

                            partes_q.append(
                                f"({coef:.8f})x"
                            )

                        else:

                            partes_q.append(
                                f"({coef:.8f})"
                            )

                    q_string = " + ".join(partes_q)

                    st.latex(
                        f"Q(x) = {q_string}"
                    )

                    # ==========================================
                    # DERIVADA ORIGINAL
                    # ==========================================

                    st.write(
                        "## 6. Primera derivada de P(x)"
                    )

                    derivada_expr = sp.diff(
                        p_sym,
                        x
                    )

                    st.latex(
                        f"P'(x) = "
                        f"{sp.latex(derivada_expr)}"
                    )

                    # ==========================================
                    # EVALUAR Q(C)
                    # ==========================================

                    st.write(
                        "## 7. Evaluar Q(C)"
                    )

                    xq = sp.Symbol("x")

                    q_expr = 0

                    grado_q = grado - 1

                    for j in range(len(q_coef)):

                        q_expr += q_coef[j] * xq**(grado_q - j)

                    st.latex(
                        f"Q(x) = {sp.latex(q_expr)}"
                    )

                    q_eval = q_expr.subs(
                        xq,
                        it["Ci"]
                    )

                    st.latex(
                        f"Q({it['Ci']:.8f}) = "
                        f"{sp.latex(q_eval)}"
                    )

                    st.latex(
                        f"Q({it['Ci']:.8f}) = "
                        f"{it['Derivada']:.8f}"
                    )



                    # ==========================================
                    # EVALUAR P'(C)
                    # ==========================================

                    
                    st.write(
                        "## 8. Evaluar P'(C)"
                    )

                    st.latex(
                        f"P'(x) = {sp.latex(derivada_expr)}"
                    )

                    derivada_sustituida = derivada_expr.subs(
                        x,
                        it["Ci"]
                    )

                    st.latex(
                        f"P'({it['Ci']:.8f}) = "
                        f"{sp.latex(derivada_sustituida)}"
                    )

                    derivada_real = float(
                        derivada_sustituida
                    )

                    st.latex(
                        f"P'({it['Ci']:.8f}) = "
                        f"{derivada_real:.8f}"
                    )



                    # ==========================================
                    # VERIFICACION
                    # ==========================================

                    st.write(
                        "## 9. Verificación"
                    )

                    st.latex(
                        f"Q({it['Ci']:.8f}) = "
                        f"P'({it['Ci']:.8f})"
                    )

                    st.latex(
                        f"{it['Derivada']:.8f} = "
                        f"{float(derivada_real):.8f}"
                    )

                mostrar_horner = False
                # ==========================================
                # NEWTON-RAPHSON
                # ==========================================

                st.write(
                    "## 10. Newton-Raphson"
                )

                st.latex(
                    r"C_{i+1}=C_i-\frac{P(C_i)}{P'(C_i)}"
                )

                st.latex(
                    f"C_{{{idx+1}}} = "
                    f"{it['Ci']:.8f} - "
                    f"\\frac{{{it['Funcion']:.8f}}}"
                    f"{{{it['Derivada']:.8f}}}"
                )

                st.latex(
                    f"C_{{{idx+1}}} = "
                    f"{it['Ci+1']:.8f}"
                )

                # ==========================================
                # ERROR
                # ==========================================

                st.write(
                    "## 11. Error porcentual"
                )

                st.latex(
                    f"Error = "
                    f"{it['Error%']:.8f}\\%"
                )

                st.markdown("---")

        # ==========================================
        # TABLA
        # ==========================================

        iteraciones_visibles = filtrar_iteraciones(
            iteraciones,
            tol
        )

        st.subheader(
            "Tabla de Iteraciones"
        )

        df_mostrar = pd.DataFrame(
            iteraciones_visibles
        )

        df_excel = df_mostrar.copy()

        for columna in df_excel.columns:

            df_excel[columna] = df_excel[columna].apply(
                lambda x: str(x) if isinstance(x, list) else x
            )

        st.dataframe(
            df_mostrar
        )

        # ==========================================
        # RESULTADO FINAL
        # ==========================================

        raiz_final = iteraciones_visibles[-1]["Ci+1"]

        st.success(
            f"Raíz aproximada: "
            f"{raiz_final}"
        )

        # ==========================================
        # GRAFICA
        # ==========================================

        st.subheader(
            "Visualización del Método"
        )

        fig = graficar_newton_horner(
            p_num,
            iteraciones_visibles
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================================
        # EXPORTAR EXCEL
        # ==========================================

        excel_bytes = exportar_excel_newton_horner(
            df_excel,
             p_num,
            iteraciones_visibles
        )

        st.download_button(
            label="📊 Descargar Excel",
            data=excel_bytes,
            file_name="Reporte_Newton_Horner.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
