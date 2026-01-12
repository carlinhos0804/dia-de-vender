import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração da API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Usando o modelo flash para velocidade, ou 'gemini-1.5-pro' para mais qualidade
model = genai.GenerativeModel('gemini-pro')

# 2. Configuração da Página
st.set_page_config(page_title="Expert Stories - Business", page_icon="👔", layout="wide")

# CSS Personalizado para um look mais Profissional
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #3b82f6; 
        color: white; 
        font-weight: bold;
        height: 3em;
    }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("👔 Gerador de Roteiros Profissionais")
st.write("Crie sequências estratégicas de stories para fortalecer sua autoridade.")

# 3. Entradas do Usuário em Colunas
col1, col2 = st.columns([2, 1])

with col1:
    tema = st.text_input("Qual o tema ou objetivo da sequência?", placeholder="Ex: Lançamento de consultoria, Quebra de objeção sobre preço...")

with col2:
    tom_voz = st.selectbox("Tom de Voz", ["Profissional e Autoritário", "Educativo e Calmo", "Direto e Comercial", "Inspirador"])

if st.button("Gerar Sequência de 5+ Stories"):
    if not tema:
        st.error("Por favor, descreva o tema para prosseguir.")
    else:
        with st.spinner('A IA está estruturando sua narrativa estratégica...'):
            try:
                # Prompt Refinado para Profissionalismo e Quantidade
                prompt = f"""
                Atue como um estrategista de conteúdo para Instagram. 
                Crie uma sequência de no MÍNIMO 5 stories sobre: {tema}.
                O tom de voz deve ser: {tom_voz}.
                
                Estruture a sequência para que tenha:
                1. Gancho de atenção (Hook)
                2. Desenvolvimento do problema/solução
                3. Prova social ou autoridade
                4. Quebra de objeção
                5. Chamada para ação clara (CTA)

                Responda APENAS com um JSON no formato abaixo:
                [
                  {{"id": 1, "visual": "descrição da cena", "legenda": "texto curto para tela", "fala": "script detalhado"}},
                  ...
                ]
                """
                
                response = model.generate_content(prompt)
                
                # Limpeza de Markdown do JSON
                clean_text = response.text.replace('```json', '').replace('```', '').strip()
                stories = json.loads(clean_text)

                # 4. Exibição em Grid (Opcional: 1 por linha para foco)
                for story in stories:
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 4])
                        with c1:
                            st.markdown(f"## 🎬 {story['id']}")
                        with c2:
                            st.caption("📸 VISUAL RECOMENDADO")
                            st.write(story['visual'])
                            
                            st.caption("✍️ LEGENDA (TELA)")
                            st.code(story['legenda'], language=None)
                            
                            st.caption("🗣️ SCRIPT DE FALA")
                            st.info(story['fala'])
                
                st.success(f"Sequência de {len(stories)} stories gerada com sucesso!")

            except Exception as e:
                st.error(f"Ocorreu um erro na geração. Verifique sua chave de API ou tente novamente. Erro: {e}")
