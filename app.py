import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime

# 1. CONEXÃO ESTÁVEL (AUTO-DETECÇÃO)
def conectar_expert():
    keys = [st.secrets.get("GOOGLE_API_KEY_1"), st.secrets.get("GOOGLE_API_KEY_2")]
    keys = [k for k in keys if k]
    if not keys: return None, "Chave não configurada"
    
    random.shuffle(keys)
    for key in keys:
        try:
            genai.configure(api_key=key)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return genai.GenerativeModel(m.name), m.name
        except: continue
    return None, "Erro de conexão"

# 2. DESIGN PREMIUM (ORGANIZAÇÃO POR CARTÕES)
st.set_page_config(page_title="Expert Stories Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    /* Estilização dos Expansores */
    .streamlit-expanderHeader { background-color: #111111 !important; border-left: 5px solid #f1c40f !important; color: #f1c40f !important; font-weight: bold !important; border-radius: 10px !important; }
    .stBox { background-color: #0d1a12; border: 1px dashed #2ecc71; padding: 15px; border-radius: 10px; }
    .label-expert { color: #2ecc71; font-weight: bold; font-size: 0.9em; text-transform: uppercase; margin-bottom: 5px; }
    .script-texto { color: #ffffff; font-style: italic; line-height: 1.6; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em; margin-top: 20px; }
    h1 { text-align: center; color: #f1c40f; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFACE DE ENTRADA
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div style="text-align:center;"><img src="{URL_LOGO}" width="100" style="border-radius:50%; border:3px solid #2ecc71;"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

if 'roteiro_lista' not in st.session_state:
    st.session_state.roteiro_lista = []

tema = st.text_input("Qual o foco das vendas de hoje?", placeholder="Ex: Queima de estoque, Novo serviço...")
estilo = st.selectbox("Personalidade da IA", ["Venda Direta", "Autoridade", "Humanizado"])

# 4. LÓGICA DE GERAÇÃO ESTRUTURADA
if st.button("🚀 GERAR CRONOGRAMA DE HOJE"):
    if tema:
        with st.spinner('Expert AI separando os blocos de conteúdo...'):
            model, nome_modelo = conectar_expert()
            if model:
                try:
                    # Prompt para retornar um formato que o Python consiga separar facilmente
                    prompt = (
                        f"Crie um roteiro de 5 stories para Instagram sobre '{tema}' no estilo '{estilo}'. "
                        f"Horários entre 08:00 e 19:00. Use exatamente este formato para cada um dos 5 stories:\n"
                        f"STORY_INICIO\n"
                        f"TITULO: [Horário] - [Nome Curto da Ideia]\n"
                        f"CENA: [O que filmar]\n"
                        f"SCRIPT: [O que falar]\n"
                        f"STORY_FIM"
                    )
                    response = model.generate_content(prompt)
                    texto = response.text
                    
                    # Separar o texto em uma lista de stories
                    stories = texto.split("STORY_INICIO")
                    st.session_state.roteiro_lista = [s.split("STORY_FIM")[0].strip() for s in stories if "TITULO:" in s]
                except Exception as e:
                    st.error(f"Erro: {e}")
    else:
        st.warning("Insira um tema.")

# 5. EXIBIÇÃO ORGANIZADA (UM POR UM)
if st.session_state.roteiro_lista:
    st.markdown("### 🎬 Seu Cronograma de Vendas")
    
    for i, story_txt in enumerate(st.session_state.roteiro_lista):
        # Extrair campos
        linhas = story_txt.split('\n')
        titulo = "Story " + str(i+1)
        cena = ""
        script = ""
        
        for linha in linhas:
            if "TITULO:" in linha: titulo = linha.replace("TITULO:", "").strip()
            if "CENA:" in linha: cena = linha.replace("CENA:", "").strip()
            if "SCRIPT:" in linha: script = linha.replace("SCRIPT:", "").strip()

        # Criar o Expansor (Acordeão)
        with st.expander(f"📌 {titulo}"):
            st.markdown(f'<div class="label-expert">📸 CENA / AMBIENTE:</div>', unsafe_allow_html=True)
            st.write(cena)
            st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="label-expert">🎙️ SCRIPT (O QUE FALAR):</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stBox"><span class="script-texto">"{script}"</span></div>', unsafe_allow_html=True)

    if st.button("🗑️ Limpar Tudo"):
        st.session_state.roteiro_lista = []
        st.rerun()
