import dash
import os
from dash import html, dcc
from Layouts.Layout import Tarjeta, Grafica, Mapa
from dash.dependencies import Input, Output
from Extraction.Info import *
from Extraction.Operation import *
import pandas as pd

# Datos
sensores = obtener_Sensores()
unidades = obtener_Medidas()
dispositivos = obtener_dispositivos()
ubicaciones = obtener_ubicaciones()

# Crear un diccionario de unidades para acceder rápidamente a la descripción
unidad_dict = {unidad["id"]: unidad["description"] for unidad in unidades}

# Inicializar la app de Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id="interval-component", interval=10000, n_intervals=0),
    
    # Sección para tarjetas
    html.Div(id="tarjeta-section", style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around", "padding": "20px"}),
    
    # Sección para gráficos
    html.Div(id="grafico-section", style={"padding": "20px"}),

    html.Div(id="mapa-section", style={"padding": "20px"})
])

# Callback para actualizar el tablero
@app.callback(
    [Output("tarjeta-section", "children"),
     Output("grafico-section", "children"),
     Output("mapa-section", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n_intervals):
    registros = obtener_datos()
    if isinstance(registros, list):
        df = pd.DataFrame(registros) 

    tarjetas = []
    graficos = []
    for sensor in sensores:
        # Calcular el promedio y el último valor
        promedio = promedio_registro(registros, sensor["id"])
        ultimo = ultimo_registro(registros, sensor["id"])
        
        # Tarjeta para cada sensor
        tarjetas.append(Tarjeta(f"{sensor['sensor_name']} - {sensor['function']}", promedio, ultimo))

        # Filtrar registros específicos para el gráfico del sensor actual
        registros_sensor = df[df["sensor_id"] == sensor["id"]]
        
        # Grafico por sensor
        graficos.append(html.Div(Grafica(registros_sensor, sensor), style={"margin-bottom": "20px"}))

        mapa = dcc.Graph(
            figure=Mapa(dispositivos, ubicaciones),
        style={"width": "100%", "padding": "10px", "background-color": "#e9ecef", "border-radius": "8px"}
    )

    # Devolver tarjetas y gráficos a sus secciones respectivas
    return tarjetas, graficos, mapa

# Ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Establece el puerto desde la variable de entorno
    app.run_server(host='0.0.0.0', port=port, debug=True)  # Ejecuta la app
