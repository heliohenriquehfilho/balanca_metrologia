from flask import Flask, jsonify
import serial
import time
import os

app = Flask(__name__)

BAUD_RATE = 57600
SERIAL_TIMEOUT = 1  # Timeout para a leitura da porta serial

# Verificar se a variável de ambiente 'RENDER' está configurada para o ambiente de nuvem
IS_RENDER = os.getenv("RENDER") is not None

# Configuração da porta serial - vai ser ignorada no ambiente de nuvem
SERIAL_PORT = os.getenv('SERIAL_PORT', '/dev/ttyUSB0' if not IS_RENDER else None)  # Ajuste para /dev/ttyUSB0 ou outra, se necessário

# Configuração de porta serial
ser = None

if not IS_RENDER and SERIAL_PORT:
    try:
        # Abre a porta serial apenas se não estiver no ambiente Render
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
    except Exception as e:
        print(f"Erro ao tentar abrir a porta serial: {str(e)}")
else:
    print("Ambiente de nuvem detectado, porta serial não disponível.")

@app.route("/get_weight", methods=["GET"])
def get_weight():
    if ser:
        try:
            line = ser.readline().decode('utf-8').strip()  # Lê uma linha da porta serial
            if "Peso medido" in line:
                weight = line.split(":")[1].strip()
                return jsonify({"weight": float(weight)})
            else:
                return jsonify({"error": "Não foi possível ler o peso"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "A porta serial não está disponível neste ambiente."})

if __name__ == "__main__":
    app.run(debug=True)
