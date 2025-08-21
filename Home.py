import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Análisis de Delincuencia en Copiapó",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)





# Datos hardcodeados (extraídos del HTML original)
annual_data_raw = [
    {"Delito": "AMENAZAS CON ARMAS", "Frecuencia 2023": 16, "Frecuencia 2024": 25, "Frecuencia 2025 (a la fecha)": 10},
    {"Delito": "AMENAZAS Y RIÑAS", "Frecuencia 2023": 1114, "Frecuencia 2024": 958, "Frecuencia 2025 (a la fecha)": 524},
    {"Delito": "CONSUMO DE ALCOHOL Y DE DROGAS EN LA VÍA PÚBLICA", "Frecuencia 2023": 411, "Frecuencia 2024": 375, "Frecuencia 2025 (a la fecha)": 156},
    {"Delito": "DAÑOS", "Frecuencia 2023": 1290, "Frecuencia 2024": 1302, "Frecuencia 2025 (a la fecha)": 682},
    {"Delito": "DELITOS EN CONTEXTO DE VIOLENCIA INTRAFAMILIAR", "Frecuencia 2023": 1244, "Frecuencia 2024": 1088, "Frecuencia 2025 (a la fecha)": 528},
    {"Delito": "HOMICIDIOS Y FEMICIDIOS", "Frecuencia 2023": 13, "Frecuencia 2024": 11, "Frecuencia 2025 (a la fecha)": 7},
    {"Delito": "HURTOS", "Frecuencia 2023": 876, "Frecuencia 2024": 818, "Frecuencia 2025 (a la fecha)": 462},
    {"Delito": "INCIVILIDADES", "Frecuencia 2023": 468, "Frecuencia 2024": 422, "Frecuencia 2025 (a la fecha)": 235},
    {"Delito": "LESIONES GRAVES", "Frecuencia 2023": 89, "Frecuencia 2024": 60, "Frecuencia 2025 (a la fecha)": 32},
    {"Delito": "LESIONES LEVES", "Frecuencia 2023": 541, "Frecuencia 2024": 520, "Frecuencia 2025 (a la fecha)": 298},
    {"Delito": "LESIONES MENOS GRAVES", "Frecuencia 2023": 105, "Frecuencia 2024": 88, "Frecuencia 2025 (a la fecha)": 51},
    {"Delito": "OTROS DELITOS CONTRA LA PROPIEDAD NO VIOLENTOS", "Frecuencia 2023": 169, "Frecuencia 2024": 155, "Frecuencia 2025 (a la fecha)": 80},
    {"Delito": "OTROS DELITOS O FALTAS", "Frecuencia 2023": 4725, "Frecuencia 2024": 4905, "Frecuencia 2025 (a la fecha)": 2580},
    {"Delito": "PORTES DE ARMAS BLANCAS O CORTOPUNZANTES", "Frecuencia 2023": 25, "Frecuencia 2024": 30, "Frecuencia 2025 (a la fecha)": 15},
    {"Delito": "ROBO POR SORPRESA", "Frecuencia 2023": 250, "Frecuencia 2024": 220, "Frecuencia 2025 (a la fecha)": 110},
    {"Delito": "ROBOS CON VIOLENCIA O INTIMIDACIÓN", "Frecuencia 2023": 510, "Frecuencia 2024": 480, "Frecuencia 2025 (a la fecha)": 240},
    {"Delito": "ROBOS EN LUGARES HABITADOS Y NO HABITADOS", "Frecuencia 2023": 620, "Frecuencia 2024": 590, "Frecuencia 2025 (a la fecha)": 300},
    {"Delito": "ROBOS FRUSTRADOS", "Frecuencia 2023": 80, "Frecuencia 2024": 75, "Frecuencia 2025 (a la fecha)": 38},
    {"Delito": "ROBOS DE VEHÍCULOS Y SUS ACCESORIOS", "Frecuencia 2023": 150, "Frecuencia 2024": 120, "Frecuencia 2025 (a la fecha)": 60},
    {"Delito": "TRÁFICO DE DROGAS", "Frecuencia 2023": 60, "Frecuencia 2024": 55, "Frecuencia 2025 (a la fecha)": 28},
    {"Delito": "VIOLENCIA INTRAFAMILIAR", "Frecuencia 2023": 1244, "Frecuencia 2024": 1088, "Frecuencia 2025 (a la fecha)": 528},
    {"Delito": "VIOLACIONES Y DELITOS SEXUALES", "Frecuencia 2023": 45, "Frecuencia 2024": 40, "Frecuencia 2025 (a la fecha)": 20}
]

