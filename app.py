import streamlit as st

# Configuração da página
st.set_page_config(page_title="Gerador de Stories", page_icon="🎬")

# Estilização básica para simular o visual dark do seu código original
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .stAlert {
        background-color: #1e293b;
        border: 1px solid #334155;
    }
    </style>
    """, unsafe_allow_input_with_html=True)

def render_story_card(story):
    """Função que recria o seu StoryCard do React"""
    with st.container(border=True):
        # Header do Card
        st.markdown(f"### :blue[Story {story['id']}]")
        
        # Seção Visual
        st.markdown("**🎥 O que gravar (Visual)**")
        st.write(story['visual'])
        
        st.divider()
        
        # Seção Legenda com botão de copiar automático (st.code)
        st.markdown("**📝 O que escrever (Legenda)**")
        st.code(story['legenda'], language=None)
        
        # Seção Script (Fala)
        st.markdown("**💬 O que falar (Script)**")
        st.info(story['fala'])

# --- ÁREA DE DADOS (Exemplo) ---
# Aqui entraria a lógica que você criou com o Gemini para gerar o texto
stories_exemplo = [
    {
        "id": 1,
        "visual": "Mostre os bastidores do seu setup de trabalho.",
        "legenda": "Foco total no projeto de hoje! 🚀",
        "fala": "Bom dia pessoal! Hoje estou focado em finalizar a nova interface do app..."
    },
    {
        "id": 2,
        "visual": "Close no café ou na tela do computador.",
        "legenda": "Café + Código = ❤️",
        "fala": "Sem café a gente não produz, né? Quem mais aí é viciado?"
    }
]

# --- INTERFACE PRINCIPAL ---
st.title("🎬 Planejador de Stories")
st.subheader("Seu roteiro pronto para gravar")

# Renderizando os cards
for s in stories_exemplo:
    render_story_card(s)
