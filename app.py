import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# 1. MODELO DE ALTA DISPONIBILIDADE (O ÚNICO QUE NÃO DÁ 404)
# O sufixo '-latest' força o Google a encontrar a versão ativa mais próxima
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. DESIGN PREMIUM (Ouro, Verde e Preto)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 25px !important; margin-bottom: 20px !important; border-left: 6px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-weight: 800; font-size: 2em !important; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; line-height: 1.6; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. MEMÓRIA DO APP
if 'roteiro' not in st.session_state: st.session_state.roteiro = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=10)

# 4. CABEÇALHO
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. INPUTS
tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores da produção")
estilo = st.selectbox("Estilo", ["Venda Direta", "Autoridade", "Humanizado"])

# 6. EXECUÇÃO
if can_run():
    if st.button("🚀 GERAR AGORA"):
        if tema:
            with st.spinner('Acessando o motor Flash...'):
                try:
                    # Prompt direto e sem erros
                    prompt = f"Roteiro de 5 stories para Instagram. Tema: {tema}. Estilo: {estilo}. Liste Story 1, Story 2, Story 3, Story 4 e Story 5 com Cena e Fala."
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state.roteiro = response.text
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        else:
            st.warning("Preencha o tema.")
else:
    rem = 10 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.info(f"⏳ Recarregando em {rem}s")

# 7. EXIBIÇÃO
if st.session_state.roteiro:
    st.markdown(f"""
    <div class="stBox">
        <div class="fala-texto">{st.session_state.roteiro}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Novo Roteiro"):
        st.session_state.roteiro = None
        st.rerun()

if not can_run():
    time.sleep(1)
    st.rerun()
