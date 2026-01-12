import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# 1. USANDO O MODELO EXATO DA SUA LISTA COMPATÍVEL
# Na v1beta, o identificador correto é 'models/gemini-pro'
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-pro')

# 2. DESIGN EXPERT (Preto, Verde e Amarelo)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 25px !important; margin-bottom: 20px !important; border-left: 5px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-weight: 800; font-size: 2em !important; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; line-height: 1.6; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROLE DE SESSÃO
if 'roteiro' not in st.session_state: st.session_state.roteiro = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=15)

# 4. CABEÇALHO COM SUA IDENTIDADE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. INPUTS
tema = st.text_input("Qual o tema estratégico de hoje?", placeholder="Ex: Bastidores da produção")
estilo = st.selectbox("Personalidade da IA", ["Venda Direta", "Autoridade", "Humanizado"])

# 6. EXECUÇÃO COM O MODELO DA LISTA
if can_run():
    if st.button("🚀 GERAR 5 STORIES AGORA"):
        if tema:
            with st.spinner('Acessando o modelo compatível...'):
                try:
                    # Prompt limpo para evitar erros de processamento
                    prompt = f"Crie um roteiro de 5 stories para Instagram sobre {tema} no estilo {estilo}. Para cada story, descreva: HORÁRIO, CENA, JEITO DE GRAVAR e a FALA SUGERIDA."
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state.roteiro = response.text
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro de compatibilidade: {str(e)}")
        else:
            st.warning("Insira um tema para continuar.")
else:
    rem = 15 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.info(f"⏳ Recarregando... Próximo roteiro em {rem} segundos.")

# 7. EXIBIÇÃO DOS RESULTADOS
if st.session_state.roteiro:
    st.markdown(f"""
    <div class="stBox">
        <span style="color: #f1c40f; font-weight: bold; font-size: 1.2em;">🎬 Roteiro Sugerido (Modelo Pro):</span>
        <div class="fala-texto">{st.session_state.roteiro}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Limpar e Criar Novo"):
        st.session_state.roteiro = None
        st.rerun()

# Atualização discreta do timer
if not can_run():
    time.sleep(1)
    st.rerun()
