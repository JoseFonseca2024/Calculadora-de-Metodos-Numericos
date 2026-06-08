import streamlit as st
import pandas as pd
import sympy as sp

from metodos.Interpolacion.TrazadoresCubicos import (
    ejecutarTrazadoresCubicos
)
from utils.Decimales import formatear_numero


def mostrarTrazadoresCubicos():

    st.title(
        "Interpolación por Trazadores Cúbicos"
    )

    st.subheader(
        "Tabla de valores"
    )

    # ==========================================
    # TABLA
    # ==========================================

    if "tabla_splines" not in st.session_state:

        st.session_state.tabla_splines = pd.DataFrame(
            {
                "x": [None],
                "f(x)": [None]
            }
        )

    tabla = st.data_editor(
        st.session_state.tabla_splines,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_splines"
    )

    datos = tabla.dropna()

    cantidad = len(datos)

    st.divider()

    st.write(
        f"Puntos ingresados: {cantidad}"
    )

    # ==========================================
    # CALCULAR
    # ==========================================

    if cantidad >= 2:

        if st.button(
            "Calcular Trazadores",
            use_container_width=True
        ):

            x_vals = (
                datos["x"]
                .astype(float)
                .tolist()
            )

            y_vals = (
                datos["f(x)"]
                .astype(float)
                .tolist()
            )

            ok, msg, res = (
                ejecutarTrazadoresCubicos(
                    x_vals,
                    y_vals
                )
            )

            if not ok:

                st.error(msg)
                return

            n_splines = len(x_vals) - 1

            # ======================================
            # PASO 1
            # ======================================

            st.subheader(
                "1. Definición de los Splines"
            )

            for i in range(n_splines):

                st.markdown(
                    f"### Spline {i+1}"
                )

                st.latex(
                    rf"""
                    S_{i+1}(x)=
                    a_{i+1}x^3
                    +
                    b_{i+1}x^2
                    +
                    c_{i+1}x
                    +
                    d_{i+1}
                    """
                )

                st.latex(
                    rf"""
                    {x_vals[i]}
                    \le x \le
                    {x_vals[i+1]}
                    """
                )

            # ======================================
            # PASO 2
            # ======================================

            st.subheader(
                "2. Condiciones de Ajuste"
            )

            ecuacion = 1

            for i in range(n_splines):

                xi = x_vals[i]
                xi1 = x_vals[i + 1]

                yi = y_vals[i]
                yi1 = y_vals[i + 1]

                st.markdown(
                    f"### Spline {i+1}"
                )

                # ------------------------------
                # Formula general
                # ------------------------------

                st.markdown(
                    "**Fórmula general:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}(x)=
                    a_{i+1}x^3
                    +
                    b_{i+1}x^2
                    +
                    c_{i+1}x
                    +
                    d_{i+1}
                    """
                )

                # ------------------------------
                # Primer punto
                # ------------------------------

                st.markdown(
                    "**Primer punto:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}({xi})
                    =
                    {yi}
                    """
                )

                st.markdown(
                    "**Sustituyendo:**"
                )

                st.latex(
                    rf"""
                    a_{i+1}({xi})^3
                    +
                    b_{i+1}({xi})^2
                    +
                    c_{i+1}({xi})
                    +
                    d_{i+1}
                    =
                    {yi}
                    """
                )

                st.markdown(
                    "**Resultado:**"
                )

                st.latex(
                    sp.latex(
                        res["condiciones_ajuste"][
                            ecuacion - 1
                        ]
                    )
                )

                ecuacion += 1

                # ------------------------------
                # Segundo punto
                # ------------------------------

                st.markdown(
                    "**Segundo punto:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}({xi1})
                    =
                    {yi1}
                    """
                )

                st.markdown(
                    "**Sustituyendo:**"
                )

                st.latex(
                    rf"""
                    a_{i+1}({xi1})^3
                    +
                    b_{i+1}({xi1})^2
                    +
                    c_{i+1}({xi1})
                    +
                    d_{i+1}
                    =
                    {yi1}
                    """
                )

                st.markdown(
                    "**Resultado:**"
                )

                st.latex(
                    sp.latex(
                        res["condiciones_ajuste"][
                            ecuacion - 1
                        ]
                    )
                )

                ecuacion += 1

            # ======================================
            # PASO 3
            # ======================================

            st.subheader(
                "3. Continuidad de la Primera Derivada"
            )

            for i in range(n_splines - 1):

                nodo = x_vals[i + 1]

                st.markdown(
                    f"### Nodo x = {nodo}"
                )

                st.markdown(
                    "**Fórmula:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}'({nodo})
                    =
                    S_{i+2}'({nodo})
                    """
                )

                st.markdown(
                    "**Derivadas generales:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}'(x)
                    =
                    3a_{i+1}x^2
                    +
                    2b_{i+1}x
                    +
                    c_{i+1}
                    """
                )

                st.latex(
                    rf"""
                    S_{i+2}'(x)
                    =
                    3a_{i+2}x^2
                    +
                    2b_{i+2}x
                    +
                    c_{i+2}
                    """
                )

                st.markdown(
                    "**Sustituyendo:**"
                )

                st.latex(
                    rf"""
                    3a_{i+1}({nodo})^2
                    +
                    2b_{i+1}({nodo})
                    +
                    c_{i+1}
                    =
                    3a_{i+2}({nodo})^2
                    +
                    2b_{i+2}({nodo})
                    +
                    c_{i+2}
                    """
                )

                st.markdown(
                    "**Resultado:**"
                )

                st.latex(
                    sp.latex(
                        res["condiciones_derivada1"][i]
                    )
                )

            # ======================================
            # PASO 4
            # ======================================

            st.subheader(
                "4. Continuidad de la Segunda Derivada"
            )

            for i in range(n_splines - 1):

                nodo = x_vals[i + 1]

                st.markdown(
                    f"### Nodo x = {nodo}"
                )

                st.markdown(
                    "**Fórmula:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}''({nodo})
                    =
                    S_{i+2}''({nodo})
                    """
                )

                st.markdown(
                    "**Segundas derivadas:**"
                )

                st.latex(
                    rf"""
                    S_{i+1}''(x)
                    =
                    6a_{i+1}x
                    +
                    2b_{i+1}
                    """
                )

                st.latex(
                    rf"""
                    S_{i+2}''(x)
                    =
                    6a_{i+2}x
                    +
                    2b_{i+2}
                    """
                )

                st.markdown(
                    "**Sustituyendo:**"
                )

                st.latex(
                    rf"""
                    6a_{i+1}({nodo})
                    +
                    2b_{i+1}
                    =
                    6a_{i+2}({nodo})
                    +
                    2b_{i+2}
                    """
                )

                st.markdown(
                    "**Resultado:**"
                )

                st.latex(
                    sp.latex(
                        res["condiciones_derivada2"][i]
                    )
                )

            # ======================================
            # PASO 5
            # ======================================

            st.subheader(
                "5. Condiciones Naturales"
            )

            x0 = x_vals[0]
            xn = x_vals[-1]

            st.markdown(
                "**Condición izquierda:**"
            )

            st.latex(
                rf"""
                S_1''({x0})=0
                """
            )

            st.markdown(
                "**Sustituyendo:**"
            )

            st.latex(
                rf"""
                6a_1({x0})
                +
                2b_1
                =
                0
                """
            )

            st.markdown(
                "**Resultado:**"
            )

            st.latex(
                sp.latex(
                    res["condiciones_naturales"][0]
                )
            )

            st.markdown(
                "**Condición derecha:**"
            )

            st.latex(
                rf"""
                S_{n_splines}''({xn})=0
                """
            )

            st.markdown(
                "**Sustituyendo:**"
            )

            st.latex(
                rf"""
                6a_{n_splines}({xn})
                +
                2b_{n_splines}
                =
                0
                """
            )

            st.markdown(
                "**Resultado:**"
            )

            st.latex(
                sp.latex(
                    res["condiciones_naturales"][1]
                )
            )

            # ======================================
            # PASO 6
            # ======================================

            st.subheader(
                "6. Matriz del Sistema"
            )

            st.markdown(
                "**Matriz A**"
            )

            st.latex(
                sp.latex(
                    sp.Matrix(res["A"])
                )
            )

            st.markdown(
                "**Vector B**"
            )

            st.latex(
                sp.latex(
                    sp.Matrix(res["B"])
                )
            )

            # ======================================
            # PASO 7
            # ======================================

            st.subheader(
                "7. Solución del Sistema"
            )

            # ======================================
            # MATRIZ A
            # ======================================

            st.markdown(
                "**Matriz de coeficientes:**"
            )

            st.latex(
                sp.latex(
                    sp.Matrix(
                        res["A"]
                    )
                )
            )

            # ======================================
            # VECTOR X
            # ======================================

            st.markdown(
                "**Vector de incógnitas:**"
            )

            vector_variables = sp.Matrix(
                res["variables"]
            )

            st.latex(
                sp.latex(
                    vector_variables
                )
            )

            # ======================================
            # VECTOR B
            # ======================================

            st.markdown(
                "**Vector de términos independientes:**"
            )

            st.latex(
                sp.latex(
                    sp.Matrix(
                        res["B"]
                    )
                )
            )

            # ======================================
            # ECUACION MATRICIAL
            # ======================================

            st.markdown(
                "**Sistema matricial:**"
            )

            st.latex(
                rf"""
                {sp.latex(sp.Matrix(res["A"]))}
                \cdot
                {sp.latex(vector_variables)}
                =
                {sp.latex(sp.Matrix(res["B"]))}
                """
            )

            # ======================================
            # SOLUCION
            # ======================================

            st.markdown(
                "**Resolviendo el sistema:**"
            )

            for var, val in zip(
                res["variables"],
                res["solucion"]
            ):

                st.latex(
                    rf"""
                    {sp.latex(var)}
                    =
                    {formatear_numero(val)}
                    """
                )

            # ======================================
            # PASO 8
            # ======================================

            st.subheader(
                "8. Trazadores Finales"
            )

            for i, spline in enumerate(
                res["splines_finales"]
            ):

                if i < n_splines - 1:

                    intervalo = (
                        f"{x_vals[i]}"
                        f" \\le x < "
                        f"{x_vals[i+1]}"
                    )

                else:

                    intervalo = (
                        f"{x_vals[i]}"
                        f" \\le x \\le "
                        f"{x_vals[i+1]}"
                    )

                st.markdown(
                    f"### Spline {i+1}"
                )

                st.latex(
                    rf"""
                    S_{i+1}(x)=
                    {sp.latex(spline)}
                    """
                )

                st.latex(
                    intervalo
                )

    else:

        st.info(
            "Ingrese al menos dos puntos."
        )