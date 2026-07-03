import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de página con nombre limpio en el navegador
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
        background-color: #E6E2D8 !important; 
        border-right: 1px solid #D9D4C7 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }
    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #000000 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    
    /* Cuadrícula del Resumen General */
    .dashboard-card {
        background-color: #F2EFE9;
        border: 1px solid #2C2C2C;
        border-radius: 24px !important;
        padding: 22px;
        margin-bottom: 16px;
        height: 100%;
    }
    
    /* --- SOLUCIÓN DE DISEÑO: DESPLEGABLES OSCUROS UNIFICADOS --- */
    /* Estructura para los bloques interactivos oscuros */
    .custom-accordion {
        background-color: #2C2C2C !important;
        border-radius: 24px !important;
        margin-bottom: 14px !important;
        overflow: hidden;
        border: 1px solid #2C2C2C;
    }
    
    /* La barra superior que se pulsa */
    .custom-accordion-summary {
        padding: 16px 24px !important;
        color: #F2EFE9 !important;
        font-weight: 500 !important;
        cursor: pointer;
        font-size: 1rem;
        letter-spacing: 0.02em;
        outline: none;
        list-style: none; /* Oculta la flecha nativa molesta */
    }
    .custom-accordion-summary::-webkit-details-marker {
        display: none; /* Oculta la flecha en navegadores Safari/iOS */
    }
    
    /* Contenido interior cuando se despliega el ejercicio */
    .custom-accordion-content {
        background-color: #F8FAFC !important; /* Fondo interno muy limpio e independiente */
        padding: 24px !important;
        border-top: 1px solid #2C2C2C;
        color: #000000 !important;
    }
    
    /* Estilo para los bloques de texto de las filas de datos */
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 18px;
        padding-bottom: 12px;
        border-bottom: 1px solid #E2E8F0;
    }
    .metric-box {
        flex: 1;
        text-align: left;
    }
    .metric-box-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 700;
        color: #555555;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-box-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #000000;
    }
    
    /* --- SECCIÓN FOCO TÉCNICO COMPARTIDA --- */
    .custom-foco-box {
        background-color: #2C2C2C !important;
        border-radius: 24px !important;
        padding: 18px 24px !important;
        margin-top: 16px !important;
    }
    .custom-foco-box p {
        color: #F2EFE9 !important; 
        font-size: 0.92rem !important;
        margin: 0 !important;
        letter-spacing: 0.02em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1>WORKOUT <span class="serif-italic-accent">Plans</span></h1>', unsafe_allow_html=True)
st.write("---")

def cargar_datos():
    return pd.read_excel("rutina.xlsx")

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
    bloques_totales = [b for b in df_limpio["Bloque"].unique() if b != ""]
    
    opciones_menu = ["✨ Ver Resumen General"] + list(bloques_totales)
    
    with st.sidebar:
        st.write("")
        st.write("### 🧭 INDEX")
        st.write("---")
        seleccion = st.radio("Ir a:", opciones_menu, label_visibility="collapsed")

    # -------------------------------------------------------------
    # VISTA A: RESUMEN GENERAL (CUADRÍCULA)
    # -------------------------------------------------------------
    if seleccion == "✨ Ver Resumen General":
        st.markdown('### 📊 <span class="serif-italic-accent">Resumen</span> de la Sesión', unsafe_allow_html=True)
        
        total_ejercicios = len(df_limpio[df_limpio["Ejercicio"] != ""])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Número de Bloques", value=str(len(bloques_totales)))
        with col2:
            st.metric(label="Ejercicios Programados", value=str(total_ejercicios))
            
        st.write("---")
        
        columnas_por_fila = 2
        for i in range(0, len(bloques_totales), columnas_por_fila):
            bloques_fila = bloques_totales[i:i + columnas_por_fila]
            cols = st.columns(columnas_por_fila)
            
            for idx, bloque in enumerate(bloques_fila):
                with cols[idx]:
                    df_b = df_limpio[df_limpio["Bloque"] == bloque]
                    ejercicios_del_bloque = df_b["Ejercicio"].tolist()
                    ejercicios_html = "".join([f"<li style='margin-bottom:6px; font-size:0.9rem;'>▪ {ej}</li>" for ej in ejercicios_del_bloque])
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4 style="margin: 0 0 2px 0;">{bloque}</h4>
                        <p style="margin: 0 0 14px 0; font-size: 0.8rem; color: #555555;">{len(ejercicios_del_bloque)} ejercicios</p>
                        <ul style="margin: 0; padding-left: 5px; list-style-type: none;">
                            {ejercicios_html}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # VISTA B: BLOQUE ESPECÍFICO (CON LOS NUEVOS BLOQUES OSCUROS)
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
            descanso = fila_limpia.get('Descanso (seg)', fila_limpia.get('Descanso', ''))
            descanso_limpio = limpiar_numero(descanso)
            
            # Formateamos los detalles teóricos opcionales en HTML limpio
            objetivo_html = f"<p style='margin-bottom:8px;'><strong>🎯 Objetivo:</strong> {fila_limpia['Objetivo']}</p>" if fila_limpia['Objetivo'] else ""
            justificacion_html = f"<p style='margin-bottom:8px;'><strong>💡 Justificación:</strong> {fila_limpia['Justificación']}</p>" if fila_limpia['Justificación'] else ""
            ejecucion_html = f"<p style='margin-bottom:8px;'><strong>🛠️ Ejecución:</strong> {fila_limpia['Ejecución']}</p>" if fila_limpia['Ejecución'] else ""
            
            # Bloque de foco técnico
            foco = fila_limpia.get('Foco Técnico', fila_limpia.get('Foco_Técnico', ''))
            foco_html = f"""
            <div class="custom-foco-box">
                <p><strong>👁️ FOCO TÉCNICO:</strong> {foco}</p>
            </div>
            """ if foco else ""

            # Renderizado del componente unificado 100% idéntico a tu referencia
            st.markdown(f"""
            <details class="custom-accordion">
                <summary class="custom-accordion-summary">{titulo_tarjeta}</summary>
                <div class="custom-accordion-content">
                    <div class="metric-row">
                        <div class="metric-box">
                            <div class="metric-box-label">Series</div>
                            <div class="metric-box-value">{series_limpias}</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-box-label">Reps</div>
                            <div class="metric-box-value">{reps_limpias}</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-box-label">Descanso</div>
                            <div class="metric-box-value">{descanso_limpio}</div>
                        </div>
                    </div>
                    {objetivo_html}
                    {justificacion_html}
                    {ejecucion_html}
                    {foco_html}
                </div>
            </details>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")
