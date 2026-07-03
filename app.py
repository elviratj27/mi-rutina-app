import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página con nombre limpio en el navegador
st.set_page_config(page_title="Rutina de Entrenamiento", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Importamos una tipografía refinada y moderna */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Fondo limpio blanco/gris claro premium y textos grafito oscuro */
    .stApp { 
        background-color: #F8FAFC; 
        color: #1E293B; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Títulos principales en Azul Marino Profundo (Elegante y Atlético) */
    h1, h2, h3, h4 { 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0F172A !important; 
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }
    
    /* --- MENÚ LATERAL (SIDEBAR COLAPSABLE ESTILO ZARA) --- */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9 !important; /* Gris suave de contraste */
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    /* Botones de opción en el menú */
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #334155 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Tarjetas del Dashboard en Cuadrícula (Fondo blanco puro, bordes muy finos) */
    .dashboard-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        height: 100%; /* Para que todas midan lo mismo en la cuadrícula */
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.02), 0 2px 4px -2px rgba(15, 23, 42, 0.02);
    }
    
    /* Tarjetas expandibles de ejercicios (Líneas limpias) */
    .stExpander { 
        background-color: #FFFFFF !important; 
        border: 1px solid #E2E8F0 !important; 
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.02) !important;
    }
    
    /* Ajustes de color para textos generales */
    .stMarkdown p, .stExpander label {
        color: #475569 !important;
    }
    
    /* Métricas numéricas destacadas en Verde Salvia/Atlético Mate (Unisex) */
    [data-testid="stMetricValue"] {
        color: #16A34A !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #64748B !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em;
    }
    
    /* Recuadro del Foco Técnico con un tono de alerta suave neutro */
    .stAlert {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        color: #334155 !important;
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
    
    # --- MENÚ DESPLEGABLE SIDEBAR (ESTILO ZARA) ---
    opciones_menu = ["✨ Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 🧭 Menú de Bloques")
        st.write("---")
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: RESUMEN GENERAL (DASHBOARD EN CUADRÍCULA SEGÚN TU BOCETO)
    # -------------------------------------------------------------
    if seleccion == "✨ Resumen General":
        st.write("### 📊 Resumen de la Sesión")
        
        total_ejercicios = len(df_limpio[df_limpio["Ejercicio"] != ""])
        
        # KPIs Principales en horizontal
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric(label="Número de Bloques", value=str(len(bloques_totales)))
        with kpi2:
            st.metric(label="Ejercicios Hoy", value=str(total_ejercicios))
            
        st.write("---")
        
        # --- AQUÍ CREAMOS LA CUADRÍCULA DE TU DIBUJO ---
        # Creamos filas de 2 columnas cada una
        columnas_por_fila = 2
        
        for i in range(0, len(bloques_totales), columnas_por_fila):
            # Seleccionamos el grupo de bloques para esta fila (máximo 2)
            bloques_fila = bloques_totales[i:i + columnas_por_fila]
            
            # Generamos las columnas visuales en Streamlit
            cols = st.columns(columnas_por_fila)
            
            for idx, bloque in enumerate(bloques_fila):
                with cols[idx]:
                    df_b = df_limpio[df_limpio["Bloque"] == bloque]
                    ejercicios_del_bloque = df_b["Ejercicio"].tolist()
                    
                    # Formato de lista elegante
                    ejercicios_html = "".join([f"<li style='margin-bottom:4px; font-size:0.9rem;'>🔹 {ej}</li>" for ej in ejercicios_del_bloque])
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4 style="margin: 0 0 4px 0; color: #1E3A8A !important;">{bloque}</h4>
                        <p style="margin: 0 0 12px 0; font-size: 0.8rem; color: #64748B;">{len(ejercicios_del_bloque)} ejercicios</p>
                        <ul style="margin: 0; padding-left: 15px; list-style-type: none; color: #334155;">
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
