import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração do Modelo (O que funcionou!)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Configuração Visual (Vermelho e Branco Degradê)
st.set_page_config(page_title="Story Pro", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    /* Fundo em degradê vermelho para branco */
    .stApp {
        background: linear-gradient(180deg, #ff4b4b 0%, #ffffff 100%);
        color: #1e1e1e;
    }
    
    /* Personalização dos Cards */
    .stBox {
        background-color: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 20px !important;
        border-left: 5px solid #ff4b4b !important;
    }
    
    /* Títulos e Textos */
    h1, h2, h3 { color: #ffffff !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
    .stMarkdown { color: #333333; }
    
    /* Botão Vermelho */
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        height: 3.5em !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Gerador de Stories Profissionais")

# 3. Interface de Entrada
col1, col2 = st.columns([2, 1])
with col1:
    tema = st.text_input("Qual o tema dos Stories?", placeholder="Ex: Bastidores da nova coleção...")
with col2:
    estilo = st.selectbox("Estilo do Roteiro", ["Autoridade", "Venda Direta", "Educativo", "Inspirador"])

# 4. Lógica de Geração com os 3 Pilares
if st.button("Gerar 5 Ideias de Stories"):
    if not tema:
        st.error("Por favor, digite um tema.")
    else:
        with st.spinner('Construindo seus roteiros...'):
            try:
                # Prompt focado nos 3 pilares específicos
                prompt = f"""
                Atue como um estrategista de vídeo. Crie 5 ideias de stories sobre: {tema}.
                Estilo: {estilo}.
                
                Para cada story, você deve obrigatoriamente fornecer:
                1. CENA: O que está acontecendo visualmente.
                2. JEITO DE GRAVAR: Ângulo da câmera, movimento ou técnica.
                3. PROMPT DE FALA: O roteiro exato do que deve ser dito.

                Responda APENAS com um JSON puro neste formato:
                [
                  {{
                    "id": 1,
                    "cena": "descrição da cena",
                    "jeito": "como posicionar a câmera/gravar",
                    "fala": "o que dizer"
                  }}
                ]
                """
                
                response = model.generate_content(prompt)
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(res_text)

                # 5. Exibição dos Cards com os 3 Pilares
                for s in stories:
                    with st.container():
                        st.markdown(f"""
                        <div class="stBox">
                            <h3 style="color:#ff4b4b !important;">STORY {s['id']}</h3>
                            <p><b>🎬 1. CENA:</b> {s['cena']}</p>
                            <p><b>🤳 2. JEITO DE GRAVAR:</b> {s['jeito']}</p>
                            <p><b>💬 3. PROMPT DE FALA:</b></p>
                            <div style="background-color:#f9f9f9; padding:10px; border-radius:5px; border: 1px solid #eee;">
                                <i>"{s['fala']}"</i>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.success("Roteiros gerados! Aguarde 30s para a próxima geração.")

            except Exception as e:
                st.error(f"Erro ao gerar: {e}")
