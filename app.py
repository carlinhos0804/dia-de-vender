import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DO MODELO MAIS COMPATÍVEL DA HISTÓRIA
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Usando o ID técnico completo para evitar erro de "modelo não encontrado"
model = genai.GenerativeModel('models/gemini-1.0-pro')

# Configuração de segurança para evitar que a IA trave por "conteúdo sensível" (comum no 1.0)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# 2. DESIGN (Preto, Verde e Amarelo)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; box-shadow: 0px 0px 15px rgba(46,204,113,0.3); }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 25px !important; margin-bottom: 20px !important; border-left: 6px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-size: 1.8em !important; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em !important; }
    .stButton>button:disabled { background: #333 !important; color: #777 !important; border: 1px solid #444 !important; }
    .horario-tag { color: #f1c40f; font-weight: bold; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; line-height: 1.5; border: 1px dashed #2ecc71; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. GERENCIAMENTO DO TIMER
if 'last_run' not in st.session_state:
    st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=30)

# 4. CABEÇALHO
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Story Expert")

# 5. INPUTS
tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores da Loja")
estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado", "Dicas"])

# 6. GERAÇÃO SEM MODO CHAT
if can_run():
    if st.button("🚀 GERAR ESTRATÉGIA AGORA"):
        if tema:
            with st.spinner('IA gerando roteiro...'):
                try:
                    prompt = f"Crie um roteiro de 5 stories sobre {tema}, estilo {estilo}. Responda APENAS com um JSON puro no formato: [{{'horario': '...', 'cena': '...', 'jeito': '...', 'fala': '...'}}]"
                    
                    # Chamada com configurações de segurança para não travar
                    response = model.generate_content(prompt, safety_settings=safety_settings)
                    
                    res_text = response.text.strip()
                    if "```json" in res_text:
                        res_text = res_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in res_text:
                        res_text = res_text.split("```")[1].split("```")[0].strip()
                    
                    stories = json.loads(res_text)
                    st.session_state.last_run = datetime.now()

                    for s in stories:
                        st.markdown(f"""
                        <div class="stBox">
                            <span class="horario-tag">⌚ Postar às: {s['horario']}</span>
                            <p><b>🎬 Cena:</b> {s['cena']}</p>
                            <p><b>🤳 Gravação:</b> {s['jeito']}</p>
                            <div class="fala-texto">"{s['fala']}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro no modelo 1.0: {e}. Verifique se o tema não possui palavras proibidas.")
        else:
            st.warning("Preencha o tema.")
else:
    rem = 30 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.button(f"⏳ AGUARDE {rem}s", disabled=True)
    time.sleep(1)
    st.rerun()
