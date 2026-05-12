import streamlit as st
import sympy as sp

from utils.polinomios import validar_y_preparar_polinomio
from metodos.bairstow import ejecutar_bairstow


def limpiar(valor, tol=1e-10):

    if abs(valor) < tol:
        return 0.0

    if abs(valor - round(valor)) < tol:
        return float(round(valor))

    return valor

def mostrar_bairstow():

    st.title("Método de Bairstow")

    polinomio_str = st.text_input(
        "Introduzca P(x):",
        placeholder="x^3+3x^2-x-3=0"
    )

    tol = st.number_input(
        "Tolerancia",
        value=1e-5,
        format="%.8f"
    )

    if st.button("Calcular"):

        valido, error_msg, datos = (
            validar_y_preparar_polinomio(
                polinomio_str
            )
        )

        if not valido:

            st.error(error_msg)
            return

        p_sym, _, grado, coeficientes, _, _ = datos

        ok, msg, res = ejecutar_bairstow(
            coeficientes,
            tol
        )

        if not ok:

            st.error(msg)
            return

        iteraciones = res["iteraciones"]

        raices = res["raices"]

        raices_completas = (
            res["raices_completas"]
        )

        st.subheader("Polinomio:")

        st.latex(
            f"P(x) = {sp.latex(p_sym)}"
        )

        st.write(f"Grado: {grado}")

        st.write(
            f"Coeficientes: {coeficientes}"
        )

        x = sp.symbols("x")

        # =====================================================
        # PROCEDIMIENTO
        # =====================================================

        with st.expander(
            "Ver procedimiento",
            expanded=False
        ):

            st.markdown("## Datos iniciales")

            for i, coef in enumerate(coeficientes):

                st.latex(
                    f"a_{len(coeficientes)-1-i}"
                    f" = {coef}"
                )

            polinomio_actual = (
                coeficientes.copy()
            )

            for bloque, bloque_data in enumerate(iteraciones):

                st.markdown(
                    f"# Factor cuadrático {bloque + 1}"
                )

                iteraciones_locales = (
                    bloque_data["iteraciones"]
                )

                # =========================================
                # ITERACIONES
                # =========================================

                for it in iteraciones_locales:

                    st.markdown(
                        f"## Iteración "
                        f"{it['iter'] + 1}"
                    )

                    r = it["r_old"]
                    s = it["s_old"]

                    b = it["b"]
                    c = it["c"]

                    n = len(b) - 1

                    # =====================================
                    # b
                    # =====================================

                    st.markdown(
                        "### Coeficientes b"
                    )

                    st.latex(
                        f"b_{n} = a_{n}"
                        f" = {b[n]:.8f}"
                    )

                    st.latex(
                        f"b_{n-1}"
                        f" = a_{n-1}"
                        f" + r b_n"
                        f" = {b[n-1]:.8f}"
                    )

                    for i in range(n - 2, -1, -1):

                        st.latex(
                            f"b_{i}"
                            f" = a_{i}"
                            f" + r b_{i+1}"
                            f" + s b_{i+2}"
                            f" = {b[i]:.8f}"
                        )

                    # =====================================
                    # c
                    # =====================================

                    st.markdown(
                        "### Coeficientes c"
                    )

                    st.latex(
                        f"c_{n}"
                        f" = b_{n}"
                        f" = {c[n]:.8f}"
                    )

                    st.latex(
                        f"c_{n-1}"
                        f" = b_{n-1}"
                        f" + r c_n"
                        f" = {c[n-1]:.8f}"
                    )

                    for i in range(n - 2, 0, -1):

                        st.latex(
                            f"c_{i}"
                            f" = b_{i}"
                            f" + r c_{i+1}"
                            f" + s c_{i+2}"
                            f" = {c[i]:.8f}"
                        )

                    # =====================================
                    # CORRECCIONES
                    # =====================================

                    st.markdown(
                        "### Correcciones"
                    )

                    st.latex(
                        f"\\Delta r"
                        f" = {it['dr']:.8f}"
                    )

                    st.latex(
                        f"\\Delta s"
                        f" = {it['ds']:.8f}"
                    )

                    st.latex(
                        f"r_{{nuevo}}"
                        f" = {r:.8f}"
                        f" + {it['dr']:.8f}"
                        f" = {it['r']:.8f}"
                    )

                    st.latex(
                        f"s_{{nuevo}}"
                        f" = {s:.8f}"
                        f" + {it['ds']:.8f}"
                        f" = {it['s']:.8f}"
                    )

                    # =====================================
                    # RAÍCES
                    # =====================================

                    st.markdown("### Raíces")

                    st.latex(
                        f"x = "
                        f"\\frac{{"
                        f"{it['r']:.8f}"
                        f" \\pm "
                        f"\\sqrt{{"
                        f"({it['r']:.8f})^2"
                        f" + 4({it['s']:.8f})"
                        f"}}"
                        f"}}{{2}}"
                    )

                    # x1

                    if isinstance(it["x1"], complex):

                        st.latex(
                            f"x_1 = "
                            f"{it['x1'].real:.8f}"
                            f"{'+' if it['x1'].imag >= 0 else '-'}"
                            f"{abs(it['x1'].imag):.8f}i"
                        )

                    else:

                        st.latex(
                            f"x_1 = "
                            f"{it['x1']:.8f}"
                        )

                    # x2

                    if isinstance(it["x2"], complex):

                        st.latex(
                            f"x_2 = "
                            f"{it['x2'].real:.8f}"
                            f"{'+' if it['x2'].imag >= 0 else '-'}"
                            f"{abs(it['x2'].imag):.8f}i"
                        )

                    else:

                        st.latex(
                            f"x_2 = "
                            f"{it['x2']:.8f}"
                        )

                    # =====================================
                    # ERRORES
                    # =====================================

                    if it["error_x1"] is not None:

                        st.latex(
                            f"E_{{x1}}"
                            f" = "
                            f"{it['error_x1']:.8f}\\%"
                        )

                        st.latex(
                            f"E_{{x2}}"
                            f" = "
                            f"{it['error_x2']:.8f}\\%"
                        )

                    st.markdown("---")

                # =========================================
                # FACTOR FINAL
                # =========================================

                r_final = limpiar(
                    bloque_data["factor_r"]
                )

                s_final = limpiar(
                    bloque_data["factor_s"]
                )

                st.markdown(
                    "## Factor cuadrático final"
                )

                st.latex(
                    f"x^2"
                    f" - ({r_final:.8f})x"
                    f" - ({s_final:.8f})"
                )

                # =========================================
                # DIVISIÓN SINTÉTICA
                # =========================================

                st.markdown(
                    "### División sintética"
                )

                factor = (
                    x**2
                    - r_final * x
                    - s_final
                )

                grado_actual = (
                    len(polinomio_actual) - 1
                )

                poly_actual = sum(
                    polinomio_actual[i]
                    * x**(
                        grado_actual - i
                    )
                    for i in range(
                        len(polinomio_actual)
                    )
                )

                st.latex(
                    f"\\frac{{"
                    f"{sp.latex(sp.expand(poly_actual))}"
                    f"}}{{"
                    f"{sp.latex(sp.expand(factor))}"
                    f"}}"
                )

                cociente = (
                    bloque_data["cociente"]
                )

                cociente_mostrar = cociente[::-1]

                grado_cociente = (
                    len(cociente_mostrar) - 1
                )

                poly_cociente = sum(
                    cociente_mostrar[i]
                    * x**(
                        grado_cociente - i
                    )
                    for i in range(
                        len(cociente_mostrar)
                    )
                )

                st.latex(
                    f"="
                    f"{sp.latex(sp.expand(poly_cociente))}"
                )

                polinomio_actual = (
                    cociente_mostrar.copy()
                )

            # =============================================
            # POLINOMIO FINAL
            # =============================================

            if len(polinomio_actual) == 2:

                st.markdown(
                    "# Polinomio lineal restante"
                )

                a0 = polinomio_actual[0]
                a1 = polinomio_actual[1]

                st.latex(
                    f"{a0:.8f}x"
                    f" + ({a1:.8f}) = 0"
                )

                st.latex(
                    f"x = "
                    f"-\\frac{{{a1:.8f}}}"
                    f"{{{a0:.8f}}}"
                )

        # =====================================================
        # RESULTADO FINAL
        # =====================================================

        if len(raices) == 0:

            st.warning(
                "No se encontraron raíces reales."
            )

        else:

            st.success(
                "Raíces reales aproximadas:"
            )

            for i, r in enumerate(
                raices,
                start=1
            ):

                st.latex(
                    f"x_{i}"
                    f" = {r:.8f}"
                )

        # =====================================================
        # TODAS LAS RAÍCES
        # =====================================================

        st.markdown(
            "## Todas las raíces"
        )

        for i, r in enumerate(
            raices_completas,
            start=1
        ):

            if isinstance(r, complex):

                if abs(r.imag) < 1e-10:

                    st.latex(
                        f"x_{i}"
                        f" = {r.real:.8f}"
                    )

                else:

                    st.latex(
                        f"x_{i}"
                        f" = "
                        f"{r.real:.8f}"
                        f"{'+' if r.imag >= 0 else '-'}"
                        f"{abs(r.imag):.8f}i"
                    )

            else:

                st.latex(
                    f"x_{i}"
                    f" = {r:.8f}"
                )