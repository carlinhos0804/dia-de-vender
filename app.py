import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração da API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. Configuração da Página
st.set_page_config(page_title="Expert Stories - Business", page_icon="👔", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 8px; background-color: #3b82f6; 
        color: white; font-weight: bold; height: 3em;
    }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("👔 Gerador de Roteiros Profissionais")

# 3. Interface
col1, col2 = st.columns([2, 1])
with col1:
    tema = st.text_input("Qual o tema da sequência?", placeholder="Ex: Benefícios do meu produto...")
with col2:
    tom_voz = st.selectbox("Tom de Voz", ["Profissional", "Educativo", "Comercial", "Inspirador"])

if st.button("Gerar Sequência"):
    if not tema:
        st.error("Por favor, digite um tema.")
    else:
        with st.spinner('Gerando roteiros...'):
            try:
                prompt = f"""
                Crie 5 stories para Instagram sobre: {tema}.
                Tom: {tom_voz}.
                Responda APENAS com um JSON no formato:
                [
                  {{"id": 1, "visual": "cena", "legenda": "texto", "fala": "script"}}
                ]
                """
                response = model.generate_content(prompt)
                json_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(json_text)

                for story in stories:
                    with st.container(border=True):
                        st.subheader(f"Story {story['id']}")
                        st.write(f"**🎥 Visual:** {story['visual']}")
                        st.code(story['legenda'], language=None)
                        st.info(f"🗣️ **Fala:** {story['fala']}")
                
                st.success("Pronto! Agora é só gravar.")

            except Exception as e:
                if "429" in str(e):
                    st.error("🚨 Limite de uso atingido. Aguarde 30 segundos.")
                else:
                    st.error(f"Erro: {e}")
