from dash import dcc, html
import plotly.graph_objs as go

def Tarjeta(titulo, promedio, ultimo_valor):
    return html.Div([
        html.H3(titulo),
        html.P(f"Promedio: {promedio}"),
        html.P(f"Último Registro: {ultimo_valor}"),
    ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"})

def Grafica(df_sensor, sensor):
    return html.Div(
        [
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Bar(x=df_sensor["time"], y=df_sensor["value"], marker_color="#2596be")],
                    layout=go.Layout(
                        title=f"Registro de {sensor['sensor_name']} - {sensor['function']}",
                        xaxis={"title": "Time"},
                        yaxis={"title": "Value"},
                        template="plotly_white"
                    )
                ),
                style={"width": "100%", "padding": "10px", "background-color": "#e9ecef", "border-radius": "8px"}
            )
        ],
        style={"margin-bottom": "20px"}  # Estilo para el espaciado entre gráficos
    )

 
def Mapa(dispositivos, ubicaciones):
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
                    text=[dispositivo["device_name"]],
                    textposition="top right"
                )
            )
    
    # Configuración del layout del mapa
    fig_mapa.update_layout(
        title="Ubicaciones de Dispositivos",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=float(ubicaciones[0]["latitude"]), lon=float(ubicaciones[0]["longitude"])),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig_mapa

Contenido = html.Div([
    html.H1("Dashboard", style={"text-align": "center", "color": "#339"}),

    # Tarjetas para promedios y últimos valores
    html.Div([
        html.Div([
            html.H3("Promedio de Temperatura", style={"margin-bottom": "5px", "text-align": "center"}),
            html.P(id="temp-average", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px","border-radius": "8px","background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

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
            html.H3("Última Calidad del Aire", style={"margin-bottom": "5px", "text-align": "center"}),
            html.P(id="air-quality", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

    ], style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around", "padding": "20px"}),

    # Gráficos de temperatura, humedad y calidad del aire (uno debajo del otro)
    dcc.Graph(id="temp-chart", style={"width": "100%", "padding": "10px", "background-color": "#e9ecef", "border-radius": "8px"}),
    dcc.Graph(id="hum-chart", style={"width": "100%", "padding": "10px", "background-color": "#e9ecef", "border-radius": "8px"}),
    dcc.Graph(id="air-quality-chart", style={"width": "100%", "padding": "10px", "background-color": "#e9ecef", "border-radius": "8px"}),

    # Mapa de ubicación del dispositivo
    html.Div([
        dcc.Graph(id="mapa-ubicacion", style={"width": "100%", "height": "500px"})
    ], style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px"}),

    # Tarjetas de cantidad de dispositivos, registros y usuarios
    html.Div([
        html.Div([
            html.H3("Cantidad de Dispositivos", style={"margin-top": "15px", "text-align": "center"}),
            html.P(id="device-count", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Cantidad de Registros", style={"margin-top": "15px", "text-align": "center"}),
            html.P(id="record-count", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

        html.Div([
            html.H3("Cantidad de Usuarios", style={"margin-top": "15px", "text-align": "center"}),
            html.P(id="user-count", style={"font-size": "36px", "font-weight": "bold", "text-align": "center"}),
        ], className="card", style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "30%", "margin": "10px"}),

    ], style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around", "padding": "20px"}),

    # Intervalo para actualizar datos cada 60 segundos
    dcc.Interval(id="interval-component", interval=60000, n_intervals=0)

], style={"font-family": "Arial, sans-serif", "background-color": "#f9f9f9", "padding": "20px"})
