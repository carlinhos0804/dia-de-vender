import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração da API - Usando a versão Lite (mais estável para cotas)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Este modelo estava na sua lista e é o que menos dá erro de 'Quota'
model = genai.GenerativeModel('models/gemini-2.0-flash-lite')

# 2. Configuração da Página
st.set_page_config(page_title="Dia de Vender - Stories", page_icon="🎬", layout="wide")

# Estilo Profissional Dark
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

st.title("🎬 Gerador de Stories Profissional")

# 3. Interface de entrada
col1, col2 = st.columns([2, 1])
with col1:
    tema = st.text_input("Qual o tema da sequência?", placeholder="Ex: Bastidores da produção...")
with col2:
    estilo = st.selectbox("Estilo do Roteiro", ["Autoridade", "Venda", "Dicas", "Inspirador"])

# 4. Lógica de Geração
if st.button("Gerar 5 Stories"):
    if not tema:
        st.error("Por favor, digite um tema.")
    else:
        with st.spinner('Criando roteiros estratégicos...'):
            try:
                prompt = f"""
                Atue como estrategista de Instagram. Crie 5 stories sobre: {tema}.
                Estilo: {estilo}.
                Responda APENAS com um JSON puro no formato:
                [
                  {{"id": 1, "visual": "cena", "legenda": "texto", "fala": "script"}}
                ]
                """
                
                response = model.generate_content(prompt)
                
                # Limpeza de segurança para o JSON
                texto = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(texto)

                for story in stories:
                    with st.container(border=True):
                        st.subheader(f"Story {story['id']}")
                        st.write(f"**🎥 Visual:** {story['visual']}")
                        st.code(story['legenda'], language=None)
                        st.info(f"🗣️ **O que falar:** {story['fala']}")
                
                st.success("Sucesso! Aguarde 30s antes de gerar o próximo para evitar bloqueios.")

            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Limite atingido. Aguarde 30 segundos. O Google limita a frequência de uso gratuito.")
                else:
                    st.error(f"Erro: {e}")
