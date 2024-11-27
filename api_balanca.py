from flask import Flask, jsonify
import serial
import time

app = Flask(__name__)

# Configuração da porta serial (ajuste a COM do seu Arduino, por exemplo, 'COM3' ou '/dev/ttyUSB0')
BAUD_RATE = 57600
SERIAL_TIMEOUT = 1  # Timeout para a leitura da porta serial

import os

SERIAL_PORT = os.getenv('SERIAL_PORT', 'COM3')  # Usa COM3 por padrão, mas pode ser sobreposto via variável de ambiente

# Verifica se a porta serial está configurada para algo válido
if SERIAL_PORT and SERIAL_PORT != 'COM3':
    ser = serial.Serial(SERIAL_PORT, 57600, timeout=1)
else:
    # Lógica para rodar sem a porta serial
    print("A porta serial não está disponível neste ambiente.")

# Abrir a porta serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)

@app.route("/get_weight", methods=["GET"])
def get_weight():
    # Lê o peso da porta serial
    try:
        line = ser.readline().decode('utf-8').strip()  # Lê uma linha da porta serial
        if "Peso medido" in line:
            weight = line.split(":")[1].strip()
            return jsonify({"weight": float(weight)})
        else:
            return jsonify({"error": "Não foi possível ler o peso"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
