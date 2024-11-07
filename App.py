import dash, os
from dash import html, dcc
from dash.dependencies import Input, Output
from Layouts.Layout import *
from Extraction.Info import *
from Extraction.Operation import *
import pandas as pd

# Datos obtenidos de las funciones
usuarios = obtener_usuarios()
dispositivos = obtener_dispositivos()
ubicaciones = obtener_ubicaciones()
sensores = obtener_Sensores()
relaciones = obtener_Relacion()
datos = obtener_datos()

# Crear un mapeo de `sensor_id` a `device_id`
sensor_device_map = {sensor["id"]: sensor["device_id"] for sensor in sensores}

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Layout principal de la aplicación
app.layout = html.Div([
    dcc.Dropdown(
        id="user-dropdown",
        options=[{"label": f"{user['name']} {user['secondname']}", "value": user["id"]} for user in usuarios],
        placeholder="Selecciona un usuario",
        style={"width": "50%", "margin": "20px auto", "margin-bottom": "0px"}
    ),
    dcc.Interval(id="interval-component", interval=30000, n_intervals=0),

    # Secciones para usuario, tarjetas, gráficos y mapas
    html.Div(id="usuario-section", style={"display": "flex", "justify-content": "space-around", "padding": "20px"}),
    html.Div(id="tarjeta-section", style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around", "padding": "20px"}),
    html.Div(id="grafico-section", style={"padding": "20px"}),
    html.Div(id="mapa-section", style={"padding": "20px"})
])

# Callback para actualizar el tablero basado en el usuario seleccionado
@app.callback(
    [Output("usuario-section", "children"),
     Output("tarjeta-section", "children"),
     Output("grafico-section", "children"),
     Output("mapa-section", "children")],
    [Input("user-dropdown", "value"),
     Input("interval-component", "n_intervals")]
)
def update_dashboard(selected_user_id, n_intervals):
    if selected_user_id is None:
        return ["Seleccione un usuario para ver sus datos"], [], [], []

    # Filtrar relaciones para obtener dispositivos del usuario seleccionado
    user_devices = [rel["device_id"] for rel in relaciones if rel["user_id"] == selected_user_id]

    # Crear sección de usuario
    usuario_info = []

    # Filtrar datos para dispositivos del usuario
    df_datos = pd.DataFrame(datos)
    df_datos["device_id"] = df_datos["sensor_id"].map(sensor_device_map)
    df_datos_user = df_datos[df_datos["device_id"].isin(user_devices)]

    # Crear tarjetas y gráficos basados en dispositivos
    tarjetas = []
    graficos = []
    
    # Filtrar dispositivos y ubicaciones para el usuario
    dispositivos_usuario = [d for d in dispositivos if d["id"] in user_devices]
    ubicaciones_usuario = [loc for loc in ubicaciones if loc["id"] in [d["location_id"] for d in dispositivos_usuario]]
    
    # Generar mapa con todos los dispositivos del usuario en un solo gráfico
    mapa = dcc.Graph(
        figure=Mapa(dispositivos_usuario, ubicaciones_usuario),
        style={"width": "100%", "padding": "10px", "background-color": "#e9ecef", "border-radius": "8px"}
    )

    # Generar tarjetas y gráficos para cada dispositivo
    for device in dispositivos_usuario:
        location = next((loc for loc in ubicaciones_usuario if loc["id"] == device["location_id"]), None)
        device_sensors = [s for s in sensores if s["device_id"] == device["id"]]

        # Generar tarjeta para cada dispositivo
        usuario_info.append(Tarjeta_Dispositivo(device, location, device_sensors))

        # Gráfico para cada sensor del dispositivo
        for sensor in device_sensors:
            sensor_data = df_datos_user[df_datos_user["sensor_id"] == sensor["id"]]
            if not sensor_data.empty:
                promedio = promedio_registro(sensor_data, sensor["id"])
                ultimo = ultimo_registro(sensor_data, sensor["id"])
                tarjetas.append(Tarjeta(f"{sensor['sensor_name']} - {sensor['function']}", promedio, ultimo))
                graficos.append(html.Div(Grafica(sensor_data, sensor), style={"margin-bottom": "20px"}))

    return usuario_info, tarjetas, graficos, [mapa]


# Ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host='0.0.0.0', port=port, debug=True)
