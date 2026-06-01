import streamlit as st

from utils.funciones import validar_y_preparar_funcion
from metodos.Polinomios_y_Funciones.biseccion import ejecutar_biseccion
from plot.graficas import graficar_metodo_cerrado
from Services.exportar_excel import exportar_excel_biseccion
from Services.procesamiento import convertir_biseccion_a_tabla


def mostrar_biseccion():
    st.title("Método de Bisección")

    funcion_str = st.text_input(
        "Introduzca una función f(x):",
        placeholder="Ej: x^2 - 10*cos(x) - 2",
        key="bis_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Límite inferior (a):", value=0.0, format="%.4f", key="bis_a")
    with col2:
        b = st.number_input("Límite superior (b):", value=1.0, format="%.4f", key="bis_b")
        
    tol = st.number_input("Tolerancia (%)", value=0.00001, format="%.5f", key="bis_tol")

    if st.button("Calcular"):

        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)

        if not valido:
            st.error(error_msg)
            return

        _, _, f_num, _, f_visual = datos

        ok, msg, iteraciones = ejecutar_biseccion(f_num, a, b, tol)

        if not ok:
            st.error(msg)
            return

        st.subheader("Función")
        st.latex(f"f(x) = {f_visual}")

        # 🔹 Evaluación inicial (UNA SOLA VEZ)
        fa_init = float(f_num(a))
        fb_init = float(f_num(b))

        f_a_sust = f_visual.replace("x", f"({a:.6f})")
        f_b_sust = f_visual.replace("x", f"({b:.6f})")

        st.markdown("### Evaluación en los extremos del intervalo")

        st.latex(f"f(a) = {f_visual}")
        st.latex(f"f(a) = {f_a_sust}")
        st.latex(f"f(a) = {fa_init:.6f}")

        st.latex(f"f(b) = {f_visual}")
        st.latex(f"f(b) = {f_b_sust}")
        st.latex(f"f(b) = {fb_init:.6f}")

        # 🔹 Procedimiento
        st.subheader("Procedimiento Paso a Paso")

        with st.expander("Ver cálculos detallados", expanded=False):

            st.markdown("### Evaluación Inicial")
            st.latex(f"f(a) = f({a:.4f}) = {fa_init:.6f}")
            st.latex(f"f(b) = f({b:.4f}) = {fb_init:.6f}")

            if fa_init * fb_init > 0:
                st.error("No hay cambio de signo en el intervalo inicial.")
            else:
                st.success("Cambio de signo detectado ($f(a) \\cdot f(b) < 0$).")

            st.markdown("---")
            st.markdown("### Iteraciones")

            for i, it in enumerate(iteraciones):

                idx = it.get('i', i) + 1
                a_i = it['a']
                b_i = it['b']
                c = it['Ci']
                fc = it['f(Ci)']

                st.write(f"#### Iteración {idx}")

                st.latex(
                    f"c_{{{idx}}} = \\frac{{{a_i:.6f} + {b_i:.6f}}}{{2}} = {c:.6f}"
                )

                f_sust = f_visual.replace("x", f"({c:.6f})")

                st.latex(f"f(c_{{{idx}}}) = {f_sust}")
                st.latex(f"f(c_{{{idx}}}) = {fc:.6f}")

                if i < len(iteraciones) - 1:
                    proxima = iteraciones[i+1]
                    if proxima['a'] == c:
                        st.info(f"Como $f(a) \cdot f(c) > 0$, la raíz está en $[c, b]$. Nuevo intervalo: $[{proxima['a']:.6f}, {proxima['b']:.6f}]$")
                    else:
                        st.info(f"Como $f(a) \cdot f(c) < 0$, la raíz está en $[a, c]$. Nuevo intervalo: $[{proxima['a']:.6f}, {proxima['b']:.6f}]$")
                st.markdown("---")

        # 🔹 TABLA
        df = convertir_biseccion_a_tabla(iteraciones)

        st.subheader("Tabla de Iteraciones")

        st.dataframe(
            df.style.format({
                "a": "{:.6f}",
                "b": "{:.6f}",
                "c": "{:.6f}",
                "f(a)": "{:.6f}",
                "f(b)": "{:.6f}",
                "f(c)": "{:.6f}",
                "f(a)*f(c)": "{:.6e}",
                "Ea%": "{:.5f}%"
            })
        )

        # 🔹 Resultado
        raiz = df.iloc[-1]["c"]
        st.success(f"Raíz aproximada: {raiz:.6f}")

        # 🔹 Gráfica
        fig = graficar_metodo_cerrado(f_num, iteraciones, "Bisección")
        st.plotly_chart(fig, use_container_width=True)

        # 🔹 Exportar
        excel_bytes = exportar_excel_biseccion(df, f_num, iteraciones)

        st.download_button(
            "📊 Descargar Excel",
            excel_bytes,
            "Biseccion.xlsx"
        )