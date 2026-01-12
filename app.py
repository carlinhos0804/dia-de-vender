import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração da API - Usando a versão 2.0 que apareceu na sua lista
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-pro')

# 2. Configuração da Página
st.set_page_config(page_title="Expert Stories 2.0", page_icon="👔", layout="wide")

# Estilo Profissional
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

st.title("👔 Gerador de Stories Profissional (Gemini 2.0)")

# 3. Interface de entrada
col1, col2 = st.columns([2, 1])
with col1:
    tema = st.text_input("Qual o tema da sequência?", placeholder="Ex: Lançamento do meu novo produto...")
with col2:
    tom_voz = st.selectbox("Tom de Voz", ["Profissional", "Direto e Comercial", "Educativo", "Inspirador"])

# 4. Botão e Lógica
if st.button("Gerar Sequência de 5 Stories"):
    if not tema:
        st.error("Por favor, digite um tema.")
    else:
        with st.spinner('O Gemini 2.0 está estruturando sua narrativa...'):
            try:
                # Prompt otimizado para as versões novas
                prompt = f"""
                Atue como um estrategista de conteúdo. Crie exatamente 5 stories para Instagram.
                Tema: {tema}
                Tom de voz: {tom_voz}
                
                Retorne APENAS um JSON puro, sem marcações markdown, neste formato:
                [
                  {{"id": 1, "visual": "descrição da cena", "legenda": "texto curto", "fala": "script detalhado"}},
                  {{"id": 2, "visual": "descrição da cena", "legenda": "texto curto", "fala": "script detalhado"}},
                  {{"id": 3, "visual": "descrição da cena", "legenda": "texto curto", "fala": "script detalhado"}},
                  {{"id": 4, "visual": "descrição da cena", "legenda": "texto curto", "fala": "script detalhado"}},
                  {{"id": 5, "visual": "descrição da cena", "legenda": "texto curto", "fala": "script detalhado"}}
                ]
                """
                
                response = model.generate_content(prompt)
                
                # Limpando a resposta para evitar erros de leitura do JSON
                texto_limpo = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(texto_limpo)

                # 5. Exibição dos Cards
                for story in stories:
                    with st.container(border=True):
                        st.subheader(f"Story {story['id']}")
                        st.markdown(f"**🎥 O que gravar:** {story['visual']}")
                        st.markdown("**📝 Legenda (Tela):**")
                        st.code(story['legenda'], language=None)
                        st.info(f"🗣️ **O que falar:** {story['fala']}")
                
                st.success("Sequência gerada com sucesso!")

            except Exception as e:
                # Tratamento amigável para erro de cota (comum nas versões novas)
                if "429" in str(e):
                    st.warning("⚠️ O Gemini 2.0 está muito requisitado agora. Aguarde 30 segundos e tente gerar novamente.")
                else:
                    st.error(f"Erro técnico: {e}")
