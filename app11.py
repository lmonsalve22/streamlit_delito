import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from urllib.parse import unquote
from data import get_data, get_comuna
from stylo import set_custom_styles
import datetime
import time

# Función para formatear números con separadores de miles en formato chileno
def format_number_chile(number):
    """Formatea un número con puntos como separadores de miles (formato chileno)"""
    if isinstance(number, (int, float)):
        return "{:,.0f}".format(number).replace(",", ".")
    return number

# Función para obtener parámetros de la URL
def get_url_params():
    query_params = st.query_params
    params = {}
    if 'codcom' in query_params:
        try:
            params['codcom'] = int(unquote(query_params['codcom']))
        except (ValueError, TypeError):
            params['codcom'] = 13101
    else:
        params['codcom'] = 13101
    return params

# Obtener parámetros de la URL
url_params = get_url_params()
CODCOM = url_params.get('codcom', 13101)
COMUNA_NAME = get_comuna(CODCOM)

# Configuración de la página
st.set_page_config(
    page_title=f"Análisis de Delincuencia en {COMUNA_NAME}",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados con nueva paleta de colores mejorada
st.markdown("""
<style>
    /* ===== VARIABLES Y CONFIGURACIÓN GENERAL ===== */
    :root {
        /* Nueva paleta de azules (manteniendo tus colores pero organizados) */
        --color-primary: #101967;
        --color-secondary: #2a2e7f;
        --color-tertiary: #454297;
        --color-accent: #5f57af;
        --color-light-accent: #796bc7;
        --color-extra-light: #e6e6fa;
        
        /* Colores funcionales */
        --danger-color: #ef4444;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        
        /* Colores neutros */
        --color-white: #ffffff;
        --color-light: #f8fafc;
        --color-gray: #64748b;
        --color-gray-light: #e2e8f0;
        --color-gray-dark: #334155;
        
        /* Variables de diseño */
        --border-radius: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* ===== RESET Y ESTILOS BASE ===== */
    * {
        box-sizing: border-box;
    }
    /* ===== COMPONENTES DE STREAMLIT ===== */
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: space-between;
        gap: 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, rgba(69, 66, 151, 0.1), rgba(95, 87, 175, 0.1));
        border-radius: var(--border-radius);
        padding: 6px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"]:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(69, 66, 151, 0.05), rgba(121, 107, 199, 0.05));
        z-index: -1;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1;
        height: 70px;
        font-size: 18px;
        font-weight: 700;
        background-color: transparent;
        border-radius: 12px;
        margin: 0;
        transition: var(--transition);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--color-gray);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.025em;
    }

    .stTabs [data-baseweb="tab"]:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 0;
        height: 100%;
        background: linear-gradient(135deg, var(--color-tertiary), var(--color-accent));
        transition: width 0.4s ease;
        z-index: -1;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--color-tertiary);
        transform: translateY(-2px);
    }

    .stTabs [data-baseweb="tab"]:hover:before {
        width: 100%;
    }

    
    /* ===== GARANTIZAR FONDO BLANCO EN TODOS LOS ELEMENTOS ===== */
    body, .stApp, .main, .block-container, 
    .metric-card, .analysis-card, .explanation-card,
    .hero-header, .footer, .dataframe-container,
    .plotly-container, .weekly-insight {
        background-color: var(--color-white) !important;
    }


/* Fuerza el fondo blanco en caso de que otros estilos lo estén cambiando */
    div[data-testid="stAppViewContainer"] {
        background-color: var(--color-white) !important;
    }


section[data-testid="stSidebar"] {
        background-color: var(--color-white) !important;
    }

div[data-testid="stVerticalBlock"] {
        background-color: var(--color-white) !important;
    }

/* Contenedor de gráficos */
    .plotly-container {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow);
        margin-bottom: 35px;
        border: 1px solid var(--color-gray-light);
        background: var(--color-white);
    }


    .stApp {
        background-color: var(--color-white) !important;
    }

.main .block-container {
        background-color: var(--color-white) !important;
        padding: 0;
    }

/* ===== LAYOUT PRINCIPAL ===== */
    .css-1d391kg { /* Sidebar */
        background-color: var(--color-white) !important;
        padding-top: 2rem;
        border-right: 1px solid var(--color-gray-light);
        box-shadow: 4px 0 6px -1px rgba(0, 0, 0, 0.1);
    }


body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: var(--color-white) !important;
        color: var(--color-primary);
        line-height: 1.7;
        font-size: 16px;
        margin: 0;
        padding: 0;
    }

.stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--color-tertiary), var(--color-accent));
        color: var(--color-white);
        box-shadow: 0 10px 15px -3px rgba(69, 66, 151, 0.3);
        transform: translateY(-2px);
    }
            
    /* Select boxes */
    .stSelectbox > div > div > div {
        /*
        background-color: var(--color-white);
        */
        border-radius: 12px;
        border: 2px solid var(--color-gray-light);
        padding: 14px;
        font-size: 1rem;
        box-shadow: var(--shadow-card);
    }

    .stSelectbox > div > div > div:hover {
        border-color: var(--color-tertiary);
    }

    /* Sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, var(--color-tertiary), var(--color-light-accent));
    }

    /* Multi-select */
    .stMultiSelect > div > div > div {
        background-color: var(--color-white);
        border-radius: 12px;
        border: 2px solid var(--color-gray-light);
        box-shadow: var(--shadow-card);
    }

    /* Date input */
    .stDateInput > div > div > div {
        background-color: var(--color-white);
        border-radius: 12px;
        border: 2px solid var(--color-gray-light);
        padding: 12px;
        box-shadow: var(--shadow-card);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--color-tertiary), var(--color-accent));
        color: var(--color-white);
        border: none;
        border-radius: 12px;
        padding: 16px 28px;
        font-weight: 700;
        transition: var(--transition);
        box-shadow: 0 10px 15px -3px rgba(69, 66, 151, 0.3);
        font-size: 1rem;
        letter-spacing: 0.025em;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgba(69, 66, 151, 0.4);
        background: linear-gradient(135deg, var(--color-accent), var(--color-light-accent));
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--success-color), var(--color-light-accent));
        color: var(--color-white);
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
        font-size: 1rem;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.4);
    }

    /* Spinner */
    .stSpinner > div > div {
        border-top-color: var(--color-tertiary) !important;
    }

    /* ===== COMPONENTES PERSONALIZADOS ===== */
    /* Grid de métricas */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }

    /* Tarjetas de métricas */
    .metric-card {
        background: var(--color-white);
        border-radius: var(--border-radius);
        padding: 30px;
        box-shadow: var(--shadow);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        border: 1px solid var(--color-gray-light);
    }

    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-lg);
        border-color: var(--color-tertiary);
    }

    .metric-card .icon {
        font-size: 3rem;
        margin-bottom: 20px;
        display: inline-block;
        background: linear-gradient(135deg, var(--color-tertiary), var(--color-light-accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 4px 6px rgba(69, 66, 151, 0.2));
    }

    .metric-card .title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--color-primary);
        margin-bottom: 20px;
        position: relative;
        line-height: 1.4;
    }

    .metric-card .title:after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 50px;
        height: 4px;
        background: linear-gradient(to right, var(--color-tertiary), var(--color-light-accent));
        border-radius: 4px;
    }

    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--color-primary);
        margin-top: 15px;
        line-height: 1.3;
    }

    .metric-card .value.green {
        color: var(--success-color);
    }

    .metric-card .value.red {
        color: var(--danger-color);
    }

    .metric-card .value p {
        margin: 8px 0;
        display: flex;
        align-items: center;
    }

    .metric-card .value strong {
        margin-right: 10px;
    }

    /* Tarjetas de análisis */
    .analysis-card {
        background: var(--color-white);
        border-radius: var(--border-radius);
        padding: 35px;
        box-shadow: var(--shadow);
        margin-bottom: 35px;
        border: 1px solid var(--color-gray-light);
        position: relative;
        overflow: hidden;
    }

    .analysis-card:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(to right, var(--color-tertiary), var(--color-accent));
    }

    .analysis-card h3 {
        color: var(--color-primary);
        margin-bottom: 25px;
        font-weight: 700;
        position: relative;
        padding-bottom: 15px;
        font-size: 1.5rem;
    }

    .analysis-card h3:after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 70px;
        height: 4px;
        background: linear-gradient(to right, var(--color-tertiary), var(--color-light-accent));
        border-radius: 4px;
    }

    /* Tarjetas de explicación */
    .explanation-card {
        background: var(--color-white);
        border-radius: var(--border-radius);
        padding: 35px;
        box-shadow: var(--shadow);
        margin-bottom: 35px;
        border: 1px solid var(--color-gray-light);
        position: relative;
        overflow: hidden;
    }

    .explanation-card:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(to right, var(--color-accent), var(--color-light-accent));
    }

    .explanation-card h3 {
        color: var(--color-primary);
        margin-bottom: 25px;
        font-weight: 700;
        position: relative;
        padding-bottom: 15px;
        font-size: 1.5rem;
    }

    .explanation-card h3:after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 70px;
        height: 4px;
        background: linear-gradient(to right, var(--color-accent), var(--color-light-accent));
        border-radius: 4px;
    }

    /* Insights semanales */
    .weekly-insight {
        background: linear-gradient(135deg, rgba(69, 66, 151, 0.05), rgba(121, 107, 199, 0.05));
        border-radius: var(--border-radius);
        padding: 25px;
        margin-bottom: 25px;
        border-left: 5px solid var(--color-tertiary);
        transition: var(--transition);
        position: relative;
    }

    .weekly-insight:hover {
        transform: translateX(8px);
        box-shadow: var(--shadow);
        background: linear-gradient(135deg, rgba(69, 66, 151, 0.08), rgba(121, 107, 199, 0.08));
    }

    .weekly-insight h4 {
        color: var(--color-tertiary);
        margin-top: 0;
        margin-bottom: 20px;
        font-weight: 700;
        display: flex;
        align-items: center;
        font-size: 1.2rem;
    }

    .weekly-insight h4:before {
        content: "📊";
        margin-right: 12px;
        font-size: 1.5rem;
    }

    .weekly-insight ul {
        margin-bottom: 0;
        padding-left: 25px;
    }

    .weekly-insight li {
        margin-bottom: 12px;
        position: relative;
        padding-left: 5px;
        font-size: 1.05rem;
        line-height: 1.6;
        color: var(--color-primary);
    }

    .weekly-insight li:before {
        content: "•";
        color: var(--color-tertiary);
        font-weight: bold;
        position: absolute;
        left: -18px;
        font-size: 1.2rem;
    }

    /* Header principal */
    .hero-header {
        text-align: center;
        padding: 3.5rem 0;
        margin-bottom: 3.5rem;
        position: relative;
        border-radius: var(--border-radius);
        overflow: hidden;
        background: var(--color-white);
        box-shadow: var(--shadow);
    }

    .hero-header:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(69, 66, 151, 0.1), rgba(121, 107, 199, 0.1));
        z-index: -1;
        border-radius: var(--border-radius);
    }

    .hero-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        color: var(--color-primary);
        margin-bottom: 1.5rem;
        position: relative;
        display: inline-block;
        line-height: 1.2;
        letter-spacing: -0.025em;
    }

    .hero-header h1:after {
        content: "";
        position: absolute;
        bottom: -15px;
        left: 10%;
        width: 80%;
        height: 5px;
        background: linear-gradient(to right, var(--color-tertiary), var(--color-light-accent));
        border-radius: 5px;
    }

    .hero-header p {
        font-size: 1.4rem;
        color: var(--color-gray);
        max-width: 900px;
        margin: 2rem auto 0;
        line-height: 1.6;
        font-weight: 500;
    }

    .source-info {
        font-size: 1rem;
        color: var(--color-gray);
        font-style: italic;
        margin-top: 2rem;
        font-weight: 400;
    }

    /* Contenedor de dataframes */
    .dataframe-container {
        margin: 25px 0;
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow);
        border: 1px solid var(--color-gray-light);
        background: var(--color-white);
    }

    /* Análisis dinámico */
    .dynamic-analysis {
        line-height: 1.9;
        color: var(--color-primary);
        font-size: 1.1rem;
    }

    .dynamic-analysis strong {
        color: var(--color-tertiary);
        font-weight: 700;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 0;
        margin-top: 4rem;
        color: var(--color-gray);
        font-size: 1rem;
        border-top: 1px solid var(--color-gray-light);
        background: var(--color-white);
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
    }

    

    /* ===== EFECTOS Y ANIMACIONES ===== */
    .hover-effect {
        transition: var(--transition);
    }

    .hover-effect:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }

    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes countUp {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }

    .metric-card, .analysis-card, .explanation-card {
        animation: fadeIn 0.8s ease-out;
    }

    .weekly-insight {
        animation: slideIn 0.8s ease-out;
    }

    .metric-card .value {
        animation: countUp 1s ease-out;
    }

    /* ===== MEJORAS TIPOGRÁFICAS ===== */
    h2, h3, h4 {
        letter-spacing: -0.025em;
        color: var(--color-primary);
        font-weight: 700;
    }

    /* ===== MEJORAS DE ESPACIADO ===== */
    .element-container {
        margin-bottom: 2rem;
    }

    .stTabs [data-testid="stVerticalBlock"] > div {
        padding-top: 25px;
    }

    /* ===== MÉTRICAS CLAVE ===== */
    .key-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    /* ===== MEJORAS EN LA BARRA LATERAL ===== */
    .css-1d391kg .css-1l02zno {
        font-weight: 600;
        color: var(--color-primary);
    }
            
    .stSelectbox p{
        color:black;
        font-size: 22px; /* más grande */
        font-weight: bold; /* negrita */
        color: black;
        margin-bottom: 8px;            
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar datos con caché de sesión
@st.cache_data(ttl=3600)  # Caché de 1 hora
def get_data_session(CODCOM):
    return get_data(CODCOM)

# Cargar datos con animación de carga mejorada
with st.spinner('Cargando datos...'):
    time.sleep(0.5)
    annual_df, monthly_df, weekly_df = get_data_session(CODCOM)

# Preprocesamiento de datos semanales a formato largo
@st.cache_data
def preprocess_weekly_data(weekly_df):
    weekly_df_long = pd.melt(
        weekly_df,
        id_vars=['año', 'delito'],
        var_name='semana_col',
        value_name='valor'
    )
    weekly_df_long['semana'] = weekly_df_long['semana_col'].str.extract(r'SEMANA (\d+)').astype(float)
    weekly_df_long = weekly_df_long.dropna(subset=['semana'])
    weekly_df_long['semana'] = weekly_df_long['semana'].astype(int)
    return weekly_df_long.drop(columns=['semana_col'])

weekly_df_long = preprocess_weekly_data(weekly_df)

# Preprocesamiento de datos mensuales a formato largo
@st.cache_data
def preprocess_monthly_data(monthly_df):
    return monthly_df.melt(
        id_vars=['Año', 'Delito'],
        var_name='Mes',
        value_name='Valor'
    )

monthly_df_long = preprocess_monthly_data(monthly_df)

# Función optimizada para obtener datos semanales con caché
@st.cache_data
def get_weekly_data_optimized(year, crime="All"):
    df_year = weekly_df_long[weekly_df_long['año'] == year]
    
    if crime == "All":
        df_grouped = df_year.groupby('semana')['valor'].sum().reset_index()
    else:
        df_year = df_year[df_year['delito'] == crime]
        df_grouped = df_year.groupby('semana')['valor'].sum().reset_index()
    
    return dict(zip(df_grouped['semana'], df_grouped['valor']))

# Función optimizada para obtener datos mensuales con caché
@st.cache_data
def get_monthly_data_optimized(year, crime="All"):
    df_year = monthly_df_long[monthly_df_long['Año'] == year]
    
    if crime == "All":
        df_grouped = df_year.groupby('Mes')['Valor'].sum().reset_index()
    else:
        df_year = df_year[df_year['Delito'] == crime]
        df_grouped = df_year.groupby('Mes')['Valor'].sum().reset_index()
    
    return dict(zip(df_grouped['Mes'], df_grouped['Valor']))

# Obtener lista de tipos de delitos
crime_types = sorted(annual_df['Delito'].unique())

# Encabezado mejorado con animación y diseño moderno
st.markdown(f"""
<div class="hero-header">
    <h1><span class="text-blue-300">📈</span> Panorama Delictual en {COMUNA_NAME}</h1>
    <p class="text-xl">Análisis interactivo de frecuencias de delitos por temporalidad.</p>
    <p class="source-info mt-4">Datos extraídos de la Plataforma de Información Ley STOP de Carabineros de Chile, sistematizados por el Instituto Libertad.</p>
</div>
""", unsafe_allow_html=True)

# Determinar valores por defecto basados en parámetros de URL
default_crime = url_params.get('delito', 'All')
default_temporality = url_params.get('temporalidad', None)

# Selector de temporalidad con diseño mejorado
tab1, tab2, tab3 = st.tabs(["📊 Anual", "📅 Mensual", "📆 Semanal"])

# Función para generar el análisis general
@st.cache_data
def generate_general_analysis(annual_df, monthly_df, weekly_df):
    total2023 = annual_df["Frecuencia 2023"].sum()
    total2024 = annual_df["Frecuencia 2024"].sum()
    total2025Partial = annual_df["Frecuencia 2025 (a la fecha)"].sum()
    
    # Tendencia general anual
    if total2023 > 0 and total2024 > 0:
        change23_24 = ((total2024 - total2023) / total2023 * 100)
        trendText = f"Se observó un {'incremento' if change23_24 > 0 else 'descenso'} general del {abs(change23_24):.1f}% entre 2023 y 2024. "
    else:
        trendText = "No hay suficientes datos para calcular la tendencia entre 2023 y 2024. "
    
    if total2024 > 0 and total2025Partial > 0:
        change24_25 = ((total2025Partial - total2024) / total2024 * 100)
        trendText += f"Para el periodo de 2025 (a la fecha) en comparación con el mismo periodo de 2024, se registra un {'aumento' if change24_25 > 0 else 'disminución'} del {abs(change24_25):.1f}%."
    else:
        trendText += "Los datos de 2025 muestran una tendencia inicial de aumento."
    
    # Análisis de delitos más/menos frecuentes (basado en 2024)
    crimeFrequencies = annual_df[['Delito', 'Frecuencia 2024']].copy()
    crimeFrequencies.columns = ['delito', 'total']
    crimeFrequencies = crimeFrequencies.sort_values('total', ascending=False)
    mostFrequentCrime = crimeFrequencies.iloc[0]
    leastFrequentCrime = crimeFrequencies.iloc[-1]
    
    # Análisis de meses con más/menos frecuencia
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    # Optimización: Usar operaciones vectorizadas
    monthly_2024 = monthly_df[monthly_df['Año'] == 2024][months]
    monthlyTotals2024 = monthly_2024.sum().values
    
    monthly_2025 = monthly_df[monthly_df['Año'] == 2025][months]
    monthlyTotals2025 = monthly_2025.sum().values
    
    maxMonth2024Index = np.argmax(monthlyTotals2024)
    minMonth2024Index = np.argmin(monthlyTotals2024)
    
    # Homicidios y Femicidios (Semana 12 2025) - usando función optimizada
    data_homicidios_2025 = get_weekly_data_optimized(2025, "HOMICIDIOS Y FEMICIDIOS")
    semana12Homicidios = data_homicidios_2025.get(12, 0)
    
    # Crear tarjetas en una estructura de 2 columnas
    cards_html = f"""
    <div class="metrics-grid">
        <div class="metric-card hover-effect">
            <span class="icon">📊</span>
            <h4 class="title">Cifras Anuales Totales</h4>
            <div class="value">
                <p><strong>2023:</strong> {format_number_chile(total2023)} casos</p>
                <p><strong>2024:</strong> {format_number_chile(total2024)} casos</p>
                <p><strong>2025 (a la fecha):</strong> {format_number_chile(total2025Partial)} casos</p>
            </div>
        </div>
        <div class="metric-card hover-effect">
            <span class="icon">📈</span>
            <h4 class="title">Tendencia General Anual</h4>
            <div class="value">{trendText}</div>
        </div>
        <div class="metric-card hover-effect">
            <span class="icon">🚨</span>
            <h4 class="title">Delitos Más y Menos Frecuentes (2024)</h4>
            <div class="value">
                <p><strong>Más frecuente:</strong> {mostFrequentCrime['delito']} ({format_number_chile(mostFrequentCrime['total'])} casos)</p>
                <p><strong>Menos frecuente:</strong> {leastFrequentCrime['delito']} ({format_number_chile(leastFrequentCrime['total'])} casos)</p>
            </div>
        </div>
        <div class="metric-card hover-effect">
            <span class="icon">📅</span>
            <h4 class="title">Patrones Mensuales (Frecuencia Total)</h4>
            <div class="value">
                <p><strong>2024 - Mayor frecuencia:</strong> {months[maxMonth2024Index]} ({format_number_chile(monthlyTotals2024[maxMonth2024Index])} casos)</p>
                <p><strong>2024 - Menor frecuencia:</strong> {months[minMonth2024Index]} ({format_number_chile(monthlyTotals2024[minMonth2024Index])} casos)</p>
    """
    
    if monthlyTotals2025.sum() > 0:
        maxMonth2025Index = np.argmax(monthlyTotals2025)
        minMonth2025Index = np.argmin(monthlyTotals2025)
        cards_html += f"""
                <p><strong>2025 (hasta julio) - Mayor frecuencia:</strong> {months[maxMonth2025Index]} ({format_number_chile(monthlyTotals2025[maxMonth2025Index])} casos)</p>
                <p><strong>2025 (hasta julio) - Menor frecuencia:</strong> {months[minMonth2025Index]} ({format_number_chile(monthlyTotals2025[minMonth2025Index])} casos)</p>
        """
    
    cards_html += f"""
            </div>
        </div>
        <div class="metric-card hover-effect">
            <span class="icon">💀</span>
            <h4 class="title">Datos Específicos de 2025</h4>
            <div class="value">
                <p><strong>Homicidios y Femicidios (Semana 12):</strong> {format_number_chile(semana12Homicidios)} casos</p>
            </div>
        </div>
    </div>
    """
    
    return cards_html

# Función para generar análisis dinámico
@st.cache_data
def generate_analysis_text(temporality, selected_crime, annual_df=None, monthly_df=None, weekly_df=None):
    if annual_df is None:
        annual_df = globals().get('annual_df')
    if monthly_df is None:
        monthly_df = globals().get('monthly_df')
    if weekly_df is None:
        weekly_df = globals().get('weekly_df')
    
    data_name = "Todos los delitos" if selected_crime == "All" else selected_crime
    
    if temporality == "Annual":
        if selected_crime == "All":
            total2023 = annual_df["Frecuencia 2023"].sum()
            total2024 = annual_df["Frecuencia 2024"].sum()
            total2025 = annual_df["Frecuencia 2025 (a la fecha)"].sum()
        else:
            crime_data = annual_df[annual_df["Delito"] == selected_crime].iloc[0]
            total2023 = crime_data["Frecuencia 2023"]
            total2024 = crime_data["Frecuencia 2024"]
            total2025 = crime_data["Frecuencia 2025 (a la fecha)"]
        
        analysis_text = f"Análisis Anual para <strong>{data_name}</strong>:<br><br>"
        analysis_text += f"En 2023, se registraron <strong>{format_number_chile(total2023)}</strong> casos. Para 2024, la cifra fue de <strong>{format_number_chile(total2024)}</strong> casos. Hasta la fecha en 2025, se han reportado <strong>{format_number_chile(total2025)}</strong> casos.<br><br>"
        
        if total2023 > 0:
            change23_24 = ((total2024 - total2023) / total2023 * 100)
            analysis_text += f"Se observó un {'incremento' if change23_24 > 0 else 'disminución'} del <strong>{abs(change23_24):.1f}%</strong> entre 2023 y 2024. "
        else:
            analysis_text += "No hay suficientes datos para calcular la tendencia entre 2023 y 2024. "
        
        if total2024 > 0:
            change24_25 = ((total2025 - total2024) / total2024 * 100)
            analysis_text += f"Entre 2024 y 2025 (a la fecha), se registró un {'aumento' if change24_25 > 0 else 'disminución'} del <strong>{abs(change24_25):.1f}%</strong>."
        else:
            analysis_text += "Entre 2024 y 2025 (a la fecha), no hubo variaciones significativas."
    
    elif temporality == "Monthly":
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        # Usar función optimizada
        data2024_dict = get_monthly_data_optimized(2024, selected_crime)
        data2025_dict = get_monthly_data_optimized(2025, selected_crime)
        
        data2024 = [data2024_dict.get(month, 0) for month in months]
        data2025 = [data2025_dict.get(month, 0) for month in months]
        
        analysis_text = f"Análisis Mensual para <strong>{data_name}</strong>:<br><br>"
        analysis_text += f"Comparativa entre 2024 y 2025 (hasta <strong>Julio</strong>):<br>"
        
        total2024Partial = sum(data2024[:7])
        total2025Partial = sum(data2025[:7])
        
        if total2024Partial > 0:
            changePartial = ((total2025Partial - total2024Partial) / total2024Partial * 100)
            analysis_text += f"Se observa un {'incremento' if changePartial > 0 else 'decremento'} del <strong>{abs(changePartial):.1f}%</strong> en 2025 respecto al mismo período de 2024.<br>"
        else:
            analysis_text += "Se ha registrado un aumento significativo en 2025 en comparación con el mismo período de 2024.<br>"
        
        max2024 = max(data2024)
        min2024 = min(data2024)
        maxMonth2024 = months[data2024.index(max2024)]
        minMonth2024 = months[data2024.index(min2024)]
        
        analysis_text += f"En 2024, el mes con mayor frecuencia fue <strong>{maxMonth2024}</strong> (<strong>{format_number_chile(max2024)}</strong> casos), y el de menor fue <strong>{minMonth2024}</strong> (<strong>{format_number_chile(min2024)}</strong> casos).<br>"
        
        actual2025Values = data2025[:7]
        if len(actual2025Values) > 0 and sum(actual2025Values) > 0:
            max2025Actual = max(actual2025Values)
            min2025Actual = min(actual2025Values)
            maxMonth2025Actual = months[data2025.index(max2025Actual)]
            minMonth2025Actual = months[data2025.index(min2025Actual)]
            
            analysis_text += f"Hasta el momento en 2025, el mes de mayor incidencia fue <strong>{maxMonth2025Actual}</strong> (<strong>{format_number_chile(max2025Actual)}</strong> casos), y el de menor fue <strong>{minMonth2025Actual}</strong> (<strong>{format_number_chile(min2025Actual)}</strong> casos).<br><br>"
            
            average2025 = np.mean([v for v in actual2025Values if v > 0]) if any(actual2025Values) else 0
            analysis_text += f"La proyección para los meses restantes de 2025 (a partir de <strong>Agosto</strong>) es de aproximadamente <strong>{round(average2025):,}</strong> casos por mes, con base en el promedio de los meses ya reportados de 2025."
    
    elif temporality == "Weekly":
        # Usar función optimizada
        data2024 = get_weekly_data_optimized(2024, selected_crime)
        data2025 = get_weekly_data_optimized(2025, selected_crime)
        
        analysis_text = f"Análisis Semanal para <strong>{data_name}</strong>:<br><br>"
        analysis_text += f"Análisis de las semanas disponibles en 2024 y 2025:<br>"
        
        total2024 = sum(data2024.values())
        total2025 = sum(data2025.values())
        
        if total2024 > 0:
            changePartial = ((total2025 - total2024) / total2024 * 100)
            analysis_text += f"Se observa un {'incremento' if changePartial > 0 else 'decremento'} del <strong>{abs(changePartial):.1f}%</strong> en 2025 respecto al mismo período de 2024.<br>"
        else:
            analysis_text += "Se ha registrado un aumento significativo en 2025 en comparación con el mismo período de 2024.<br>"
        
        if data2024:
            max_week2024 = max(data2024, key=data2024.get)
            min_week2024 = min(data2024, key=data2024.get)
            analysis_text += f"En las semanas disponibles de 2024, el pico se alcanzó en la <strong>Semana {max_week2024}</strong> (<strong>{format_number_chile(data2024[max_week2024])}</strong> casos) y el punto más bajo en la <strong>Semana {min_week2024}</strong> (<strong>{format_number_chile(data2024[min_week2024])}</strong> casos).<br>"
        else:
            analysis_text += "No hay datos disponibles para 2024.<br>"
        
        if data2025:
            max_week2025 = max(data2025, key=data2025.get)
            min_week2025 = min(data2025, key=data2025.get)
            analysis_text += f"Para 2025, en las semanas con datos, la semana con más casos fue la <strong>Semana {max_week2025}</strong> (<strong>{format_number_chile(data2025[max_week2025])}</strong> casos) y la de menor fue la <strong>Semana {min_week2025}</strong> (<strong>{format_number_chile(data2025[min_week2025])}</strong> casos)."
        else:
            analysis_text += "No hay datos disponibles para 2025."
    
    return analysis_text

# Función para renderizar gráfico anual
@st.cache_data
def render_annual_chart(selected_crime, annual_df=None):
    if annual_df is None:
        annual_df = globals().get('annual_df')
    
    if selected_crime == "All":
        data2023 = annual_df["Frecuencia 2023"].sum()
        data2024 = annual_df["Frecuencia 2024"].sum()
        data2025 = annual_df["Frecuencia 2025 (a la fecha)"].sum()
    else:
        crime_data = annual_df[annual_df["Delito"] == selected_crime].iloc[0]
        data2023 = crime_data["Frecuencia 2023"]
        data2024 = crime_data["Frecuencia 2024"]
        data2025 = crime_data["Frecuencia 2025 (a la fecha)"]
    
    fig = go.Figure()
    
    categories = ['2023', '2024', '2025 (a la fecha)']
    
    # Colores con nueva paleta mejorada
    colors = ['rgba(30, 64, 175, 0.8)', 'rgba(59, 130, 246, 0.8)', 'rgba(96, 165, 250, 0.8)']
    
    fig.add_trace(go.Bar(
        name='Frecuencia',
        x=categories,
        y=[data2023, data2024, data2025],
        marker_color=colors,
        showlegend=False,
        textposition='auto',
        text=[format_number_chile(data2023), format_number_chile(data2024), format_number_chile(data2025)],
        textfont=dict(size=14, color='#1e40af'),
        marker_line_color='rgba(0,0,0,0)',
        marker_line_width=0
    ))
    
    fig.update_layout(
        title=f"Frecuencia Anual de {'Todos los Delitos' if selected_crime == 'All' else selected_crime}",
        title_font=dict(size=22, color='#1e40af', family='Inter'),
        xaxis_title="Año",
        yaxis_title="Frecuencia de Casos",
        height=500,
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=categories,
            tickfont=dict(size=14, color='#4b5563', family='Inter')
        ),
        yaxis=dict(
            tickformat=".",  # Formato chileno
            separatethousands=True,
            tickfont=dict(size=14, color='#4b5563', family='Inter')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=80, b=60),
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )
    
    return fig

# Función para renderizar gráfico mensual
@st.cache_data
def render_monthly_chart(selected_crime, monthly_df=None):
    if monthly_df is None:
        monthly_df = globals().get('monthly_df')
    
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    # Usar función optimizada
    data2024_dict = get_monthly_data_optimized(2024, selected_crime)
    data2025_dict = get_monthly_data_optimized(2025, selected_crime)
    
    data2024 = [data2024_dict.get(month, 0) for month in months]
    data2025 = [data2025_dict.get(month, 0) for month in months]
    
    # Determinar el último mes con datos reales de 2025
    currentMonthIndex = 6  # Julio (índice 6)
    for i in range(7, 12):
        if data2025[i] > 0:
            currentMonthIndex = i
    
    # Calcular promedio para proyección
    actual2025Values = data2025[:currentMonthIndex+1]
    average2025 = np.mean([v for v in actual2025Values if v > 0]) if any(actual2025Values) else 0
    
    # Crear datos de proyección
    projection2025 = list(data2025)
    for i in range(currentMonthIndex+1, 12):
        projection2025[i] = round(average2025)
    
    fig = go.Figure()
    
    # Datos de 2024
    fig.add_trace(go.Scatter(
        x=months,
        y=data2024,
        mode='lines+markers',
        name=f'Frecuencia 2024 ({selected_crime if selected_crime != "All" else "Total"})',
        line=dict(color='#3b82f6', width=4),
        marker=dict(size=10, color='#3b82f6', line=dict(width=2, color='white')),
        text=[format_number_chile(val) for val in data2024],
        textposition="top center",
        hovertemplate='%{text}<extra></extra>'
    ))
    
    # Datos de 2025 (reales y proyectados)
    # Parte real (línea sólida)
    fig.add_trace(go.Scatter(
        x=months[:currentMonthIndex+1],
        y=data2025[:currentMonthIndex+1],
        mode='lines+markers',
        name=f'Frecuencia 2025 (Datos reales)',
        line=dict(color='#60a5fa', width=4),
        marker=dict(size=10, color='#60a5fa', line=dict(width=2, color='white')),
        text=[format_number_chile(val) for val in data2025[:currentMonthIndex+1]],
        textposition="top center",
        hovertemplate='%{text}<extra></extra>',
        showlegend=False
    ))
    
    # Parte proyectada (línea discontinua)
    fig.add_trace(go.Scatter(
        x=months[currentMonthIndex:],
        y=projection2025[currentMonthIndex:],
        mode='lines+markers',
        name=f'Frecuencia 2025 (Proyección)',
        line=dict(color='#60a5fa', width=4, dash='dash'),
        marker=dict(size=10, symbol='diamond', color='#60a5fa', line=dict(width=2, color='white')),
        text=[f"Proy: {format_number_chile(val)}" for val in projection2025[currentMonthIndex:]],
        textposition="top center",
        hovertemplate='%{text}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Frecuencia Mensual de {'Todos los Delitos' if selected_crime == 'All' else selected_crime} (2024 vs. 2025 Proyectado)",
        title_font=dict(size=22, color='#1e40af', family='Inter'),
        xaxis_title="Mes",
        yaxis_title="Frecuencia de Casos",
        height=500,
        hovermode='x unified',
        yaxis=dict(
            tickformat=".",  # Formato chileno
            separatethousands=True,
            tickfont=dict(size=14, color='#4b5563', family='Inter')
        ),
        xaxis=dict(tickfont=dict(size=14, color='#4b5563', family='Inter')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=80, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, family='Inter')
        )
    )
    
    return fig

# Función para renderizar gráfico semanal
@st.cache_data
def render_weekly_chart(selected_crime, weekly_df=None):
    if weekly_df is None:
        weekly_df = globals().get('weekly_df')
    
    # Usar función optimizada
    data2024 = get_weekly_data_optimized(2024, selected_crime)
    data2025 = get_weekly_data_optimized(2025, selected_crime)
    
    # Ordenar las semanas
    weeks2024 = sorted(data2024.keys())
    values2024 = [data2024[week] for week in weeks2024]
    
    weeks2025 = sorted(data2025.keys())
    values2025 = [data2025[week] for week in weeks2025]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks2024,
        y=values2024,
        mode='lines+markers',
        name=f'Frecuencia Semanal 2024 ({selected_crime if selected_crime != "All" else "Total"})',
        line=dict(color='#3b82f6', width=4),
        marker=dict(size=10, color='#3b82f6', line=dict(width=2, color='white')),
        text=[format_number_chile(val) for val in values2024],
        textposition="top center",
        hovertemplate='Semana %{x}: %{text}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=weeks2025,
        y=values2025,
        mode='lines+markers',
        name=f'Frecuencia Semanal 2025 (a la fecha) ({selected_crime if selected_crime != "All" else "Total"})',
        line=dict(color='#60a5fa', width=4),
        marker=dict(size=10, color='#60a5fa', line=dict(width=2, color='white')),
        text=[format_number_chile(val) for val in values2025],
        textposition="top center",
        hovertemplate='Semana %{x}: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Frecuencia Semanal de {'Todos los Delitos' if selected_crime == 'All' else selected_crime} (2024 vs. 2025)",
        title_font=dict(size=22, color='#1e40af', family='Inter'),
        xaxis_title="Semana",
        yaxis_title="Frecuencia de Casos",
        height=500,
        hovermode='x unified',
        yaxis=dict(
            tickformat=".",  # Formato chileno
            separatethousands=True,
            tickfont=dict(size=14, color='#4b5563', family='Inter')
        ),
        xaxis=dict(tickfont=dict(size=14, color='#4b5563', family='Inter')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=80, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, family='Inter')
        )
    )
    
    return fig

# Contenido de la pestaña Anual
with tab1:
    default_index = 0
    if default_crime != 'All' and default_crime in crime_types:
        default_index = crime_types.index(default_crime) + 1
    
    selected_crime_annual = st.selectbox(
        "Seleccionar Delito:",
        ["All"] + crime_types,
        key="annual_crime_select",
        index=default_index
    )
    
    fig_annual = render_annual_chart(selected_crime_annual)
    st.plotly_chart(fig_annual, use_container_width=True)
    
    # Tabla de datos anuales con diseño mejorado
    st.subheader("Datos Anuales Detallados")
    if selected_crime_annual == "All":
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(annual_df.style.format({
            "Frecuencia 2023": lambda x: format_number_chile(x),
            "Frecuencia 2024": lambda x: format_number_chile(x),
            "Frecuencia 2025 (a la fecha)": lambda x: format_number_chile(x)
        }).set_properties(**{'background-color': '#ffffff', 'color': '#1e40af', 'font-size': '16px'}), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        crime_data = annual_df[annual_df["Delito"] == selected_crime_annual]
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(crime_data.style.format({
            "Frecuencia 2023": lambda x: format_number_chile(x),
            "Frecuencia 2024": lambda x: format_number_chile(x),
            "Frecuencia 2025 (a la fecha)": lambda x: format_number_chile(x)
        }).set_properties(**{'background-color': '#ffffff', 'color': '#1e40af', 'font-size': '16px'}), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis dinámico
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Tendencias Específicas")
    analysis_text = generate_analysis_text("Annual", selected_crime_annual)
    st.markdown(f'<div class="dynamic-analysis">{analysis_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Contenido de la pestaña Mensual
with tab2:
    default_index = 0
    if default_crime != 'All' and default_crime in crime_types:
        default_index = crime_types.index(default_crime) + 1
    
    selected_crime_monthly = st.selectbox(
        "Seleccionar Delito:",
        ["All"] + crime_types,
        key="monthly_crime_select",
        index=default_index
    )
    
    fig_monthly = render_monthly_chart(selected_crime_monthly)
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Análisis mensual detallado
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis Mensual Detallado")
    
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    # Usar función optimizada
    data2024_dict = get_monthly_data_optimized(2024, selected_crime_monthly)
    data2025_dict = get_monthly_data_optimized(2025, selected_crime_monthly)
    
    data2024 = [data2024_dict.get(month, 0) for month in months]
    data2025 = [data2025_dict.get(month, 0) for month in months]
    
    # Análisis 1: Meses con más y menos delitos
    max_month2024 = months[np.argmax(data2024)]
    min_month2024 = months[np.argmin(data2024)]
    max_value2024 = data2024[np.argmax(data2024)]
    min_value2024 = data2024[np.argmin(data2024)]
    
    st.markdown(f"""
    <div class="weekly-insight">
        <h4>📅 Análisis de Meses Críticos (2024)</h4>
        <ul>
            <li><strong>Mes con mayor delincuencia:</strong> {max_month2024} con {format_number_chile(max_value2024)} casos</li>
            <li><strong>Mes con menor delincuencia:</strong> {min_month2024} con {format_number_chile(min_value2024)} casos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Para 2025 (solo hasta julio)
    if sum(data2025[:7]) > 0:
        max_month2025 = months[:7][np.argmax(data2025[:7])]
        min_month2025 = months[:7][np.argmin(data2025[:7])]
        max_value2025 = data2025[:7][np.argmax(data2025[:7])]
        min_value2025 = data2025[:7][np.argmin(data2025[:7])]
        
        st.markdown(f"""
        <div class="weekly-insight">
            <h4>📅 Análisis de Meses Críticos (2025)</h4>
            <ul>
                <li><strong>Mes con mayor delincuencia:</strong> {max_month2025} con {format_number_chile(max_value2025)} casos</li>
                <li><strong>Mes con menor delincuencia:</strong> {min_month2025} con {format_number_chile(min_value2025)} casos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p>No hay datos disponibles para 2025.</p>", unsafe_allow_html=True)
    
    # Análisis 2: Variación porcentual entre meses comparables
    variations = {}
    for i in range(min(7, len(data2025))):
        if data2024[i] > 0:
            variation = (data2025[i] - data2024[i]) / data2024[i] * 100
            variations[months[i]] = variation
    
    if variations:
        max_increase_month = max(variations, key=variations.get)
        max_decrease_month = min(variations, key=variations.get)
        
        st.markdown(f"""
        <div class="weekly-insight">
            <h4>📈 Variación Porcentual entre Meses Comparables</h4>
            <ul>
                <li><strong>Mayor aumento:</strong> {max_increase_month} con un incremento del {variations[max_increase_month]:.1f}%</li>
                <li><strong>Mayor disminución:</strong> {max_decrease_month} con una reducción del {abs(variations[max_decrease_month]):.1f}%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p>No se pudo calcular la variación porcentual para los meses comparables.</p>", unsafe_allow_html=True)
    
    # Análisis 3: Comparación por trimestre
    quarters = {
        "Q1 (Ene-Mar)": (0, 2),
        "Q2 (Abr-Jun)": (3, 5),
        "Q3 (Jul-Sep)": (6, 8),
        "Q4 (Oct-Dic)": (9, 11)
    }
    
    st.markdown("<p><strong>Comparación por trimestre (promedio mensual):</strong></p>", unsafe_allow_html=True)
    
    for q_name, q_range in quarters.items():
        months_in_q2024 = list(range(q_range[0], q_range[1] + 1))
        avg2024 = sum(data2024[i] for i in months_in_q2024) / len(months_in_q2024)
        
        if q_range[0] <= 6:
            months_in_q2025 = [i for i in months_in_q2024 if i < 7]
            
            if months_in_q2025:
                avg2025 = sum(data2025[i] for i in months_in_q2025) / len(months_in_q2025)
                
                if avg2024 > 0:
                    change = ((avg2025 - avg2024) / avg2024 * 100)
                    change_text = f"({change:+.1f}%)"
                else:
                    change_text = "(N/A)"
                
                st.markdown(f"<p><strong>{q_name}:</strong> 2024: {avg2024:.1f} casos/mes, 2025: {avg2025:.1f} casos/mes {change_text}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p><strong>{q_name}:</strong> 2024: {avg2024:.1f} casos/mes, 2025: Sin datos</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p><strong>{q_name}:</strong> 2024: {avg2024:.1f} casos/mes, 2025: Sin datos</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis dinámico existente
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Tendencias Específicas")
    analysis_text = generate_analysis_text("Monthly", selected_crime_monthly)
    st.markdown(f'<div class="dynamic-analysis">{analysis_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Contenido de la pestaña Semanal
with tab3:
    default_index = 0
    if default_crime != 'All' and default_crime in crime_types:
        default_index = crime_types.index(default_crime) + 1
    
    selected_crime_weekly = st.selectbox(
        "Seleccionar Delito:",
        ["All"] + crime_types,
        key="weekly_crime_select",
        index=default_index
    )
    
    fig_weekly = render_weekly_chart(selected_crime_weekly)
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Análisis semanal detallado
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis Semanal Detallado")
    
    # Usar función optimizada
    data2024 = get_weekly_data_optimized(2024, selected_crime_weekly)
    data2025 = get_weekly_data_optimized(2025, selected_crime_weekly)
    
    # Análisis 1: Mejor y peor semana
    if data2024:
        max_week2024 = max(data2024, key=data2024.get)
        min_week2024 = min(data2024, key=data2024.get)
        
        st.markdown(f"""
        <div class="weekly-insight">
            <h4>📅 Análisis de Semanas Críticas (2024)</h4>
            <ul>
                <li><strong>Peor semana:</strong> Semana {max_week2024} con {format_number_chile(data2024[max_week2024])} casos (mayor incidencia delictiva)</li>
                <li><strong>Mejor semana:</strong> Semana {min_week2024} con {format_number_chile(data2024[min_week2024])} casos (menor incidencia delictiva)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p>No hay datos disponibles para 2024.</p>", unsafe_allow_html=True)
    
    if data2025:
        max_week2025 = max(data2025, key=data2025.get)
        min_week2025 = min(data2025, key=data2025.get)
        
        st.markdown(f"""
        <div class="weekly-insight">
            <h4>📅 Análisis de Semanas Críticas (2025)</h4>
            <ul>
                <li><strong>Peor semana:</strong> Semana {max_week2025} con {format_number_chile(data2025[max_week2025])} casos (mayor incidencia delictiva)</li>
                <li><strong>Mejor semana:</strong> Semana {min_week2025} con {format_number_chile(data2025[min_week2025])} casos (menor incidencia delictiva)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p>No hay datos disponibles para 2025.</p>", unsafe_allow_html=True)
    
    # Análisis 2: Variación porcentual entre semanas comparables
    common_weeks = set(data2024.keys()) & set(data2025.keys())
    
    if common_weeks:
        variations = {}
        for week in common_weeks:
            if data2024[week] > 0:
                variation = (data2025[week] - data2024[week]) / data2024[week] * 100
                variations[week] = variation
        
        if variations:
            max_increase_week = max(variations, key=variations.get)
            max_decrease_week = min(variations, key=variations.get)
            
            st.markdown(f"""
            <div class="weekly-insight">
                <h4>📈 Variación Porcentual entre Semanas Comparables</h4>
                <ul>
                    <li><strong>Mayor aumento:</strong> Semana {max_increase_week} con un incremento del {variations[max_increase_week]:.1f}%</li>
                    <li><strong>Mayor disminución:</strong> Semana {max_decrease_week} con una reducción del {abs(variations[max_decrease_week]):.1f}%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<p>No se pudo calcular la variación porcentual para las semanas comparables.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p>No hay semanas comparables entre 2024 y 2025.</p>", unsafe_allow_html=True)
    
    # Análisis 3: Comparación por trimestre
    quarters = {
        "Q1 (Ene-Mar)": (1, 13),
        "Q2 (Abr-Jun)": (14, 26),
        "Q3 (Jul-Sep)": (27, 39),
        "Q4 (Oct-Dic)": (40, 52)
    }
    
    def calculate_quarter_avg(data, quarter_range):
        weeks_in_quarter = [week for week in data.keys() if quarter_range[0] <= week <= quarter_range[1]]
        if weeks_in_quarter:
            total = sum(data[week] for week in weeks_in_quarter)
            return total / len(weeks_in_quarter)
        return None
    
    st.markdown("<p><strong>Comparación por trimestre (promedio semanal):</strong></p>", unsafe_allow_html=True)
    
    for q_name, q_range in quarters.items():
        avg2024 = calculate_quarter_avg(data2024, q_range)
        avg2025 = calculate_quarter_avg(data2025, q_range)
        
        if avg2024 is None and avg2025 is None:
            continue
            
        if avg2024 is not None and avg2025 is not None:
            change = ((avg2025 - avg2024) / avg2024 * 100) if avg2024 > 0 else float('nan')
            change_text = f"({change:+.1f}%)" if not np.isnan(change) else "(N/A)"
            
            st.markdown(f"<p><strong>{q_name}:</strong> 2024: {avg2024:.1f} casos/semana, 2025: {avg2025:.1f} casos/semana {change_text}</p>", unsafe_allow_html=True)
        elif avg2024 is not None:
            st.markdown(f"<p><strong>{q_name}:</strong> 2024: {avg2024:.1f} casos/semana, 2025: Sin datos</p>", unsafe_allow_html=True)
        elif avg2025 is not None:
            st.markdown(f"<p><strong>{q_name}:</strong> 2024: Sin datos, 2025: {avg2025:.1f} casos/semana</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis dinámico existente
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Tendencias Específicas")
    analysis_text = generate_analysis_text("Weekly", selected_crime_weekly)
    st.markdown(f'<div class="dynamic-analysis">{analysis_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Sección de métricas clave
st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
st.subheader("Métricas Clave de Delincuencia")

# Total Casos 2024
total2024 = annual_df["Frecuencia 2024"].sum()
# Total Casos 2025 (a la fecha)
total2025Partial = annual_df["Frecuencia 2025 (a la fecha)"].sum()
# Delito Más Frecuente (2024)
crimeFrequencies2024 = annual_df[['Delito', 'Frecuencia 2024']].copy()
crimeFrequencies2024.columns = ['delito', 'total']
crimeFrequencies2024 = crimeFrequencies2024.sort_values('total', ascending=False)
mostFrequent2024 = crimeFrequencies2024.iloc[0]
# Delito Más Frecuente (2025 a la fecha)
crimeFrequencies2025 = annual_df[['Delito', 'Frecuencia 2025 (a la fecha)']].copy()
crimeFrequencies2025.columns = ['delito', 'total']
crimeFrequencies2025 = crimeFrequencies2025.sort_values('total', ascending=False)
mostFrequent2025 = crimeFrequencies2025.iloc[0]
# Variación % (2025 vs Mismo Periodo 2024)
monthsForComparison = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio"]
# Usar función optimizada
data2024_all = get_monthly_data_optimized(2024, "All")
data2025_all = get_monthly_data_optimized(2025, "All")
total2024_comparable = sum(data2024_all.get(month, 0) for month in monthsForComparison)
change25_vs_24partial = ((total2025Partial - total2024_comparable) / total2024_comparable * 100) if total2024_comparable > 0 else float('nan')
# Variación % Total (2024 vs 2023)
total2023 = annual_df["Frecuencia 2023"].sum()
change24_vs_23 = ((total2024 - total2023) / total2023 * 100) if total2023 > 0 else float('nan')
# Robos con Violencia (Julio 2025)
data_robos_2025 = get_monthly_data_optimized(2025, "ROBOS CON VIOLENCIA O INTIMIDACIÓN")
julioRobosViolencia = data_robos_2025.get("Julio", 0)
# Homicidios y Femicidios (Semana 12 2025)
data_homicidios_2025 = get_weekly_data_optimized(2025, "HOMICIDIOS Y FEMICIDIOS")
semana12Homicidios = data_homicidios_2025.get(12, 0)

# Mostrar métricas en columnas con diseño mejorado
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">📅</span>
        <h4 class="title">Total Casos 2024</h4>
        <p class="value">{format_number_chile(total2024)}</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">📈</span>
        <h4 class="title">Total Casos 2025 (a la fecha)</h4>
        <p class="value">{format_number_chile(total2025Partial)}</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">🚨</span>
        <h4 class="title">Delito Más Frecuente (2024)</h4>
        <p class="value"><strong>{mostFrequent2024['delito']}</strong><br>({format_number_chile(mostFrequent2024['total'])})</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">🔥</span>
        <h4 class="title">Delito Más Frecuente (2025 a la fecha)</h4>
        <p class="value"><strong>{mostFrequent2025['delito']}</strong><br>({format_number_chile(mostFrequent2025['total'])})</p>
    </div>
    """, unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)
with col5:
    color_class = "green" if not np.isnan(change25_vs_24partial) and change25_vs_24partial < 0 else "red"
    change_text = f"{abs(change25_vs_24partial):.1f}%" if not np.isnan(change25_vs_24partial) else "N/A"
    
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">↔️</span>
        <h4 class="title">Variación % (2025 vs Mismo Periodo 2024)</h4>
        <p class="value {color_class}">{change_text}</p>
    </div>
    """, unsafe_allow_html=True)
with col6:
    color_class = "green" if not np.isnan(change24_vs_23) and change24_vs_23 < 0 else "red"
    change_text = f"{abs(change24_vs_23):.1f}%" if not np.isnan(change24_vs_23) else "N/A"
    
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">⚡</span>
        <h4 class="title">Variación % Total (2024 vs 2023)</h4>
        <p class="value {color_class}">{change_text}</p>
    </div>
    """, unsafe_allow_html=True)
with col7:
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">🔪</span>
        <h4 class="title">Robos con Violencia (Julio 2025)</h4>
        <p class="value">{format_number_chile(julioRobosViolencia)}</p>
    </div>
    """, unsafe_allow_html=True)
with col8:
    st.markdown(f"""
    <div class="metric-card hover-effect">
        <span class="icon">💀</span>
        <h4 class="title">Homicidios y Femicidios (Semana 12 2025)</h4>
        <p class="value">{format_number_chile(semana12Homicidios)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sección de explicaciones con diseño mejorado
st.markdown('<div class="explanation-card">', unsafe_allow_html=True)
st.subheader("¿Qué son estos gráficos?")
st.markdown(f"""
Los gráficos muestran la **frecuencia de ocurrencia** de diferentes tipos de delitos en la Comuna de {COMUNA_NAME}. 
Esto nos ayuda a identificar patrones y cambios a lo largo del tiempo.
- **Gráfico Anual:** Compara la cantidad de casos en los años 2023, 2024 y lo que va de 2025.
- **Gráfico Mensual y Semanal:** Muestran el número de casos por mes/semana, permitiendo una **comparación directa entre 2024 y 2025**. 
  En la vista mensual, los valores futuros de 2025 son proyecciones.
""")
st.subheader("¿Cómo interpretar las tendencias?")
st.markdown("""
Un **aumento** en la frecuencia puede indicar un incremento real del delito, una mejora en los reportes, o una mayor actividad policial en ciertas áreas. 
Una **disminución** puede sugerir lo contrario.
Es crucial considerar el **contexto**: cambios en las leyes, operaciones policiales específicas, factores socioeconómicos, o incluso eventos estacionales pueden influir en estas cifras.
💡 **Dato Clave:**
Las cifras reales de 2025 están disponibles hasta julio para la vista mensual y las últimas semanas disponibles para la semanal. 
Los valores posteriores a julio en el gráfico mensual de 2025 son **proyecciones** basadas en el promedio de los meses ya reportados de 2025, 
y se visualizan con una **línea segmentada**.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Pie de página
st.markdown("""
<div class="footer">
    <p>&copy; 2025 Instituto Libertad. Datos proporcionados por Carabineros de Chile (Plataforma Ley STOP).</p>
</div>
""", unsafe_allow_html=True)