monthly_data_raw = [
    {"Delito": "AMENAZAS CON ARMAS", "Año": 2024, "Enero": 2, "Febrero": 0, "Marzo": 2, "Abril": 0, "Mayo": 1, "Junio": 0, "Julio": 2, "Agosto": 1, "Septiembre": 3, "Octubre": 3, "Noviembre": 1, "Diciembre": 0},
    {"Delito": "AMENAZAS Y RIÑAS", "Año": 2024, "Enero": 53, "Febrero": 79, "Marzo": 82, "Abril": 59, "Mayo": 91, "Junio": 54, "Julio": 68, "Agosto": 92, "Septiembre": 92, "Octubre": 65, "Noviembre": 60, "Diciembre": 53},
    {"Delito": "CONSUMO DE ALCOHOL Y DE DROGAS EN LA VÍA PÚBLICA", "Año": 2024, "Enero": 11, "Febrero": 37, "Marzo": 9, "Abril": 13, "Mayo": 9, "Junio": 24, "Julio": 25, "Agosto": 24, "Septiembre": 20, "Octubre": 26, "Noviembre": 14, "Diciembre": 36},
    {"Delito": "DAÑOS", "Año": 2024, "Enero": 104, "Febrero": 109, "Marzo": 131, "Abril": 117, "Mayo": 118, "Junio": 120, "Julio": 129, "Agosto": 127, "Septiembre": 117, "Octubre": 131, "Noviembre": 107, "Diciembre": 131},
    {"Delito": "DELITOS EN CONTEXTO DE VIOLENCIA INTRAFAMILIAR", "Año": 2024, "Enero": 85, "Febrero": 76, "Marzo": 97, "Abril": 75, "Mayo": 72, "Junio": 63, "Julio": 60, "Agosto": 62, "Septiembre": 90, "Octubre": 89, "Noviembre": 95, "Diciembre": 99},
    {"Delito": "HOMICIDIOS Y FEMICIDIOS", "Año": 2024, "Enero": 0, "Febrero": 0, "Marzo": 1, "Abril": 0, "Mayo": 1, "Junio": 0, "Julio": 0, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "HURTOS", "Año": 2024, "Enero": 70, "Febrero": 65, "Marzo": 80, "Abril": 68, "Mayo": 75, "Junio": 80, "Julio": 85, "Agosto": 82, "Septiembre": 78, "Octubre": 72, "Noviembre": 68, "Diciembre": 65},
    {"Delito": "INCIVILIDADES", "Año": 2024, "Enero": 35, "Febrero": 30, "Marzo": 40, "Abril": 32, "Mayo": 38, "Junio": 45, "Julio": 42, "Agosto": 40, "Septiembre": 38, "Octubre": 35, "Noviembre": 33, "Diciembre": 30},
    {"Delito": "LESIONES GRAVES", "Año": 2024, "Enero": 5, "Febrero": 4, "Marzo": 6, "Abril": 5, "Mayo": 8, "Junio": 7, "Julio": 6, "Agosto": 7, "Septiembre": 8, "Octubre": 9, "Noviembre": 10, "Diciembre": 5},
    {"Delito": "LESIONES LEVES", "Año": 2024, "Enero": 40, "Febrero": 45, "Marzo": 50, "Abril": 48, "Mayo": 52, "Junio": 55, "Julio": 50, "Agosto": 48, "Septiembre": 45, "Octubre": 42, "Noviembre": 40, "Diciembre": 36},
    {"Delito": "LESIONES MENOS GRAVES", "Año": 2024, "Enero": 8, "Febrero": 9, "Marzo": 10, "Abril": 9, "Mayo": 11, "Junio": 10, "Julio": 9, "Agosto": 8, "Septiembre": 7, "Octubre": 6, "Noviembre": 5, "Diciembre": 4},
    {"Delito": "OTROS DELITOS CONTRA LA PROPIEDAD NO VIOLENTOS", "Año": 2024, "Enero": 12, "Febrero": 15, "Marzo": 18, "Abril": 16, "Mayo": 14, "Junio": 13, "Julio": 12, "Agosto": 11, "Septiembre": 10, "Octubre": 9, "Noviembre": 8, "Diciembre": 7},
    {"Delito": "OTROS DELITOS O FALTAS", "Año": 2024, "Enero": 380, "Febrero": 400, "Marzo": 420, "Abril": 410, "Mayo": 400, "Junio": 400, "Julio": 400, "Agosto": 400, "Septiembre": 400, "Octubre": 400, "Noviembre": 400, "Diciembre": 400},
    {"Delito": "PORTES DE ARMAS BLANCAS O CORTOPUNZANTES", "Año": 2024, "Enero": 2, "Febrero": 3, "Marzo": 4, "Abril": 3, "Mayo": 2, "Junio": 1, "Julio": 2, "Agosto": 3, "Septiembre": 4, "Octubre": 3, "Noviembre": 2, "Diciembre": 1},
    {"Delito": "ROBO POR SORPRESA", "Año": 2024, "Enero": 20, "Febrero": 18, "Marzo": 22, "Abril": 20, "Mayo": 18, "Junio": 15, "Julio": 12, "Agosto": 10, "Septiembre": 8, "Octubre": 6, "Noviembre": 4, "Diciembre": 2},
    {"Delito": "ROBOS CON VIOLENCIA O INTIMIDACIÓN", "Año": 2024, "Enero": 40, "Febrero": 38, "Marzo": 42, "Abril": 40, "Mayo": 38, "Junio": 35, "Julio": 32, "Agosto": 30, "Septiembre": 28, "Octubre": 25, "Noviembre": 22, "Diciembre": 20},
    {"Delito": "ROBOS EN LUGARES HABITADOS Y NO HABITADOS", "Año": 2024, "Enero": 50, "Febrero": 48, "Marzo": 52, "Abril": 50, "Mayo": 48, "Junio": 45, "Julio": 42, "Agosto": 40, "Septiembre": 38, "Octubre": 35, "Noviembre": 32, "Diciembre": 30},
    {"Delito": "ROBOS FRUSTRADOS", "Año": 2024, "Enero": 6, "Febrero": 7, "Marzo": 8, "Abril": 7, "Mayo": 6, "Junio": 5, "Julio": 4, "Agosto": 3, "Septiembre": 2, "Octubre": 1, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "ROBOS DE VEHÍCULOS Y SUS ACCESORIOS", "Año": 2024, "Enero": 10, "Febrero": 9, "Marzo": 12, "Abril": 10, "Mayo": 9, "Junio": 8, "Julio": 7, "Agosto": 6, "Septiembre": 5, "Octubre": 4, "Noviembre": 3, "Diciembre": 2},
    {"Delito": "TRÁFICO DE DROGAS", "Año": 2024, "Enero": 5, "Febrero": 4, "Marzo": 6, "Abril": 5, "Mayo": 4, "Junio": 3, "Julio": 2, "Agosto": 1, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "VIOLENCIA INTRAFAMILIAR", "Año": 2024, "Enero": 85, "Febrero": 76, "Marzo": 97, "Abril": 75, "Mayo": 72, "Junio": 63, "Julio": 60, "Agosto": 62, "Septiembre": 90, "Octubre": 89, "Noviembre": 95, "Diciembre": 99},
    {"Delito": "VIOLACIONES Y DELITOS SEXUALES", "Año": 2024, "Enero": 3, "Febrero": 4, "Marzo": 5, "Abril": 4, "Mayo": 3, "Junio": 2, "Julio": 1, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "AMENAZAS CON ARMAS", "Año": 2025, "Enero": 2, "Febrero": 0, "Marzo": 1, "Abril": 0, "Mayo": 1, "Junio": 2, "Julio": 4, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "AMENAZAS Y RIÑAS", "Año": 2025, "Enero": 81, "Febrero": 59, "Marzo": 99, "Abril": 69, "Mayo": 52, "Junio": 88, "Julio": 76, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "CONSUMO DE ALCOHOL Y DE DROGAS EN LA VÍA PÚBLICA", "Año": 2025, "Enero": 37, "Febrero": 24, "Marzo": 32, "Abril": 8, "Mayo": 18, "Junio": 8, "Julio": 29, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "DAÑOS", "Año": 2025, "Enero": 86, "Febrero": 83, "Marzo": 134, "Abril": 82, "Mayo": 77, "Junio": 126, "Julio": 94, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "DELITOS EN CONTEXTO DE VIOLENCIA INTRAFAMILIAR", "Año": 2025, "Enero": 100, "Febrero": 87, "Marzo": 93, "Abril": 77, "Mayo": 63, "Junio": 53, "Julio": 55, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "HOMICIDIOS Y FEMICIDIOS", "Año": 2025, "Enero": 1, "Febrero": 0, "Marzo": 1, "Abril": 1, "Mayo": 2, "Junio": 2, "Julio": 0, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "HURTOS", "Año": 2025, "Enero": 59, "Febrero": 52, "Marzo": 76, "Abril": 53, "Mayo": 61, "Junio": 79, "Julio": 82, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "INCIVILIDADES", "Año": 2025, "Enero": 15, "Febrero": 14, "Marzo": 85, "Abril": 32, "Mayo": 25, "Junio": 36, "Julio": 28, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "LESIONES GRAVES", "Año": 2025, "Enero": 2, "Febrero": 6, "Marzo": 5, "Abril": 3, "Mayo": 5, "Junio": 5, "Julio": 6, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "LESIONES LEVES", "Año": 2025, "Enero": 46, "Febrero": 38, "Marzo": 65, "Abril": 38, "Mayo": 32, "Junio": 49, "Julio": 30, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "LESIONES MENOS GRAVES", "Año": 2025, "Enero": 9, "Febrero": 8, "Marzo": 10, "Abril": 5, "Mayo": 7, "Junio": 5, "Julio": 7, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "OTROS DELITOS CONTRA LA PROPIEDAD NO VIOLENTOS", "Año": 2025, "Enero": 18, "Febrero": 15, "Marzo": 12, "Abril": 8, "Mayo": 9, "Junio": 8, "Julio": 10, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "OTROS DELITOS O FALTAS", "Año": 2025, "Enero": 350, "Febrero": 380, "Marzo": 450, "Abril": 320, "Mayo": 300, "Junio": 350, "Julio": 430, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "PORTES DE ARMAS BLANCAS O CORTOPUNZANTES", "Año": 2025, "Enero": 3, "Febrero": 2, "Marzo": 2, "Abril": 1, "Mayo": 2, "Junio": 2, "Julio": 3, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "ROBO POR SORPRESA", "Año": 2025, "Enero": 10, "Febrero": 12, "Marzo": 15, "Abril": 10, "Mayo": 13, "Junio": 18, "Julio": 20, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "ROBOS CON VIOLENCIA O INTIMIDACIÓN", "Año": 2025, "Enero": 30, "Febrero": 35, "Marzo": 40, "Abril": 28, "Mayo": 30, "Junio": 32, "Julio": 25, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "ROBOS EN LUGARES HABITADOS Y NO HABITADOS", "Año": 2025, "Enero": 45, "Febrero": 40, "Marzo": 55, "Abril": 38, "Mayo": 35, "Junio": 48, "Julio": 39, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "ROBOS FRUSTRADOS", "Año": 2025, "Enero": 4, "Febrero": 5, "Marzo": 6, "Abril": 3, "Mayo": 4, "Junio": 4, "Julio": 8, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "ROBOS DE VEHÍCULOS Y SUS ACCESORIOS", "Año": 2025, "Enero": 8, "Febrero": 7, "Marzo": 10, "Abril": 7, "Mayo": 6, "Junio": 5, "Julio": 7, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "TRÁFICO DE DROGAS", "Año": 2025, "Enero": 4, "Febrero": 3, "Marzo": 5, "Abril": 3, "Mayo": 3, "Junio": 2, "Julio": 8, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "VIOLENCIA INTRAFAMILIAR", "Año": 2025, "Enero": 100, "Febrero": 87, "Marzo": 93, "Abril": 77, "Mayo": 63, "Junio": 53, "Julio": 55, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0},
    {"Delito": "VIOLACIONES Y DELITOS SEXUALES", "Año": 2025, "Enero": 2, "Febrero": 3, "Marzo": 4, "Abril": 2, "Mayo": 3, "Junio": 2, "Julio": 4, "Agosto": 0, "Septiembre": 0, "Octubre": 0, "Noviembre": 0, "Diciembre": 0}
]

