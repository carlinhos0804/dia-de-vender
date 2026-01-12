import streamlit as st
import google.generativeai as genai
import json
import time

# 1. Configuração da API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Trocamos para o 1.5-flash que tem limites de uso gratuito maiores
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. Configuração da Página
st.set_page_config(page_title="Expert Stories - Business", page_icon="👔", layout="wide")

# CSS para visual Dark e Profissional
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 8px; background-color: #3b82f6; 
        color: white; font-weight: bold; height: 3em;
    }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; border: 1px solid #334155; }
    [data-testid="stMetricValue"] { color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("👔 Gerador de Roteiros Profissionais")
st.write("Crie sequências estratégicas de no mínimo 5 stories.")

# 3. Interface de Entrada
col1, col2 = st.columns([2, 1])

with col1:
    tema = st.text_input("Qual o tema ou objetivo da sequência?", placeholder="Ex: Por que meu serviço é exclusivo...")

with col2:
    tom_voz = st.selectbox("Tom de Voz", ["Profissional e Autoritário", "Educativo e Calmo", "Direto e Comercial", "Inspirador"])

# 4. Lógica de Geração
if st.button("Gerar Sequência Estratégica"):
    if not tema:
        st.error("Por favor, descreva o tema.")
    else:
        with st.spinner('O Gemini está estruturando sua narrativa...'):
            try:
                prompt = f"""
                Atue como um estrategista de conteúdo. Crie uma sequência de no MÍNIMO 5 stories sobre: {tema}.
                Tom de voz: {tom_voz}.
                Estrutura: Gancho, Problema, Autoridade, Objeção e CTA.
                Responda APENAS com um JSON puro (sem markdown) no formato:
                [
                  {{"id": 1, "visual": "cena", "legenda": "texto", "fala": "script"}},
                  ...
                ]
                """
                
                response = model.generate_content(prompt)
                # Limpeza para garantir que o JSON seja lido corretamente
                clean_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(clean_text)

                # 5. Exibição dos Stories
                for story in stories:
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 5])
                        with c1:
                            st.subheader(f"#{story['id']}")
                        with c2:
                            st.markdown(f"**🎥 Visual:** {story['visual']}")
                            st.markdown("**📝 Legenda (Copie abaixo):**")
                            st.code(story['legenda'], language=None)
                            st.info(f"🗣️ **O que falar:** {story['fala']}")
                
                st.success("Pronto! Agora é só gravar.")

           except Exception as e:
    if "429" in str(e):
        st.error("🚨 Limite de uso atingido! Aguarde 30 segundos e tente novamente. O Google limita a quantidade de gerações gratuitas por minuto.")
    else:
        st.error(f"Erro ao processar: {e}")
