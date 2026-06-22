import streamlit as st
import pandas as pd

from views.inicio_view import mostrarInicio
from views.RaicesEnoL.biseccion_view import mostrar_biseccion
from views.RaicesEnoL.regla_falsa_view import mostrar_regla_falsa
from views.RaicesEnoL.newton_raphson_view import mostrar_newton_raphson
from views.RaicesEnoL.secante_view import mostrar_secante
from views.RaicesEnoL.punto_fijo_view import mostrar_punto_fijo
from views.RaicesPol.bairstow_view import mostrar_bairstow
from views.Aproximacion.taylor_view import mostrar_taylor
from views.RaicesPol.muller_views import mostrar_muller
from views.RaicesPol.newton_horner_view import mostrar_newton_horner
from views.SEL.jacobi_view import mostrarJacobi
from views.SEL.gaussseidel_view import mostrargaussSeidel
from views.Interpolacion.PolNewton_view import mostrarPolNewton
from views.Interpolacion.PolLagrange_view import mostrarPolLagrange
from views.Interpolacion.TrazadoresCubic_view import mostrarTrazadoresCubicos
from views.Integrales.trapecio_view import mostrarRegladelTrapecio
from views.Integrales.Simpson13_view import mostrarSimpson1_3
from views.Integrales.Simpson3_8_view import mostrarSimpson3_8

if "ultimo_metodo" not in st.session_state:
    st.session_state.ultimo_metodo = None

st.set_page_config(
    page_title="Calculadora de Métodos Numéricos",
    layout="wide"
)

st.sidebar.markdown("Menú")

if "metodo" not in st.session_state:
    st.session_state.metodo = None

# Aproximación
with st.sidebar.expander("Aproximación de un valor", expanded = False):
    if st.button("Serie de Taylor", key = "btn_SerieTaylor"):
        st.session_state.metodo = "Serie de Taylor"

# Raíces
with st.sidebar.expander("Raíces de ecuaciones no lineales", expanded=False):

    st.markdown("Métodos Cerrados")
    if st.button("Bisección", key = "btn_Bisección"):
        st.session_state.metodo = "Bisección"
    if st.button("Regla Falsa"):
        st.session_state.metodo = "Regla Falsa"

    st.markdown("Métodos Abiertos")
    if st.button("Newton-Raphson"):
        st.session_state.metodo = "Newton-Raphson"
    if st.button("Secante"):
        st.session_state.metodo = "Secante"
    if st.button("Punto Fijo"):
        st.session_state.metodo = "Punto Fijo"

with st.sidebar.expander("Raices de un polinomio", expanded=False):
    if st.button("Metodo de Bairstow", key = "btnBairstow"):
        st.session_state.metodo = "Bairstow"
    if st.button("Muller"):
        st.session_state.metodo = "Muller"
    if st.button("Newton-Horner"):
        st.session_state.metodo = "Newton-Horner"

#SEL
with st.sidebar.expander("Sistema de Ecuaciones Lineales", expanded=False):
    if st.button("Metodo de Jacobi", key = "btnJacobi"):
        st.session_state.metodo = "Jacobi"
    if st.button("Metodo de Gauss-Seibel"):
        st.session_state.metodo = "Gauss-Seibel"

#Ajuste por interpolación
with st.sidebar.expander("Ajuste de funciones por interpolación", expanded=False):
    st.markdown("Ajuste de curvas discretas por minimos cuadrados")
    if st.button("Modelo de regresión simple", key = "btnRegresionSimple"):
        st.session_state.metodo = "Regresión simple"

    if st.button("Modelo de regresión cuadratica", key = "btnRegresionCuadratica"):
        st.session_state.metodo = "Regresión Cuadratica"

    st.markdown("Ajuste por polinomios interpolares")
    if st.button("Polinomio de Newton por diferencias divididas", key = "btnPolNewton"):
        st.session_state.metodo = "Polinomio de Newton"

    if st.button("Polinomio interpolante de lagrange", key = "btnPolLagrange"):
        st.session_state.metodo = "Polinimio de Lagrange"
    
    if st.button("Interpolación por trazadores cubicos", key = "btnTrazCub"):
        st.session_state.metodo = "Trazadores cubicos"

#Integración por aproximación
with st.sidebar.expander("Integración por aproximación", expanded= False):
    if st.button("Regla del Trapecio", key = "btnRegladelTrapecio"):
        st.session_state.metodo = "Regla del Trapecio"
    if st.button("Simpson 1/3", key="btnSimpson1/3"):
        st.session_state.metodo = "Simpson 1/3"
    if st.button("Simpson 3/8", key="btnSimpson3/8"):
        st.session_state.metodo = "Simpson 3/8"


# CAMBIO DE MÉTODO

if st.session_state.metodo != st.session_state.ultimo_metodo:

    if st.session_state.metodo == "Polinomio de Newton":

        st.session_state.tabla_newton = pd.DataFrame(
            {
                "x": [None],
                "f(x)": [None]
            }
        )

        if "editor_newton" in st.session_state:
            del st.session_state["editor_newton"]

    st.session_state.ultimo_metodo = st.session_state.metodo

# Mostrar contenido
if st.session_state.metodo is None:
    mostrarInicio()

elif st.session_state.metodo == "Serie de Taylor":
    mostrar_taylor()

elif st.session_state.metodo == "Newton-Raphson":
    mostrar_newton_raphson()

elif st.session_state.metodo == "Secante":
    mostrar_secante()

elif st.session_state.metodo == "Bisección":
    mostrar_biseccion()

elif st.session_state.metodo == "Regla Falsa":
    mostrar_regla_falsa()
elif st.session_state.metodo == "Punto Fijo":
    mostrar_punto_fijo()
elif st.session_state.metodo == "Bairstow":
    mostrar_bairstow()
elif st.session_state.metodo == "Muller": 
    mostrar_muller()
elif st.session_state.metodo == "Newton-Horner": 
    mostrar_newton_horner()
elif st.session_state.metodo == "Jacobi":
    mostrarJacobi()
elif st.session_state.metodo == "Gauss-Seibel":
    mostrargaussSeidel()
elif st.session_state.metodo == "Polinomio de Newton":
    mostrarPolNewton()
elif st.session_state.metodo == "Polinimio de Lagrange":
    mostrarPolLagrange()
elif st.session_state.metodo == "Trazadores cubicos":
    mostrarTrazadoresCubicos()
elif st.session_state.metodo == "Regla del Trapecio":
    mostrarRegladelTrapecio()
elif st.session_state.metodo == "Simpson 1/3":
    mostrarSimpson1_3()
elif st.session_state.metodo == "Simpson 3/8":
    mostrarSimpson3_8()