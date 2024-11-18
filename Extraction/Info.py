from sqlalchemy import create_engine
import pandas as pd

# Configuración de la conexión a la base de datos
DATABASE_URL = "postgresql+psycopg2://orlando:2TNKEuccZQY02IV0KQxENy7sykDingap@dpg-csgsgibtq21c73dv2fm0-a.oregon-postgres.render.com:5432/mediciondb"
engine = create_engine(DATABASE_URL)

# Función para obtener ubicaciones
def obtener_ubicaciones():
    query = "SELECT * FROM locations"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

# Función para obtener dispositivos
def obtener_dispositivos():
    query = "SELECT * FROM devices"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

# Función para obtener datos de sensores
def obtener_datos():
    query = "SELECT * FROM record"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

# Función para obtener datos de usuarios
def obtener_usuarios():
    query = "SELECT * FROM users"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

# Función para obtener unidades de medida
def obtener_Medidas():
    query = "SELECT * FROM units"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

# Función para obtener sensores
def obtener_Sensores():
    query = "SELECT * FROM sensor"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

# Función para obtener relaciones
def obtener_Relacion():
    query = "SELECT * FROM user_device"
    return pd.read_sql_query(query, engine).to_dict(orient="records")

