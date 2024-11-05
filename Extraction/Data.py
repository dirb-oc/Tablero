import requests
import pandas as pd

def obtener_ubicaciones():
    url = "https://api-medicion.onrender.com/locations"
    data = requests.get(url)
    return data.json() if data.status_code == 200 else []

# Función para obtener datos de los dispositivos desde la API
def obtener_dispositivos():
    url = "https://api-medicion.onrender.com/devices"
    data = requests.get(url)
    return data.json() if data.status_code == 200 else []

# Función para obtener y procesar los datos de sensores
def obtener_datos():
    url = "https://api-medicion.onrender.com/records"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    return df

# Función para obtener datos de usuarios
def obtener_usuarios():
    url = "https://api-medicion.onrender.com/users"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def obtener_Medidas():
    url = "https://api-medicion.onrender.com/units"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def obtener_Sensores():
    url = "https://api-medicion.onrender.com/sensors"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def obtener_Relacion():
    url = "https://api-medicion.onrender.com/relations"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []