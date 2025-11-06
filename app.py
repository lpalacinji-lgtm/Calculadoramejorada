import streamlit as st
from datetime import datetime
from calculator import calcular_tabletas, calcular_ampollas
from PIL import Image
import pytz

# ======================================
# CONFIGURACIÓN GENERAL
# ======================================
st.set_page_config(
    page_title="Calculadora de Medicamentos 💊",
    layout="wide",
    page_icon="💉"
)

# ======================================
# ESTILO HOSPITALARIO AZUL + AVISO DESTACADO
# ======================================
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1300px;
        }
        h1 {
            color: #005b96;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }
        h2, h3 {
            color: #0074cc;
            margin-bottom: 0.4rem;
        }
        button[kind="primary"] {
            background-color: #0074cc !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.35rem 0.8rem !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }
        button[kind="primary"]:hover {
            background-color: #000000 !important;
        }
        [data-testid="stMetric"] {
            background-color: #e7f1fb;
            border-radius: 10px;
            padding: 0.4rem;
            border: 1px solid #b6d4f0;
        }
        div[data-testid="stMetricValue"] {
            color: #005b96;
            font-size: 1.3rem;
            font-weight: 700;
        }
        .logo-title-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ======================================
# ENCABEZADO CON LOGO Y TÍTULO CENTRADO
# ======================================
col_logo, col_title = st.columns([0.12, 1])
with col_logo:
    logo = Image.open("Logo/LOGO HORIZONTAL.png")
    st.image(logo, width=120)

with col_title:
    st.markdown("""
        <div class="logo-title-container">
            <h1>💊 Calculadora de Dispensación Médica</h1>
        </div>
        <p style='margin-top:-0.8rem; color:gray; font-size:0.9rem;'>SISTEMAS DE INFORMACIÓN</p>
    """, unsafe_allow_html=True)

# ======================================
# LAYOUT PRINCIPAL
# ======================================
col_form, col_result = st.columns([1.1, 1])

# ======================================
# COLUMNA IZQUIERDA — FORMULARIO
# ======================================
with col_form:
    st.subheader("🧾 Datos del Medicamento")

    tipo = st.selectbox("Tipo:", ["Tableta 💊", "Ampolla 💉"])
    frecuencia = st.number_input("Frecuencia (horas):", min_value=1, max_value=24, value=8)
    duracion = st.number_input("Duración (días):", min_value=1, max_value=120, value=1)

    # ✅ Fecha local ajustada a zona horaria de Colombia
    zona_colombia = pytz.timezone("America/Bogota")
    fecha_local = datetime.now(zona_colombia).date()
    fecha_orden = st.date_input("Fecha de orden:", fecha_local)

    inicio_mismo_dia = st.checkbox("Inicia el mismo día", value=True)
    st.caption("Si no marca Check, inicia el día siguiente.")

    st.divider()

    if tipo == "Tableta 💊":
        dosis_toma = st.number_input("Dosis por toma (tabletas):", min_value=0.25, step=0.25, value=1.0)
        unidades_presentacion = st.number_input("Unidades por caja:", min_value=1, step=1, value=30)
        calcular = st.button("🧮 Calcular Tabletas", use_container_width=True)
    else:
        dosis_inyeccion = st.number_input("Dosis por inyección (ml):", min_value=0.1, step=0.1, value=1.0)
        calcular = st.button("🧮 Calcular Ampollas", use_container_width=True)

# ======================================
# COLUMNA DERECHA — RESULTADOS
# ======================================
with col_result:
    st.subheader("📊 Resultados")

    if tipo == "Tableta 💊" and calcular:
        resultados = calcular_tabletas(frecuencia, duracion, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia)

        st.success(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")
        colA, colB, colC = st.columns(3)
        colA.metric("Tomas", resultados["Total de tomas"])
        colB.metric("Tabletas", resultados["Total de tabletas"])
        colC.metric("Presentaciones", resultados["Presentaciones necesarias"])

        st.caption("📆 Distribución mensual:")

        fecha_inicio = datetime.strptime(resultados["Fecha de inicio"], "%Y-%m-%d").date()
        if fecha_inicio.month != fecha_orden.month:
            st.warning(f"📌 Nota: La orden inicia en el mes siguiente ({fecha_inicio.strftime('%B')}). Todas las tabletas se asignan a ese mes.")

        st.markdown(f"""
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px; margin-bottom:0.5rem;'>
                <strong>📌 Este mes:</strong> {resultados['Tabletas este mes']} tabletas
            </div>
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px;'>
                <strong>📌 Próximo mes:</strong> {resultados['Tabletas próximo mes']} tabletas
            </div>
        """, unsafe_allow_html=True)

    elif tipo == "Ampolla 💉" and calcular:
        resultados = calcular_ampollas(frecuencia, duracion, dosis_inyeccion, fecha_orden, inicio_mismo_dia)

        st.success(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")
        colA, colB = st.columns(2)
        colA.metric("Inyecciones", resultados["Total de inyecciones"])
        colB.metric("Ampollas utilizadas", resultados["Ampollas necesarias"])

        st.caption("📆 Distribución mensual:")

        fecha_inicio = datetime.strptime(resultados["Fecha de inicio"], "%Y-%m-%d").date()
        if fecha_inicio.month != fecha_orden.month:
            st.warning(f"📌 Nota: La orden inicia en el mes siguiente ({fecha_inicio.strftime('%B')}). Todas las ampollas se asignan a ese mes.")

        st.markdown(f"""
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px; margin-bottom:0.5rem;'>
                <strong>📌 Este mes:</strong> {resultados['Ampollas este mes']} ampolla(s) ({resultados['Dosis por inyección (ml)']} ml)
            </div>
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px;'>
                <strong>📌 Próximo mes:</strong> {resultados['Ampollas próximo mes']} ampolla(s) ({resultados['Dosis por inyección (ml)']} ml)
            </div>
        """, unsafe_allow_html=True)





