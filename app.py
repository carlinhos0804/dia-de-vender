import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime, timedelta

# 1. MOTOR COM INSTRUÇÃO DE SISTEMA (Contorno de Filtro)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Definimos que ele é um roteirista criativo ANTES de começar
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"temperature": 0.7},
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)

# 2. DESIGN PREMIUM (Ouro, Verde e Preto)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 20px !important; margin-bottom: 20px !important; border-left: 5px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-weight: 800; font-size: 2em !important; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. MEMÓRIA DE SESSÃO
if 'stories' not in st.session_state: st.session_state.stories = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=15)

# 4. CABEÇALHO
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. INPUTS
tema = st.text_input("Sobre o que vamos postar hoje?", placeholder="Ex: Bastidores, Dica do dia...")
estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado"])

# 6. LÓGICA DE EXECUÇÃO
if can_run():
    if st.button("🚀 GERAR 5 STORIES AGORA"):
        if tema:
            with st.spinner('A IA está roteirizando para você...'):
                try:
                    # PROMPT REFORÇADO (Para evitar bloqueios)
                    prompt_final = f"""
                    Você é um assistente de marketing criativo. 
                    Crie 5 sugestões de roteiros para stories de Instagram sobre: {tema}. 
                    Estilo de comunicação: {estilo}.
                    Responda estritamente em formato JSON: 
                    [
                      {{"horario": "09:00", "cena": "descreva a cena", "jeito": "como gravar", "fala": "fala sugerida"}},
                      ... (repita para 5 stories)
                    ]
                    """
                    response = model.generate_content(prompt_final)
                    
                    if response.text:
                        clean_text = response.text.replace("```json", "").replace("```", "").strip()
                        st.session_state.stories = json.loads(clean_text)
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                except Exception as e:
                    st.warning("IA em manutenção momentânea. Tente um tema mais genérico ou aguarde.")
        else:
            st.warning("Preencha o tema.")
else:
    rem = 15 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.info(f"⏳ IA descansando... Disponível em {rem} segundos.")

# 7. EXIBIÇÃO DOS RESULTADOS
if st.session_state.stories:
    for s in st.session_state.stories:
        st.markdown(f"""
        <div class="stBox">
            <span style="color: #f1c40f; font-weight: bold;">⌚ {s.get('horario', 'Sugerido')}</span>
            <p><b>🎬 Cena:</b> {s.get('cena', '...')}</p>
            <p><b>🤳 Gravação:</b> {s.get('jeito', '...')}</p>
            <div class="fala-texto">"{s.get('fala', '...')}"</div>
        </div>
        """, unsafe_allow_html=True)

if not can_run():
    time.sleep(1)
    st.rerun()
