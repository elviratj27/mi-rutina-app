import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración y Estilo "Modo Oscuro Cyber-Verde Premium"
st.set_page_config(page_title="Rutina Premium", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Fondo negro grafito profundo */
    .stApp { 
        background-color: #0B0F19; 
        color: #F8FAFC; 
    }
    
    /* Títulos en blanco brillante */
    h1, h2, h3 { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }
    
    /* Selector de bloques */
    .stSelectbox label { 
        color: #94A3B8 !important; 
        font-weight: 600;
    }
    
    /* Personalización de las PESTAÑAS (Tabs) superiores */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B !important;
        color: #94A3B8 !important;
        border: 1px solid #334155 !important;
        border-radius: 20px !important; /* Estilo botón flotante redondeado */
        padding: 6px 16px !important;
        font-weight: 600 !important;
    }
    /* Pestaña activa (seleccionada): Texto blanco y borde Verde Deportivo */
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #22C55E !important;
        border: 2px solid #22C55E !important;
    }
    
    /* Tarjetas de información interna */
    .stMarkdown p {
        color: #E2E8F0 !important;
    }
    
    /* Números de las métricas en color VERDE destacado */
    [data-testid="stMetricValue"] {
        color: #22C55E !important;
        font-weight: 700 !important;
    }
    
    /* Etiquetas de las métricas (Series, Reps) en gris suave */
    [data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
    }
    
    /* Recuadro del Foco Técnico con un toque verde sutil */
    .stAlert {
        background-color: #0F172A !important;
        border: 1px solid #22C55E !important;
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

    # --- AQUÍ ESTÁ LA MAGIA DE LAS PESTAÑAS ---
    # Creamos la lista de nombres para las pestañas superiores
    nombres_ejercicios = df_filtrado["Ejercicio"].dropna().tolist()
    
    # La primera pestaña es la Visión General, y luego añadimos una pestaña por ejercicio
    lista_pestanas = ["📊 Visión General"] + [f"👟 {ej}" for ej in nombres_ejercicios]
    pestanas_interactivas = st.tabs(lista_pestanas)

    # PESTAÑA 1: VISIÓN GENERAL
    with pestanas_interactivas[0]:
        st.write("")
        st.markdown(f"""
        <div style="background-color: #1E293B; border-left: 4px solid #22C55E; padding: 15px; border-radius: 8px;">
            <h4 style="margin: 0 0 10px 0; color: #FFFFFF;">📋 Resumen de la sesión</h4>
            <p style="margin: 0; color: #94A3B8;">Este bloque consta de <b>{len(nombres_ejercicios)} ejercicios</b> ordenados. Toca las pestañas de arriba para ver la ejecución y series de cada uno.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("**Lista de ejercicios de hoy:**")
        for i, ej in enumerate(nombres_ejercicios, 1):
            st.markdown(f"{i}. **{ej}**")

    # RESTO DE PESTAÑAS: UNA PARA CADA EJERCICIO
    for idx, (index, fila) in enumerate(df_filtrado.iterrows(), start=1):
        with pestanas_interactivas[idx]:
            # Limpiamos los NaN automáticamente
            fila_limpia = fila.replace({np.nan: ""})
            
            carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
            st.write("")
            st.subheader(f"{fila_limpia['Ejercicio']}")
            st.caption(f"🏋️‍♂️ Carga recomendada: {carga}")
            st.write("---")
            
            # Fila de datos numéricos rápidos (Series, Reps, Descanso)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="🔢 Series", value=str(fila_limpia['Series']))
            with col2:
                st.metric(label="🔁 Reps", value=str(fila_limrera_val := fila_limpia['Reps']))
            with col3:
                descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                st.metric(label="⏱️ Descanso", value=str(descanso))
            
            st.write("---")
            
            # Bloque teórico explicativo
            if fila_limpia['Objetivo']:
                st.markdown(f"**🎯 Objetivo:** {fila_limpia['Objetivo']}")
            if fila_limpia['Justificación']:
                st.markdown(f"**💡 Justificación:** {fila_limpia['Justificación']}")
            if fila_limpia['Ejecución']:
                st.markdown(f"**🛠️ Ejecución:** {fila_limpia['Ejecución']}")
            
            # Foco técnico interactivo con recuadro verde
            foco = fila_limpia.get('Foco Técnico', fila_limpia.get('Foco_Técnico', ''))
            if foco:
                st.info(f"👁️ **Foco Técnico:** {foco}")

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")
