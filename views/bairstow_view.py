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

        valido, error_msg, datos = validar_y_preparar_polinomio(polinomio_str)

        if not valido:
            st.error(error_msg)
            return

        p_sym, _, grado, coeficientes, _, _ = datos

        ok, msg, res = ejecutar_bairstow(coeficientes, tol)

        if not ok:
            st.error(msg)
            return

        iteraciones = res["iteraciones"]
        raices = res["raices"]
        raices_completas = res["raices_completas"]

        st.subheader("Polinomio:")
        st.latex(f"P(x) = {sp.latex(p_sym)}")

        st.write(f"Grado: {grado}")
        st.write(f"Coeficientes: {coeficientes}")

        x = sp.symbols("x")

        # =====================================================
        # PROCEDIMIENTO
        # =====================================================

        with st.expander("Ver procedimiento", expanded=False):

            st.markdown("## Datos iniciales")

            for i, coef in enumerate(coeficientes):
                st.latex(f"a_{len(coeficientes)-1-i} = {coef}")

            polinomio_actual = coeficientes.copy()

            for bloque, bloque_data in enumerate(iteraciones):

                st.markdown(f"# Factor cuadrático {bloque + 1}")

                st.markdown("## Valores iniciales")

                r0 = bloque_data["r_inicial"]
                s0 = bloque_data["s_inicial"]

                grado_actual = len(polinomio_actual) - 1

                # =====================================================
                # POLINOMIO ACTUAL EN ORDEN ASCENDENTE
                # =====================================================
                a = polinomio_actual[::-1]

                # =====================================================
                # CASO 1: raíces pequeñas
                # =====================================================
                if bloque_data["tipo_inicial"] == "peque":

                    a1 = a[1]
                    a2 = a[2]
                    a0 = a[0]

                    st.latex(
                        rf"""
                        r_0 = \frac{{a_1}}{{a_2}} =
                        \frac{{{a1:.8f}}}{{{a2:.8f}}}
                        = {r0:.8f}
                        """
                    )

                    st.latex(
                        rf"""
                        s_0 = \frac{{a_0}}{{a_2}} =
                        \frac{{{a0:.8f}}}{{{a2:.8f}}}
                        = {s0:.8f}
                        """
                    )

                # =====================================================
                # CASO 2: raíces grandes
                # =====================================================
                elif bloque_data["tipo_inicial"] == "grande":

                    an = a[-1]
                    an1 = a[-2]
                    an2 = a[-3]

                    st.latex(
                        rf"""
                        r_0 = \frac{{a_{{n-1}}}}{{a_n}} =
                        \frac{{{an1:.8f}}}{{{an:.8f}}}
                        = {r0:.8f}
                        """
                    )

                    st.latex(
                        rf"""
                        s_0 = \frac{{a_{{n-2}}}}{{a_n}} =
                        \frac{{{an2:.8f}}}{{{an:.8f}}}
                        = {s0:.8f}
                        """
                    )

                iteraciones_locales = bloque_data["iteraciones"]

                # =====================================================
                # ITERACIONES
                # =====================================================
                for it in iteraciones_locales:

                    st.markdown(f"## Iteración {it['iter'] + 1}")

                    r = it["r_old"]
                    s = it["s_old"]

                    b = it["b"]
                    c = it["c"]

                    n = len(b) - 1

                    # =====================================================
                    # B
                    # =====================================================
                    st.markdown("### Coeficientes b")

                    st.latex(f"b_{{{n}}} = a_{{{n}}} = {b[n]:.8f}")

                    st.latex(
                        f"b_{{{n-1}}} = a_{{{n-1}}} + r b_{{{n}}} = "
                        f"{a[n-1]:.8f} + ({r:.8f})({b[n]:.8f}) = {b[n-1]:.8f}"
                    )

                    for i in range(n - 2, -1, -1):
                        st.latex(
                            f"b_{{{i}}} = a_{{{i}}} + r b_{{{i+1}}} + s b_{{{i+2}}} = "
                            f"{a[i]:.8f} + ({r:.8f})({b[i+1]:.8f}) + ({s:.8f})({b[i+2]:.8f}) = {b[i]:.8f}"
                        )

                    # =====================================================
                    # C
                    # =====================================================
                    st.markdown("### Coeficientes c")

                    st.latex(f"c_{{{n}}} = b_{{{n}}} = {c[n]:.8f}")

                    st.latex(
                        f"c_{{{n-1}}} = b_{{{n-1}}} + r c_{{{n}}} = "
                        f"{b[n-1]:.8f} + ({r:.8f})({c[n]:.8f}) = {c[n-1]:.8f}"
                    )

                    for i in range(n - 2, 0, -1):
                        st.latex(
                            f"c_{{{i}}} = b_{{{i}}} + r c_{{{i+1}}} + s c_{{{i+2}}} = "
                            f"{b[i]:.8f} + ({r:.8f})({c[i+1]:.8f}) + ({s:.8f})({c[i+2]:.8f}) = {c[i]:.8f}"
                        )

                    # =====================================================
                    # CORRECCIONES
                    # =====================================================
                    st.markdown("### Correcciones")

                    b0, b1 = it["b"][0], it["b"][1]
                    c1, c2, c3 = it["c"][1], it["c"][2], it["c"][3]

                    st.latex(
                        rf"""
                        \Delta r =
                        \frac{{({b0:.8f})({c3:.8f}) - ({b1:.8f})({c2:.8f})}}
                            {{{c2:.8f}^2 - ({c1:.8f})({c3:.8f})}}
                        =
                        {it['dr']:.8f}
                        """
                    )

                    st.latex(
                        rf"""
                        \Delta s =
                        \frac{{({b1:.8f})({c1:.8f}) - ({b0:.8f})({c2:.8f})}}
                            {{{c2:.8f}^2 - ({c1:.8f})({c3:.8f})}}
                        =
                        {it['ds']:.8f}
                        """
                    )

                    st.latex(
                        rf"""
                        r_{{nuevo}} =
                        {it['r_old']:.8f}
                        + ({it['dr']:.8f})
                        =
                        {it['r']:.8f}
                        """
                    )

                    st.latex(
                        rf"""
                        s_{{nuevo}} =
                        {it['s_old']:.8f}
                        + ({it['ds']:.8f})
                        =
                        {it['s']:.8f}
                        """
                    )

                    # =====================================================
                    # RAÍCES
                    # =====================================================
                    st.markdown("### Raíces")

                    st.latex(
                        f"x = \\frac{{{it['r']:.8f} \\pm \\sqrt{{({it['r']:.8f})^2 + 4({it['s']:.8f})}}}}{{2}}"
                    )

                    if isinstance(it["x1"], complex):

                        st.latex(
                            f"x_1 = {it['x1'].real:.8f}"
                            f"{'+' if it['x1'].imag >= 0 else '-'}"
                            f"{abs(it['x1'].imag):.8f}i"
                        )

                        st.latex(
                            f"x_2 = {it['x2'].real:.8f}"
                            f"{'+' if it['x2'].imag >= 0 else '-'}"
                            f"{abs(it['x2'].imag):.8f}i"
                        )

                    else:
                        st.latex(f"x_1 = {it['x1']:.8f}")
                        st.latex(f"x_2 = {it['x2']:.8f}")

                    if it["error_x1"] is not None:
                        st.latex(f"E_{{x1}} = {it['error_x1']:.8f}\\%")
                        st.latex(f"E_{{x2}} = {it['error_x2']:.8f}\\%")

                    st.markdown("---")

                # =====================================================
                # FACTOR FINAL
                # =====================================================
                r_final = limpiar(bloque_data["factor_r"])
                s_final = limpiar(bloque_data["factor_s"])

                st.markdown("## Factor cuadrático final")

                st.latex(
                    f"x^2 - ({r_final:.8f})x - ({s_final:.8f})"
                )

                factor = x**2 - r_final * x - s_final

                grado_actual = len(polinomio_actual) - 1

                poly_actual = sum(
                    polinomio_actual[i] * x**(grado_actual - i)
                    for i in range(len(polinomio_actual))
                )

                st.latex(
                    f"\\frac{{{sp.latex(sp.expand(poly_actual))}}}{{{sp.latex(sp.expand(factor))}}}"
                )

                # cociente REAL en orden ascendente
                cociente = bloque_data["cociente"]

                # solo para mostrar
                cociente_desc = cociente[::-1]

                poly_cociente = sum(
                    cociente_desc[i] * x**(len(cociente_desc)-1-i)
                    for i in range(len(cociente_desc))
                )

                st.latex(f"= {sp.latex(sp.expand(poly_cociente))}")

                # mantener orden ascendente internamente
                polinomio_actual = cociente[::-1]

            # =====================================================
            # FINAL
            # =====================================================
            if len(polinomio_actual) == 2:

                st.markdown("# Polinomio lineal restante")

                a0, a1 = polinomio_actual

                st.latex(f"{a0:.8f}x + ({a1:.8f}) = 0")
                st.latex(f"x = -\\frac{{{a1:.8f}}}{{{a0:.8f}}}")
        # =====================================================
        # RESULTADOS
        # =====================================================

        if len(raices) == 0:
            st.warning("No se encontraron raíces reales.")
        else:
            st.success("Raíces reales aproximadas:")
            for i, r in enumerate(raices, start=1):
                st.latex(f"x_{i} = {r:.8f}")

        st.markdown("## Todas las raíces")

        for i, r in enumerate(raices_completas, start=1):

            if isinstance(r, complex):

                if abs(r.imag) < 1e-10:
                    st.latex(f"x_{i} = {r.real:.8f}")
                else:
                    st.latex(
                        f"x_{i} = {r.real:.8f}"
                        f"{'+' if r.imag >= 0 else '-'}"
                        f"{abs(r.imag):.8f}i"
                    )
            else:
                st.latex(f"x_{i} = {r:.8f}")