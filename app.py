import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração do Modelo
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Configuração Visual (Corrigida para evitar SyntaxError)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: -10px;
        padding-top: 30px;
    }
    .logo-img {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #2ecc71;
        box-shadow: 0px 0px 20px rgba(46, 204, 113, 0.4);
        background-color: #111;
    }
    .stBox {
        background-color: #1a1a1a !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        margin-bottom: 25px !important;
        border-left: 6px solid #f1c40f !important;
    }
    h1 { 
        color: #f1c40f !important; 
        text-align: center; 
        font-size: 2.2em !important; 
        font-weight: 800 !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: none !important;
        height: 4em !important;
    }
    .horario-badge {
        background-color: #f1c40f;
        color: #000;
        padding: 6px 18px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
    }
    .fala-container {
        background: #0d2116; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px dashed #2ecc71;
        color: #2ecc71;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho com Sua Imagem
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 

st.markdown(f"""
    <div class="logo-container">
        <img src="{URL_LOGO}" class="logo-img" onerror="this.src='https://cdn-icons-png.flaticon.com/512/149/149071.png'">
    </div>
    """, unsafe_allow_html=True)

st.title("Story Expert - Black & Gold")

# 4. Interface
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        tema = st.text_input("Qual o objetivo de hoje?", placeholder="Ex: Venda de mentoria...")
    with col2:
        estilo = st.selectbox("Personalidade", ["Venda Direta", "Autoridade", "Humanizado", "Curiosidade"])

# 5. Lógica de Geração
if st.button("Gerar Cronograma Estratégico"):
    if not tema:
        st.warning("Por favor, preencha o tema.")
    else:
        with st.spinner('Processando...'):
            try:
                prompt = f"Crie um cronograma de 5 stories sobre: {tema}. Estilo: {estilo}. Distribua em horários comerciais. Retorne um JSON puro com: horario, cena, jeito, fala."
                response = model.generate_content(prompt)
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(res_text)

                for s in stories:
                    st.markdown(f"""
                    <div class="stBox">
                        <div class="horario-badge">⌚ {s['horario']}</div>
                        <p style="margin-top:15px; color: #eee;"><b>🎬 CENA:</b> {s['cena']}</p>
                        <p style="color: #eee;"><b>🤳 GRAVAÇÃO:</b> {s['jeito']}</p>
                        <hr style="border: 0.5px solid #333">
                        <p style="color:#f1c40f; font-weight:bold; margin-bottom:10px;">🗣️ O QUE FALAR:</p>
                        <div class="fala-container">
                            <i>"{s['fala']}"</i>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.success("Roteiro finalizado!")
            except Exception as e:
                st.error(f"Erro: {e}")
