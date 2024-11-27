import streamlit as st
import requests
import pandas as pd
import time

# Configuração da API Flask
API_URL = "http://localhost:5000/dados"  # URL da API Flask
REFRESH_INTERVAL = 3  # Intervalo de atualização (segundos)

# Inicializar o estado da aplicação
if "weights" not in st.session_state:
    st.session_state["weights"] = []  # Lista para registrar os pesos medidos
    st.session_state["timestamps"] = []  # Lista para os horários das medições

# Função para buscar o peso da API Flask
def get_weight_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weight = float(data["valor"])  # "valor" é a chave retornada pela API
            return weight
        else:
            st.error(f"Erro ao obter o peso (status {response.status_code}). Verifique a API.")
            return None
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")
        return None

# Título da aplicação
st.title("Sistema de Medição de Peso - Online")

# Medição de peso
current_weight = get_weight_from_api()

if current_weight is not None:
    if current_weight == 0.0:
        st.warning("Balança em processo de recalibração. Por favor, aguarde.")
    else:
        st.metric(label="Peso Atual (g)", value=f"{current_weight:.3f}")  # Três casas decimais
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
    st.rerun()  # Reinicia a página para refletir a mudança

# Atualização automática da página
with st.empty():
    for seconds in range(REFRESH_INTERVAL, 0, -1):
        st.write(f"Atualizando em {seconds} segundos...")
        time.sleep(1)
    st.rerun()
