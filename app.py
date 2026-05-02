import streamlit as st
# Importación de las vistas (asegúrate de que los nombres de archivos coincidan)
from views.inicio_view import mostrarInicio
from views.taylor_view import mostrar_taylor 
from views.biseccion_view import mostrar_biseccion
from views.regla_falsa_view import mostrar_regla_falsa
from views.newton_raphson_view import mostrar_newton_raphson
from views.secante_view import mostrar_secante
from views.punto_fijo_view import mostrar_punto_fijo
from views.bairstow_view import mostrar_bairstow

# Configuración de la página
st.set_page_config(page_title="Calculadora Métodos Numéricos", layout="wide")

# Inicialización del estado del método en la sesión
if "metodo" not in st.session_state:
    st.session_state.metodo = None

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Menú de Métodos")

with st.sidebar.expander("Unidad 1: Teoría de Errores", expanded=True):
    if st.button("Serie de Taylor", key="btn_taylor", use_container_width=True):
        st.session_state.metodo = "Taylor"

with st.sidebar.expander("Unidad 2: Raíces de Ecuaciones", expanded=True):
    if st.button("Bisección", key="btn_biseccion", use_container_width=True):
        st.session_state.metodo = "Bisección"
    
    if st.button("Regla Falsa", key="btn_regla_falsa", use_container_width=True):
        st.session_state.metodo = "Regla Falsa"
    
    if st.button("Newton-Raphson", key="btn_newton", use_container_width=True):
        st.session_state.metodo = "Newton"
    
    if st.button("Secante", key="btn_secante", use_container_width=True):
        st.session_state.metodo = "Secante"
    
    if st.button("Punto Fijo", key="btn_punto_fijo", use_container_width=True):
        st.session_state.metodo = "Punto Fijo"
        
    if st.button("Bairstow", key="btn_bairstow", use_container_width=True):
        st.session_state.metodo = "Bairstow"

# --- LÓGICA DE RENDERIZADO DE VISTAS ---
if st.session_state.metodo == "Taylor":
    mostrar_taylor()
elif st.session_state.metodo == "Bisección":
    mostrar_biseccion()
elif st.session_state.metodo == "Regla Falsa":
    mostrar_regla_falsa()
elif st.session_state.metodo == "Newton":
    mostrar_newton_raphson()
elif st.session_state.metodo == "Secante":
    mostrar_secante()
elif st.session_state.metodo == "Punto Fijo":
    mostrar_punto_fijo()
elif st.session_state.metodo == "Bairstow":
    mostrar_bairstow()
else:
    # Si no hay método seleccionado, muestra la pantalla de inicio
    mostrarInicio()