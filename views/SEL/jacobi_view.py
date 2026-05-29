import streamlit as st
import pandas as pd
import sympy as sp

from metodos.SEL.jacobi import ejecutarJacobi
from utils.ordenarMatrix import ordenar_matriz_diagonalmente

def mostrarJacobi():

    st.title("Método de Jacobi")

    # ==========================================
    # TAMAÑO INICIAL DEL SISTEMA
    # ==========================================

    if "tam_jacobi" not in st.session_state:
        st.session_state.tam_jacobi = 3

    n = st.session_state.tam_jacobi

    st.subheader("Sistema de ecuaciones")

    st.write(
        "Introduzca los coeficientes del sistema:"
    )

    # ==========================================
    # CABECERA DE VARIABLES (Se dibuja una sola vez)
    # ==========================================
    cols_header = st.columns([1]*n + [0.3, 1.2])

    # Etiquetas para las x_n
    for j in range(n):
        with cols_header[j]:
            st.markdown(
                f"""
                <div style='text-align:center; margin-bottom:4px; font-weight:bold;'>
                    x<sub>{j+1}</sub>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Espacio vacío sobre el signo "="
    with cols_header[n]:
        st.write("")

    # Etiqueta para el vector b
    with cols_header[n + 1]:
        st.markdown(
            """
            <div style='text-align:center; margin-bottom:4px; font-weight:bold;'>
                b
            </div>
            """,
            unsafe_allow_html=True
        )


    # ==========================================
    # MATRIZ A Y VECTOR B (Solo inputs y el signo =)
    # ==========================================
    matriz = []
    vector_b = []

    for i in range(n):
        cols = st.columns([1]*n + [0.3, 1.2])
        fila = []

        # ======================================
        # COEFICIENTES
        # ======================================
        for j in range(n):
            with cols[j]:
                valor = st.number_input(
                    f"a{i}{j}",
                    value=0.0,
                    key=f"a_{i}_{j}",
                    label_visibility="collapsed"
                )
                fila.append(valor)

        # ======================================
        # SIGNO IGUAL (Ajustado el margen superior)
        # ======================================
        with cols[n]:
            st.markdown(
                """
                <div style='text-align:center; font-size:24px; margin-top:4px;'>
                    =
                </div>
                """,
                unsafe_allow_html=True
            )

        # ======================================
        # TÉRMINO INDEPENDIENTE
        # ======================================
        with cols[n + 1]:
            b = st.number_input(
                f"b{i}",
                value=0.0,
                key=f"b_{i}",
                label_visibility="collapsed"
            )
            vector_b.append(b)

        matriz.append(fila)
    # ==========================================
    # TOLERANCIA
    # ==========================================

    tol = st.number_input(
        "Tolerancia (%)",
        value=0.001,
        format="%.6f"
    )

    # ==========================================
    # BOTONES
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("➕ Agregar ecuación"):

            st.session_state.tam_jacobi += 1
            st.rerun()

    with col2:

        if st.button("➖ Quitar ecuación"):

            if st.session_state.tam_jacobi > 2:

                st.session_state.tam_jacobi -= 1
                st.rerun()

    with col3:

        if st.button("🔄 Reiniciar sistema"):

            st.session_state.tam_jacobi = 3

            claves_borrar = []

            for clave in st.session_state.keys():

                if (
                    clave.startswith("a_")
                    or clave.startswith("b_")
                ):

                    claves_borrar.append(clave)

            for clave in claves_borrar:

                del st.session_state[clave]

            st.rerun()

    # ==========================================
    # CALCULAR
    # ==========================================

    st.divider()

    if st.button("Calcular Método de Jacobi"):

        ok_ord, msg_ord, matriz_ord, vector_b_ord = ordenar_matriz_diagonalmente(
            matriz,
            vector_b
        )

        if not ok_ord:

            st.error(msg_ord)
            return

        ok, msg, iteraciones = ejecutarJacobi(
            matriz_ord,
            vector_b_ord,
            tol
        )

        if not ok:

            st.error(msg)
            return

        # ======================================
        # MATRIZ A
        # ======================================

        st.subheader("Matriz A")

        st.latex(
            sp.latex(
                sp.Matrix(matriz)
            )
        )

        # ======================================
        # VECTOR B
        # ======================================

        st.subheader("Vector B")

        st.latex(
            sp.latex(
                sp.Matrix(vector_b)
            )
        )

        st.subheader("Matriz A Ordenada")

        st.latex(
            sp.latex(
                sp.Matrix(matriz_ord)
            )
        )

        st.subheader("Vector B Ordenado")

        st.latex(
            sp.latex(
                sp.Matrix(vector_b_ord)
            )
        )

        # ======================================
        # VECTOR INICIAL
        # ======================================

        st.subheader("Vector Inicial")

        st.latex(
            f"X^{{(0)}} = {[0 for _ in range(n)]}"
        )

        # ======================================
        # PROCEDIMIENTO
        # ======================================

        with st.expander(
            "Ver procedimiento detallado",
            expanded=False
        ):

            for it in iteraciones:

                k = it["i"]

                st.markdown(
                    f"# Iteración {k+1}"
                )

                Xi = it["Xi"]
                Xi1 = it["Xi+1"]

                # ==================================
                # VECTOR ACTUAL
                # ==================================

                st.write("## Vector actual")

                for i in range(n):

                    st.latex(
                        f"x_{{{i+1}}}^{{({k})}} = "
                        f"{Xi[i]:.8f}"
                    )

                # ==================================
                # CALCULOS
                # ==================================

                st.write("## Cálculo de nuevos valores")

                for i in range(n):

                    suma_txt = ""

                    for j in range(n):

                        if i != j:

                            suma_txt += (
                                f"({matriz[i][j]:.8f})"
                                f"({Xi[j]:.8f}) + "
                            )

                    suma_txt = suma_txt[:-3]

                    st.latex(
                        f"x_{{{i+1}}}^{{({k+1})}}="
                        f"\\frac{{"
                        f"{vector_b[i]:.8f}"
                        f"-({suma_txt})"
                        f"}}{{{matriz[i][i]:.8f}}}"
                    )

                    st.latex(
                        f"x_{{{i+1}}}^{{({k+1})}}="
                        f"{Xi1[i]:.8f}"
                    )

                # ==================================
                # ERRORES
                # ==================================

                st.write("## Errores")

                for i in range(n):

                    st.latex(
                        f"Error_{{x_{i+1}}}="
                        f"{it['Errores'][i]:.8f}\\%"
                    )

                st.latex(
                    f"Error\\ máximo="
                    f"{it['Error%']:.8f}\\%"
                )

                st.markdown("---")

        # ======================================
        # TABLA
        # ======================================

        st.subheader("Tabla de Iteraciones")

        filas = []

        for it in iteraciones:

            fila = {
                "Iteración": it["i"],
                "Error%": it["Error%"]
            }

            for i in range(n):

                fila[f"x{i+1}"] = it["Xi+1"][i]

            filas.append(fila)

        df = pd.DataFrame(filas)

        st.dataframe(df)

        # ======================================
        # RESULTADO FINAL
        # ======================================

        ultima = iteraciones[-1]["Xi+1"]

        st.success(
            f"Solución aproximada: {ultima}"
        )