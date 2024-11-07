from Extraction.Info import *
from datetime import datetime

# Promedio de registros para un sensor específico
def promedio_registro(registros, id):
    registros_sensor = registros[registros["sensor_id"] == id]["value"]
    # Calcular el promedio si hay registros
    if not registros_sensor.empty:
        promedio = registros_sensor.mean()
        return promedio
    else:
        return 0
    
# Último registro de un sensor específico
def ultimo_registro(registros, id):
    registros_sensor = registros[registros["sensor_id"] == id]
    # Encontrar el último registro en base al campo 'time'
    if not registros_sensor.empty:
        ultimo = registros_sensor.loc[registros_sensor["time"].idxmax()]["value"]
        return ultimo
    else:
        return 0