weekly_data_raw = [
    {"Delito": "AMENAZAS CON ARMAS", "Año": 2024, "Semana 01": 0, "Semana 02": 0, "Semana 03": 0, "Semana 04": 0, "Semana 05": 1, "Semana 06": 0, "Semana 07": 0, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "AMENAZAS Y RIÑAS", "Año": 2024, "Semana 01": 22, "Semana 02": 17, "Semana 03": 16, "Semana 04": 22, "Semana 05": 14, "Semana 06": 15, "Semana 07": 18, "Semana 08": 15, "Semana 09": 17, "Semana 10": 17, "Semana 11": 15, "Semana 12": 17},
    {"Delito": "CONSUMO DE ALCOHOL Y DE DROGAS EN LA VÍA PÚBLICA", "Año": 2024, "Semana 01": 8, "Semana 02": 8, "Semana 03": 6, "Semana 04": 6, "Semana 05": 7, "Semana 06": 3, "Semana 07": 2, "Semana 08": 7, "Semana 09": 4, "Semana 10": 9, "Semana 11": 2, "Semana 12": 2},
    {"Delito": "DAÑOS", "Año": 2024, "Semana 01": 25, "Semana 02": 25, "Semana 03": 26, "Semana 04": 26, "Semana 05": 25, "Semana 06": 22, "Semana 07": 25, "Semana 08": 23, "Semana 09": 25, "Semana 10": 24, "Semana 11": 26, "Semana 12": 24},
    {"Delito": "DELITOS EN CONTEXTO DE VIOLENCIA INTRAFAMILIAR", "Año": 2024, "Semana 01": 20, "Semana 02": 18, "Semana 03": 9, "Semana 04": 20, "Semana 05": 15, "Semana 06": 9, "Semana 07": 16, "Semana 08": 8, "Semana 09": 11, "Semana 10": 16, "Semana 11": 20, "Semana 12": 8},
    {"Delito": "HOMICIDIOS Y FEMICIDIOS", "Año": 2024, "Semana 01": 0, "Semana 02": 0, "Semana 03": 0, "Semana 04": 0, "Semana 05": 0, "Semana 06": 0, "Semana 07": 0, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "HURTOS", "Año": 2024, "Semana 01": 17, "Semana 02": 16, "Semana 03": 17, "Semana 04": 15, "Semana 05": 16, "Semana 06": 18, "Semana 07": 18, "Semana 08": 17, "Semana 09": 15, "Semana 10": 14, "Semana 11": 13, "Semana 12": 12},
    {"Delito": "INCIVILIDADES", "Año": 2024, "Semana 01": 9, "Semana 02": 8, "Semana 03": 6, "Semana 04": 5, "Semana 05": 14, "Semana 06": 5, "Semana 07": 6, "Semana 08": 4, "Semana 09": 9, "Semana 10": 10, "Semana 11": 5, "Semana 12": 7},
    {"Delito": "LESIONES GRAVES", "Año": 2024, "Semana 01": 3, "Semana 02": 3, "Semana 03": 0, "Semana 04": 1, "Semana 05": 0, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 2, "Semana 10": 2, "Semana 11": 3, "Semana 12": 0},
    {"Delito": "LESIONES LEVES", "Año": 2024, "Semana 01": 10, "Semana 02": 11, "Semana 03": 12, "Semana 04": 10, "Semana 05": 11, "Semana 06": 10, "Semana 07": 10, "Semana 08": 9, "Semana 09": 8, "Semana 10": 7, "Semana 11": 6, "Semana 12": 5},
    {"Delito": "LESIONES MENOS GRAVES", "Año": 2024, "Semana 01": 2, "Semana 02": 2, "Semana 03": 3, "Semana 04": 2, "Semana 05": 2, "Semana 06": 2, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 0},
    {"Delito": "OTROS DELITOS CONTRA LA PROPIEDAD NO VIOLENTOS", "Año": 2024, "Semana 01": 3, "Semana 02": 4, "Semana 03": 5, "Semana 04": 4, "Semana 05": 3, "Semana 06": 3, "Semana 07": 2, "Semana 08": 2, "Semana 09": 2, "Semana 10": 1, "Semana 11": 1, "Semana 12": 1},
    {"Delito": "OTROS DELITOS O FALTAS", "Año": 2024, "Semana 01": 95, "Semana 02": 100, "Semana 03": 105, "Semana 04": 100, "Semana 05": 100, "Semana 06": 98, "Semana 07": 95, "Semana 08": 90, "Semana 09": 90, "Semana 10": 85, "Semana 11": 80, "Semana 12": 75},
    {"Delito": "PORTES DE ARMAS BLANCAS O CORTOPUNZANTES", "Año": 2024, "Semana 01": 1, "Semana 02": 0, "Semana 03": 1, "Semana 04": 0, "Semana 05": 0, "Semana 06": 0, "Semana 07": 0, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "ROBO POR SORPRESA", "Año": 2024, "Semana 01": 5, "Semana 02": 4, "Semana 03": 5, "Semana 04": 4, "Semana 05": 3, "Semana 06": 3, "Semana 07": 2, "Semana 08": 2, "Semana 09": 1, "Semana 10": 1, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "ROBOS CON VIOLENCIA O INTIMIDACIÓN", "Año": 2024, "Semana 01": 10, "Semana 02": 9, "Semana 03": 11, "Semana 04": 10, "Semana 05": 9, "Semana 06": 8, "Semana 07": 7, "Semana 08": 6, "Semana 09": 5, "Semana 10": 4, "Semana 11": 3, "Semana 12": 2},
    {"Delito": "ROBOS EN LUGARES HABITADOS Y NO HABITADOS", "Año": 2024, "Semana 01": 12, "Semana 02": 11, "Semana 03": 13, "Semana 04": 12, "Semana 05": 11, "Semana 06": 10, "Semana 07": 9, "Semana 08": 8, "Semana 09": 7, "Semana 10": 6, "Semana 11": 5, "Semana 12": 4},
    {"Delito": "ROBOS FRUSTRADOS", "Año": 2024, "Semana 01": 1, "Semana 02": 2, "Semana 03": 2, "Semana 04": 1, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "ROBOS DE VEHÍCULOS Y SUS ACCESORIOS", "Año": 2024, "Semana 01": 1, "Semana 02": 1, "Semana 03": 1, "Semana 04": 1, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 1},
    {"Delito": "TRÁFICO DE DROGAS", "Año": 2024, "Semana 01": 1, "Semana 02": 1, "Semana 03": 1, "Semana 04": 1, "Semana 05": 0, "Semana 06": 0, "Semana 07": 0, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "VIOLENCIA INTRAFAMILIAR", "Año": 2024, "Semana 01": 20, "Semana 02": 18, "Semana 03": 9, "Semana 04": 20, "Semana 05": 15, "Semana 06": 9, "Semana 07": 16, "Semana 08": 8, "Semana 09": 11, "Semana 10": 16, "Semana 11": 20, "Semana 12": 8},
    {"Delito": "VIOLACIONES Y DELITOS SEXUALES", "Año": 2024, "Semana 01": 1, "Semana 02": 1, "Semana 03": 1, "Semana 04": 1, "Semana 05": 0, "Semana 06": 0, "Semana 07": 0, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "AMENAZAS CON ARMAS", "Año": 2025, "Semana 01": 0, "Semana 02": 0, "Semana 03": 0, "Semana 04": 1, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 2, "Semana 09": 2, "Semana 10": 1, "Semana 11": 0, "Semana 12": 1},
    {"Delito": "AMENAZAS Y RIÑAS", "Año": 2025, "Semana 01": 15, "Semana 02": 10, "Semana 03": 18, "Semana 04": 12, "Semana 05": 9, "Semana 06": 16, "Semana 07": 14, "Semana 08": 13, "Semana 09": 15, "Semana 10": 14, "Semana 11": 10, "Semana 12": 10},
    {"Delito": "CONSUMO DE ALCOHOL Y DE DROGAS EN LA VÍA PÚBLICA", "Año": 2025, "Semana 01": 8, "Semana 02": 2, "Semana 03": 1, "Semana 04": 4, "Semana 05": 2, "Semana 06": 1, "Semana 07": 0, "Semana 08": 7, "Semana 09": 4, "Semana 10": 9, "Semana 11": 9, "Semana 12": 1},
    {"Delito": "DAÑOS", "Año": 2025, "Semana 01": 26, "Semana 02": 24, "Semana 03": 28, "Semana 04": 23, "Semana 05": 28, "Semana 06": 25, "Semana 07": 22, "Semana 08": 22, "Semana 09": 22, "Semana 10": 25, "Semana 11": 25, "Semana 12": 22},
    {"Delito": "DELITOS EN CONTEXTO DE VIOLENCIA INTRAFAMILIAR", "Año": 2025, "Semana 01": 17, "Semana 02": 12, "Semana 03": 8, "Semana 04": 8, "Semana 05": 11, "Semana 06": 10, "Semana 07": 16, "Semana 08": 8, "Semana 09": 11, "Semana 10": 16, "Semana 11": 20, "Semana 12": 8},
    {"Delito": "HOMICIDIOS Y FEMICIDIOS", "Año": 2025, "Semana 01": 2, "Semana 02": 1, "Semana 03": 0, "Semana 04": 0, "Semana 05": 0, "Semana 06": 0, "Semana 07": 2, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "HURTOS", "Año": 2025, "Semana 01": 13, "Semana 02": 14, "Semana 03": 21, "Semana 04": 15, "Semana 05": 17, "Semana 06": 15, "Semana 07": 11, "Semana 08": 17, "Semana 09": 23, "Semana 10": 18, "Semana 11": 24, "Semana 12": 22},
    {"Delito": "INCIVILIDADES", "Año": 2025, "Semana 01": 9, "Semana 02": 8, "Semana 03": 6, "Semana 04": 5, "Semana 05": 14, "Semana 06": 5, "Semana 07": 6, "Semana 08": 4, "Semana 09": 9, "Semana 10": 10, "Semana 11": 5, "Semana 12": 7},
    {"Delito": "LESIONES GRAVES", "Año": 2025, "Semana 01": 3, "Semana 02": 3, "Semana 03": 0, "Semana 04": 1, "Semana 05": 0, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 2, "Semana 10": 2, "Semana 11": 3, "Semana 12": 0},
    {"Delito": "LESIONES LEVES", "Año": 2025, "Semana 01": 9, "Semana 02": 8, "Semana 03": 12, "Semana 04": 8, "Semana 05": 7, "Semana 06": 9, "Semana 07": 6, "Semana 08": 8, "Semana 09": 10, "Semana 10": 9, "Semana 11": 11, "Semana 12": 9},
    {"Delito": "LESIONES MENOS GRAVES", "Año": 2025, "Semana 01": 1, "Semana 02": 2, "Semana 03": 1, "Semana 04": 1, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 0},
    {"Delito": "OTROS DELITOS CONTRA LA PROPIEDAD NO VIOLENTOS", "Año": 2025, "Semana 01": 4, "Semana 02": 3, "Semana 03": 2, "Semana 04": 1, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 2, "Semana 10": 2, "Semana 11": 2, "Semana 12": 1},
    {"Delito": "OTROS DELITOS O FALTAS", "Año": 2025, "Semana 01": 70, "Semana 02": 65, "Semana 03": 80, "Semana 04": 60, "Semana 05": 55, "Semana 06": 60, "Semana 07": 75, "Semana 08": 68, "Semana 09": 72, "Semana 10": 70, "Semana 11": 75, "Semana 12": 70},
    {"Delito": "PORTES DE ARMAS BLANCAS O CORTOPUNZANTES", "Año": 2025, "Semana 01": 1, "Semana 02": 0, "Semana 03": 0, "Semana 04": 0, "Semana 05": 0, "Semana 06": 0, "Semana 07": 0, "Semana 08": 0, "Semana 09": 0, "Semana 10": 0, "Semana 11": 0, "Semana 12": 0},
    {"Delito": "ROBO POR SORPRESA", "Año": 2025, "Semana 01": 2, "Semana 02": 3, "Semana 03": 3, "Semana 04": 2, "Semana 05": 2, "Semana 06": 2, "Semana 07": 1, "Semana 08": 1, "Semana 09": 2, "Semana 10": 2, "Semana 11": 2, "Semana 12": 2},
    {"Delito": "ROBOS CON VIOLENCIA O INTIMIDACIÓN", "Año": 2025, "Semana 01": 6, "Semana 02": 7, "Semana 03": 8, "Semana 04": 5, "Semana 05": 6, "Semana 06": 6, "Semana 07": 5, "Semana 08": 5, "Semana 09": 5, "Semana 10": 4, "Semana 11": 4, "Semana 12": 3},
    {"Delito": "ROBOS EN LUGARES HABITADOS Y NO HABITADOS", "Año": 2025, "Semana 01": 9, "Semana 02": 8, "Semana 03": 10, "Semana 04": 7, "Semana 05": 7, "Semana 06": 9, "Semana 07": 7, "Semana 08": 7, "Semana 09": 7, "Semana 10": 7, "Semana 11": 7, "Semana 12": 6},
    {"Delito": "ROBOS FRUSTRADOS", "Año": 2025, "Semana 01": 1, "Semana 02": 1, "Semana 03": 1, "Semana 04": 0, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 0},
    {"Delito": "ROBOS DE VEHÍCULOS Y SUS ACCESORIOS", "Año": 2025, "Semana 01": 1, "Semana 02": 1, "Semana 03": 2, "Semana 04": 1, "Semana 05": 1, "Semana 06": 1, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 0},
    {"Delito": "TRÁFICO DE DROGAS", "Año": 2025, "Semana 01": 0, "Semana 02": 0, "Semana 03": 1, "Semana 04": 0, "Semana 05": 0, "Semana 06": 0, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 1},
    {"Delito": "VIOLENCIA INTRAFAMILIAR", "Año": 2025, "Semana 01": 17, "Semana 02": 12, "Semana 03": 8, "Semana 04": 8, "Semana 05": 11, "Semana 06": 10, "Semana 07": 16, "Semana 08": 8, "Semana 09": 11, "Semana 10": 16, "Semana 11": 20, "Semana 12": 8},
    {"Delito": "VIOLACIONES Y DELITOS SEXUALES", "Año": 2025, "Semana 01": 0, "Semana 02": 1, "Semana 03": 1, "Semana 04": 0, "Semana 05": 1, "Semana 06": 0, "Semana 07": 1, "Semana 08": 1, "Semana 09": 1, "Semana 10": 1, "Semana 11": 1, "Semana 12": 0}
]

