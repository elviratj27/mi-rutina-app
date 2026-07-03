import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página con nombre limpio en el navegador
st.set_page_config(page_title="Rutina de Entrenamiento", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Importamos tipografías elegantes desde Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Fondo general estilo lino/crema suave de Sereniti y textos grafito */
    .stApp { 
        background-color: #F4F1EA; 
        color: #2E2A25; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Títulos principales con tipografía Serif elegante */
    h1, h2, h3 { 
        font-family: 'Playfair Display', serif !important;
        color: #2E2A25 !important; 
        font-weight: 600 !important; 
    }
    
    /* Subtítulos y énfasis en cursiva elegante */
    .serif-italic {
        font-family: 'Playfair Display', serif !important;
        font-style: italic;
        color: #D4A3B3; /* Tono rosa viejo/malva de acento */
    }
    
    /* --- MENÚ LATERAL (SIDEBAR COLAPSABLE ESTILO ZARA) --- */
    [data-testid="stSidebar"] {
        background-color: #ECE8DF !important; /* Un tono más oscuro que el fondo para dar contraste */
        border-right: 1px solid #E3DDD0 !important;
    }
    [data-testid="stSidebar"] h3 {
        font-family: 'Playfair Display', serif !important;
        color: #2E2A25 !important;
    }
    /* Estilo para los botones de opción en el menú */
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #4A443C !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Tarjetas del Dashboard de la página principal (Blanco puro con bordes suaves) */
    .dashboard-card {
        background-color: #FFFFFF;
        border: 1px solid #EAE5DB;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(74, 68, 60, 0.04);
    }
    
    /* Tarjetas expandibles de ejercicios (Estilo bloques inferiores de Sereniti) */
    .stExpander { 
        background-color: #FFFFFF !important; 
        border: 1px solid #EAE5DB !important; 
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 20px rgba(74, 68, 60, 0.04) !important;
    }
    
    /* Ajustes de color para textos generales */
    .stMarkdown p, .stExpander label {
        color: #4A443C !important;
    }
    
    /* Métricas numéricas destacados en Rosa Malva Suave */
    [data-testid="stMetricValue"] {
        color: #C28CA0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #7A7265 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em;
    }
    
    /* Icono o viñeta de los ejercicios en el Dashboard */
    .bullet-icon {
        color: #C28CA0;
        margin-right: 8px;
    }
    
    /* Recuadro del Foco Técnico con fondo sutil malva */
    .stAlert {
        background-color: #FAF6F0 !important;
        border: 1px solid #EAD5DC !important;
        border-radius: 12px !important;
        color: #4A443C !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal adaptado al diseño minimalista
st.markdown('<h1>Mi Espacio de <span class="serif-italic">Entrenamiento</span></h1>', unsafe_allow_html=True)
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
    opciones_menu = ["✨ Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 🧭 Explorar Bloques")
        st.write("---")
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: RESUMEN GENERAL (ESTILO DASHBOARD SERENITI)
    # -------------------------------------------------------------
    if seleccion == "✨ Resumen General":
        st.markdown('### 📊 <span class="serif-italic">Resumen</span> de la Sesión', unsafe_allow_html=True)
        
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
            
            ejercicios_html = "".join([f"<li style='margin-bottom:6px; font-size:0.95rem;'><span style='color:#C28CA0;'>✦</span> {ej}</li>" for ej in ejercicios_del_bloque])
            
            st.markdown(f"""
            <div class="dashboard-card">
                <h4 style="margin: 0 0 6px 0; font-family: 'Playfair Display', serif; color: #2E2A25 !important;">{bloque}</h4>
                <p style="margin: 0 0 12px 0; font-size: 0.85rem; color: #7A7265; font-family: 'Plus Jakarta Sans', sans-serif;">Consta de {len(ejercicios_del_bloque)} fases de movimiento</p>
                <ul style="margin: 0; padding-left: 5px; list-style-type: none; color: #4A443C;">
                    {ejercicios_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # VISTA B: BLOQUE ESPECÍFICO
    # -------------------------------------------------------------
    else:
        bloque_actual = seleccion
        st.markdown(f'### <span class="serif-italic">Fase</span> — {bloque_actual}', unsafe_allow_html=True)
        
        df_bloque = df_limpio[df_limpio["Bloque"] == bloque_actual]
        
        for index, fila_limpia in df_bloque.iterrows():
            carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
            titulo_tarjeta = f"✨ {fila_limpia['Ejercicio']} — {carga}"
            
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
