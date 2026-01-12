import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime

# 1. FUNÇÃO EXPERT: DESCOBERTA DE MODELO ATIVO
def conectar_expert():
    # Lista de chaves para revezamento
    keys = [st.secrets.get("GOOGLE_API_KEY_1"), st.secrets.get("GOOGLE_API_KEY_2")]
    keys = [k for k in keys if k]
    if not keys:
        return None, "Chave API não configurada"
    
    random.shuffle(keys)
    
    for key in keys:
        try:
            genai.configure(api_key=key)
            # O SEGREDO: Listar o que o servidor autoriza para VOCÊ
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Retorna o primeiro modelo que suporta geração (ex: models/gemini-1.5-flash)
                    model = genai.GenerativeModel(m.name)
                    return model, m.name
        except Exception as e:
            continue
    return None, "Nenhum modelo disponível para esta chave"

# 2. DESIGN EXPERT
st.set_page_config(page_title="Expert Stories Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 25px; border-left: 5px solid #f1c40f; margin-top: 20px; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

if 'roteiro' not in st.session_state: st.session_state.roteiro = None

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>Expert Stories Pro</h1>", unsafe_allow_html=True)

tema = st.text_input("Qual o tema estratégico?", placeholder="Ex: Bastidores da produção")
estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado"])

# 3. GERAÇÃO SEM ERRO 404
if st.button("🚀 GERAR COM AUTO-DETECÇÃO"):
    if tema:
        with st.spinner('Expert AI escaneando modelos disponíveis...'):
            model, nome_modelo = conectar_expert()
            if model:
                try:
                    prompt = f"Roteiro de 5 stories sobre {tema} no estilo {estilo}. Liste Story 1 a 5 com Cena e Fala."
                    response = model.generate_content(prompt)
                    st.session_state.roteiro = response.text
                    st.success(f"Conectado com sucesso ao modelo: {nome_modelo}")
                except Exception as e:
                    if "429" in str(e):
                        st.error("Cota excedida. Aguarde 60 segundos.")
                    else:
                        st.error(f"Erro na geração: {e}")
            else:
                st.error(f"Erro de Conexão: {nome_modelo}")
    else:
        st.warning("Preencha o tema.")

if st.session_state.roteiro:
    st.markdown(f'<div class="stBox"><div class="fala-texto">{st.session_state.roteiro}</div></div>', unsafe_allow_html=True)