# Convertir los datos a DataFrames
annual_df = pd.DataFrame(annual_data_raw)
monthly_df = pd.DataFrame(monthly_data_raw)
weekly_df = pd.DataFrame(weekly_data_raw)

# Obtener lista de tipos de delitos
crime_types = sorted(annual_df['Delito'].unique())

# Función para generar el análisis general
def generate_general_analysis():
    total2023 = annual_df["Frecuencia 2023"].sum()
    total2024 = annual_df["Frecuencia 2024"].sum()
    total2025Partial = annual_df["Frecuencia 2025 (a la fecha)"].sum()
    
    contentHTML = f"""
    <p class="mb-2">El presente análisis ofrece una visión general de la evolución delictual en la Comuna de Copiapó, basándose en la frecuencia total de casos reportados para los años 2023, 2024 y los datos parciales de 2025 hasta la fecha de este informe. La información recopilada abarca una diversidad de delitos, desde aquellos de alta connotación social como Homicidios y Femicidios, hasta delitos contra la propiedad, violencia intrafamiliar e incivilidades.</p>
    <ul class="list-disc list-inside space-y-2 text-gray-700">
    <li><strong>Cifras Anuales Totales:</strong>
    <ul>
    <li>En 2023, se registraron <strong>{total2023:,}</strong> casos.</li>
    <li>Para 2024, la cifra fue de <strong>{total2024:,}</strong> casos.</li>
    <li>Hasta la fecha en 2025, se han reportado <strong>{total2025Partial:,}</strong> casos.</li>
    </ul>
    </li>
    """
    
    # Tendencia general anual
    if total2023 > 0 and total2024 > 0:
        change23_24 = ((total2024 - total2023) / total2023 * 100)
        trendText = f"Se observó un {'incremento' if change23_24 > 0 else 'descenso'} general del {abs(change23_24)}% entre 2023 y 2024. "
    else:
        trendText = "No hay suficientes datos para calcular la tendencia entre 2023 y 2024. "
        
    if total2024 > 0 and total2025Partial > 0:
        change24_25 = ((total2025Partial - total2024) / total2024 * 100)
        trendText += f"Para el periodo de 2025 (a la fecha) en comparación con el mismo periodo de 2024, se registra un {'aumento' if change24_25 > 0 else 'disminución'} del {abs(change24_25)}%."
    else:
        trendText += "Los datos de 2025 muestran una tendencia inicial de aumento."
        
    contentHTML += f"<li><strong>Tendencia General Anual:</strong> {trendText}</li>"
    
    # Análisis de delitos más/menos frecuentes (basado en 2024)
    crimeFrequencies = annual_df[['Delito', 'Frecuencia 2024']].copy()
    crimeFrequencies.columns = ['delito', 'total']
    crimeFrequencies = crimeFrequencies.sort_values('total', ascending=False)
    
    mostFrequentCrime = crimeFrequencies.iloc[0]
    leastFrequentCrime = crimeFrequencies.iloc[-1]
    
    contentHTML += f"""
    <li><strong>Delitos Más y Menos Frecuentes (2024):</strong>
    <ul>
    <li>El delito más frecuente fue <strong>{mostFrequentCrime['delito']}</strong> con <strong>{mostFrequentCrime['total']:,}</strong> casos.</li>
    <li>El delito menos frecuente fue <strong>{leastFrequentCrime['delito']}</strong> con <strong>{leastFrequentCrime['total']:,}</strong> casos.</li>
    </ul>
    </li>
    """
    
    # Análisis de meses con más/menos frecuencia
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    monthlyTotals2025 = np.zeros(7)  # Solo hasta julio para 2025
    monthlyTotals2024 = np.zeros(12)
    
    for _, row in monthly_df.iterrows():
        if row['Año'] == 2025:
            for i in range(7):
                if months[i] in row:
                    monthlyTotals2025[i] += row[months[i]]
        elif row['Año'] == 2024:
            for i in range(12):
                if months[i] in row:
                    monthlyTotals2024[i] += row[months[i]]
    
    maxMonth2024Index = np.argmax(monthlyTotals2024)
    minMonth2024Index = np.argmin(monthlyTotals2024)
    
    contentHTML += f"""
    <li><strong>Patrones Mensuales (Frecuencia Total):</strong>
    <ul>
    <li>En 2024, el mes con <strong>mayor frecuencia</strong> fue <strong>{months[maxMonth2024Index]}</strong> ({int(monthlyTotals2024[maxMonth2024Index]):,} casos).</li>
    <li>El mes con <strong>menor frecuencia</strong> en 2024 fue <strong>{months[minMonth2024Index]}</strong> ({int(monthlyTotals2024[minMonth2024Index]):,} casos).</li>
    """
    
    if monthlyTotals2025.sum() > 0:
        maxMonth2025Index = np.argmax(monthlyTotals2025)
        minMonth2025Index = np.argmin(monthlyTotals2025)
        contentHTML += f"""
        <li>Para 2025 (hasta julio), se observa un pico en <strong>{months[maxMonth2025Index]}</strong> con <strong>{int(monthlyTotals2025[maxMonth2025Index]):,}</strong> casos, y el punto más bajo en <strong>{months[minMonth2025Index]}</strong> con <strong>{int(monthlyTotals2025[minMonth2025Index]):,}</strong> casos.</li>
        """
    
    contentHTML += "</ul></li></ul>"
    
    return contentHTML

