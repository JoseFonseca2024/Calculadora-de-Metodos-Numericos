import streamlit as st
import pandas as pd
import numpy as np
# Importación de utilidades (Asegúrate de que funciones.py esté en la carpeta utils)
from utils.funciones import validar_y_preparar_funcion
# Importación de la lógica del método
from metodos.muller import ejecutar_muller
# Importación de servicios y gráficas
from Services.procesamiento import filtrar_iteraciones
from plot.graficas import graficar_muller
from Services.exportar_excel import exportar_excel_muller

def mostrar_muller():
    st.title("Método de Muller")
    
    st.markdown("""
    Este método encuentra raíces mediante una aproximación parabólica a través de tres puntos. 
    Es ideal para encontrar raíces reales y complejas.
    """)

    funcion_str = st.text_input("Introduzca f(x):", placeholder="Ej: x^3 - x - 1")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        x0 = st.number_input("x₀:", value=0.0, format="%.4f")
    with col2:
        x1 = st.number_input("x₁:", value=0.5, format="%.4f")
    with col3:
        x2 = st.number_input("x₂:", value=1.0, format="%.4f")

    tol = st.number_input("Tolerancia (%)", value=0.0001, format="%.5f")

    if st.button("Calcular"):
        # 1. Validación de la función
        valido, error_msg, datos = validar_y_preparar_funcion(funcion_str)
        if not valido:
            st.error(error_msg)
            return

        # Desempaquetado de datos (f_num es la función, f_visual es el LaTeX)
        _, _, f_num, _, f_visual = datos

        # 2. Ejecución del algoritmo
        ok, msg, iteraciones = ejecutar_muller(f_num, x0, x1, x2, tol)
        if not ok:
            st.error(msg)
            return

        # 3. Mostrar la función procesada
        st.subheader("Función:")
        st.latex(f"f(x) = {f_visual}")

        # 4. Evaluación inicial (Tu estilo de diseño)
        st.subheader("Evaluación inicial")
        f_x0, f_x1, f_x2 = f_num(x0), f_num(x1), f_num(x2)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a: st.latex(f"f(x_0) = {f_x0:.8f}")
        with col_b: st.latex(f"f(x_1) = {f_x1:.8f}")
        with col_c: st.latex(f"f(x_2) = {f_x2:.8f}")

        # 5. Procedimiento detallado (LaTeX dinámico)
        with st.expander("Ver procedimiento detallado paso a paso", expanded=False):
            for it in iteraciones:
                idx = it["i"]
                st.markdown(f"### **Iteración {idx + 1}**")
                
                # 1. Definición de puntos actuales
                st.write("1. **Identificación de puntos y evaluación:**")
                st.latex(f"x_0 = {it['x0']:.6f}, \\quad x_1 = {it['x1']:.6f}, \\quad x_2 = {it['x2']:.6f}")
                st.latex(f"f(x_0) = {it['f(x0)']:.6f}, \\quad f(x_1) = {it['f(x1)']:.6f}, \\quad f(x_2) = {it['f(x2)']:.6f}")

                # 2. Cálculo de diferencias (Las h y d)
                # Nota: Estos valores los calcula tu lógica de muller.py, asegúrate de que existan en el diccionario 'it'
                h1, h2 = it['x1'] - it['x0'], it['x2'] - it['x1']
                d1, d2 = (it['f(x1)'] - it['f(x0)']) / h1, (it['f(x2)'] - it['f(x1)']) / h2
                
                st.write("2. **Cálculo de diferencias y pendientes:**")
                st.latex(f"h_1 = x_1 - x_0 = {h1:.6f}, \\quad h_2 = x_2 - x_1 = {h2:.6f}")
                st.latex(f"d_1 = \\frac{{f(x_1) - f(x_0)}}{{h_1}} = {d1:.6f}, \\quad d_2 = \\frac{{f(x_2) - f(x_1)}}{{h_2}} = {d2:.6f}")

                # 3. Coeficientes a, b, c
                st.write("3. **Cálculo de los coeficientes de la parábola:**")
                st.latex(f"a = \\frac{{d_2 - d_1}}{{h_2 + h_1}} = \\frac{{{d2:.6f} - ({d1:.6f})}}{{{h2:.6f} + {h1:.6f}}} = {it['a']:.8f}")
                st.latex(f"b = a h_2 + d_2 = ({it['a']:.6f})({h2:.6f}) + {d2:.6f} = {it['b']:.8f}")
                st.latex(f"c = f(x_2) = {it['c']:.8f}")

                # 4. Sustitución en la fórmula de Muller
                st.write("4. **Sustitución en la fórmula cuadrática de Muller:**")
                # Mostramos la fórmula con los valores reales sustituidos
                discriminante_val = it['b']**2 - 4*it['a']*it['c']
                # Usamos abs() para el denominador mayor para que el LaTeX no se rompa
                st.latex(r"x_3 = x_2 + \frac{-2c}{b \pm \sqrt{b^2 - 4ac}}")
                st.latex(
                    f"x_{{{idx+3}}} = {it['x2']:.6f} + \\frac{{-2({it['c']:.6f})}}{{{it['b']:.6f} \\pm \\sqrt{{({it['b']:.6f})^2 - 4({it['a']:.6f})({it['c']:.6f})}}}}"
                )

                # 5. Resultado de la aproximación
                st.write("5. **Resultado de la iteración:**")
                val_x3 = it['x3']
                # Si es complejo, lo mostramos bonito
                if isinstance(val_x3, complex):
                    st.latex(f"x_{{{idx+3}}} = {val_x3.real:.8f} + {val_x3.imag:.8f}i")
                else:
                    st.latex(f"x_{{{idx+3}}} = {val_x3:.8f}")
                
                st.latex(f"Error = {it['Error%']:.8f}\\%")
                st.markdown("---")

        # 6. Tabla de Iteraciones
        iteraciones_visibles = filtrar_iteraciones(iteraciones, tol)
        st.subheader("Tabla de Iteraciones")
        df_mostrar = pd.DataFrame(iteraciones_visibles)
        st.dataframe(df_mostrar)

        # 7. Resultado final
        raiz_final = iteraciones_visibles[-1]['x3']
        st.success(f"Raíz aproximada: {raiz_final}")

        # 8. Gráfica
        st.subheader("Visualización del Método")
        fig = graficar_muller(f_num, iteraciones_visibles)
        st.pyplot(fig)

        # 9. Exportación a Excel (Usando tu procesador universal)
        excel_bytes = exportar_excel_muller(
            df_mostrar,
            f_num,
            iteraciones_visibles
        )

        st.download_button(
            label="📊 Descargar Excel",
            data=excel_bytes,
            file_name="Reporte_Muller.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )