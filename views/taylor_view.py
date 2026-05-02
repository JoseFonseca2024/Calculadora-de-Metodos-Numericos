import streamlit as st
import pandas as pd
import math
import sympy as sp
from metodos.taylor import ejecutar_taylor
from utils.funciones import validar_y_preparar_funcion
from plot.graficas import graficar_taylor
from Services.exportar_excel import exportar_excel_taylor
from utils.parsers import normalizar_funcion 

def mostrar_taylor():
    st.title("Serie de Taylor - Reporte Académico")
    st.markdown("Calcula el polinomio de aproximación y el error mediante el Resto de Lagrange.")

    # --- ENTRADA DE DATOS ---
    # Las variables se definen aquí (fuera del botón) para que Pylance las reconozca siempre
    funcion_str = st.text_input(
        "Introduzca la función f(x):", 
        value="sin(x)", 
        help="Ejemplos: sin(x), 2x^2 + e^x, log(x). Usa siempre paréntesis."
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Punto de expansión (a):", value=0.0, format="%.4f", help="Centro de la serie (a)")
    with col2:
        n_max = st.number_input("Grado máximo (n):", min_value=0, max_value=20, value=0, help="Grado n del polinomio")
    with col3:
        x_eval = st.number_input("Valor a evaluar (x):", value=0.0, format="%.4f", help="Punto a aproximar")

    tol = st.number_input("Tolerancia (Epsilon):", value=0.0001, format="%.8f")

    if st.button("Calcular Desarrollo Detallado"):
        # 1. Procesamiento con tu parsers.py
        f_limpia = normalizar_funcion(funcion_str)
        
        # 2. LIMPIEZA DE EMERGENCIA (Para evitar: FunctionClass * Symbol)
        # Evita que el parser convierta sin(x) en sin*(x), lo cual rompe SymPy
        f_limpia = f_limpia.replace("sin*(", "sin(").replace("cos*(", "cos(").replace("exp*(", "exp(")
        
        # 3. VALIDACIÓN (Usando tu funciones.py original)
        valido, error_msg, datos = validar_y_preparar_funcion(f_limpia)
        
        if valido:
            # Desempaquetado: (f_sym, x_sym, f_num, f_der_num, f_visual)
            f_sym, x_sym, f_num, f_der_num, f_visual = datos
            
            # 4. EJECUCIÓN DEL MÉTODO
            ok, msg, res = ejecutar_taylor(f_limpia, a, n_max, x_eval)
            
            if ok:
                st.success("✅ Desarrollo generado exitosamente")

                # --- PROCEDIMIENTO PASO A PASO ---
                st.subheader("1. Procedimiento y Construcción")
                polinomio_acumulado = ""
                
                for i, it in enumerate(res["iteraciones"]):
                    with st.expander(f"PASO PARA GRADO n = {i}", expanded=(i == 0)):
                        # Derivada evaluada
                        st.latex(rf"f^{{({i})}}({a}) = {it['f^(i)(a)']:.8f}")
                        
                        # Cálculo del término
                        fact = math.factorial(i)
                        distancia = x_eval - a
                        st.latex(rf"T_{{{i}}} = \frac{{{it['f^(i)(a)']:.8f}}}{{{fact}}} ({distancia:.4f})^{{{i}}} = {it['Termino']}")

                        # Construcción del Polinomio
                        term_str = str(it['Termino'])
                        if i == 0: 
                            polinomio_acumulado = term_str
                        else:
                            signo = " + " if not term_str.startswith('-') else " "
                            polinomio_acumulado += f"{signo}{term_str}"
                        
                        st.latex(rf"P_{{{i}}}(x) = {polinomio_acumulado}")

                # --- TABLA DE RESULTADOS ---
                st.subheader("2. Tabla de Aproximaciones")
                data_tabla = []
                for it in res["iteraciones"]:
                    cumple = "CUMPLE" if it['Error_Abs'] < tol else "NO CUMPLE"
                    data_tabla.append({
                        "Grado (n)": it['i'],
                        "Aproximación Pn(x)": it['Aproximacion'],
                        "Error (Rn)": it['Error_Abs'],
                        "Decisión": cumple
                    })
                
                df_final = pd.DataFrame(data_tabla)
                
                # Formato visual con colores para la decisión
                st.dataframe(
                    df_final.style.format({
                        "Aproximación Pn(x)": "{:.8f}",
                        "Error (Rn)": "{:.8f}"
                    }).map(lambda v: f'background-color: {"#d4edda" if v == "CUMPLE" else "#f8d7da"}', subset=['Decisión']),
                    use_container_width=True
                )

                # --- GRÁFICA ---
                st.subheader("3. Comportamiento Gráfico")
                st.pyplot(graficar_taylor(f_num, res["poly_func_num"], x_eval, a))

                # --- EXCEL ---
                # Preparamos los datos para tu exportador de Taylor
                df_excel = df_final.rename(columns={
                    'Grado (n)': 'i',
                    'Aproximación Pn(x)': 'aprox',
                    'Error (Rn)': 'error',
                    'Decisión': 'decision'
                })
                excel_bytes = exportar_excel_taylor(df_excel, f_num, res["poly_func_num"], x_eval, a)
                st.download_button("📥 Descargar Reporte Excel", excel_bytes, f"Taylor_{f_limpia}.xlsx", use_container_width=True)

            else:
                st.error(f"Error en Taylor: {msg}")
        else:
            st.error(f"Error en funciones.py: {error_msg}")