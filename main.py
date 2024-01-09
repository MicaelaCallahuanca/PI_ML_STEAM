from fastapi import FastAPI
import os
import csv

# Asigna directamente los valores de las variables de entorno
db_host = os.environ.get("DB_HOST", "valor_por_defecto_host")
db_port = os.environ.get("DB_PORT", "valor_por_defecto_puerto")
db_user = os.environ.get("DB_USER", "valor_por_defecto_usuario")
db_password = os.environ.get("DB_PASSWORD", "valor_por_defecto_contraseña")
csv_file_path = os.environ.get("CSV_FILE_PATH", "valor_por_defecto_ruta_csv")

app = FastAPI()

# Obtiene la ubicación del archivo CSV desde las variables de entorno
nombre_archivo_csv = csv_file_path

# Verifica si la variable de entorno está configurada
if not nombre_archivo_csv:
    raise Exception("La variable de entorno CSV_FILE_PATH no está configurada.")

def cargar_datos_desde_csv(nombre_archivo):
    datos = []
    with open(nombre_archivo, newline='') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        for fila in lector_csv:
            datos.append(fila)
    return datos

@app.get("/")
def index():
    return {"detail": "Hello, World!!"}

'''
def obtener_nombres(datos):
    return [persona['Nombre'] for persona in datos]

def obtener_personas_mayores(datos, edad_minima):
    return [persona for persona in datos if int(persona['Edad']) >= edad_minima]

def obtener_personas_por_ciudad(datos, ciudad):
    return [persona for persona in datos if persona['Ciudad'].lower() == ciudad.lower()]

# Rutas FastAPI
@app.get("/nombres", response_model=List[str])
def obtener_nombres_api():
    return obtener_nombres(datos)

@app.get("/personas-mayores/{edad_minima}", response_model=List[dict])
def obtener_personas_mayores_api(edad_minima: int):
    return obtener_personas_mayores(datos, edad_minima)

@app.get("/personas-por-ciudad/{ciudad}", response_model=List[dict])
def obtener_personas_por_ciudad_api(ciudad: str):
    return obtener_personas_por_ciudad(datos, ciudad)
'''