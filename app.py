import streamlit as st

from views.inicio_view import mostrarInicio
from views.newton_raphson_view import mostrar_newton_raphson
from views.secante_view import mostrar_secante

st.set_page_config(
    page_title="Calculadora de Métodos Numéricos",
    layout="wide"
)

st.sidebar.markdown("Menú")

if "metodo" not in st.session_state:
    st.session_state.metodo = None

# Aproximación
with st.sidebar.expander("Aproximación de un valor"):
    if st.button("Serie de Taylor", key = "btn_SerieTaylor"):
        st.session_state.metodo = "Serie de Taylor"

# Raíces
with st.sidebar.expander("Raíces de ecuaciones no lineales", expanded=True):

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

# Mostrar contenido
if st.session_state.metodo is None:
    mostrarInicio()

elif st.session_state.metodo == "Newton-Raphson":
    mostrar_newton_raphson()

elif st.session_state.metodo == "Secante":
    mostrar_secante()