import streamlit as st
import sympy as sp
from utils.polinomios import validar_Y_preparar_polinomio
from metodos.bairstow import ejecutar_bairstow

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
        valido, error_msg, datos = validar_Y_preparar_polinomio(polinomio_str)

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

        st.subheader("Polinomio:")
        st.latex(f"f(x) = {sp.latex(p_sym)}")

        st.write(f"Grado: {grado}")
        st.write(f"Coeficientes: {coeficientes}")

        # 🔹 PROCEDIMIENTO DETALLADO
        with st.expander("Ver procedimiento", expanded=False):
            st.markdown("## Datos iniciales")
            for i, coef in enumerate(coeficientes):
                st.latex(f"a_{len(coeficientes)-1-i} = {coef}")

            for it in iteraciones:
                st.markdown(f"# Iteración {it['iter']} (modo: {it['modo']})")

                r = it["r_old"]
                s = it["s_old"]
                b = it["b"]
                c = it["c"]

                if it["iter"] == 0:
                    if it["modo"] == "pequeñas":
                        st.latex(f"r_0 = a_1/a_2 = ({coeficientes[-2]})/({coeficientes[-3]}) = {r:.8f}")
                        st.latex(f"s_0 = a_0/a_2 = ({coeficientes[-1]})/({coeficientes[-3]}) = {s:.8f}")
                    elif it["modo"] == "grandes":
                        st.latex(f"r_0 = a_(n-1)/a_n = ({coeficientes[1]})/({coeficientes[0]}) = {r:.8f}")
                        st.latex(f"s_0 = a_(n-2)/a_n = ({coeficientes[2]})/({coeficientes[0]}) = {s:.8f}")

                # 🔹 b
                st.markdown("### Coeficientes b")
                n = len(b) - 1
                st.latex(f"b_{n} = a_{n} = {b[n]:.8f}")
                st.latex(
                    f"b_{n-1} = a_{n-1} + r b_{n} = "
                    f"{coeficientes[-3]} + ({r:.8f})({b[n]:.8f}) = {b[n-1]:.8f}"
                )
                for i in range(n-2, -1, -1):
                    st.latex(
                        f"b_{i} = a_{i} + r b_{i+1} + s b_{i+2} = "
                        f"{coeficientes[::-1][i]} + ({r:.8f})({b[i+1]:.8f}) + ({s:.8f})({b[i+2]:.8f}) = {b[i]:.8f}"
                    )

                # 🔹 c
                st.markdown("### Coeficientes c")
                st.latex(f"c_{n} = b_{n} = {c[n]:.8f}")
                st.latex(
                    f"c_{n-1} = b_{n-1} + r c_{n} = "
                    f"{b[n-1]:.8f} + ({r:.8f})({c[n]:.8f}) = {c[n-1]:.8f}"
                )
                for i in range(n-2, 0, -1):
                    st.latex(
                        f"c_{i} = b_{i} + r c_{i+1} + s c_{i+2} = "
                        f"{b[i]:.8f} + ({r:.8f})({c[i+1]:.8f}) + ({s:.8f})({c[i+2]:.8f}) = {c[i]:.8f}"
                    )

                # 🔹 Correcciones
                st.markdown("### Correcciones")
                st.latex(
                    f"\\Delta r = \\frac{{({b[0]:.8f})({c[3]:.8f}) - ({b[1]:.8f})({c[2]:.8f})}}"
                    f"{{({c[2]:.8f})^2 - ({c[1]:.8f})({c[3]:.8f})}} = {it['dr']:.8f}"
                )
                st.latex(
                    f"\\Delta s = \\frac{{({b[1]:.8f})({c[1]:.8f}) - ({b[0]:.8f})({c[2]:.8f})}}"
                    f"{{({c[2]:.8f})^2 - ({c[1]:.8f})({c[3]:.8f})}} = {it['ds']:.8f}"
                )

                st.latex(f"r_{{nuevo}} = {r:.8f} + {it['dr']:.8f} = {it['r']:.8f}")
                st.latex(f"s_{{nuevo}} = {s:.8f} + {it['ds']:.8f} = {it['s']:.8f}")

                # 🔹 raíces
                st.markdown("### Raíces")
                st.latex(
                    f"x = \\frac{{{it['r']:.8f} \\pm \\sqrt{{({it['r']:.8f})^2 + 4({it['s']:.8f})}}}}{{2}}"
                )
                if isinstance(it["x1"], complex):
                    st.latex(f"x_1 = {it['x1'].real:.8f} + {it['x1'].imag:.8f}i")
                    st.latex(f"x_2 = {it['x2'].real:.8f} - {it['x2'].imag:.8f}i")
                else:
                    st.latex(f"x_1 = {it['x1']:.8f}")
                    st.latex(f"x_2 = {it['x2']:.8f}")

                if it["error_x1"] is not None:
                    st.latex(f"E_{{x1}} = {it['error_x1']:.8f}\\%")
                    st.latex(f"E_{{x2}} = {it['error_x2']:.8f}\\%")

                st.markdown("---")

        # 🔹 RESULTADO FINAL
        st.success("Raíces aproximadas:")
        for i, r in enumerate(raices, 1):
            if isinstance(r, complex):
                st.latex(f"x_{i} = {r.real:.8f} {'+' if r.imag >= 0 else '-'} {abs(r.imag):.8f}i")
            else:
                st.latex(f"x_{i} = {r:.8f}")