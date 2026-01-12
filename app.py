import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# 1. Configuração Única e Direta
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Estilização Premium
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 25px !important; margin-bottom: 20px !important; border-left: 6px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-weight: 800; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; line-height: 1.6; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Memória e Timer (15 Segundos)
if 'roteiro' not in st.session_state: st.session_state.roteiro = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=15)

# 4. Interface
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores")
estilo = st.selectbox("Estilo", ["Venda Direta", "Autoridade", "Humanizado"])

# 5. Execução (Sem a função 'chat', apenas geração direta)
if can_run():
    if st.button("🚀 GERAR 5 STORIES"):
        if tema:
            with st.spinner('Gerando roteiro...'):
                try:
                    prompt = f"Crie um roteiro de 5 stories para Instagram sobre {tema} no estilo {estilo}. Para cada story, descreva: HORÁRIO, CENA, JEITO DE GRAVAR e a FALA SUGERIDA."
                    # Usando generate_content (mais estável que o modo chat)
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state.roteiro = response.text
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                except Exception as e:
                    st.error("Erro na comunicação. Verifique se sua chave API está correta nos Secrets.")
        else:
            st.warning("Preencha o tema.")
else:
    rem = 15 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.info(f"⏳ Recarregando... Disponível em {rem}s")

# 6. Resultado Permanente
if st.session_state.roteiro:
    st.markdown(f"""
    <div class="stBox">
        <div class="fala-texto">{st.session_state.roteiro}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Limpar"):
        st.session_state.roteiro = None
        st.rerun()

if not can_run():
    time.sleep(1)
    st.rerun()
