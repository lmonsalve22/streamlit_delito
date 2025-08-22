import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data import get_data

# Función auxiliar para extraer datos semanales por año
def get_weekly_data(weekly_df, year, crime="All"):
    # Filtrar por año y delito
    if crime == "All":
        df_year = weekly_df[weekly_df['año'] == year].copy()
        if df_year.empty:
            return {}
        # Sumar todas las filas (de todos los delitos) para este año
        df_year = df_year.drop(columns=['delito', 'año']).sum().to_frame().T
    else:
        df_year = weekly_df[(weekly_df['año'] == year) & (weekly_df['delito'] == crime)]
        if df_year.empty:
            return {}
        # Tomar la primera fila (debería haber solo una)
        df_year = df_year.drop(columns=['delito', 'año'])
    
    # Obtener las columnas que corresponden a semanas de este año
    weeks_cols = [col for col in df_year.columns if str(year) in col and 'SEMANA' in col]
    data = {}
    for col in weeks_cols:
        # Extraer número de semana: está al final, después de "SEMANA "
        parts = col.split()
        week_num_str = parts[-1]
        try:
            week_num = int(week_num_str)
        except:
            continue
        value = df_year[col].values[0]
        data[week_num] = value
    
    return data

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Delincuencia en Copiapó",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

CODCOM = 1101
df = get_data()
df_codcom = df[df["codcom"] == CODCOM]
df_codcom["año"] = df_codcom["fecha"].dt.year.astype(int)

pivot = df_codcom[["delito","frecuencia",'codcom','año']].pivot_table(
    index=["delito", "codcom"],   # lo que se mantiene como índice
    columns="año",                # lo que pasa a ser columnas
    values="frecuencia",          # los valores que llenan la tabla
    aggfunc="sum",                # cómo se agregan si hay duplicados
    fill_value=0                  # rellena NaN con 0
).reset_index()

pivot.columns = ["Delito","codcom", "Frecuencia 2023", "Frecuencia 2024", "Frecuencia 2025 (a la fecha)"]

meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

df_codcom["meses"] = df_codcom["fecha"].dt.month
df_codcom["meses_str"] =  df_codcom["meses"].map(meses)

pivot2 = df_codcom[df_codcom["año"] > 2023][['delito', 'frecuencia', 'año', 'meses_str']].pivot_table(
    index=["delito", "año"],   # lo que se mantiene como índice
    columns="meses_str",                # lo que pasa a ser columnas
    values="frecuencia",          # los valores que llenan la tabla
    aggfunc="sum",                # cómo se agregan si hay duplicados
    fill_value=0                  # rellena NaN con 0
).reset_index()

