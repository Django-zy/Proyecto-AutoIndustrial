from taipy import Gui
import pandas as pd
from datetime import datetime
import random  # Para generar datos aleatorios

# --- Variables simuladas (en lugar de leer de la ESP32) ---
temperature = 25.0
humidity = 60.0
mode = "PI"
ref_temp = 45.0
ref_hum = 15.0
kp_temp = 2.5
ki_temp = 0.08

# DataFrame para histórico de datos (simulado)
data_history = pd.DataFrame(columns=["Time", "Temperature", "Humidity"])

# --- Funciones simuladas (no hacen requests reales) ---
def fetch_telemetry():
    # Simula datos aleatorios
    return {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(50, 70), 2),
        "controlMode": mode,
        "tempReference": ref_temp,
        "humReference": ref_hum
    }

def send_control(mode=None, temp_ref=None, hum_ref=None):
    print(f"Simulando envío de control: mode={mode}, temp_ref={temp_ref}, hum_ref={hum_ref}")
    return True  # Simula éxito

def update_config(kp, ki, umbral_alto, umbral_bajo):
    print(f"Simulando actualización de config: kp={kp}, ki={ki}")
    return True  # Simula éxito

# Actualizar estado con datos simulados
def update_state(state):
    telemetry = fetch_telemetry()  # Usa la función simulada
    state.temperature = telemetry["temperature"]
    state.humidity = telemetry["humidity"]
    
    # Actualizar histórico (simulado)
    new_data = pd.DataFrame({
        "Time": [datetime.now().strftime("%H:%M:%S")],
        "Temperature": [state.temperature],
        "Humidity": [state.humidity]
    })
    state.data_history = pd.concat([state.data_history, new_data]).tail(20)

# --- Interfaz (igual que antes) ---
page = """
# 🌡️ **Control de Planta de Secado** (Modo Simulación)

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
## 📊 **Datos Simulados**
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

# Ejecutar GUI
Gui(page).run(title="Control ESP32 (Simulación)", port=5005, dark_mode=True)