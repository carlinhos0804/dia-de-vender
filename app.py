import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração do Modelo
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Configuração Visual (Vermelho e Branco Degradê)
st.set_page_config(page_title="Story Pro - Cronograma", page_icon="⏰", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #ff4b4b 0%, #ffffff 100%);
        color: #1e1e1e;
    }
    .stBox {
        background-color: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 20px !important;
        border-left: 8px solid #ff4b4b !important;
    }
    h1, h2, h3 { color: #ffffff !important; }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 3.5em !important;
    }
    .horario-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
        margin-bottom: 10px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Cronograma de Stories Diário")

# 3. Interface de Entrada
col1, col2 = st.columns([2, 1])
with col1:
    tema = st.text_input("Qual o foco do dia na loja?", placeholder="Ex: Promoção de Verão ou Chegada de Novidades...")
with col2:
    estilo = st.selectbox("Estilo do Roteiro", ["Venda Direta", "Bastidores/Humanizado", "Educativo", "Autoridade"])

# 4. Lógica de Geração com Horários e 3 Pilares
if st.button("Gerar Cronograma do Dia"):
    if not tema:
        st.error("Por favor, digite o foco do dia.")
    else:
        with st.spinner('Mapeando horários e roteiros...'):
            try:
                prompt = f"""
                Atue como um estrategista de marketing de varejo. 
                Crie um cronograma de 5 stories para um dia inteiro de loja sobre: {tema}.
                Estilo: {estilo}.
                
                Distribua os stories em horários estratégicos (Ex: 08:30, 11:00, 14:30, 18:00, 21:00).
                
                Para cada story, forneça:
                1. HORÁRIO: Horário sugerido para postagem.
                2. CENA: Descrição visual.
                3. JEITO DE GRAVAR: Técnica/Ângulo.
                4. PROMPT DE FALA: Texto para falar.

                Responda APENAS com um JSON puro:
                [
                  {{
                    "horario": "00:00",
                    "cena": "...",
                    "jeito": "...",
                    "fala": "..."
                  }}
                ]
                """
                
                response = model.generate_content(prompt)
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(res_text)

                # 5. Exibição dos Cards em Linha do Tempo
                for i, s in enumerate(stories):
                    with st.container():
                        st.markdown(f"""
                        <div class="stBox">
                            <div class="horario-badge">⏰ Sugestão de Postagem: {s['horario']}</div>
                            <h3 style="color:#333 !important; margin-top:10px;">Story {i+1}</h3>
                            <p><b>🎬 1. CENA:</b> {s['cena']}</p>
                            <p><b>🤳 2. JEITO DE GRAVAR:</b> {s['jeito']}</p>
                            <p><b>💬 3. PROMPT DE FALA:</b></p>
                            <div style="background-color:#fff5f5; padding:15px; border-radius:8px; border-left: 3px solid #ff4b4b;">
                                <i>"{s['fala']}"</i>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.success("Cronograma pronto! Siga os horários para melhor engajamento.")

            except Exception as e:
                st.error(f"Erro ao gerar cronograma: {e}")