pivot2 = pivot2[['delito', 'año', "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]]
pivot2.columns = ["Delito", "Año", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

def get_semana(fila):
    semana_detalle = fila["semana_detalle"][:9]
    anio = fila["año"]
    return f"{anio} - {semana_detalle}"

df_codcom["semana"] = df_codcom.apply(get_semana, axis=1)

pivot3 = df_codcom[df_codcom["año"] > 2023][['delito', 'frecuencia', 'año', 'semana']].pivot_table(
    index=["delito", "año"],   # lo que se mantiene como índice
    columns="semana",                # lo que pasa a ser columnas
    values="frecuencia",          # los valores que llenan la tabla
    aggfunc="sum",                # cómo se agregan si hay duplicados
    fill_value=0                  # rellena NaN con 0
).reset_index()

pivot3 = pivot3[["delito","año"] + sorted(pivot3.columns[2:])]

# Datos hardcodeados (extraídos del HTML original)
# Convertir los datos a DataFrames
#annual_df = pd.DataFrame(annual_data_raw)
annual_df = pivot
monthly_df = pivot2# pd.DataFrame(monthly_data_raw)
weekly_df = pivot3

# Obtener lista de tipos de delitos
crime_types = sorted(annual_df['Delito'].unique())

# Función para generar el análisis general
def generate_general_analysis():
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
    
    # Homicidios y Femicidios (Semana 12 2025) - usando la función auxiliar
    data_homicidios_2025 = get_weekly_data(weekly_df, 2025, "HOMICIDIOS Y FEMICIDIOS")
    semana12Homicidios = data_homicidios_2025.get(12, 0)
    
    # Crear tarjetas en una estructura de 2 columnas
    cards_html = f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <span class="icon">📊</span>
            <h4 class="title">Cifras Anuales Totales</h4>
            <div class="value">
                <p><strong>2023:</strong> {total2023:,} casos</p>
                <p><strong>2024:</strong> {total2024:,} casos</p>
                <p><strong>2025 (a la fecha):</strong> {total2025Partial:,} casos</p>
            </div>
        </div>
        <div class="metric-card">
            <span class="icon">📈</span>
            <h4 class="title">Tendencia General Anual</h4>
            <div class="value">{trendText}</div>
        </div>
        <div class="metric-card">
            <span class="icon">🚨</span>
            <h4 class="title">Delitos Más y Menos Frecuentes (2024)</h4>
            <div class="value">
                <p><strong>Más frecuente:</strong> {mostFrequentCrime['delito']} ({mostFrequentCrime['total']:,} casos)</p>
                <p><strong>Menos frecuente:</strong> {leastFrequentCrime['delito']} ({leastFrequentCrime['total']:,} casos)</p>
            </div>
        </div>
        <div class="metric-card">
            <span class="icon">📅</span>
            <h4 class="title">Patrones Mensuales (Frecuencia Total)</h4>
            <div class="value">
                <p><strong>2024 - Mayor frecuencia:</strong> {months[maxMonth2024Index]} ({int(monthlyTotals2024[maxMonth2024Index]):,} casos)</p>
                <p><strong>2024 - Menor frecuencia:</strong> {months[minMonth2024Index]} ({int(monthlyTotals2024[minMonth2024Index]):,} casos)</p>
    """
    
    if monthlyTotals2025.sum() > 0:
        maxMonth2025Index = np.argmax(monthlyTotals2025)
        minMonth2025Index = np.argmin(monthlyTotals2025)
        cards_html += f"""
                <p><strong>2025 (hasta julio) - Mayor frecuencia:</strong> {months[maxMonth2025Index]} ({int(monthlyTotals2025[maxMonth2025Index]):,} casos)</p>
                <p><strong>2025 (hasta julio) - Menor frecuencia:</strong> {months[minMonth2025Index]} ({int(monthlyTotals2025[minMonth2025Index]):,} casos)</p>
        """
    
    cards_html += f"""
            </div>
        </div>
        <div class="metric-card">
            <span class="icon">💀</span>
            <h4 class="title">Datos Específicos de 2025</h4>
            <div class="value">
                <p><strong>Homicidios y Femicidios (Semana 12):</strong> {semana12Homicidios:,} casos</p>
            </div>
        </div>
    </div>
    """
    
    return cards_html

# Función para generar análisis dinámico
def generate_analysis_text(temporality, selected_crime):
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
        
        if selected_crime == "All":
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
        # Usar la función auxiliar para obtener datos semanales
        data2024 = get_weekly_data(weekly_df, 2024, selected_crime)
        data2025 = get_weekly_data(weekly_df, 2025, selected_crime)
        
        analysis_text = f"Análisis Semanal para <strong>{data_name}</strong>:\n\n"
        analysis_text += f"Análisis de las semanas disponibles en 2024 y 2025:\n"
        
        total2024 = sum(data2024.values())
        total2025 = sum(data2025.values())
        
        if total2024 > 0:
            changePartial = ((total2025 - total2024) / total2024 * 100)
            analysis_text += f"Se observa un {'incremento' if changePartial > 0 else 'decremento'} del <strong>{abs(changePartial):.1f}%</strong> en 2025 respecto al mismo período de 2024.\n"
        else:
            analysis_text += "Se ha registrado un aumento significativo en 2025 en comparación con el mismo período de 2024.\n"
        
        if data2024:
            max_week2024 = max(data2024, key=data2024.get)
            min_week2024 = min(data2024, key=data2024.get)
            analysis_text += f"En las semanas disponibles de 2024, el pico se alcanzó en la <strong>Semana {max_week2024}</strong> (<strong>{data2024[max_week2024]:,}</strong> casos) y el punto más bajo en la <strong>Semana {min_week2024}</strong> (<strong>{data2024[min_week2024]:,}</strong> casos).\n"
        else:
            analysis_text += "No hay datos disponibles para 2024.\n"
        
        if data2025:
            max_week2025 = max(data2025, key=data2025.get)
            min_week2025 = min(data2025, key=data2025.get)
            analysis_text += f"Para 2025, en las semanas con datos, la semana con más casos fue la <strong>Semana {max_week2025}</strong> (<strong>{data2025[max_week2025]:,}</strong> casos) y la de menor fue la <strong>Semana {min_week2025}</strong> (<strong>{data2025[min_week2025]:,}</strong> casos)."
        else:
            analysis_text += "No hay datos disponibles para 2025."
    
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
    
    # Homicidios y Femicidios (Semana 12 2025) - usando la función auxiliar
    data_homicidios_2025 = get_weekly_data(weekly_df, 2025, "HOMICIDIOS Y FEMICIDIOS")
    semana12Homicidios = data_homicidios_2025.get(12, 0)
    
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
    
    # Definir las categorías del eje X
    categories = ['2023', '2024', '2025 (a la fecha)']
    
    # Crear una sola barra con tres valores, uno para cada categoría
    fig.add_trace(go.Bar(
        name='Frecuencia',
        x=categories,
        y=[data2023, data2024, data2025],
        marker_color=['rgba(76, 81, 191, 0.7)', 'rgba(237, 137, 45, 0.7)', 'rgba(56, 178, 172, 0.7)'],
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Frecuencia Anual de {'Todos los Delitos' if selected_crime == 'All' else selected_crime}",
        xaxis_title="Año",
        yaxis_title="Frecuencia de Casos",
        height=400,
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=categories
        )
    )
    
    return fig

# Función para renderizar gráfico mensual
def render_monthly_chart(selected_crime):
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    if selected_crime == "All":
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
    # Usar la función auxiliar para obtener datos semanales
    data2024 = get_weekly_data(weekly_df, 2024, selected_crime)
    data2025 = get_weekly_data(weekly_df, 2025, selected_crime)
    
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
        line=dict(color='#38b2ac', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=weeks2025,
        y=values2025,
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
        margin-bottom: 16px;
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
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 20px;
    }
    .analysis-card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 20px;
    }
    .general-analysis {
        background-color: #ffffff;
        border-left: 4px solid #718096;
        color: #2d3748;
        padding: 16px;
        border-radius: 0.375rem;
    }
    .general-analysis ul {
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .general-analysis li {
        margin-bottom: 8px;
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
    .dataframe-container {
        margin-top: 20px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
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

#general_analysis_html = generate_general_analysis()
#st.markdown(general_analysis_html, unsafe_allow_html=True)
#st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Tabla de datos anuales
    st.subheader("Datos Anuales Detallados")
    if selected_crime_annual == "All":
        # Mostrar toda la tabla
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(annual_df.style.format({
            "Frecuencia 2023": "{:,}",
            "Frecuencia 2024": "{:,}",
            "Frecuencia 2025 (a la fecha)": "{:,}"
        }), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Mostrar solo la fila del delito seleccionado
        crime_data = annual_df[annual_df["Delito"] == selected_crime_annual]
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(crime_data.style.format({
            "Frecuencia 2023": "{:,}",
            "Frecuencia 2024": "{:,}",
            "Frecuencia 2025 (a la fecha)": "{:,}"
        }), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
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
#display_key_metrics()
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
    <p>Las cifras reales de 2025 están disponibles hasta julio para la vista mensual y las últimas semanas disponibles para la semanal. Los valores posteriores a julio en el gráfico mensual de 2025 son <strong>proyecciones</strong> basadas en el promedio de los meses ya reportados de 2025, y se visualizan con una **línea segmentada**.</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Pie de página
st.markdown("""
<div class="footer">
    <p>&copy; 2025 Instituto Libertad. Datos proporcionados por Carabineros de Chile (Plataforma Ley STOP).</p>
</div>
""", unsafe_allow_html=True)