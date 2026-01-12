import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# 1. MODELO DA SUA LISTA (Sem números e sem erro de chat)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Usando o identificador direto que você confirmou que funciona
model = genai.GenerativeModel('gemini-flash')

# 2. DESIGN PREMIUM
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #2ecc71; object-fit: cover; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #f1c40f; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. PERSISTÊNCIA (Garante que as 5 ideias fiquem na tela)
if 'meus_stories' not in st.session_state:
    st.session_state.meus_stories = None
if 'timer_run' not in st.session_state:
    st.session_state.timer_run = None

def liberado():
    if st.session_state.timer_run is None:
        return True
    return datetime.now() - st.session_state.timer_run > timedelta(seconds=20)

# 4. INTERFACE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#f1c40f;'>Expert Stories Pro</h1>", unsafe_allow_html=True)

tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores")
estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado"])

# 5. GERAÇÃO (Usando generate_content direto para evitar erro de chat)
if liberado():
    if st.button("🚀 GERAR 5 STORIES"):
        if tema:
            with st.spinner('Acessando Gemini Flash...'):
                try:
                    # Instrução focada em 5 blocos de texto
                    prompt = f"Crie 5 stories para Instagram sobre {tema} no estilo {estilo}. Para cada story, descreva: Horário, Cena e Fala."
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state.meus_stories = response.text
                        st.session_state.timer_run = datetime.now()
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro no modelo Flash: {str(e)}")
        else:
            st.warning("Preencha o tema.")
else:
    espera = 20 - int((datetime.now() - st.session_state.timer_run).total_seconds())
    st.info(f"⏳ IA recarregando em {espera}s")
    time.sleep(1)
    st.rerun()

# 6. EXIBIÇÃO FINAL
if st.session_state.meus_stories:
    st.markdown(f"""
    <div class="stBox">
        <div class="fala-texto">{st.session_state.meus_stories}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Gerar Novos"):
        st.session_state.meus_stories = None
        st.rerun()
