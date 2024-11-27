from flask import Flask, jsonify
import serial

app = Flask(__name__)

# Configuração da porta serial
PORTA = "COM3"
BAUDRATE = 57600

try:
    arduino = serial.Serial(PORTA, BAUDRATE, timeout=1)
except Exception as e:
    arduino = None

@app.route("/dados", methods=["GET"])
def dados():
    if arduino:
        linha = arduino.readline().decode("utf-8").strip()
        return jsonify({"valor": linha})
    else:
        return jsonify({"erro": "Arduino não conectado"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
