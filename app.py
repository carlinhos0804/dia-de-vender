import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime, timedelta

# 1. O MOTOR MAIS CONSISTENTE
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. DESIGN PREMIUM (Ouro, Verde e Preto)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; box-shadow: 0px 0px 15px rgba(46,204,113,0.3); }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 20px !important; margin-bottom: 20px !important; border-left: 5px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-size: 1.8em !important; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em !important; }
    .stButton>button:disabled { background: #333 !important; color: #777 !important; }
    .horario-tag { color: #f1c40f; font-weight: bold; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; line-height: 1.5; border: 1px dashed #2ecc71; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. GERENCIAMENTO DE REQUISIÇÃO (30s)
if 'last_run' not in st.session_state:
    st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=30)

# 4. IDENTIDADE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. INPUTS
tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores da Loja")
estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado"])

# 6. EXECUÇÃO DE SUCESSO
if can_run():
    if st.button("🚀 GERAR 5 STORIES AGORA"):
        if tema:
            with st.spinner('A IA está gerando suas 5 ideias...'):
                try:
                    # Prompt estruturado para 5 blocos exatos
                    prompt = f"Crie 5 stories para Instagram sobre {tema} no estilo {estilo}. Responda apenas um JSON: [{{'horario': '...', 'cena': '...', 'jeito': '...', 'fala': '...'}}]"
                    
                    response = model.generate_content(prompt)
                    res_text = response.text.strip()
                    
                    # Limpeza agressiva de formato
                    if "```json" in res_text:
                        res_text = res_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in res_text:
                        res_text = res_text.split("```")[1].split("```")[0].strip()
                    
                    stories = json.loads(res_text)
                    st.session_state.last_run = datetime.now()

                    for s in stories:
                        st.markdown(f"""
                        <div class="stBox">
                            <span class="horario-tag">⌚ {s.get('horario', 'Sugerido')}</span>
                            <p><b>🎬 Cena:</b> {s.get('cena', '...')}</p>
                            <p><b>🤳 Gravação:</b> {s.get('jeito', '...')}</p>
                            <div class="fala-texto">"{s.get('fala', '...')}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.rerun()
                except Exception as e:
                    st.error("Aguarde o contador de segurança para nova tentativa.")
                    st.session_state.last_run = datetime.now()
        else:
            st.warning("Preencha o tema.")
else:
    rem = 30 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.button(f"⏳ RECARREGANDO EM {rem}s", disabled=True)
    time.sleep(1)
    st.rerun()
