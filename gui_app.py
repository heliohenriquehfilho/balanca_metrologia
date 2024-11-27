import streamlit as st
import requests
import pandas as pd
import time

# Configuração da API Flask
API_URL = "https://balanca-metrologia.onrender.com"  # URL da API Flask
REFRESH_INTERVAL = 5  # Intervalo de atualização (segundos)

# Inicializar o estado da aplicação
if "weights" not in st.session_state:
    st.session_state["weights"] = []  # Lista para registrar os pesos medidos
    st.session_state["timestamps"] = []  # Lista para os horários das medições

# Função para buscar o peso da API Flask
def get_weight_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return float(response.json()["weight"])
        else:
            st.error("Erro ao obter o peso. Verifique a API.")
            return None
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")
        return None

# Título da aplicação
st.title("Sistema de Medição de Peso - Online")

# Medição de peso
current_weight = get_weight_from_api()

if current_weight is not None:
    st.metric(label="Peso Atual (g)", value=f"{current_weight:.2f}")
    # Adicionar o peso e o timestamp à lista
    st.session_state["weights"].append(current_weight)
    st.session_state["timestamps"].append(time.strftime("%H:%M:%S"))

# Exibir gráfico
st.header("Histórico de Pesos")
if st.session_state["weights"]:
    df = pd.DataFrame({
        "Horário": st.session_state["timestamps"],
        "Peso (g)": st.session_state["weights"],
    })
    st.line_chart(df.set_index("Horário"))

# Botão para reiniciar os dados
if st.button("Reiniciar Dados"):
    st.session_state["weights"] = []
    st.session_state["timestamps"] = []

# Atualização automática da página
st.write(f"Atualizando em {REFRESH_INTERVAL} segundos...")
time.sleep(REFRESH_INTERVAL)
st.rerun()