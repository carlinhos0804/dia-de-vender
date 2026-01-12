import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime, timedelta

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

# 2. DESIGN PREMIUM E LIMPEZA DE MENU (REMOÇÃO DO GITHUB/HEADER)
st.set_page_config(page_title="Expert Stories Pro", layout="centered")
st.markdown("""
    <style>
    /* Esconde o Header (GitHub/Menu) e o Footer (Made with Streamlit) */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    .stApp { background-color: #000000; color: #ffffff; }
    .stBox { background-color: #0d1a12; border: 1px dashed #2ecc71; padding: 15px; border-radius: 10px; }
    .label-expert { color: #2ecc71; font-weight: bold; font-size: 0.9em; text-transform: uppercase; margin-bottom: 5px; }
    .script-texto { color: #ffffff; font-style: italic; line-height: 1.6; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em; margin-top: 20px; }
    .timer-aviso { text-align: center; color: #f1c40f; font-weight: bold; padding: 10px; border: 1px solid #f1c40f; border-radius: 10px; margin-top: 20px; background-color: rgba(241, 196, 15, 0.1); }
    h1 { text-align: center; color: #f1c40f; font-weight: 800; }
    
    /* Ajuste para o expansor ficar discreto no modo escuro */
    .streamlit-expanderHeader { background-color: #111111 !important; border-radius: 10px !important; border-left: 5px solid #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROLE DE SESSÃO
if 'last_run_time' not in st.session_state: st.session_state.last_run_time = None
if 'roteiro_lista' not in st.session_state: st.session_state.roteiro_lista = []

def tempo_espera_restante():
    if st.session_state.last_run_time is None: return 0
    passado = (datetime.now() - st.session_state.last_run_time).total_seconds()
    restante = 20 - passado
    return int(restante) if restante > 0 else 0

# 4. INTERFACE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div style="text-align:center;"><img src="{URL_LOGO}" width="100" style="border-radius:50%; border:3px solid #2ecc71;"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

tema = st.text_input("Qual o foco das vendas de hoje?", placeholder="Ex: Queima de estoque")
estilo = st.selectbox("Personalidade da IA", ["Venda Direta", "Autoridade", "Humanizado"])

espera = tempo_espera_restante()

# 5. LÓGICA DO BOTÃO
if espera > 0:
    st.markdown(f'<div class="timer-aviso">⏳ Aguarde {espera}s para gerar novas ideias...</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.rerun()
else:
    if st.button("🚀 GERAR CRONOGRAMA DE HOJE"):
        if tema:
            with st.spinner('Expert AI processando...'):
                model, nome_modelo = conectar_expert()
                if model:
                    try:
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
                        stories = response.text.split("STORY_INICIO")
                        st.session_state.roteiro_lista = [s.split("STORY_FIM")[0].strip() for s in stories if "TITULO:" in s]
                        st.session_state.last_run_time = datetime.now()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
        else:
            st.warning("Insira um tema.")

# 6. EXIBIÇÃO ORGANIZADA
if st.session_state.roteiro_lista:
    st.markdown("---")
    for i, story_txt in enumerate(st.session_state.roteiro_lista):
        linhas = story_txt.split('\n')
        titulo, cena, script = f"Story {i+1}", "", ""
        for linha in linhas:
            if "TITULO:" in linha: titulo = linha.replace("TITULO:", "").strip()
            if "CENA:" in linha: cena = linha.replace("CENA:", "").strip()
            if "SCRIPT:" in linha: script = linha.replace("SCRIPT:", "").strip()

        with st.expander(f"📌 {titulo}"):
            st.markdown('<div class="label-expert">📸 CENA:</div>', unsafe_allow_html=True)
            st.write(cena)
            st.markdown('<div class="label-expert" style="margin-top:10px;">🎙️ SCRIPT:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stBox"><span class="script-texto">"{script}"</span></div>', unsafe_allow_html=True)

    if st.button("🗑️ Limpar e Criar Novo"):
        st.session_state.roteiro_lista = []
        st.session_state.last_run_time = None 
        st.rerun()
