import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração Direta
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Usando o item 20 da sua lista (O mais estável de todos)
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Interface Simples e Profissional
st.set_page_config(page_title="Gerador de Stories", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { width: 100%; background-color: #3b82f6; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Gerador de Stories")

col1, col2 = st.columns([2, 1])
with col1:
    tema = st.text_input("Tema da sequência:", placeholder="Sobre o que quer falar?")
with col2:
    estilo = st.selectbox("Estilo:", ["Profissional", "Venda", "Educativo", "Inspirador"])

if st.button("Gerar 5 Stories"):
    if not tema:
        st.error("Digite um tema.")
    else:
        with st.spinner('Gerando...'):
            try:
                # Prompt simplificado para evitar erros de processamento
                prompt = f"Crie 5 stories sobre {tema} no estilo {estilo}. Responda apenas com um JSON: [{{'id': 1, 'visual': '...', 'legenda': '...', 'fala': '...'}}]"
                
                response = model.generate_content(prompt)
                
                # Tratamento robusto do texto
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(res_text)

                for story in stories:
                    with st.container(border=True):
                        st.subheader(f"Story {story['id']}")
                        st.write(f"**🎥 Cena:** {story['visual']}")
                        st.code(story['legenda'], language=None)
                        st.info(f"🗣️ **Fala:** {story['fala']}")
                
                st.success("Gerado com sucesso!")

            except Exception as e:
                st.error(f"Erro: {e}")