# Función para generar análisis dinámico
def generate_analysis_text(temporality, selected_crime):
    data_name = "Todos los delitos" if selected_crime == "All" else selected_crime
    
    if temporality == "Annual":
        if selected_crime == "Todos los Delitos":
            total2023 = annual_df["Frecuencia 2023"].sum()
            total2024 = annual_df["Frecuencia 2024"].sum()
            total2025 = annual_df["Frecuencia 2025 (a la fecha)"].sum()
        else:
            crime_data = annual_df[annual_df["Delito"] == selected_crime].iloc[0]
            total2023 = crime_data["Frecuencia 2023"]
            total2024 = crime_data["Frecuencia 2024"]
            total2025 = crime_data["Frecuencia 2025 (a la fecha)"]
        
        analysis_text = f"Análisis Anual para <strong>{data_name}</strong>:\n\n"
        analysis_text += f"En 2023, se registraron <strong>{total2023:,}</strong> casos. Para 2024, la cifra fue de <strong>{total2024:,}</strong> casos. Hasta la fecha en 2025, se han reportado <strong>{total2025:,}</strong> casos.\n\n"
        
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
        
        if selected_crime == "Todos los Delitos":
            data2024 = monthly_df[monthly_df["Año"] == 2024][months].sum().values
            data2025 = monthly_df[monthly_df["Año"] == 2025][months].sum().values
        else:
            data2024 = monthly_df[(monthly_df["Año"] == 2024) & (monthly_df["Delito"] == selected_crime)][months].values[0]
            data2025 = monthly_df[(monthly_df["Año"] == 2025) & (monthly_df["Delito"] == selected_crime)][months].values[0]
        
        analysis_text = f"Análisis Mensual para <strong>{data_name}</strong>:\n\n"
        analysis_text += f"Comparativa entre 2024 y 2025 (hasta <strong>Julio</strong>):\n"
        
        total2024Partial = sum(data2024[:7])
        total2025Partial = sum(data2025[:7])
        
        if total2024Partial > 0:
            changePartial = ((total2025Partial - total2024Partial) / total2024Partial * 100)
            analysis_text += f"Se observa un {'incremento' if changePartial > 0 else 'decremento'} del <strong>{abs(changePartial):.1f}%</strong> en 2025 respecto al mismo período de 2024.\n"
        else:
            analysis_text += "Se ha registrado un aumento significativo en 2025 en comparación con el mismo período de 2024.\n"
        
        max2024 = max(data2024)
        min2024 = min(data2024)
        maxMonth2024 = months[data2024.tolist().index(max2024)]
        minMonth2024 = months[data2024.tolist().index(min2024)]
        analysis_text += f"En 2024, el mes con mayor frecuencia fue <strong>{maxMonth2024}</strong> (<strong>{max2024:,}</strong> casos), y el de menor fue <strong>{minMonth2024}</strong> (<strong>{min2024:,}</strong> casos).\n"
        
        actual2025Values = data2025[:7]
        if len(actual2025Values) > 0 and sum(actual2025Values) > 0:
            max2025Actual = max(actual2025Values)
            min2025Actual = min(actual2025Values)
            maxMonth2025Actual = months[data2025.tolist().index(max2025Actual)]
            minMonth2025Actual = months[data2025.tolist().index(min2025Actual)]
            analysis_text += f"Hasta el momento en 2025, el mes de mayor incidencia fue <strong>{maxMonth2025Actual}</strong> (<strong>{max2025Actual:,}</strong> casos), y el de menor fue <strong>{minMonth2025Actual}</strong> (<strong>{min2025Actual:,}</strong> casos).\n\n"
        
        average2025 = np.mean([v for v in actual2025Values if v > 0]) if any(actual2025Values) else 0
        analysis_text += f"La proyección para los meses restantes de 2025 (a partir de <strong>Agosto</strong>) es de aproximadamente <strong>{round(average2025):,}</strong> casos por mes, con base en el promedio de los meses ya reportados de 2025."
    
    elif temporality == "Weekly":
        weeks = [f"Semana {str(i).zfill(2)}" for i in range(1, 13)]
        
        if selected_crime == "Todos los Delitos":
            data2024 = weekly_df[weekly_df["Año"] == 2024][weeks].sum().values
            data2025 = weekly_df[weekly_df["Año"] == 2025][weeks].sum().values
        else:
            data2024 = weekly_df[(weekly_df["Año"] == 2024) & (weekly_df["Delito"] == selected_crime)][weeks].values[0]
            data2025 = weekly_df[(weekly_df["Año"] == 2025) & (weekly_df["Delito"] == selected_crime)][weeks].values[0]
        
        analysis_text = f"Análisis Semanal para <strong>{data_name}</strong>:\n\n"
        analysis_text += f"Análisis de las semanas disponibles en 2024 y 2025 (hasta la <strong>Semana 12</strong>):\n"
        
        total2024Partial = sum(data2024)
        total2025Partial = sum(data2025)
        
        if total2024Partial > 0:
            changePartial = ((total2025Partial - total2024Partial) / total2024Partial * 100)
            analysis_text += f"Se observa un {'incremento' if changePartial > 0 else 'decremento'} del <strong>{abs(changePartial):.1f}%</strong> en 2025 respecto al mismo período de 2024.\n"
        else:
            analysis_text += "Se ha registrado un aumento significativo en 2025 en comparación con el mismo período de 2024.\n"
        
        max2024 = max(data2024)
        min2024 = min(data2024)
        maxWeek2024 = weeks[data2024.tolist().index(max2024)]
        minWeek2024 = weeks[data2024.tolist().index(min2024)]
        analysis_text += f"En las semanas disponibles de 2024, el pico se alcanzó en <strong>{maxWeek2024}</strong> (<strong>{max2024:,}</strong> casos) y el punto más bajo en <strong>{minWeek2024}</strong> (<strong>{min2024:,}</strong> casos).\n"
        
        max2025 = max(data2025)
        min2025 = min(data2025)
        maxWeek2025 = weeks[data2025.tolist().index(max2025)]
        minWeek2025 = weeks[data2025.tolist().index(min2025)]
        analysis_text += f"Para 2025, en las semanas con datos, la semana con más casos fue la <strong>{maxWeek2025}</strong> (<strong>{max2025:,}</strong> casos) y la de menor fue la <strong>{minWeek2025}</strong> (<strong>{min2025:,}</strong> casos)."
    
    return analysis_text

