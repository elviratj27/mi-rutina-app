import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración y Estilo "Modo Oscuro & Verde Pastel Premium"
st.set_page_config(page_title="Rutina Premium", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Fondo oscuro grafito y textos limpios */
    .stApp { 
        background-color: #0B0F19; 
        color: #F8FAFC; 
    }
    
    /* ELIMINAR LA LÍNEA ROJA DE CARGA (Running indicator) */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    div[role="progressbar"] {
        display: none !important;
    }
    .stProgress > div > div {
        background-color: transparent !important;
    }
    
    /* Títulos en blanco brillante */
    h1, h2, h3, h4 { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }
    
    /* Personalización de las PESTAÑAS (Tabs) superiores */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B !important;
        color: #94A3B8 !important;
        border: 1px solid #334155 !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
    }
    /* Pestaña activa: Texto verde pastel y borde verde suave */
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #A7F3D0 !important;
        border: 2px solid #86EFAC !important;
    }
    
    /* Tarjetas de ejercicios internas */
    .stExpander { 
        background-color: #1E293B !important; 
        border: 1px solid #334155 !important; 
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }
    
    /* Textos dentro de las tarjetas */
    .stMarkdown p, .stExpander label {
        color: #E2E8F0 !important;
    }
    
    /* Números de las métricas en color VERDE PASTEL destacado */
    [data-testid="stMetricValue"] {
        color: #A7F3D0 !important;
        font-weight: 700 !important;
    }
    
    /* Etiquetas de las métricas en gris suave */
    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
    }
    
    /* Recuadro del Foco Técnico con un toque verde pastel sutil */
    .stAlert {
        background-color: #0F172A !important;
        border: 1px solid #86EFAC !important;
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
    # Limpiamos los NaN de todo el DataFrame desde el inicio
    df_limpio = df.replace({np.nan: ""})

    # Obtener todos los bloques únicos ordenados
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    # --- CREACIÓN DE LAS PESTAÑAS PRINCIPALES ---
    # La primera pestaña es la Visión General de toda la rutina, las siguientes son los bloques
    lista_pestanas = ["📊 Visión General"] + [f"🧱 {bloque}" for bloque in bloques_totales]
    pestanas_interactivas = st.tabs(lista_pestanas)

    # -------------------------------------------------------------
    # PESTAÑA 1: VISIÓN GENERAL (De toda la rutina completa)
    # -------------------------------------------------------------
    with pestanas_interactivas[0]:
        st.write("")
        st.markdown("""
        <div style="background-color: #1E293B; border-left: 4px solid #86EFAC; padding: 15px; border-radius: 8px;">
            <h4 style="margin: 0 0 5px 0; color: #FFFFFF;">📋 Estructura Completa de la Rutina</h4>
            <p style="margin: 0; color: #94A3B8;">A continuación tienes un resumen de todos los bloques que componen tu entrenamiento de hoy. Usa las pestañas de arriba para ver el desglose paso a paso de cada bloque.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        # Mostramos el resumen de cada bloque
        for bloque in bloques_totales:
            ejercicios_del_bloque = df_limpio[df_limpio["Bloque"] == bloque]["Ejercicio"].tolist()
            
            with st.container():
                st.markdown(f"### 🧱 {bloque}")
                texto_ejercicios = " • ".join([f"**{ej}**" for ej in ejercicios_del_bloque])
                st.markdown(texto_ejercicios)
                st.write("---")

    # -------------------------------------------------------------
    # RESTO DE PESTAÑAS: UNA PARA CADA BLOQUE INDIVIDUAL
    # -------------------------------------------------------------
    for idx, bloque in enumerate(bloques_totales, start=1):
        with pestanas_interactivas[idx]:
            st.write("")
            st.write(f"### Ejercicios del {bloque}")
            
            # Filtramos el Excel solo por el bloque de esta pestaña
            df_bloque = df_limpio[df_limpio["Bloque"] == bloque]
            
            # Mostramos los ejercicios de este bloque en formato acordeón
            for index, fila_limpia in df_bloque.iterrows():
                carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
                titulo_tarjeta = f"👟 {fila_limpia['Ejercicio']} ({carga})"
                
                with st.expander(titulo_tarjeta):
                    # Fila de datos numéricos (Series, Reps, Descanso)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="🔢 Series", value=str(fila_limpia['Series']))
                    with col2:
                        st.metric(label="🔁 Reps", value=str(fila_limpia['Reps']))
                    with col3:
                        descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                        st.metric(label="⏱️ Descanso", value=str(descanso))
                    
                    st.write("---")
                    
                    # Detalles teóricos
                    if fila_limpia['Objetivo']:
                        st.markdown(f"**🎯 Objetivo:** {fila_limpia['Objetivo']}")
                    if fila_limpia['Justificación']:
                        st.markdown(f"**💡 Justificación:** {fila_limpia['Justificación']}")
                    if fila_limpia['Ejecución']:
                        st.markdown(f"**🛠️ Ejecución:** {fila_limpia['Ejecución']}")
                    
                    # Foco técnico interactivo con recuadro verde pastel
                    foco = fila_limpia.get('Foco Técnico', fila_limpia.get('Foco_Técnico', ''))
                    if foco:
                        st.info(f"👁️ **Foco Técnico:** {foco}")

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")
