import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração com o modelo que FUNCIONOU para você
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Design Premium (Preto, Verde e Amarelo)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .logo-container { display: flex; justify-content: center; padding-top: 20px; }
    .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #2ecc71; box-shadow: 0px 0px 15px rgba(46,204,113,0.3); }
    .stBox { background-color: #111111 !important; border-radius: 15px !important; padding: 20px !important; margin-bottom: 20px !important; border-left: 5px solid #f1c40f !important; border-top: 1px solid #222 !important; }
    h1 { color: #f1c40f !important; text-align: center; font-size: 1.8em !important; font-weight: 800; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important; color: white !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; height: 3.5em !important; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 20px rgba(46, 204, 113, 0.4); }
    .horario-tag { color: #f1c40f; font-weight: bold; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .fala-texto { background-color: #0d1a12; color: #2ecc71; padding: 15px; border-radius: 10px; font-style: italic; line-height: 1.5; border: 1px dashed #2ecc71; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    /* Ajuste dos inputs */
    .stTextInput>div>div>input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho com sua imagem
URL_LOGO = "https://i.postimg.cc/v1zDLM9S/image.png" 
st.markdown(f'<div class="logo-container"><img src="{URL_LOGO}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("Story Expert")

# 4. Interface de Entrada
tema = st.text_input("Qual o tema de hoje?", placeholder="Ex: Lançamento do novo serviço")
estilo = st.selectbox("Personalidade do Roteiro", ["Venda Direta", "Autoridade", "Bastidores", "Educativo"])

# 5. Lógica de Geração
if st.button("GERAR ESTRATÉGIA COMPLETA"):
    if tema:
        with st.spinner('IA gerando cronograma...'):
            try:
                # Prompt focado em extrair apenas o necessário para evitar erros de cota
                prompt = f"""
                Crie um cronograma de 5 stories para Instagram sobre: {tema}. 
                Estilo: {estilo}.
                Distribua em horários comerciais (08:00 às 20:00).
                Retorne APENAS um JSON no formato:
                [
                  {{"horario": "00:00", "cena": "...", "jeito": "...", "fala": "..."}}
                ]
                """
                response = model.generate_content(prompt)
                
                # Limpeza de resposta (Remover markdown se houver)
                res_text = response.text.strip()
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0].strip()
                elif "```" in res_text:
                    res_text = res_text.split("```")[1].split("```")[0].strip()
                
                stories = json.loads(res_text)

                for s in stories:
                    st.markdown(f"""
                    <div class="stBox">
                        <span class="horario-tag">⌚ Postar às: {s['horario']}</span>
                        <p style="margin-bottom:8px;"><b>🎬 Cena:</b> {s['cena']}</p>
                        <p style="margin-bottom:15px;"><b>🤳 Gravação:</b> {s['jeito']}</p>
                        <p style="color:#f1c40f; font-size:0.8em; font-weight:bold; margin-bottom:5px;">SCRIPT DE FALA:</p>
                        <div class="fala-texto">"{s['fala']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.success("Estratégia pronta para gravar!")

            except Exception as e:
                # Se der erro de cota, explicamos de forma amigável
                if "429" in str(e):
                    st.error("O Google está respirando... Aguarde 30 segundos e clique novamente no botão.")
                else:
                    st.error(f"Ocorreu um ajuste necessário. Tente novamente. (Erro: {e})")
    else:
        st.warning("Por favor, digite o tema para começar.")
