import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página con nombre limpio en el navegador
st.set_page_config(page_title="Rutina de Entrenamiento", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Importamos una tipografía muy limpia, robusta y deportiva (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Fondo grafito oscuro texturizado, muy premium y masculino */
    .stApp { 
        background-color: #0E131F; 
        color: #E2E8F0; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Títulos principales con tipografía deportiva y de bloque pesado */
    h1, h2, h3 { 
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    
    /* Texto destacado con el verde de rendimiento deportivo */
    .sport-accent {
        color: #00F5A0; /* Verde menta/neón de alta competición, muy enérgico */
    }
    
    /* --- MENÚ LATERAL (SIDEBAR COLAPSABLE ESTILO ZARA) --- */
    [data-testid="stSidebar"] {
        background-color: #171E2E !important; /* Gris carbón integrado */
        border-right: 1px solid #242F41 !important;
    }
    [data-testid="stSidebar"] h3 {
        font-family: 'Inter', sans-serif !important;
        color: #00F5A0 !important;
        font-weight: 700 !important;
    }
    /* Estilo para los botones de opción en el menú */
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #94A3B8 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Tarjetas del Dashboard de la página principal (Gris oscuro con sutil borde verde al pasar el ratón) */
    .dashboard-card {
        background-color: #171E2E;
        border: 1px solid #242F41;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Tarjetas expandibles de ejercicios */
    .stExpander { 
        background-color: #171E2E !important; 
        border: 1px solid #242F41 !important; 
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Ajustes de color para textos generales */
    .stMarkdown p, .stExpander label {
        color: #94A3B8 !important;
    }
    
    /* Métricas numéricas destacados en Verde Menta Deportivo */
    [data-testid="stMetricValue"] {
        color: #00F5A0 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #64748B !important;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
    }
    
    /* Recuadro del Foco Técnico con fondo oscuro y borde verde */
    .stAlert {
        background-color: #0E131F !important;
        border: 1px solid #00F5A0 !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título con fuerza deportiva
st.markdown('<h1>CENTRO DE <span class="sport-accent">RENDIMIENTO</span></h1>', unsafe_allow_html=True)
st.write("---")

# 2. Cargar datos del Excel
def cargar_datos():
    return pd.read_excel("rutina.xlsx")

try:
    df = cargar_datos()
    df_limpio = df.replace({np.nan: ""})

    # Obtener los bloques únicos
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    # --- MENÚ DESPLEGABLE SIDEBAR ---
    opciones_menu = ["⚡ Ver Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 🧭 Bloques de Carga")
        st.write("---")
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: RESUMEN GENERAL (DASHBOARD ATLETAS)
    # -------------------------------------------------------------
    if seleccion == "⚡ Ver Resumen General":
        st.markdown('### 📊 <span class="sport-accent">Métricas</span> de la Sesión', unsafe_allow_html=True)
        
        total_ejercicios = len(df_limpio[df_limpio["Ejercicio"] != ""])
        
        # KPIs Principales
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric(label="Número de Bloques", value=str(len(bloques_totales)))
        with kpi2:
            st.metric(label="Ejercicios Programados", value=str(total_ejercicios))
            
        st.write("")
        
        # Renderizado de las tarjetas del Dashboard
        for bloque in bloques_totales:
            df_b = df_limpio[df_limpio["Bloque"] == bloque]
            ejercicios_del_bloque = df_b["Ejercicio"].tolist()
            
            ejercicios_html = "".join([f"<li style='margin-bottom:6px; font-size:0.95rem; color:#E2E8F0;'><span style='color:#00F5A0;'>■</span> {ej}</li>" for ej in ejercicios_del_bloque])
            
            st.markdown(f"""
            <div class="dashboard-card">
                <h4 style="margin: 0 0 4px 0; font-family: 'Inter', sans-serif; color: #FFFFFF !important;">{bloque}</h4>
                <p style="margin: 0 0 12px 0; font-size: 0.85rem; color: #64748B; font-weight:600;">{len(ejercicios_del_bloque)} ejercicios prescritos</p>
                <ul style="margin: 0; padding-left: 5px; list-style-type: none;">
                    {ejercicios_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # VISTA B: BLOQUE ESPECÍFICO
    # -------------------------------------------------------------
    else:
        bloque_actual = seleccion
        st.markdown(f'### ⚡ {bloque_actual}', unsafe_allow_html=True)
        
        df_bloque = df_limpio[df_limpio["Bloque"] == bloque_actual]
        
        for index, fila_limpia in df_bloque.iterrows():
            carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
            titulo_tarjeta = f"▶ {fila_limpia['Ejercicio']} — ({carga})"
            
            with st.expander(titulo_tarjeta):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Series", value=str(fila_limpia['Series']))
                with col2:
                    st.metric(label="Reps", value=str(fila_limpia['Reps']))
                with col3:
                    descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                    st.metric(label="Descanso", value=str(descanso))
                
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
