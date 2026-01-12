import streamlit as st

def story_card(story_id, visual, legenda, fala):
    with st.container(border=True):
        st.markdown(f"**Story {story_id}**")
        
        st.caption("🎥 O que gravar (Visual)")
        st.write(visual)
        
        st.caption("📝 O que escrever (Legenda)")
        st.code(legenda, language=None) # O st.code já vem com botão de copiar!
        
        st.caption("💬 O que falar (Script)")
        st.info(fala)
        if st.button(f"Copiar Script {story_id}"):
            st.write("Copiado para o clipboard! (Simulação)")
            # Nota: Streamlit lida melhor com o st.code para cópia direta

# Exemplo de uso
story_card(
    1, 
    "Gravando o rosto falando para a câmera", 
    "Dica do dia!", 
    "Olá pessoal, hoje vou ensinar..."
)
