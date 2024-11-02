import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests  # Asegúrate de importar requests

# Configuración inicial de la app de Dash
app = dash.Dash(__name__)

# Función para obtener datos de ubicación desde la API
def obtener_ubicaciones():
    url = "https://api-medicion.onrender.com/locations"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

# Función para obtener datos de los dispositivos desde la API
def obtener_dispositivos():
    url = "https://api-medicion.onrender.com/devices"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

# Función para obtener y procesar los datos de sensores
def obtener_datos():
    url = "https://api-medicion.onrender.com/records"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    return df

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard", style={"text-align": "center", "color": "#339"}),

    # Tarjetas para promedios y últimos valores
    html.Div([
        html.Div([
            html.H3("Promedio de Temperatura", style={"margin-bottom": "5px", "text-align": "center"}),
            html.P(id="temp-average", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Promedio de Humedad", style={"margin-bottom": "5px", "text-align": "center"}),
            html.P(id="hum-average", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Promedio del Aire", style={"margin-bottom": "5px", "text-align": "center"}),
            html.P(id="air_avg", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Última Temperatura Registrada", style={"margin-top": "15px", "text-align": "center"}),
            html.P(id="temp-last", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Última Humedad Registrada", style={"margin-top": "15px", "text-align": "center"}),
            html.P(id="hum-last", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Ultimo registro del Aire", style={"margin-bottom": "5px", "text-align": "center"}),
            html.P(id="air-quality", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),
        
    ], style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around", "padding": "20px"}),

    # Gráficos de temperatura, humedad y calidad del aire en barras con fondo blanco
    html.Div([
        dcc.Graph(id="temp-chart", style={"flex": "1", "padding": "10px"}),
        dcc.Graph(id="hum-chart", style={"flex": "1", "padding": "10px"}),
        dcc.Graph(id="air-quality-chart", style={"flex": "1", "padding": "10px"})
    ], style={"display": "flex", "justify-content": "space-around", "padding": "20px", "background-color": "#e9ecef", "border-radius": "8px"}),

    # Mapa de ubicación del dispositivo
    html.Div([
        dcc.Graph(id="mapa-ubicacion", style={"width": "100%", "height": "500px"})
    ], style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px"}),

    # Intervalo para actualizar datos cada 60 segundos
    dcc.Interval(id="interval-component", interval=60000, n_intervals=0)
    
], style={"font-family": "Arial, sans-serif", "background-color": "#f9f9f9", "padding": "20px"})

# Callback para actualizar gráficos, tarjetas y mapa
@app.callback(
    [
        Output("temp-chart", "figure"), Output("hum-chart", "figure"),
        Output("air-quality-chart", "figure"),  # Salida para calidad del aire
        Output("temp-average", "children"), Output("temp-last", "children"),
        Output("hum-average", "children"), Output("hum-last", "children"),
        Output("air-quality", "children"),  # Salida para calidad del aire
        Output("air_avg", "children"),
        Output("mapa-ubicacion", "figure")
    ],
    [Input("interval-component", "n_intervals")]
)
def actualizar_dashboard(n):
    # Obtener datos de sensores, dispositivos y ubicaciones
    df = obtener_datos()
    dispositivos = obtener_dispositivos()
    ubicaciones = obtener_ubicaciones()

    # Filtrar datos para temperatura, humedad y calidad del aire
    df_temp = df[df["sensor_id"] == 1]  # Temperatura
    df_hum = df[df["sensor_id"] == 2]   # Humedad
    df_air = df[df["sensor_id"] == 3]   # Calidad del aire

    # Calcular promedios y últimos valores
    temp_avg = df_temp["value"].mean() if not df_temp.empty else "N/A"
    temp_last = df_temp["value"].iloc[-1] if not df_temp.empty else "N/A"
    hum_avg = df_hum["value"].mean() if not df_hum.empty else "N/A"
    hum_last = df_hum["value"].iloc[-1] if not df_hum.empty else "N/A"
    air_avg = df_air["value"].mean() if not df_air.empty else "N/A"  # Promedio de calidad del aire
    air_quality = df_air["value"].iloc[-1] if not df_air.empty else "N/A"  # Último valor de calidad del aire

    # Configurar gráfico de temperatura en barras con fondo blanco
    fig_temp = go.Figure(
        data=[go.Bar(x=df_temp["time"], y=df_temp["value"], name="Temperatura", marker_color='red')],
        layout=go.Layout(
            title="Registro de Temperatura",
            xaxis=dict(title="Tiempo"),
            yaxis=dict(title="Temperatura (°C)"),
            plot_bgcolor='white',
            template="plotly_white"
        )
    )

    # Configurar gráfico de humedad en barras con fondo blanco
    fig_hum = go.Figure(
        data=[go.Bar(x=df_hum["time"], y=df_hum["value"], name="Humedad", marker_color='blue')],
        layout=go.Layout(
            title="Registro de Humedad",
            xaxis=dict(title="Tiempo"),
            yaxis=dict(title="Humedad (%)"),
            plot_bgcolor='white',
            template="plotly_white"
        )
    )

    # Configurar gráfico de calidad del aire en barras con fondo blanco
    fig_air_quality = go.Figure(
        data=[go.Bar(x=df_air["time"], y=df_air["value"], name="Calidad del Aire", marker_color='green')],
        layout=go.Layout(
            title="Registro de Calidad del Aire",
            xaxis=dict(title="Tiempo"),
            yaxis=dict(title="Calidad del Aire (Valor)"),
            plot_bgcolor='white',
            template="plotly_white"
        )
    )

    # Configurar mapa con ubicaciones de dispositivos
    fig_mapa = go.Figure()
    for dispositivo in dispositivos:
        ubicacion = next((u for u in ubicaciones if u["id"] == dispositivo["location_id"]), None)
        if ubicacion:
            fig_mapa.add_trace(
                go.Scattermapbox(
                    lat=[ubicacion["latitude"]],
                    lon=[ubicacion["longitude"]],
                    mode="markers+text",
                    marker=dict(size=14, color="blue"),
                    text=[dispositivo["device_name"]],  # Coloca el nombre del dispositivo como texto del marcador
                    textposition="top right"
                )
            )

    fig_mapa.update_layout(
        title="Ubicaciones de Dispositivos",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=float(ubicaciones[0]["latitude"]), lon=float(ubicaciones[0]["longitude"])),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig_temp, fig_hum, fig_air_quality, temp_avg, temp_last, hum_avg, hum_last, air_quality, air_avg, fig_mapa

# Ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Establece el puerto desde la variable de entorno
    app.run_server(host='0.0.0.0', port=port, debug=True)  # Ejecuta la app