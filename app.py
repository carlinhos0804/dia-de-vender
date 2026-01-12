import streamlit as st
import google.generativeai as genai
import time
import random
from datetime import datetime, timedelta

# 1. SISTEMA DE REVEZAMENTO DE CHAVES (FAILOVER)
def obter_modelo():
    # Lista de chaves configuradas nos Secrets
    chaves = [st.secrets.get("GOOGLE_API_KEY_1"), st.secrets.get("GOOGLE_API_KEY_2")]
    # Remove chaves nulas caso você só tenha configurado uma
    chaves = [c for c in chaves if c]
    
    # Tenta as chaves em ordem aleatória para distribuir a carga
    random.shuffle(chaves)
    
    for chave in chaves:
        try:
            genai.configure(api_key=chave)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Teste rápido de conexão
            return model, "Sucesso"
        except:
            continue
    return None, "Erro"

# 2. DESIGN PREMIUM (Ouro, Verde e Preto)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #2ecc71; object-fit: cover; }
    .stBox { background-color: #111111; border-radius: 15px; padding: 25px; margin-bottom: 20px; border-left: 6px solid #f1c40f; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; border: 1px dashed #2ecc71; white-space: pre-wrap; line-height: 1.6; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; height: 3.5em !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. MEMÓRIA
if 'conteudo' not in st.session_state: st.session_state.conteudo = None
if 'last_run' not in st.session_state: st.session_state.last_run = None

def liberado():
    if st.session_state.last_run is None: return True
    return datetime.now() - st.session_state.last_run > timedelta(seconds=15)

# 4. INTERFACE
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#f1c40f;'>Expert Stories Pro</h1>", unsafe_allow_html=True)

tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores")
estilo = st.selectbox("Estilo", ["Venda Direta", "Autoridade", "Humanizado"])

# 5. EXECUÇÃO COM RODÍZIO DE CHAVES
if liberado():
    if st.button("🚀 GERAR ROTEIRO COM REVEZAMENTO"):
        if tema:
            with st.spinner('Alternando entre chaves API para evitar bloqueio...'):
                model, status = obter_modelo()
                if status == "Sucesso":
                    try:
                        prompt = f"Crie 5 stories para Instagram sobre {tema} no estilo {estilo}. Liste Horário, Cena e Fala."
                        response = model.generate_content(prompt)
                        st.session_state.conteudo = response.text
                        st.session_state.last_run = datetime.now()
                        st.rerun()
                    except Exception as e:
                        if "429" in str(e):
                            st.error("🚨 Ambas as chaves atingiram o limite. Aguarde 1 minuto.")
                        else:
                            st.error(f"Erro inesperado: {e}")
                else:
                    st.error("Nenhuma chave API configurada ou válida encontrada.")
        else:
            st.warning("Preencha o tema.")
else:
    espera = 15 - int((datetime.now() - st.session_state.last_run).total_seconds())
    st.info(f"⏳ IA em resfriamento... Disponível em {espera}s")
    time.sleep(1)
    st.rerun()

# 6. EXIBIÇÃO
if st.session_state.conteudo:
    st.markdown(f'<div class="stBox"><div class="fala-texto">{st.session_state.conteudo}</div></div>', unsafe_allow_html=True)
