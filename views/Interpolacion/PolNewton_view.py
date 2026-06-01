import streamlit as st
import pandas as pd
import sympy as sp

from metodos.Interpolacion.PolinomioNewton import ejecutarPolNewton

def mostrarPolNewton():

    st.title("Interpolación por el Polinomio de Newton")

    st.subheader("Tabla de valores")

    # ==========================================
    # INICIALIZAR TABLA
    # ==========================================

    if "tabla_newton" not in st.session_state:

        st.session_state.tabla_newton = pd.DataFrame(
            {
                "x": [None],
                "f(x)": [None]
            }
        )

    # ==========================================
    # TABLA EDITABLE
    # ==========================================

    tabla = st.data_editor(
        st.session_state.tabla_newton,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_newton"
    )

    # ==========================================
    # DATOS VÁLIDOS
    # ==========================================

    datos = tabla.dropna()

    cantidad_puntos = len(datos)

    st.divider()

    # ==========================================
    # INFORMACIÓN
    # ==========================================

    st.write(
        f"Puntos ingresados: {cantidad_puntos}"
    )

    if cantidad_puntos >= 2:

        st.write(
            f"Grado máximo posible: {cantidad_puntos - 1}"
        )

        # ======================================
        # GRADO DEL POLINOMIO
        # ======================================

        grado = st.selectbox(
            "Seleccione el grado a desarrollar",
            options=list(
                range(
                    1,
                    cantidad_puntos
                )
            )
        )

        # ======================================
        # CALCULAR
        # ======================================

        if st.button(
            "Calcular Polinomio de Newton",
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

            ok, msg, resultado = ejecutarPolNewton(
                x_vals,
                y_vals,
                grado
            )

            if not ok:

                st.error(msg)
                return
            

            # =====================================================
            # PASO 1
            # =====================================================

            st.subheader(
                "1. Cálculo de las Diferencias Divididas"
            )

            for orden in range(1, grado + 1):

                st.markdown(
                    f"### Diferencias de Orden {orden}"
                )

                for i in range(
                    orden,
                    len(x_vals)
                ):

                    nombres_actual = ",".join(
                        [
                            f"x_{{{k}}}"
                            for k in range(
                                i - orden,
                                i + 1
                            )
                        ]
                    )

                    nombres_sup = ",".join(
                        [
                            f"x_{{{k}}}"
                            for k in range(
                                i - orden + 1,
                                i + 1
                            )
                        ]
                    )

                    nombres_inf = ",".join(
                        [
                            f"x_{{{k}}}"
                            for k in range(
                                i - orden,
                                i
                            )
                        ]
                    )

                    with st.expander(
                        f"f({nombres_actual})",
                        expanded=False
                    ):

                        st.markdown(
                            "**Fórmula:**"
                        )

                        st.latex(
                            rf"""
                            f({nombres_actual})
                            =
                            \frac
                            {{
                            f({nombres_sup})
                            -
                            f({nombres_inf})
                            }}
                            {{
                            x_{{{i}}}
                            -
                            x_{{{i-orden}}}
                            }}
                            """
                        )

                        numerador1 = resultado[
                            "tabla"
                        ][i][orden - 1]

                        numerador2 = resultado[
                            "tabla"
                        ][i - 1][orden - 1]

                        st.markdown(
                            "**Sustituyendo valores:**"
                        )

                        st.latex(
                            rf"""
                            f({nombres_actual})
                            =
                            \frac
                            {{
                            {numerador1:.8f}
                            -
                            {numerador2:.8f}
                            }}
                            {{
                            {x_vals[i]:.8f}
                            -
                            {x_vals[i-orden]:.8f}
                            }}
                            """
                        )

                        st.markdown(
                            "**Resultado:**"
                        )

                        st.latex(
                            rf"""
                            f({nombres_actual})
                            =
                            {
                                resultado["tabla"]
                                [i]
                                [orden]
                            :.8f}
                            """
                        )

            # =====================================================
            # PASO 2
            # =====================================================

            st.subheader(
                "2. Obtención de los Coeficientes"
            )

            tabla_dd = resultado["tabla"]

            for orden in range(grado + 1):

                with st.expander(
                    f"Coeficiente a{orden}",
                    expanded=(orden == 0)
                ):

                    if orden == 0:

                        st.latex(
                            r"a_0=f(x_0)"
                        )

                        st.latex(
                            rf"""
                            a_0=
                            f({x_vals[0]})
                            =
                            {y_vals[0]}
                            """
                        )

                    else:

                        nombres_actual = ",".join(
                            [
                                f"x_{{{i}}}"
                                for i in range(
                                    orden + 1
                                )
                            ]
                        )

                        nombres_sup = ",".join(
                            [
                                f"x_{{{i}}}"
                                for i in range(
                                    1,
                                    orden + 1
                                )
                            ]
                        )

                        nombres_inf = ",".join(
                            [
                                f"x_{{{i}}}"
                                for i in range(
                                    orden
                                )
                            ]
                        )

                        st.markdown(
                            "**Fórmula:**"
                        )

                        st.latex(
                            rf"""
                            f({nombres_actual})
                            =
                            \frac
                            {{
                            f({nombres_sup})
                            -
                            f({nombres_inf})
                            }}
                            {{
                            x_{{{orden}}}
                            -
                            x_0
                            }}
                            """
                        )

                        numerador1 = (
                            tabla_dd[orden]
                            [orden - 1]
                        )

                        numerador2 = (
                            tabla_dd[orden - 1]
                            [orden - 1]
                        )

                        st.markdown(
                            "**Sustituyendo valores:**"
                        )

                        st.latex(
                            rf"""
                            f({nombres_actual})
                            =
                            \frac
                            {{
                            {numerador1:.8f}
                            -
                            {numerador2:.8f}
                            }}
                            {{
                            {x_vals[orden]}
                            -
                            {x_vals[0]}
                            }}
                            """
                        )

                        st.markdown(
                            "**Resultado:**"
                        )

                        st.latex(
                            rf"""
                            a_{{{orden}}}
                            =
                            {resultado["coeficientes"][orden]:.8f}
                            """
                        )

            # =====================================================
            # PASO 3
            # =====================================================

            st.subheader(
                "3. Tabla de Diferencias Divididas"
            )

            columnas = [
                "f(xi)"
            ]

            for i in range(
                1,
                grado + 1
            ):

                columnas.append(
                    f"Orden {i}"
                )

            filas = []

            for i in range(
                len(x_vals)
            ):

                fila = {
                    "i": i,
                    "xi": x_vals[i]
                }

                for j in range(
                    grado + 1
                ):

                    valor = resultado["tabla"][i][j]

                    if valor is not None:

                        fila[
                            columnas[j]
                        ] = round(
                            valor,
                            8
                        )

                filas.append(
                    fila
                )

            df_dd = pd.DataFrame(
                filas
            )

            st.dataframe(
                df_dd,
                use_container_width=True
            )

            # =====================================================
            # PASO 4
            # =====================================================

            st.subheader(
                "4. Construcción del Polinomio"
            )

            coef = resultado[
                "coeficientes"
            ]

            polinomio_acumulado = 0

            for i, termino in enumerate(
                resultado[
                    "terminos_expr"
                ]
            ):

                with st.expander(
                    f"Paso para grado {i}",
                    expanded=(i == 0)
                ):

                    if i == 0:

                        st.markdown(
                            "**Primer término:**"
                        )

                        st.latex(
                            rf"""
                            T_0(x)
                            =
                            a_0
                            =
                            {coef[0]:.8f}
                            """
                        )

                    else:

                        producto_txt = ""

                        for j in range(i):

                            producto_txt += (
                                f"(x-{x_vals[j]})"
                            )

                        st.markdown(
                            "**Fórmula:**"
                        )

                        st.latex(
                            rf"""
                            T_{{{i}}}(x)
                            =
                            a_{{{i}}}
                            {producto_txt}
                            """
                        )

                        st.markdown(
                            "**Sustituyendo coeficiente:**"
                        )

                        st.latex(
                            rf"""
                            T_{{{i}}}(x)
                            =
                            {coef[i]:.8f}
                            {producto_txt}
                            """
                        )

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
            # PASO 5
            # =====================================================

            st.subheader(
                "5. Polinomio de Newton"
            )

            st.latex(
                sp.latex(
                    resultado[
                        "polinomio"
                    ]
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