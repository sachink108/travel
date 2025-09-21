import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAPI"]["OPENAI_API_KEY"])  # Create a client instance
