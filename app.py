import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página con nombre limpio en el navegador
st.set_page_config(page_title="Rutina de Entrenamiento", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Importamos la tipografía limpia y ultra-fina de Momentus */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Fondo oscuro azulado/grafito de la referencia y tipografía fina */
    .stApp { 
        background-color: #0E131F; 
        color: #F1F5F9; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Títulos limpios, finos y elegantes en blanco puro */
    h1, h2, h3, h4 { 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #FFFFFF !important; 
        font-weight: 500 !important; /* Más fina para dar elegancia */
        letter-spacing: -0.01em;
    }
    
    /* Acento azul celeste de la imagen Momentus */
    .momentus-accent {
        color: #93C5FD;
        font-weight: 600;
    }
    
    /* --- MENÚ LATERAL INTERACTIVO (ESTILO ZARA / COLAPSABLE) --- */
    [data-testid="stSidebar"] {
        background-color: #171E2E !important;
        border-right: 1px solid #242F41 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #93C5FD !important;
        font-weight: 600 !important;
    }
    /* Opciones del menú */
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #94A3B8 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    /* Cuadrícula del Resumen General (Tarjetas estilo Momentus) */
    .dashboard-card {
        background-color: #171E2E;
        border: 1px solid #242F41;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
        height: 100%;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* Tarjetas expandibles para los ejercicios */
    .stExpander { 
        background-color: #171E2E !important; 
        border: 1px solid #242F41 !important; 
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Textos internos más claros y legibles */
    .stMarkdown p, .stExpander label {
        color: #94A3B8 !important;
        font-weight: 400;
    }
    
    /* Métricas con el Azul Celeste Fino de Momentus */
    [data-testid="stMetricValue"] {
        color: #93C5FD !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600 !important;
        font-size: 2.2rem !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #64748B !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em;
    }
    
    /* Caja de Foco Técnico elegante y limpia */
    .stAlert {
        background-color: #0E131F !important;
        border: 1px solid #242F41 !important;
        border-radius: 12px !important;
        color: #E2E8F0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💪 Mi Panel de Entrenamiento")
st.write("---")

# 2. Cargar datos del Excel
def cargar_datos():
    return pd.read_excel("rutina.xlsx")

try:
    df = cargar_datos()
    df_limpio = df.replace({np.nan: ""})

    # Obtener los bloques únicos
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    # --- MENÚ SIDEBAR ---
    opciones_menu = ["✨ Ver Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 🧭 Menú de Sesión")
        st.write("---")
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: RESUMEN GENERAL (ESTILO DASHBOARD MOMENTUS EN CUADRÍCULA)
    # -------------------------------------------------------------
    if seleccion == "✨ Ver Resumen General":
        st.write("### 📊 Resumen del Entrenamiento")
        
        total_ejercicios = len(df_limpio[df_limpio["Ejercicio"] != ""])
        
        # KPIs de cabecera finos
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric(label="Número de Bloques", value=str(len(bloques_totales)))
        with kpi2:
            st.metric(label="Ejercicios Programados", value=str(total_ejercicios))
            
        st.write("---")
        
        # Cuadrícula horizontal (2 bloques por fila)
        columnas_por_fila = 2
        for i in range(0, len(bloques_totales), columnas_por_fila):
            bloques_fila = bloques_totales[i:i + columnas_por_fila]
            cols = st.columns(columnas_por_fila)
            
            for idx, bloque in enumerate(bloques_fila):
                with cols[idx]:
                    df_b = df_limpio[df_limpio["Bloque"] == bloque]
                    ejercicios_del_bloque = df_b["Ejercicio"].tolist()
                    
                    # Lista minimalista con punto azul claro
                    ejercicios_html = "".join([f"<li style='margin-bottom:6px; font-size:0.9rem; color:#E2E8F0;'><span style='color:#93C5FD; margin-right:6px;'>◦</span>{ej}</li>" for ej in ejercicios_del_bloque])
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4 style="margin: 0 0 2px 0;">{bloque}</h4>
                        <p style="margin: 0 0 14px 0; font-size: 0.8rem; color: #64748B;">{len(ejercicios_del_bloque)} ejercicios asignados</p>
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
        st.write(f"### {bloque_actual}")
        
        df_bloque = df_limpio[df_limpio["Bloque"] == bloque_actual]
        
        for index, fila_limpia in df_bloque.iterrows():
            carga = str(fila_limpia['Carga']) if fila_limpia['Carga'] != "" else "Peso corporal"
            titulo_tarjeta = f"🔹 {fila_limpia['Ejercicio']} — ({carga})"
            
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
