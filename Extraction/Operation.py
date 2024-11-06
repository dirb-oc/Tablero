from Extraction.Info import *
from datetime import datetime

def promedio_registro(registros, id):
    registros_sensor = [registro["value"] for registro in registros if registro["sensor_id"] == id]
    
    if registros_sensor:
        promedio = sum(registros_sensor) / len(registros_sensor)
        return promedio
    else:
        return 0
    
def ultimo_registro(registros, id):
    # Filtrar los registros del sensor específico
    registros_sensor = [registro for registro in registros if registro["sensor_id"] == id]
    
    # Si hay registros, encontrar el último basándose en el campo 'time'
    if registros_sensor:
        ultimo = max(registros_sensor, key=lambda x: datetime.fromisoformat(x["time"].replace("Z", "")))
        return ultimo["value"]
    else:
        return 0