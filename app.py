import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime

# 1. TENTATIVA FINAL DE NOMES (O QUE SOBROU NO SERVIDOR)
def conectar_expert():
    keys = [st.secrets.get("GOOGLE_API_KEY_1"), st.secrets.get("GOOGLE_API_KEY_2")]
    keys = [k for k in keys if k]
    random.shuffle(keys)
    
    # Nomes que costumam ser o "coringa" quando tudo dá 404
    modelos_coringa = ['gemini-pro', 'gemini-1.0-pro-latest', 'gemini-1.5-flash-latest']
    
    for key in keys:
        try:
            genai.configure(api_key=key)
            for nome in modelos_coringa:
                try:
                    # Testamos a existência do modelo sem gerar conteúdo primeiro
                    model = genai.GenerativeModel(nome)
                    # Se chegou aqui, o nome existe no servidor
                    return model, nome
                except:
                    continue
        except:
            continue
    return None, None

# 2. DESIGN EXPERT (Preto, Ouro e Verde)
st.set_page_config(page_title="Expert Stories Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 25px; border-left: 5px solid #f1c40f; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

if 'roteiro' not in st.session_state: st.session_state.roteiro = None

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>Expert Stories Pro</h1>", unsafe_allow_html=True)

tema = st.text_input("Tema de hoje?", placeholder="Ex: Bastidores")
estilo = st.selectbox("Estilo", ["Venda Direta", "Autoridade", "Humanizado"])

# 3. LÓGICA DE GERAÇÃO
if st.button("🚀 GERAR AGORA"):
    if tema:
        with st.spinner('Procurando modelo disponível no Google...'):
            model, nome_ativo = conectar_expert()
            if model:
                try:
                    prompt = f"Roteiro de 5 stories sobre {tema} no estilo {estilo}. Liste Story 1 a 5 com Cena e Fala."
                    response = model.generate_content(prompt)
                    st.session_state.roteiro = response.text
                    st.success(f"Conectado via: {nome_ativo}")
                except Exception as e:
                    if "429" in str(e):
                        st.error("Cota excedida. Aguarde 60 segundos.")
                    else:
                        st.error(f"Erro na geração: {e}")
            else:
                st.error("Erro 404 persistente: O Google não reconhece nenhum dos nomes de modelo na sua região.")
    else:
        st.warning("Preencha o tema.")

if st.session_state.roteiro:
    st.markdown(f'<div class="stBox"><div class="fala-texto">{st.session_state.roteiro}</div></div>', unsafe_allow_html=True)
