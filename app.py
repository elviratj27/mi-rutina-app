import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de la página y Estilo "Modo Oscuro Grafito / Premium"
st.set_page_config(page_title="Rutina Deportiva", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Fondo negro grafito profundo, muy elegante */
    .stApp { 
        background-color: #0B0F19; 
        color: #F8FAFC; 
    }
    
    /* Títulos principales en blanco puro y brillante */
    h1, h2, h3 { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }
    
    /* El texto del selector de bloques */
    .stSelectbox label { 
        color: #94A3B8 !important; 
        font-weight: 600;
    }
    
    /* Tarjetas de ejercicios: Gris satinado que contrasta con el fondo negro */
    .stExpander { 
        background-color: #1E293B !important; 
        border: 1px solid #334155 !important; 
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Forzar que los textos dentro de las tarjetas sean gris claro/blanco */
    .stMarkdown p, .stExpander label {
        color: #E2E8F0 !important;
    }
    
    /* Números de las métricas (Series, Reps) en un color blanco destacado */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* Las etiquetas de las métricas en gris suave */
    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
    }
    
    /* El recuadro del Foco Técnico adaptado al modo oscuro */
    .stAlert {
        background-color: #0F172A !important;
        border: 1px solid #38BDF8 !important;
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

    # 3. Selector de Bloque
    bloques_disponibles = df["Bloque"].dropna().unique()
    bloque_seleccionado = st.selectbox("Selecciona el Bloque de hoy:", bloques_disponibles)

    # Filtrar los ejercicios del bloque activo
    df_filtrado = df[df["Bloque"] == bloque_seleccionado]

    st.write(f"## {bloque_seleccionado}")

    # 4. Lista de Ejercicios en Tarjetas
    for index, fila in df_filtrado.iterrows():
        
        # Cambiamos los NaN por texto vacío "" de forma automática
        fila_limpia = fila.replace({np.nan: ""})
        
        # Si la carga está vacía, ponemos "Peso corporal"
        carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
        titulo_tarjeta = f"👟 {fila_limpia['Ejercicio']} ({carga})"
        
        with st.expander(titulo_tarjeta):
            # Fila de datos numéricos rápidos (Series, Reps, Descanso)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="🔢 Series", value=str(fila_limpia['Series']))
            with col2:
                # Si está vacío en Excel, saldrá completamente despejado en lugar de NaN
                st.metric(label="🔁 Reps", value=str(fila_limpia['Reps']))
            with col3:
                descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                st.metric(label="⏱️ Descanso", value=str(descanso))
            
            st.write("---")
            
            # Bloque teórico explicativo (solo se muestra si tiene texto en el Excel)
            if fila_limpia['Objetivo']:
                st.markdown(f"**🎯 Objetivo:** {fila_limpia['Objetivo']}")
            if fila_limpia['Justificación']:
                st.markdown(f"**💡 Justificación:** {fila_limpia['Justificación']}")
            if fila_limpia['Ejecución']:
                st.markdown(f"**🛠️ Ejecución:** {fila_limpia['Ejecución']}")
            
            # Foco técnico interactivo y seguro
            foco = fila_limpia.get('Foco Técnico', fila_limpia.get('Foco_Técnico', ''))
            if foco:
                st.info(f"👁️ **Foco Técnico:** {foco}")

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")