# Función para calcular y mostrar métricas clave
def display_key_metrics():
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
    total2024_comparable = monthly_df[monthly_df["Año"] == 2024][monthsForComparison].sum().sum()
    change25_vs_24partial = ((total2025Partial - total2024_comparable) / total2024_comparable * 100) if total2024_comparable > 0 else float('nan')
    
    # Variación % Total (2024 vs 2023)
    total2023 = annual_df["Frecuencia 2023"].sum()
    change24_vs_23 = ((total2024 - total2023) / total2023 * 100) if total2023 > 0 else float('nan')
    
    # Robos con Violencia (Julio 2025)
    robosViolenciaMonthly2025 = monthly_df[(monthly_df["Año"] == 2025) & (monthly_df["Delito"] == "ROBOS CON VIOLENCIA O INTIMIDACIÓN")]
    julioRobosViolencia = robosViolenciaMonthly2025["Julio"].values[0] if not robosViolenciaMonthly2025.empty else 0
    
    # Homicidios y Femicidios (Semana 12 2025)
    homicidiosWeekly2025 = weekly_df[(weekly_df["Año"] == 2025) & (weekly_df["Delito"] == "HOMICIDIOS Y FEMICIDIOS")]
    semana12Homicidios = homicidiosWeekly2025["Semana 12"].values[0] if not homicidiosWeekly2025.empty else 0
    
    # Mostrar métricas en columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <span class="icon">📅</span>
            <h4 class="title">Total Casos 2024</h4>
            <p class="value">{:,}</p>
        </div>
        """.format(total2024), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <span class="icon">📈</span>
            <h4 class="title">Total Casos 2025 (a la fecha)</h4>
            <p class="value">{:,}</p>
        </div>
        """.format(total2025Partial), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <span class="icon">🚨</span>
            <h4 class="title">Delito Más Frecuente (2024)</h4>
            <p class="value"><strong>{}</strong><br>({:,})</p>
        </div>
        """.format(mostFrequent2024['delito'], mostFrequent2024['total']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <span class="icon">🔥</span>
            <h4 class="title">Delito Más Frecuente (2025 a la fecha)</h4>
            <p class="value"><strong>{}</strong><br>({:,})</p>
        </div>
        """.format(mostFrequent2025['delito'], mostFrequent2025['total']), unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        color_class = "green" if not np.isnan(change25_vs_24partial) and change25_vs_24partial < 0 else "red"
        change_text = f"{abs(change25_vs_24partial):.1f}%" if not np.isnan(change25_vs_24partial) else "N/A"
        st.markdown("""
        <div class="metric-card">
            <span class="icon">↔️</span>
            <h4 class="title">Variación % (2025 vs Mismo Periodo 2024)</h4>
            <p class="value {}">{}</p>
        </div>
        """.format(color_class, change_text), unsafe_allow_html=True)
    
    with col6:
        color_class = "green" if not np.isnan(change24_vs_23) and change24_vs_23 < 0 else "red"
        change_text = f"{abs(change24_vs_23):.1f}%" if not np.isnan(change24_vs_23) else "N/A"
        st.markdown("""
        <div class="metric-card">
            <span class="icon">⚡</span>
            <h4 class="title">Variación % Total (2024 vs 2023)</h4>
            <p class="value {}">{}</p>
        </div>
        """.format(color_class, change_text), unsafe_allow_html=True)
    
    with col7:
        st.markdown("""
        <div class="metric-card">
            <span class="icon">🔪</span>
            <h4 class="title">Robos con Violencia (Julio 2025)</h4>
            <p class="value">{:,}</p>
        </div>
        """.format(julioRobosViolencia), unsafe_allow_html=True)
    
    with col8:
        st.markdown("""
        <div class="metric-card">
            <span class="icon">💀</span>
            <h4 class="title">Homicidios y Femicidios (Semana 12 2025)</h4>
            <p class="value">{:,}</p>
        </div>
        """.format(semana12Homicidios), unsafe_allow_html=True)

