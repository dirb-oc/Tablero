from dash import dcc, html

Contenido = html.Div([
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
