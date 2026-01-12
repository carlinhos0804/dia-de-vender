import streamlit as st
import google.generativeai as genai
import json

# 1. Configuração do Modelo
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. Configuração Visual Avançada (Preto, Verde e Amarelo)
st.set_page_config(page_title="Expert Stories Pro", page_icon="🎬", layout="centered")

st.markdown(f"""
    <style>
    /* Fundo Principal em Preto Profundo */
    .stApp {{
        background-color: #000000;
        color: #ffffff;
    }}
    
    /* Container da Sua Logo/Imagem */
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: -10px;
        padding-top: 30px;
    }}
    .logo-img {{
        width: 130px;
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #2ecc71; /* Borda Verde */
        box-shadow: 0px 0px 20px rgba(46, 204, 113, 0.4);
        background-color: #111;
    }}

    /* Estilo dos Cards de Stories */
    .stBox {{
        background-color: #1a1a1a !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        margin-bottom: 25px !important;
        border-left: 6px solid #f1c40f !important; /* Detalhe Amarelo */
    }}
    
    h1 {{ 
        color: #f1c40f !important; 
        text-align: center; 
        font-size: 2.2em !important; 
        margin-bottom: 30px !important; 
        font-weight: 800 !important;
    }}
    
    /* Input de texto personalizado */
    .stTextInput>div>div>input {{
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }}

    /* Botão Verde Vibrante */
    .stButton>button {{
        width: 1