# Función para renderizar gráfico anual
def render_annual_chart(selected_crime):
    if selected_crime == "Todos los Delitos":
        data2023 = annual_df["Frecuencia 2023"].sum()
        data2024 = annual_df["Frecuencia 2024"].sum()
        data2025 = annual_df["Frecuencia 2025 (a la fecha)"].sum()
    else:
        crime_data = annual_df[annual_df["Delito"] == selected_crime].iloc[0]
        data2023 = crime_data["Frecuencia 2023"]
        data2024 = crime_data["Frecuencia 2024"]
        data2025 = crime_data["Frecuencia 2025 (a la fecha)"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Frecuencia 2023',
        x=['2023'],
        y=[data2023],
        marker_color='rgba(76, 81, 191, 0.7)'
    ))
    
    fig.add_trace(go.Bar(
        name='Frecuencia 2024',
        x=['2024'],
        y=[data2024],
        marker_color='rgba(237, 137, 45, 0.7)'
    ))
    
    fig.add_trace(go.Bar(
        name='Frecuencia 2025 (a la fecha)',
        x=['2025 (a la fecha)'],
        y=[data2025],
        marker_color='rgba(56, 178, 172, 0.7)'
    ))
    
    fig.update_layout(
        title=f"Frecuencia Anual de {'Todos los Delitos' if selected_crime == 'All' else selected_crime}",
        xaxis_title="Año",
        yaxis_title="Frecuencia de Casos",
        barmode='group',
        height=400
    )
    
    return fig

