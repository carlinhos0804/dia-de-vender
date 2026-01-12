with st.spinner('O Gemini está estruturando sua narrativa...'):
            try:
                # ... (todo o seu código de geração do prompt e json.loads)
                
                for story in stories:
                    with st.container(border=True):
                        # ... (código de exibição dos stories)
                
                st.success("Pronto! Agora é só gravar.")

            except Exception as e:  # ESTA LINHA DEVE ESTAR ALINHADA COM O 'try' ACIMA
                if "429" in str(e):
                    st.error("🚨 Limite atingido! Aguarde 30 segundos.")
                else:
                    st.error(f"Erro ao processar: {e}")
