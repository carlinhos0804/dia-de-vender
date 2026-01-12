import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração do Modelo
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Configuração Visual (Estilo Premium sem cara de código)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    /* Fundo Preto */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Logo Centralizada */
    .logo-container {
        display: flex;
        justify-content: center;
        padding-top: 20px;
    }
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #2ecc71;
        box-shadow: 0px 0px 15px rgba(46, 204, 113, 0.3);
    }

    /* Cards Elegantes */
    .stBox {
        background-color: #111111 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        border: 1px solid #222 !important;
        border-left: 5px solid #f1c40f !important;
    }
    
    h1 { color: #f1c40f !important; text-align: center; font-size: 1.8em !important; }
    
    /* Botão sem bordas técnicas */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        height: 3.5em !important;
        font-size: 16px !important;
    }

    .horario-tag {
        color: #f1c40f;
        font-weight: bold;
        font-size: 0.9em;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: block;
    }

    .fala-texto {
        background-color: #0d1a12;
        color: #2ecc71;
        padding: 15px;
        border-radius: 8px;
        font-style: italic;
        line-height: 1.5;
        border-left: 2px solid #2ecc71;
    }

    /* Esconder elementos desnecessários do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f"""
    <div class="logo-container">
        <img src="{URL_LOGO}" class="logo-img" onerror="this.src='https://cdn-icons-png.flaticon.com/512/149/149071.png'">
    </div>
    """, unsafe_allow_html=True)

st.title("Story Expert")

# 4. Entrada simples
tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Bastidores da Loja")
estilo = st.selectbox("Estilo", ["Venda", "Autoridade", "Bastidores", "Dicas"])

if st.button("GERAR ROTEIRO DO DIA"):
    if tema:
        with st.spinner('Criando estratégia...'):
            try:
                prompt = f"Crie 5 stories para Instagram sobre {tema} no estilo {estilo}. Sugira horários. Retorne JSON com: horario, cena, jeito, fala."
                response = model.generate_content(prompt)
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(res_text)

                for s in stories:
                    st.markdown(f"""
                    <div class="stBox">
                        <span class="horario-tag">⏰ Sugestão: {s['horario']}</span>
                        <p style="margin-bottom:8px;"><b>🎬 Cena:</b> {s['cena']}</p>
                        <p style="margin-bottom:15px;"><b>🤳 Como gravar:</b> {s['jeito']}</p>
                        <p style="color:#f1c40f; font-size:0.8em; font-weight:bold; margin-bottom:5px;">O QUE FALAR:</p>
                        <div class="fala-texto">
                            "{s['fala']}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                st.error("Erro ao gerar. Tente novamente em alguns segundos.")
    else:
        st.warning("Coloque um tema primeiro.")
