from taipy import Gui
import pandas as pd
from datetime import datetime
import random

# --- Variables simuladas ---
temperature = 25.0
humidity = 60.0
mode = "PID"
ref_temp = 45.0
ref_hum = 15.0
kp_temp = 2.5
ki_temp = 0.08
emergency_stop = False  # Nuevo estado para parada de emergencia

# DataFrame para histórico
data_history = pd.DataFrame(columns=["Time", "Temperature", "Humidity"])

# --- Funciones modificadas ---
def fetch_telemetry():
    if emergency_stop:
        return {  # Valores seguros cuando está parado
            "temperature": 0.0,
            "humidity": 0.0,
            "controlMode": "STOP",
            "tempReference": 0.0,
            "humReference": 0.0
        }
    return {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(50, 70), 2),
        "controlMode": mode,
        "tempReference": ref_temp,
        "humReference": ref_hum
    }

def trigger_emergency_stop(state):
    state.emergency_stop = not state.emergency_stop  # Alternar estado
    print(f"🚨 PARADA DE EMERGENCIA {'ACTIVADA' if state.emergency_stop else 'DESACTIVADA'}")

def update_state(state):
    telemetry = fetch_telemetry()
    state.temperature = telemetry["temperature"]
    state.humidity = telemetry["humidity"]
    
    new_data = pd.DataFrame({
        "Time": [datetime.now().strftime("%H:%M:%S")],
        "Temperature": [state.temperature],
        "Humidity": [state.humidity]
    })
    state.data_history = pd.concat([state.data_history, new_data]).tail(20)

# --- Interfaz actualizada ---
page = """
# 🌡️ **Control de Planta de Secado**

<|layout|columns=1 2 2|
<|
## 🔧 **Control**
<|{mode}|selector|lov=PID;CAL;IDENT|on_change=send_control|label=Modo|>

**Referencias:**
<|{ref_temp}|number|on_change=send_control|label=Temperatura (°C)|>
<|{ref_hum}|number|on_change=send_control|label=Humedad (%)|>

<|Actualizar Parámetros|button|on_action=update_config|>
|>
<|
## 📊 **Datos**
**Estado:** <|{"🟢 NORMAL" if not emergency_stop else "🔴 DETENIDO"}|>

**Temperatura:** <|{temperature}|> °C  
**Humedad:** <|{humidity}|> %  

<|{data_history}|chart|type=line|x=Time|y[1]=Temperature|y[2]=Humidity|height=300px|>
|>

<|
## ⚙️ **Configuración**
<|{kp_temp}|number|label=Kp (Temperatura)|>
<|{ki_temp}|number|label=Ki (Temperatura)|>

## **Umbrales Humedad:**
<|25.0|number|label=Alto (%)|variable=umbral_alto|>
<|15.0|number|label=Bajo (%)|variable=umbral_bajo|>

### 🚨 **Parada de Emergencia**
<|{emergency_stop}|button|on_action=trigger_emergency_stop|label=ACTIVAR/DESACTIVAR|active={not emergency_stop}|>
|>
|>
"""

Gui(page).run(title="Control ESP32", port=5005, dark_mode=True)