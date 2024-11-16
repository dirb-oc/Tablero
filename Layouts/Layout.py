from dash import dcc, html
import plotly.graph_objs as go

def Tarjeta_Dispositivo(Dispositivo, Ubicacion, Sensores):
    nombres_sensores = ', '.join(sensor['sensor_name'] for sensor in Sensores) if Sensores else "No hay sensores"
    return html.Div([
        html.P(f"{Dispositivo['device_name']}"),
        html.P(f"Lugar: {Ubicacion.get('name_place', 'No disponible') if Ubicacion else 'No disponible'}"),
        html.P(f"Sensores: {nombres_sensores}")
    ], className='card_User', style={"padding": "20px", "border-radius": "8px", "background-color": "#f4f4f8", "width": "40%", "margin": "10px"})

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
                    data=[
                        go.Scatter(
                            x=df_sensor["time"], 
                            y=df_sensor["value"], 
                            mode="lines+markers",  # Modo línea con puntos
                            line=dict(color="#000"),  # Color de la línea
                            marker=dict(size=5, color="#1ebeee")  # Configuración de los puntos
                        )
                    ],
                    layout=go.Layout(
                        title=f"Registro de {sensor['sensor_name']} - {sensor['function']}",
                        xaxis={"title": "Time"},
                        yaxis={"title": "Value"},
                        template="plotly_white"
                    )
                ),
                style={
                    "width": "100%",
                    "padding": "10px",
                    "background-color": "#e9ecef",
                    "border-radius": "8px"
                }
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
