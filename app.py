import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DO MODELO MAIS ATUAL (2026)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# O modelo 2.0-flash é o sucessor definitivo do 1.5, focado em velocidade e precisão
model = genai.GenerativeModel('gemini-2.0-flash')

# 2. DESIGN PREMIUM (Black, Green & Gold)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; box-shadow: 0px 0px 15px rgba(46,204,113,0.3); }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 25px !important; margin-bottom: 20px !important; border-left: 6px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-size: 1.8em !important; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em !important; }
    .stButton>button:disabled { background: #333 !important; color: #777 !important; border: 1px solid #444 !important; }
    .horario-tag { color: #f1c40f; font-weight: bold; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; line-height: 1.5; border: 1px dashed #2ecc71; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROLE DE COTA (Timer de 30s)
if 'last_run' not in st.session_state:
    st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=30)

# 4. CABEÇALHO (Sua Imagem)
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. INPUTS
tema = st.text_input("Qual o foco estratégico de hoje?", placeholder="Ex: Lançamento de Mentorias")
estilo = st.selectbox("Tom de Voz da IA", ["Venda Direta", "Autoridade/Líder", "Humanizado", "Curiosidade"])

# 6. GERAÇÃO DE CONTEÚDO (MÉTODO OTIMIZADO)
if can_run():
    if st.button("🚀 GERAR ESTRATÉGIA AGORA"):
        if tema:
            with st.spinner('O Gemini 2.0 está processando sua estratégia...'):
                try:
                    # Usamos uma instrução de sistema para o modelo 2.0 garantir o JSON
                    prompt = f"Crie 5 stories sobre {tema} no estilo {estilo}. Responda estritamente em JSON
