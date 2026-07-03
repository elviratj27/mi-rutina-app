import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página 
st.set_page_config(page_title="Rutina de Entrenamiento", page_icon="💪", layout="centered")

st.markdown("""
    <style>
    /* Importamos las fuentes de la imagen: Inter para lo moderno y Playfair para el toque de diseño */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@1,400;1,500&display=swap');

    /* Fondo ARENA CLARO de la imagen y textos negro profundo */
    .stApp { 
        background-color: #F2EFE9; 
        color: #000000; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Títulos principales en Mayúsculas, tipografía limpia e impacto editorial */
    h1, h2, h3, h4 { 
        font-family: 'Inter', sans-serif !important;
        color: #000000 !important; 
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* El toque cursiva elegante que aparece en tu captura (ej. Workout Plans) */
    .serif-italic-accent {
        font-family: 'Playfair Display', serif !important;
        font-style: italic !important;
        text-transform: none !important; /* Para que mantenga las minúsculas elegantes */
        font-weight: 400 !important;
        color: #000000 !important;
    }
    
    /* --- MENÚ LATERAL INTERACTIVO (ESTILO ZARA / COLAPSABLE) --- */
    [data-testid="stSidebar"] {
        background-color: #E6E2D8 !important; /* Un tono un pelín más oscuro para contrastar */
        border-right: 1px solid #D9D4C7 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }
    /* Opciones del menú lateral */
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #000000 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    
    /* Cuadrícula del Resumen General (Tarjetas del mismo color con borde negro muy fino) */
    .dashboard-card {
        background-color: #F2EFE9;
        border: 1px solid #000000;
        border-radius: 0px; /* Estilo editorial rectilíneo, sin bordes redondeados infantiles */
        padding: 22px;
        margin-bottom: 16px;
        height: 100%;
    }
    
    /* Tarjetas expandibles para los ejercicios (Estilo minimalista puro) */
    .stExpander { 
        background-color: #F2EFE9 !important; 
        border: 1px solid #000000 !important; 
        border-radius: 0px !important;
        margin-bottom: 12px !important;
    }
    
    /* Textos internos de las tarjetas */
    .stMarkdown p, .stExpander label {
        color: #000000 !important;
        font-weight: 400;
    }
    
    /* Métricas destacadas en NEGRO ABSOLUTO */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
        font-size: 2.4rem !important;
    }
    /* Etiquetas de métricas en gris oscuro/grafito */
    [data-testid="stMetricLabel"] p {
        color: #555555 !important;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
    }
    
    /* Caja de Foco Técnico ultra limpia */
    .stAlert {
        background-color: #E6E2D8 !important;
        border: 1px solid #000000 !important;
        border-radius: 0px !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cabecera con el estilo tipográfico de tu captura
st.markdown('<h1>WORKOUT <span class="serif-italic-accent">Plans</span></h1>', unsafe_allow_html=True)
st.write("---")

# 2. Cargar datos del Excel
def cargar_datos():
    return pd.read_excel("rutina.xlsx")

# Función auxiliar para limpiar números con .0
def limpiar_numero(valor):
    if valor == "":
        return ""
    try:
        float_val = float(valor)
        if float_val.is_integer():
            return str(int(float_val))
        return str(valor)
    except ValueError:
        return str(valor)

try:
    df = cargar_datos()
    df_limpio = df.replace({np.nan: ""})

    # Obtener los bloques únicos
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    # --- MENÚ SIDEBAR ---
    opciones_menu = ["✨ Ver Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 🧭 INDEX")
        st.write("---")
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: RESUMEN GENERAL (DASHBOARD EDITORIAL EN CUADRÍCULA)
    # -------------------------------------------------------------
    if seleccion == "✨ Ver Resumen General":
        st.markdown('### 📊 <span class="serif-italic-accent">Resumen</span> de la Sesión', unsafe_allow_html=True)
        
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
                    
                    # Lista minimalista limpia
                    ejercicios_html = "".join([f"<li style='margin-bottom:6px; font-size:0.9rem;'>▪ {ej}</li>" for ej in ejercicios_del_bloque])
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4 style="margin: 0 0 2px 0;">{bloque}</h4>
                        <p style="margin: 0 0 14px 0; font-size: 0.8rem; color: #555555;">{len(ejercicios_del_bloque)} ejercicios prescritos</p>
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
            titulo_tarjeta = f"→ {fila_limpia['Ejercicio']} — ({carga})"
            
            series_limpias = limpiar_numero(fila_limpia['Series'])
            reps_limpias = limpiar_numero(fila_limpia['Reps'])
            
            with st.expander(titulo_tarjeta):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Series", value=series_limpias)
                with col2:
                    st.metric(label="Reps", value=reps_limpias)
                with col3:
                    descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
                    descanso_limpio = limpiar_numero(descanso)
                    st.metric(label="Descanso", value=descanso_limpio)
                
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
