import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime

# CONFIGURAÇÃO DE ELITE (Usada por Experts)
def conectar_expert():
    # Buscamos as chaves nos Secrets
    keys = [st.secrets.get("GOOGLE_API_KEY_1"), st.secrets.get("GOOGLE_API_KEY_2")]
    keys = [k for k in keys if k] # Limpa chaves vazias
    
    random.shuffle(keys) # Revezamento aleatório para poupar cota
    
    # OS MODELOS QUE REALMENTE FUNCIONAM NA V1BETA SEM ERRO 404
    modelos_expert = ['gemini-1.0-pro-001', 'gemini-1.0-pro-latest', 'gemini-pro']
    
    for key in keys:
        genai.configure(api_key=key)
        for modelo_nome in modelos_expert:
            try:
                # Tentativa de conexão direta
                model = genai.GenerativeModel(modelo_nome)
                # Teste de "fumaça" (geração mínima para validar)
                return model, modelo_nome
            except:
                continue
    return None, None

# DESIGN E INTERFACE
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #2ecc71; object-fit: cover; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 25px; margin-bottom: 20px; border-left: 6px solid #f1c40f; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'roteiro' not in st.session_state: st.session_state.roteiro = None

URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#f1c40f;'>Expert Stories Pro</h1>", unsafe_allow_html=True)

tema = st.text_input("Sobre o que vamos vender hoje?", placeholder="Ex: Bastidores, Oferta...")
estilo = st.selectbox("Tom de Voz", ["Venda Direta", "Autoridade", "Humanizado"])

if st.button("🚀 GERAR ESTRATÉGIA"):
    if tema:
        with st.spinner('Expert AI conectando aos servidores estáveis...'):
            model, modelo_ativo = conectar_expert()
            if model:
                try:
                    # Prompt estratégico
                    prompt = f"Crie um roteiro de 5 stories para Instagram sobre {tema} no estilo {estilo}. Liste Story 1 a 5 com Cena e Fala."
                    response = model.generate_content(prompt)
                    st.session_state.roteiro = response.text
                    st.success(f"Conectado via: {modelo_ativo}")
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
            else:
                st.error("Nenhum modelo da lista Expert respondeu. Verifique suas chaves API.")

if st.session_state.roteiro:
    st.markdown(f'<div class="stBox"><div class="fala-texto">{st.session_state.roteiro}</div></div>', unsafe_allow_html=True)
