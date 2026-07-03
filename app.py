import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página y Estilo "Dashboard Oscuro Premium"
st.set_page_config(page_title="Rutina Premium", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Fondo oscuro grafito y textos limpios */
    .stApp { 
        background-color: #0B0F19; 
        color: #F8FAFC; 
    }
    
    /* Títulos principales */
    h1, h2, h3, h4 { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }
    
    /* --- FULMINAR LA LÍNEA ROJA DE LAS PESTAÑAS --- */
    /* Eliminamos la línea roja inferior por defecto de Streamlit */
    .stTabs [data-baseweb="tab-highlight-bar"] {
        background-color: transparent !important;
        display: none !important;
    }
    /* Quitamos el borde inferior de la lista de pestañas */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: none !important;
        gap: 10px;
    }
    
    /* Estilo de los botones/pestañas superiores */
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B !important;
        color: #94A3B8 !important;
        border: 1px solid #334155 !important;
        border-radius: 20px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
    }
    /* Botón/Pestaña seleccionada (Verde Pastel suave sin línea roja abajo) */
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #A7F3D0 !important;
        border: 2px solid #A7F3D0 !important;
    }
    
    /* Tarjetas de ejercicios internas */
    .stExpander { 
        background-color: #1E293B !important; 
        border: 1px solid #334155 !important; 
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }
    
    /* Dashboard: Contenedores para la visión general */
    .dashboard-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }
    
    /* Ajustes para los textos generales */
    .stMarkdown p, .stExpander label {
        color: #E2E8F0 !important;
    }
    
    /* Números de las métricas (Verde Pastel Suave) */
    [data-testid="stMetricValue"] {
        color: #A7F3D0 !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
    }
    
    /* Recuadro del Foco Técnico */
    .stAlert {
        background-color: #0F172A !important;
        border: 1px solid #A7F3D0 !important;
        color: #E2E8F0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ Mi Panel de Entrenamiento")
st.write("---")

# 2. Cargar datos del Excel
def cargar_datos():
    return pd.read_excel("rutina.xlsx")

try:
    df = cargar_datos()
    df_limpio = df.replace({np.nan: ""})

    # Obtener la lista limpia de bloques
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    # --- PESTAÑAS (Limpias, sin emoticonos raros) ---
    lista_pestanas = ["Visión General"] + [str(bloque) for bloque in bloques_totales]
    pestanas_interactivas = st.tabs(lista_pestanas)

    # -------------------------------------------------------------
    # PESTAÑA 1: VISIÓN GENERAL (ESTILO DASHBOARD)
    # -------------------------------------------------------------
    with pestanas_interactivas[0]:
        st.write("")
        st.write("### 📊 Dashboard de la Sesión")
        
        # Fila de kpis principales arriba
        total_ejercicios = len(df_limpio[df_limpio["Ejercicio"] != ""])
        
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric(label="⏱️ Bloques Totales", value=str(len(bloques_totales)))
        with kpi2:
            st.metric(label="💪 Ejercicios Hoy", value=str(total_ejercicios))
            
        st.write("")
        
        # Listado estilo tarjetas de Dashboard
        for bloque in bloques_totales:
            df_b = df_limpio[df_limpio["Bloque"] == bloque]
            ejercicios_del_bloque = df_b["Ejercicio"].tolist()
            
            # Tarjeta HTML limpia para cada bloque
            ejercicios_html = "".join([f"<li style='margin-bottom:4px;'>🔹 {ej}</li>" for ej in ejercicios_del_bloque])
            
            st.markdown(f"""
            <div class="dashboard-card">
                <h4 style="margin: 0 0 8px 0; color: #A7F3D0 !important;">📍 {bloque}</h4>
                <p style="margin: 0 0 10px 0; font-size: 0.9rem; color: #94A3B8;">Contiene {len(ejercicios_del_bloque)} ejercicios prescritos</p>
                <ul style="margin: 0; padding-left: 20px; list-style-type: none; color: #E2E8F0;">
                    {ejercicios_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # RESTO DE PESTAÑAS: UNA PARA CADA BLOQUE
    # -------------------------------------------------------------
    for idx, bloque in enumerate(bloques_totales, start=1):
        with pestanas_interactivas[idx]:
            st.write("")
            st.write(f"### {bloque}")
            
            df_bloque = df_limpio[df_limpio["Bloque"] == bloque]
            
            for index, fila_limpia in df_bloque.iterrows():
                carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
                titulo_tarjeta = f"🎯 {fila_limpia['Ejercicio']} ({carga})"
                
                with st.expander(titulo_tarjeta):
                    # Fila de métricas rápidas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="🔢 Series", value=str(fila_limpia['Series']))
                    with col2:
                        st.metric(label="🔁 Reps", value=str(fila_limpia['Reps']))
                    with col3:
                        descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                        st.metric(label="⏱️ Descanso", value=str(descanso))
                    
                    st.write("---")
                    
                    # Textos descriptivos
                    if fila_limpia['Objetivo']:
                        st.markdown(f"**🎯 Objetivo:** {fila_limpia['Objetivo']}")
                    if fila_limpia['Justificación']:
                        st.markdown(f"**💡 Justificación:** {fila_limpia['Justificación']}")
                    if fila_limpia['Ejecución']:
                        st.markdown(f"**🛠️ Ejecución:** {fila_limpia['Ejecución']}")
                    
                    # Foco técnico
                    foco = fila_limpia.get('Foco Técnico', fila_limpia.get('Foco_Técnico', ''))
                    if foco:
                        st.info(f"👁️ **Foco Técnico:** {foco}")

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")