# Función para renderizar gráfico mensual
def render_monthly_chart(selected_crime):
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    if selected_crime == "Todos los Delitos":
        data2024 = monthly_df[monthly_df["Año"] == 2024][months].sum().values
        data2025 = monthly_df[monthly_df["Año"] == 2025][months].sum().values
    else:
        data2024 = monthly_df[(monthly_df["Año"] == 2024) & (monthly_df["Delito"] == selected_crime)][months].values[0]
        data2025 = monthly_df[(monthly_df["Año"] == 2025) & (monthly_df["Delito"] == selected_crime)][months].values[0]
    
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
        line=dict(color='#4c51bf', width=2),
        marker=dict(size=6)
    ))
    
    # Datos de 2025 (reales y proyectados)
    # Parte real (línea sólida)
    fig.add_trace(go.Scatter(
        x=months[:currentMonthIndex+1],
        y=data2025[:currentMonthIndex+1],
        mode='lines+markers',
        name=f'Frecuencia 2025 (Datos reales)',
        line=dict(color='#ed8936', width=2),
        marker=dict(size=6),
        showlegend=False
    ))
    
    # Parte proyectada (línea discontinua)
    fig.add_trace(go.Scatter(
        x=months[currentMonthIndex:],
        y=projection2025[currentMonthIndex:],
        mode='lines+markers',
        name=f'Frecuencia 2025 (Proyección)',
        line=dict(color='#ed8936', width=2, dash='dash'),
        marker=dict(size=6, symbol='square'),
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Frecuencia Mensual de {'Todos los Delitos' if selected_crime == 'All' else selected_crime} (2024 vs. 2025 Proyectado)",
        xaxis_title="Mes",
        yaxis_title="Frecuencia de Casos",
        height=400,
        hovermode='x unified'
    )
    
    return fig

# Función para renderizar gráfico semanal
def render_weekly_chart(selected_crime):
    weeks = [f"Semana {str(i).zfill(2)}" for i in range(1, 13)]
    
    if selected_crime == "Todos los Delitos":
        data2024 = weekly_df[weekly_df["Año"] == 2024][weeks].sum().values
        data2025 = weekly_df[weekly_df["Año"] == 2025][weeks].sum().values
    else:
        data2024 = weekly_df[(weekly_df["Año"] == 2024) & (weekly_df["Delito"] == selected_crime)][weeks].values[0]
        data2025 = weekly_df[(weekly_df["Año"] == 2025) & (weekly_df["Delito"] == selected_crime)][weeks].values[0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=data2024,
        mode='lines+markers',
        name=f'Frecuencia Semanal 2024 ({selected_crime if selected_crime != "All" else "Total"})',
        line=dict(color='#38b2ac', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=data2025,
        mode='lines+markers',
        name=f'Frecuencia Semanal 2025 (a la fecha) ({selected_crime if selected_crime != "All" else "Total"})',
        line=dict(color='#6b46c1', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=f"Frecuencia Semanal de {'Todos los Delitos' if selected_crime == 'All' else selected_crime} (2024 vs. 2025)",
        xaxis_title="Semana",
        yaxis_title="Frecuencia de Casos",
        height=400,
        hovermode='x unified'
    )
    
    return fig

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f0f4f8;
        color: #2d3748;
    }
    .hero-header {
        background: linear-gradient(135deg, #4c51bf 0%, #6b46c1 100%);
        color: #ffffff;
        padding: 40px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .hero-header p {
        font-size: 1.25rem;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .hero-header .source-info {
        font-size: 0.875rem;
        opacity: 0.7;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 120px;
    }
    .metric-card .icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }
    .metric-card .title {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2c5282;
        line-height: 1.2;
    }
    .metric-card .value.green {
        color: #2f855a;
    }
    .metric-card .value.red {
        color: #e53e3e;
    }
    .analysis-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 20px;
    }
    .general-analysis {
        background-color: #f7fafc;
        border-left: 4px solid #718096;
        color: #2d3748;
        padding: 16px;
        border-radius: 0.375rem;
    }
    .dynamic-analysis {
        background-color: #ebf8ff;
        border-left: 4px solid #3182ce;
        color: #2c5282;
        padding: 16px;
        border-radius: 0.375rem;
        white-space: pre-wrap;
    }
    .explanation-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 20px;
    }
    .key-info {
        background-color: #ebf8ff;
        border-left: 4px solid #3182ce;
        color: #2c5282;
        padding: 16px;
        border-radius: 0.375rem;
        margin-top: 16px;
    }
    .footer {
        text-align: center;
        color: #718096;
        font-size: 0.875rem;
        margin-top: 40px;
    }
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 600;
        background-color: #e2e8f0;
        color: #4a5568;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #4c51bf;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("""
<div class="hero-header">
    <h1><span class="text-yellow-300">📈</span> Panorama Delictual en Copiapó</h1>
    <p class="text-xl">Análisis interactivo de frecuencias de delitos por temporalidad.</p>
    <p class="source-info mt-4">Datos extraídos de la Plataforma de Información Ley STOP de Carabineros de Chile, sistematizados por el Instituto Libertad.</p>
</div>
""", unsafe_allow_html=True)

# Análisis general
st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
st.subheader("Visión General de la Situación Delictual Anual en Copiapó (2023-2025)")
st.markdown('<div class="general-analysis">' + generate_general_analysis() + '</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Selector de temporalidad
tab1, tab2, tab3 = st.tabs(["Anual", "Mensual", "Semanal"])

# Contenido de la pestaña Anual
with tab1:
    selected_crime_annual = st.selectbox(
        "Seleccionar Delito:",
        ["All"] + crime_types,
        key="annual_crime_select"
    )
    
    fig_annual = render_annual_chart(selected_crime_annual)
    st.plotly_chart(fig_annual, use_container_width=True)
    
    # Análisis dinámico
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Tendencias Específicas")
    analysis_text = generate_analysis_text("Annual", selected_crime_annual)
    st.markdown(f'<div class="dynamic-analysis">{analysis_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Contenido de la pestaña Mensual
with tab2:
    selected_crime_monthly = st.selectbox(
        "Seleccionar Delito:",
        ["All"] + crime_types,
        key="monthly_crime_select"
    )
    
    fig_monthly = render_monthly_chart(selected_crime_monthly)
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Análisis dinámico
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Tendencias Específicas")
    analysis_text = generate_analysis_text("Monthly", selected_crime_monthly)
    st.markdown(f'<div class="dynamic-analysis">{analysis_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Contenido de la pestaña Semanal
with tab3:
    selected_crime_weekly = st.selectbox(
        "Seleccionar Delito:",
        ["All"] + crime_types,
        key="weekly_crime_select"
    )
    
    fig_weekly = render_weekly_chart(selected_crime_weekly)
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Análisis dinámico
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Tendencias Específicas")
    analysis_text = generate_analysis_text("Weekly", selected_crime_weekly)
    st.markdown(f'<div class="dynamic-analysis">{analysis_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Sección de métricas clave
st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
st.subheader("Métricas Clave de Delincuencia")
display_key_metrics()
st.markdown('</div>', unsafe_allow_html=True)

# Sección de explicaciones
st.markdown('<div class="explanation-card">', unsafe_allow_html=True)
st.subheader("¿Qué son estos gráficos?")
st.markdown("""
<p>Los gráficos muestran la <strong>frecuencia de ocurrencia</strong> de diferentes tipos de delitos en la Comuna de Copiapó. Esto nos ayuda a identificar patrones y cambios a lo largo del tiempo.</p>
<ul>
    <li><strong>Gráfico Anual:</strong> Compara la cantidad de casos en los años 2023, 2024 y lo que va de 2025.</li>
    <li><strong>Gráfico Mensual y Semanal:</strong> Muestran el número de casos por mes/semana, permitiendo una <strong>comparación directa entre 2024 y 2025</strong>. En la vista mensual, los valores futuros de 2025 son proyecciones.</li>
</ul>
""")

st.subheader("¿Cómo interpretar las tendencias?")
st.markdown("""
<p>Un <strong>aumento</strong> en la frecuencia puede indicar un incremento real del delito, una mejora en los reportes, o una mayor actividad policial en ciertas áreas. Una <strong>disminución</strong> puede sugerir lo contrario.</p>
<p>Es crucial considerar el <strong>contexto</strong>: cambios en las leyes, operaciones policiales específicas, factores socioeconómicos, o incluso eventos estacionales pueden influir en estas cifras.</p>
""")

st.markdown("""
<div class="key-info">
    <p><strong>💡 Dato Clave:</strong></p>
    <p>Las cifras reales de 2025 están disponibles hasta julio para la vista mensual y las últimas 12 semanas para la semanal. Los valores posteriores a julio en el gráfico mensual de 2025 son <strong>proyecciones</strong> basadas en el promedio de los meses ya reportados de 2025, y se visualizan con una **línea segmentada**.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Pie de página
st.markdown("""
<div class="footer">
    <p>&copy; 2025 Instituto Libertad. Datos proporcionados por Carabineros de Chile (Plataforma Ley STOP).</p>
</div>
""", unsafe_allow_html=True)


# =========================
# FILTRO GLOBAL DE DELITO
# =========================
with st.sidebar:
    st.header("🔍 Filtros")
    selected_crime = st.selectbox("Selecciona un delito", ["Todos los Delitos"] + list(crime_types))
    # Guardamos el valor en session_state para que esté disponible en todas las páginas
    st.session_state["selected_crime"] = selected_crime

st.title("📊 Análisis de Delincuencia en Copiapó")
st.markdown("""
Bienvenido al dashboard de análisis delictual en **Copiapó**.  

En el menú lateral puedes navegar a:
- 📌 Análisis General  
- 📅 Análisis Anual  
- 📆 Análisis Mensual  
- 📈 Análisis Semanal
""")
