import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime, timedelta

# 1. Configuração do Modelo
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# 2. Design Premium
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; box-shadow: 0px 0px 15px rgba(46,204,113,0.3); }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 20px !important; margin-bottom: 20px !important; border-left: 6px solid #f1c40f !important; }
    h1 { color: #f1c40f !important; text-align: center; font-size: 1.8em !important; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em !important; }
    .stButton>button:disabled { background: #333 !important; color: #777 !important; }
    .horario-tag { color: #f1c40f; font-weight: bold; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; line-height: 1.5; border: 1px dashed #2ecc71; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Gerenciamento de Memória
if 'last_run' not in st.session_state:
    st.session_state.last_run = None

def can_run():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=40)

# 4. Cabeçalho
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Expert Stories Pro")

# 5. Entradas
tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores da Loja")
estilo = st.selectbox("Estilo", ["Venda Direta", "Autoridade", "Humanizado"])

# 6. GERAÇÃO "FORÇA BRUTA"
if can_run():
    if st.button("🚀 GERAR ROTEIRO AGORA"):
        if tema:
            with st.spinner('A IA está preparando tudo...'):
                try:
                    # Prompt que obriga a resposta a ser simples
                    prompt = f"Crie 3 stories para Instagram sobre {tema} no estilo {estilo}. Use este formato exato para cada story: HORARIO: texto, CENA: texto, JEITO: texto, FALA: texto."
                    
                    response = model.generate_content(prompt)
                    
                    if not response.text:
                        st.error("O Google não liberou essa resposta. Tente mudar um pouco as palavras do tema.")
                    else:
                        conteudo = response.text
                        st.session_state.last_run = datetime.now()
                        
                        # Tenta mostrar como cards, se falhar, mostra o texto puro
                        try:
                            # Se a IA mandou em blocos de texto, vamos apenas exibir
                            st.markdown(f"""
                            <div class="stBox">
                                <span class="horario-tag">🎬 Roteiro Gerado</span>
                                <div style="white-space: pre-wrap;">{conteudo}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        except:
                            st.write(conteudo)
                except Exception as e:
                    st.error("Aguarde o contador terminar para tentar novamente.")
                    st.session_state.last_run = datetime.now()
        else:
            st.warning("Preencha o tema.")
else:
    rem = 40 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.button(f"⏳ RECARREGANDO EM {rem}s", disabled=True)
    time.sleep(1)
    st.rerun()
