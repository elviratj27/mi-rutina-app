import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página con nombre limpio en el navegador
st.set_page_config(page_title="Rutina de Entrenamiento", page_icon="💪", layout="centered")

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
    
    /* --- ESTILO PARA EL MENÚ LATERAL (SIDEBAR) ESTILO ZARA --- */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important; /* Un gris satinado elegante */
        border-right: 1px solid #334155 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #A7F3D0 !important; /* Título del menú en verde pastel */
    }
    /* Estilo para los botones de opción de radio en el menú */
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #E2E8F0 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 5px 0;
    }
    
    /* Tarjetas del Dashboard de la página principal */
    .dashboard-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* Tarjetas expandibles de ejercicios */
    .stExpander { 
        background-color: #1E293B !important; 
        border: 1px solid #334155 !important; 
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }
    
    /* Ajustes de color para textos y marcas */
    .stMarkdown p, .stExpander label {
        color: #E2E8F0 !important;
    }
    
    /* Métricas numéricas (Verde Pastel Suave) */
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

    # Obtener los bloques únicos
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    # --- MENÚ DESPLEGABLE SUPERIOR IZQUIERDO (SIDEBAR ESTILO ZARA) ---
    # Creamos las opciones del menú. La primera siempre regresa al Dashboard global.
    opciones_menu = ["📊 Ver Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 📂 Categorías / Bloques")
        st.write("---")
        # El selector visual tipo lista interactiva
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: SI EL USUARIO SELECCIONA EL RESUMEN GENERAL
    # -------------------------------------------------------------
    if seleccion == "📊 Ver Resumen General":
        st.write("### 📊 Resumen del Entrenamiento")
        
        total_ejercicios = len(df_limpio[df_limpio["Ejercicio"] != ""])
        
        # KPIs Principales con el texto corregido a "Número de Bloques"
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric(label="⏱️ Número de Bloques", value=str(len(bloques_totales)))
        with kpi2:
            st.metric(label="💪 Ejercicios Hoy", value=str(total_ejercicios))
            
        st.write("")
        
        # Renderizado de las tarjetas del Dashboard
        for bloque in bloques_totales:
            df_b = df_limpio[df_limpio["Bloque"] == bloque]
            ejercicios_del_bloque = df_b["Ejercicio"].tolist()
            
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
    # VISTA B: SI EL USUARIO SELECCIONA UN BLOQUE ESPECÍFICO
    # -------------------------------------------------------------
    else:
        # Aquí entra cuando pinchas un bloque del menú desplegable
        bloque_actual = seleccion
        st.write(f"### {bloque_actual}")
        
        df_bloque = df_limpio[df_limpio["Bloque"] == bloque_actual]
        
        for index, fila_limpia in df_bloque.iterrows():
            carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
            titulo_tarjeta = f"🎯 {fila_limpia['Ejercicio']} ({carga})"
            
            with st.expander(titulo_tarjeta):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="🔢 Series", value=str(fila_limpia['Series']))
                with col2:
                    st.metric(label="🔁 Reps", value=str(fila_limpia['Reps']))
                with col3:
                    descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                    st.metric(label="⏱️ Descanso", value=str(descanso))
                
                st.write("---")
                
                if fila_limpia['Objetivo']:
                    st.markdown(f"**🎯 Objetivo:** {fila_limpia['Objetivo']}")
                if fila_limpia['Justificación']:
                    st.markdown(f"**💡 Justificación:** {fila_limpia['Justificación']}")
                if fila_limpia['Ejecución']:
                    st.markdown(f"**🛠️ Ejecución:** {fila_limpia['Ejecución']}")
                
                foco = fila_limpia.get('Foco Técnico', fila_limpia.get('Foco_Técnico', ''))
                if foco:
                    st.info(f"👁️ **Foco Técnico:** {foco}")

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")
