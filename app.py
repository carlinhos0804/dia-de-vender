import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DO MOTOR (Foco total em 1.5-flash)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. DESIGN PREMIUM (Ouro, Verde e Preto)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 25px !important; margin-bottom: 20px !important; border-left: 6px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-weight: 800; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. MEMÓRIA SIMPLIFICADA
if 'roteiro_final' not in st.session_state: st.session_state.roteiro_final = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=15)

# 4. CABEÇALHO
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. INPUTS
tema = st.text_input("Sobre o que vamos postar hoje?", placeholder="Ex: Bastidores, Oferta Irresistível...")
estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado"])

# 6. LÓGICA DE SUCESSO ABSOLUTO
if can_run():
    if st.button("🚀 GERAR ROTEIRO AGORA"):
        if tema:
            with st.spinner('A IA está escrevendo sua estratégia...'):
                try:
                    # Pedimos o roteiro de forma clara e sem frescura técnica
                    prompt = f"Crie um roteiro de 5 stories para Instagram sobre {tema} no estilo {estilo}. Para cada story, descreva: HORÁRIO, CENA, JEITO DE GRAVAR e a FALA SUGERIDA. Seja criativo e direto."
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state.roteiro_final = response.text
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                except Exception:
                    st.error("Erro na conexão com o Google. Verifique sua chave API ou o tema.")
        else:
            st.warning("Preencha o tema.")
else:
    rem = 15 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.info(f"⏳ IA descansando... Disponível em {rem} segundos.")

# 7. EXIBIÇÃO (Sempre funciona!)
if st.session_state.roteiro_final:
    st.markdown(f"""
    <div class="stBox">
        <span style="color: #f1c40f; font-weight: bold; font-size: 1.2em;">🎬 Seu Roteiro Personalizado:</span>
        <hr style="border: 0.5px solid #333;">
        <div class="fala-texto">{st.session_state.roteiro_final}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Limpar e Criar Outro"):
        st.session_state.roteiro_final = None
        st.rerun()

if not can_run():
    time.sleep(1)
    st.rerun()
