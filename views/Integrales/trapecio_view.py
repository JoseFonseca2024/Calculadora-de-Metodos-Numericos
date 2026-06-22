import streamlit as st
import sympy as sp
import pandas as pd

from utils.funciones_integrales import validar_y_preparar_funcion_integral
from metodos.Integrales.Trapecio import ejecutarTrapecio
from utils.Decimales import formatear_numero


def mostrarRegladelTrapecio():

    st.title(
        "Regla del Trapecio"
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

            ok, msg, res = ejecutarTrapecio(
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

            ok, msg, res = ejecutarTrapecio(
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

        st.success(
            "Cálculo realizado correctamente."
        )

        # ======================================
        # INTEGRAL DOBLE
        # ======================================

        if res["tipo"] == "doble":

            st.subheader(
                "1. Resolución de la Integral Interna"
            )

            st.markdown(
                "**Integral interna:**"
            )

            st.latex(
                rf"""
                \int_{{{ay}}}^{{{by}}}
                {sp.latex(res["expr"])}
                \,dy
                """
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

            st.markdown(
                "**Sustituyendo límite superior:**"
            )

            st.latex(
                sp.latex(
                    res["integral_superior"]
                )
            )

            st.markdown(
                "**Sustituyendo límite inferior:**"
            )

            st.latex(
                sp.latex(
                    res["integral_inferior"]
                )
            )

            st.markdown(
                "**Restando:**"
            )

            st.latex(
                rf"""
                {sp.latex(res["integral_superior"])}
                -
                {sp.latex(res["integral_inferior"])}
                """
            )

            st.markdown(
                "**Resultado simplificado:**"
            )

            st.latex(
                sp.latex(
                    res["integral_interna"]
                )
            )
            st.subheader(
                "2. Función Resultante"
            )

            st.latex(
                rf"""
                F(x)=
                {sp.latex(res["integral_interna"])}
                """
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
                \frac{{{b}-{a}}}
                {{{n}}}
                =
                {res["h"]}
                """
            )

        else:

            st.latex(
                rf"""
                h=
                \frac{{{bx}-{ax}}}
                {{{n}}}
                =
                {res["h"]}
                """
            )

        # ======================================
        # GENERACIÓN DE PUNTOS
        # ======================================

        st.subheader(
            f"{paso_actual+1}. Generación de los Puntos"
        )

        for i, xi in enumerate(res["xi"]):

            st.latex(
                rf"""
                x_{i}
                =
                {formatear_numero(xi)}
                """
            )

        # ======================================
        # EVALUACIÓN DE LA FUNCIÓN
        # ======================================

        st.subheader(
            f"{paso_actual+2}. Evaluación de la Función"
        )

        for i in range(len(res["xi"])):

            xi = res["xi"][i]
            fi = res["fi"][i]

            st.markdown(
                f"**Punto {i}**"
            )

            st.latex(
                rf"""
                f(x_{i})
                =
                f(
                {formatear_numero(xi)}
                )
                """
            )

            funcion_sustituida = (
                f_visual.replace(
                    "x",
                    f"({formatear_numero(xi)})"
                )
            )

            st.latex(
                rf"""
                f(x_{i})
                =
                {funcion_sustituida}
                """
            )

            st.latex(
                rf"""
                f(x_{i})
                =
                {formatear_numero(fi)}
                """
            )

        # ======================================
        # TABLA
        # ======================================

        st.subheader(
            f"{paso_actual+3}. Tabla de Evaluaciones"
        )

        filas = []

        for i in range(
            len(res["xi"])
        ):

            filas.append(
                {
                    "i": i,
                    "xi": formatear_numero(
                        res["xi"][i]
                    ),
                    "f(xi)": formatear_numero(
                        res["fi"][i]
                    )
                }
            )

        df = pd.DataFrame(
            filas
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # ======================================
        # FORMULA
        # ======================================

        st.subheader(
            f"{paso_actual+4}. Aplicación de la Fórmula"
        )

        st.markdown(
            "**Fórmula del Trapecio:**"
        )

        st.latex(
            r"""
            I
            \approx
            \frac{h}{2}
            \left[
            f(x_0)
            +
            2\sum_{i=1}^{n-1}
            f(x_i)
            +
            f(x_n)
            \right]
            """
        )

        # ======================================
        # SUSTITUCIÓN
        # ======================================

        st.subheader(
            f"{paso_actual+5}. Sustitución de Valores"
        )

        suma_detallada = " + ".join(
            [
                formatear_numero(valor)
                for valor in res["fi"][1:-1]
            ]
        )

        st.latex(
            rf"""
            I
            \approx
            \frac{{{formatear_numero(res["h"])}}}{2}
            \left[
            {formatear_numero(res["fi"][0])}
            +
            2(
            {suma_detallada}
            )
            +
            {formatear_numero(res["fi"][-1])}
            \right]
            """
        )

        st.latex(
            rf"""
            I
            \approx
            \frac{{{formatear_numero(res["h"])}}}{2}
            \left[
            {formatear_numero(res["fi"][0])}
            +
            2(
            {formatear_numero(res["suma_interna"])}
            )
            +
            {formatear_numero(res["fi"][-1])}
            \right]
            """
        )

        valor_corchete = (
            res["fi"][0]
            +
            2 * res["suma_interna"]
            +
            res["fi"][-1]
        )

        st.latex(
            rf"""
            I
            \approx
            \frac{{{formatear_numero(res["h"])}}}{2}
            (
            {formatear_numero(valor_corchete)}
            )
            """
        )

        st.latex(
            rf"""
            I
            \approx
            {formatear_numero(
                res["resultado"]
            )}
            """
        )

        # ======================================
        # RESULTADO
        # ======================================

        st.subheader(
            f"{paso_actual+6}. Resultado"
        )

        st.success(
            f"I ≈ "
            f"{formatear_numero(res['resultado'])}"
        )