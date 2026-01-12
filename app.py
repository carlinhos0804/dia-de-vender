import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# 1. FUNÇÃO DE DESCOBERTA AUTOMÁTICA
def inicializar_modelo():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Procuramos na sua conta qual modelo está ativo para você
        modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Prioridade: 1.5 Flash -> 1.5 Pro -> Pro -> Flash
        selecionado = None
        for m in modelos_disponiveis:
            if '1.5-flash' in m: selecionado = m; break
        if not selecionado:
            for m in modelos_disponiveis:
                if 'pro' in m: selecionado = m; break
        
        return genai.GenerativeModel(selecionado or modelos_disponiveis[0])
    except Exception as e:
        return None

model = inicializar_modelo()

# 2. DESIGN (Ouro e Verde)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #2ecc71; object-fit: cover; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #f1c40f; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. MEMÓRIA
if 'stories' not in st.session_state: st.session_state.stories = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def liberado():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=10)

# 4. INTERFACE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#f1c40f;'>Expert Stories Pro</h1>", unsafe_allow_html=True)

if model:
    tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores")
    estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado"])

    if liberado():
        if st.button("🚀 GERAR ROTEIRO AGORA"):
            if tema:
                with st.spinner('Gerando conteúdo...'):
                    try:
                        prompt = f"Crie 5 stories para Instagram. Tema: {tema}. Estilo: {estilo}. Liste Horário, Cena e Fala."
                        response = model.generate_content(prompt)
                        st.session_state.stories = response.text
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro na geração: {e}")
            else:
                st.warning("Preencha o tema.")
    else:
        st.info(f"⏳ Recarregando... {10 - int((datetime.now() - st.session_state.last_run).total_seconds())}s")
        time.sleep(1)
        st.rerun()

    if st.session_state.stories:
        st.markdown(f'<div class="stBox"><div class="fala-texto">{st.session_state.stories}</div></div>', unsafe_allow_html=True)
        if st.button("🗑️ Limpar"):
            st.session_state.stories = None
            st.rerun()
else:
    st.error("Sua API Key não encontrou modelos disponíveis. Verifique-a no Google AI Studio.")
