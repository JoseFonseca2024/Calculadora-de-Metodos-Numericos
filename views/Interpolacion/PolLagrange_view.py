import streamlit as st
import pandas as pd
import sympy as sp

from metodos.Interpolacion.Lagrange import ejecutarLagrange


def mostrarPolLagrange():

    st.title(
        "Polinomio Interpolante de Lagrange"
    )

    st.subheader(
        "Tabla de valores"
    )

    # ==========================================
    # TABLA
    # ==========================================

    if "tabla_lagrange" not in st.session_state:

        st.session_state.tabla_lagrange = pd.DataFrame(
            {
                "x": [None],
                "f(x)": [None]
            }
        )

    tabla = st.data_editor(
        st.session_state.tabla_lagrange,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_lagrange"
    )

    datos = tabla.dropna()

    cantidad = len(datos)

    st.divider()

    st.write(
        f"Puntos ingresados: {cantidad}"
    )

    # ==========================================
    # PUNTO DE PRUEBA
    # ==========================================

    usar_prueba = st.checkbox(
        "Evaluar punto de prueba"
    )

    x_prueba = None

    if usar_prueba:

        x_prueba = st.number_input(
            "Valor de prueba x:",
            value=0.0,
            format="%.6f"
        )

    # ==========================================
    # CALCULAR
    # ==========================================

    if cantidad >= 2:

        if st.button(
            "Calcular Polinomio de Lagrange",
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

            ok, msg, resultado = ejecutarLagrange(
                x_vals,
                y_vals,
                x_prueba
            )

            if not ok:

                st.error(msg)
                return

            # =====================================================
            # PASO 1
            # =====================================================

            st.subheader(
                "1. Construcción de los Polinomios Lᵢ(x)"
            )

            for item in resultado["Li"]:

                i = item["i"]

                with st.expander(
                    f"Polinomio L{i}(x)",
                    expanded=(i == 0)
                ):

                    # ==========================================
                    # FORMULA GENERAL
                    # ==========================================

                    st.markdown(
                        "**Fórmula general:**"
                    )

                    st.latex(
                        rf"""
                        L_{{{i}}}(x)
                        =
                        \prod_{{j=0 \atop j \ne {i}}}^{{{len(x_vals)-1}}}
                        \frac{{x-x_j}}{{x_{{{i}}}-x_j}}
                        """
                    )

                    # ==========================================
                    # SUSTITUCIÓN
                    # ==========================================

                    numerador_txt = ""
                    denominador_txt = ""

                    for j in range(len(x_vals)):

                        if i != j:

                            numerador_txt += (
                                f"(x-{x_vals[j]})"
                            )

                            denominador_txt += (
                                f"({x_vals[i]}-{x_vals[j]})"
                            )

                    st.markdown(
                        "**Sustituyendo valores:**"
                    )

                    st.latex(
                        rf"""
                        L_{{{i}}}(x)
                        =
                        \frac
                        {{
                        {numerador_txt}
                        }}
                        {{
                        {denominador_txt}
                        }}
                        """
                    )

                    # ==========================================
                    # RESULTADO
                    # ==========================================

                    st.markdown(
                        "**Resultado simplificado:**"
                    )

                    st.latex(
                        rf"""
                        L_{{{i}}}(x)
                        =
                        {sp.latex(item["Li"])}
                        """
                    )

            # =====================================================
            # PASO 2
            # =====================================================

            st.subheader(
                "2. Construcción del Polinomio"
            )

            st.markdown(
                "**Fórmula general:**"
            )

            st.latex(
                r"""
                P(x)=
                \sum_{i=0}^{n}
                y_iL_i(x)
                """
            )

            polinomio_acumulado = 0

            for item in resultado["Li"]:

                i = item["i"]

                termino = item["termino"]

                with st.expander(
                    f"Término {i}",
                    expanded=(i == 0)
                ):

                    # ==========================================
                    # FORMULA
                    # ==========================================

                    st.markdown(
                        "**Construcción del término:**"
                    )

                    st.latex(
                        rf"""
                        T_{{{i}}}(x)
                        =
                        y_{{{i}}}
                        L_{{{i}}}(x)
                        """
                    )

                    # ==========================================
                    # SUSTITUIR
                    # ==========================================

                    st.markdown(
                        "**Sustituyendo valores:**"
                    )

                    st.latex(
                        rf"""
                        T_{{{i}}}(x)
                        =
                        ({y_vals[i]})
                        ({sp.latex(item["Li"])})
                        """
                    )

                    # ==========================================
                    # RESULTADO
                    # ==========================================

                    st.markdown(
                        "**Término desarrollado:**"
                    )

                    st.latex(
                        rf"""
                        T_{{{i}}}(x)
                        =
                        {sp.latex(
                            sp.expand(
                                termino
                            )
                        )}
                        """
                    )

                    # ==========================================
                    # ACUMULADO
                    # ==========================================

                    polinomio_acumulado += termino

                    st.markdown(
                        "**Polinomio acumulado:**"
                    )

                    st.latex(
                        rf"""
                        P_{{{i}}}(x)
                        =
                        {sp.latex(
                            sp.expand(
                                polinomio_acumulado
                            )
                        )}
                        """
                    )

            # =====================================================
            # PASO 3
            # =====================================================

            st.subheader(
                "3. Verificación con los puntos"
            )

            for ver in resultado["verificaciones"]:

                with st.expander(
                    f"Verificar x = {ver['x']}",
                    expanded=False
                ):

                    st.markdown(
                        "**Sustituyendo en el polinomio:**"
                    )

                    st.latex(
                        rf"""
                        P({ver["x"]})
                        =
                        {ver["obtenido"]:.8f}
                        """
                    )

                    st.markdown(
                        "**Comparación con la tabla:**"
                    )

                    st.latex(
                        rf"""
                        f({ver["x"]})
                        =
                        {ver["esperado"]:.8f}
                        """
                    )

                    st.markdown(
                        "**Verificación:**"
                    )

                    st.latex(
                        rf"""
                        {ver["obtenido"]:.8f}
                        =
                        {ver["esperado"]:.8f}
                        """
                    )

            # =====================================================
            # PASO 4
            # =====================================================

            if resultado["x_prueba"] is not None:

                st.subheader(
                    "4. Evaluación del Punto de Prueba"
                )

                st.markdown(
                    "**Sustituyendo en el polinomio:**"
                )

                st.latex(
                    rf"""
                    P({resultado["x_prueba"]})
                    =
                    {resultado["valor_prueba"]:.8f}
                    """
                )

            # =====================================================
            # PASO 5
            # =====================================================

            st.subheader(
                "5. Polinomio de Lagrange"
            )

            st.latex(
                sp.latex(
                    resultado["polinomio"]
                )
            )

            # =====================================================
            # PASO 6
            # =====================================================

            st.subheader(
                "6. Polinomio Expandido"
            )

            st.latex(
                sp.latex(
                    resultado[
                        "polinomio_expandido"
                    ]
                )
            )

    else:

        st.info(
            "Ingrese al menos dos puntos."
        )