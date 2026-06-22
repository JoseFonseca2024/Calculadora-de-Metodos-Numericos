import streamlit as st
import sympy as sp
import pandas as pd

from utils.funciones_integrales import validar_y_preparar_funcion_integral
from metodos.Integrales.Simpson3_8 import ejecutarSimpson38
from utils.Decimales import formatear_numero


def mostrarSimpson3_8():

    st.title(
        "Regla de Simpson 3/8"
    )

    # ==========================================
    # FUNCIÓN
    # ==========================================

    funcion_str = st.text_input(
        "Introduzca la función a integrar",
        placeholder="Ej: x^2 - 10*cos(x) - 2"
    )

    # ==========================================
    # TIPO DE INTEGRAL
    # ==========================================

    tipo_integral = st.radio(
        "Tipo de integral",
        [
            "Integral simple",
            "Integral doble"
        ],
        horizontal=True
    )

    st.divider()

    # ==========================================
    # INTEGRAL SIMPLE
    # ==========================================

    if tipo_integral == "Integral simple":

        st.subheader(
            "Límites de integración"
        )

        col1, col2 = st.columns(2)

        with col1:

            a = st.number_input(
                "Límite inferior (a)",
                value=0.0
            )

        with col2:

            b = st.number_input(
                "Límite superior (b)",
                value=1.0
            )

    # ==========================================
    # INTEGRAL DOBLE
    # ==========================================

    else:

        st.subheader(
            "Límites de integración"
        )

        st.markdown(
            "### Integral interna (Variable y)"
        )

        col1, col2 = st.columns(2)

        with col1:

            ay = st.number_input(
                "Límite inferior de y",
                value=0.0
            )

        with col2:

            by = st.number_input(
                "Límite superior de y",
                value=1.0
            )

        st.markdown(
            "### Integral externa (Variable x)"
        )

        col3, col4 = st.columns(2)

        with col3:

            ax = st.number_input(
                "Límite inferior de x",
                value=0.0
            )

        with col4:

            bx = st.number_input(
                "Límite superior de x",
                value=1.0
            )

    # ==========================================
    # SUBINTERVALOS
    # ==========================================

    n = st.number_input(
        "Número de subintervalos (n)",
        min_value=1,
        value=4
    )

    st.divider()

    # ==========================================
    # CALCULAR
    # ==========================================

    if st.button(
        "Calcular",
        use_container_width=True
    ):

        valido, error_msg, datos = (
            validar_y_preparar_funcion_integral(
                funcion_str
            )
        )

        if not valido:

            st.error(error_msg)
            return

        f_sym, _, _, f_visual = datos

        st.subheader(
            "Integral a aproximar"
        )

        # ======================================
        # INTEGRAL SIMPLE
        # ======================================

        if tipo_integral == "Integral simple":

            st.latex(
                rf"""
                \int_{{{a}}}^{{{b}}}
                {f_visual}
                \,dx
                """
            )

            ok, msg, res = ejecutarSimpson38(
                f_sym,
                tipo_integral,
                n,
                a=a,
                b=b
            )

        # ======================================
        # INTEGRAL DOBLE
        # ======================================

        else:

            st.latex(
                rf"""
                \int_{{{ax}}}^{{{bx}}}
                \int_{{{ay}}}^{{{by}}}
                {f_visual}
                \,dy\,dx
                """
            )

            ok, msg, res = ejecutarSimpson38(
                f_sym,
                tipo_integral,
                n,
                ax=ax,
                bx=bx,
                ay=ay,
                by=by
            )

        if not ok:

            st.error(msg)
            return
        
        # ======================================
        # INTEGRAL DOBLE
        # ======================================

        if res["tipo"] == "doble":

            st.subheader(
                "1. Resolución de la Integral Interna"
            )

            st.markdown(
                "**Integral indefinida:**"
            )

            st.latex(
                rf"""
                \int
                {sp.latex(res["expr"])}
                \,dy
                =
                {sp.latex(res["integral_indefinida"])}
                """
            )

            st.markdown(
                "**Aplicando límites:**"
            )

            st.latex(
                rf"""
                \left[
                {sp.latex(res["integral_indefinida"])}
                \right]_{{{ay}}}^{{{by}}}
                """
            )

            st.latex(
                sp.latex(
                    res["integral_superior"]
                )
            )

            st.latex(
                sp.latex(
                    res["integral_inferior"]
                )
            )

            st.latex(
                sp.latex(
                    res["integral_interna"]
                )
            )

            paso_actual = 3

        else:

            paso_actual = 1


        # ======================================
        # h
        # ======================================

        st.subheader(
            f"{paso_actual}. Tamaño de Paso"
        )

        if res["tipo"] == "simple":

            st.latex(
                rf"""
                h=
                \frac{{{formatear_numero(b)}-
                {formatear_numero(a)}}}
                {{{n}}}
                =
                {formatear_numero(res["h"])}
                """
            )

        else:

            st.latex(
                rf"""
                h=
                \frac{{{formatear_numero(bx)}-
                {formatear_numero(ax)}}}
                {{{n}}}
                =
                {formatear_numero(res["h"])}
                """
            )


        # ======================================
        # FORMULA
        # ======================================

        st.subheader(
            f"{paso_actual+1}. Aplicación de la Fórmula"
        )

        st.latex(
            r"""
            I \approx
            \frac{3h}{8}
            \left[
            f(x_0)
            +
            3\sum f(x_i)
            +
            2\sum f(x_j)
            +
            f(x_n)
            \right]
            """
        )


        # ======================================
        # EVALUACIONES
        # ======================================

        st.subheader(
            f"{paso_actual+2}. Evaluación de los Puntos"
        )

        for i in range(len(res["xi"])):

            st.latex(
                rf"""
                x_{{{i}}}
                =
                {formatear_numero(res["xi"][i])}
                """
            )

            st.latex(
                rf"""
                f(x_{{{i}}})
                =
                {formatear_numero(res["fi"][i])}
                """
            )


        # ======================================
        # TABLA
        # ======================================

        st.subheader(
            f"{paso_actual+3}. Tabla de Evaluaciones"
        )

        filas = []

        for i in range(len(res["xi"])):

            filas.append(
                {
                    "i": i,
                    "xi": res["xi"][i],
                    "f(xi)": res["fi"][i],
                    "Peso": res["pesos"][i]
                }
            )

        df = pd.DataFrame(filas)

        st.dataframe(
            df,
            use_container_width=True
        )


        # ======================================
        # SUMAS
        # ======================================

        st.subheader(
            f"{paso_actual+4}. Sumas de Simpson"
        )

        suma3_txt = " + ".join(

            [
                formatear_numero(res["fi"][i])

                for i in range(
                    1,
                    len(res["fi"]) - 1
                )

                if i % 3 != 0
            ]
        )

        suma2_txt = " + ".join(

            [
                formatear_numero(res["fi"][i])

                for i in range(
                    1,
                    len(res["fi"]) - 1
                )

                if i % 3 == 0
            ]
        )

        st.latex(
            rf"""
            \sum f(x_i)_{{peso\,3}}
            =
            {suma3_txt}
            =
            {formatear_numero(res["suma_3"])}
            """
        )

        st.latex(
            rf"""
            \sum f(x_i)_{{peso\,2}}
            =
            {suma2_txt}
            =
            {formatear_numero(res["suma_2"])}
            """
        )

        # ======================================
        # SUSTITUCIÓN
        # ======================================

        st.subheader(
            f"{paso_actual+5}. Sustitución de Valores"
        )

        st.latex(
            rf"""
            I \approx
            \frac{{3({formatear_numero(res["h"])})}}{8}
            \left[
            {formatear_numero(res["fi"][0])}
            +
            3(
            {formatear_numero(res["suma_3"])}
            )
            +
            2(
            {formatear_numero(res["suma_2"])}
            )
            +
            {formatear_numero(res["fi"][-1])}
            \right]
            """
        )

        st.latex(
            rf"""
            I \approx
            \frac{{3({formatear_numero(res["h"])})}}{8}
            \left[
            {formatear_numero(res["fi"][0])}
            +
            {formatear_numero(
                3 * res["suma_3"]
            )}
            +
            {formatear_numero(
                2 * res["suma_2"]
            )}
            +
            {formatear_numero(res["fi"][-1])}
            \right]
            """
        )

        valor_corchete = (

            res["fi"][0]

            +

            3 * res["suma_3"]

            +

            2 * res["suma_2"]

            +

            res["fi"][-1]

        )

        st.latex(
            rf"""
            I \approx
            \frac{{3({formatear_numero(res["h"])})}}{8}
            (
            {formatear_numero(valor_corchete)}
            )
            """
        )


        # ======================================
        # RESULTADO
        # ======================================

        st.subheader(
            f"{paso_actual+6}. Resultado"
        )

        st.success(
            f"I ≈ {formatear_numero(res['resultado'])}"
        )