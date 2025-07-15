from taipy import Gui
import requests
import pandas as pd
from datetime import datetime

# Configuración de la ESP32 (reemplaza con tu IP local)
ESP32_IP = "192.168.1.100"  # Ejemplo: "192.168.1.150"
API_BASE = f"http://{ESP32_IP}/api/v1"

# Variables de estado
temperature = 0.0
humidity = 0.0
mode = "PI"
ref_temp = 45.0
ref_hum = 15.0
kp_temp = 2.5
ki_temp = 0.08

# DataFrame para histórico de datos
data_history = pd.DataFrame(columns=["Time", "Temperature", "Humidity"])

# Función para obtener datos de telemetría
def fetch_telemetry():
    try:
        response = requests.get(f"{API_BASE}/telemetry", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None

# Función para enviar comandos de control
def send_control(mode=None, temp_ref=None, hum_ref=None):
    payload = {}
    if mode: payload["mode"] = mode
    if temp_ref: payload["temp_ref"] = temp_ref
    if hum_ref: payload["hum_ref"] = hum_ref
    
    try:
        response = requests.post(
            f"{API_BASE}/control",
            json=payload,
            timeout=3
        )
        return response.status_code == 200
    except:
        return False

# Función para actualizar parámetros de control
def update_config(kp, ki, umbral_alto, umbral_bajo):
    payload = {
        "kp_temp": kp,
        "ki_temp": ki,
        "umbral_alto": umbral_alto,
        "umbral_bajo": umbral_bajo
    }
    try:
        response = requests.post(
            f"{API_BASE}/config",
            json=payload,
            timeout=3
        )
        return response.status_code == 200
    except:
        return False

# Actualizar datos periódicamente
def update_state(state):
    telemetry = fetch_telemetry()
    if telemetry:
        state.temperature = telemetry["temperature"]
        state.humidity = telemetry["humidity"]
        state.mode = telemetry["controlMode"]
        state.ref_temp = telemetry["tempReference"]
        state.ref_hum = telemetry["humReference"]
        
        # Actualizar histórico
        new_data = pd.DataFrame({
            "Time": [datetime.now().strftime("%H:%M:%S")],
            "Temperature": [state.temperature],
            "Humidity": [state.humidity]
        })
        state.data_history = pd.concat([state.data_history, new_data]).tail(20)

# Definición de la interfaz
page = """
# 🌡️ **Control de Planta de Secado** (ESP32-S3)

<|layout|columns=1 2 2|
<|
## 🔧 **Control**
<|{mode}|selector|lov=PI;CAL;IDENT|on_change=send_control|label=Modo|>

**Referencias:**
<|{ref_temp}|number|on_change=send_control|label=Temperatura (°C)|>
<|{ref_hum}|number|on_change=send_control|label=Humedad (%)|>

<|Actualizar Parámetros|button|on_action=update_config|>
|>

<|
## 📊 **Datos en Tiempo Real**
**Temperatura:** <|{temperature}|> °C  
**Humedad:** <|{humidity}|> %  

<|{data_history}|chart|type=line|x=Time|y[1]=Temperature|y[2]=Humidity|height=300px|>
|>

<|
## ⚙️ **Configuración PI**
<|{kp_temp}|number|label=Kp (Temperatura)|>
<|{ki_temp}|number|label=Ki (Temperatura)|>

**Umbrales Humedad:**
<|25.0|number|label=Alto (%)|variable=umbral_alto|>
<|15.0|number|label=Bajo (%)|variable=umbral_bajo|>
|>
|>
"""

# Crear y ejecutar GUI
gui = Gui(page)
gui.run(title="Control ESP32", port=5005, dark_mode=True)