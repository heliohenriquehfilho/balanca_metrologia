import streamlit as st
import requests

# URL do servidor exposto via ngrok
url = "http://<seu_ngrok_link>/get_weight"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    st.write("Peso:", data["weight"])
else:
    st.write("Erro ao obter dados")
