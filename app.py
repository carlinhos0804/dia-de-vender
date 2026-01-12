import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime

# 1. FUNÇÃO DE CONEXÃO ESTÁVEL (AUTO-DETECÇÃO)
def conectar_expert():
    keys = [st.secrets.get("GOOGLE_API_KEY_1"), st.secrets.get("GOOGLE_API_KEY_2")]
    keys = [k for k in keys if k]
    if not keys:
        return None, "Chave API não configurada"
    
    random.shuffle(keys)
    for key in keys:
        try:
            genai.configure(api_key=key)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model = genai.GenerativeModel(m.name)
                    return model, m.name
        except:
            continue
    return None, "Nenhum modelo disponível"

# 2. DESIGN PREMIUM (PRETO, OURO E VERDE)
st.set_page_config(page_title="Expert Stories Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 25px; border-left: 5px solid #f1c40f; margin-bottom: 20px; }
    .header-story { color: #f1c40f; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
    .cena-box { color: #888888; font-size: 0.9em; margin-bottom: 10px; }
    .script-box { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em; }
    h1 { text-align: center; color: #f1c40f; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFACE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div style="text-align:center;"><img src="{URL_LOGO}" width="120" style="border-radius:50%; border:3px solid #2ecc71;"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

if 'roteiro' not in st.session_state:
    st.session_state.roteiro = None

tema = st.text_input("Qual o produto ou tema de hoje?", placeholder="Ex: Lançamento de Coleção")
estilo = st.selectbox("Estilo de Abordagem", ["Venda Direta", "Autoridade", "Humanizado"])

# 4. GERAÇÃO ESTRUTURADA
if st.button("🚀 GERAR CRONOGRAMA COMERCIAL"):
    if tema:
        with st.spinner('Expert AI organizando horários comerciais...'):
            model, nome_modelo = conectar_expert()
            if model:
                try:
                    # Prompt ultra específico para os horários de 8h às 19h
                    prompt = (
                        f"Atue como um estrategista de vendas. Crie um roteiro de 5 stories para Instagram sobre '{tema}' "
                        f"no estilo '{estilo}'. Distribua os stories entre 08:00 e 19:00. "
                        f"Para cada story use EXATAMENTE este formato:\n"
                        f"HORÁRIO: [Horário]\n"
                        f"STORY: [Título do Story]\n"
                        f"CENA: [Descrição da imagem ou vídeo]\n"
                        f"SCRIPT: [Texto exato para o vendedor falar ou legendar]\n"
                        f"---"
                    )
                    response = model.generate_content(prompt)
                    st.session_state.roteiro = response.text
                except Exception as e:
                    st.error(f"Erro: {e}")
            else:
                st.error("Erro de conexão com o modelo.")
    else:
        st.warning("Insira um tema.")

# 5. EXIBIÇÃO ORGANIZADA
if st.session_state.roteiro:
    # Dividir o texto da IA em blocos para organizar visualmente
    blocos = st.session_state.roteiro.split("---")
    
    for bloco in blocos:
        if bloco.strip():
            st.markdown(f'<div class="stBox">{bloco.strip()}</div>', unsafe_allow_html=True)

    if st.button("🗑️ Limpar Roteiro"):
        st.session_state.roteiro = None
        st.rerun()
