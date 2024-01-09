from fastapi import FastAPI
import pandas as pd
import os
import csv

# Asigna directamente los valores de las variables de entorno
db_host = os.environ.get("DB_HOST", "valor_por_defecto_host")
db_port = os.environ.get("DB_PORT", "valor_por_defecto_puerto")
db_user = os.environ.get("DB_USER", "valor_por_defecto_usuario")
db_password = os.environ.get("DB_PASSWORD", "valor_por_defecto_contraseña")
csv_file_path = os.environ.get("CSV_FILE_PATH", "valor_por_defecto_ruta_csv")

app = FastAPI()

df = pd.read_csv('dataframe_final.csv')

'''
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
'''

@app.get("/")
def index():
    return {"detail": "Hello, World!"}


@app.get('/PlayTimeGenre/')
def PlayTimeGenre(genero: str) -> dict:
    # método capitalize, capitaliza el género para asegurar consistencia en el formato.
    genero = genero.capitalize()

    # Filtra el DataFrame para incluir solo las filas con el género especificado.
    df_genero = df[df[genero] == 1]
    
    # Verifica si no hay datos disponibles para el género especificado.
    if df_genero.empty:
        return {"error": f"No hay datos disponibles para el género '{genero}'."}

    # Agrupa el DataFrame filtrado por 'year' y calcula la suma de 'playtime_forever' para cada año.
    year_df_playtime = df_genero.groupby('year')['playtime_forever'].sum().reset_index()

    # Verifica si no hay datos de tiempo de juego para el género especificado.
    if year_df_playtime.empty:
        return {"error": f"No hay datos de tiempo de juego para el género '{genero}'."}

    # Encuentra el año con el tiempo de juego total máximo.
    max_playtime_year = year_df_playtime.loc[year_df_playtime['playtime_forever'].idxmax(), 'year']

    # Devuelve la respuesta en el formato especificado.
    return {"Año de lanzamiento con más horas jugadas para Género": int(max_playtime_year)}



@app.get('/UserForGenre/')
def UserForGenre(genero: str) -> dict:
    # Convierte la primera letra del género a mayúscula
    genero = genero.capitalize()
    
    # Filtra el DataFrame para obtener solo las filas con el género especificado
    df_genero = df[df[genero] == 1]
    
    # Encuentra el usuario con más horas jugadas en ese género
    usuario_max_horas = df_genero.loc[df_genero['playtime_forever'].idxmax(), 'user_id']
    
    # Calcula la suma del tiempo jugado por año para ese género
    df_tiempo_juego_anio = df_genero.groupby('year')['playtime_forever'].sum().reset_index()

    # Renombra las columnas para que coincidan con lo esperado
    df_tiempo_juego_anio = df_tiempo_juego_anio.rename(columns={'year': 'anio', 'playtime_forever': 'horas'})
    
    # Convierte el DataFrame a una lista de diccionarios con orientación 'records'
    lista_tiempo_juego = df_tiempo_juego_anio.to_dict(orient='records')
    
    # Crear un diccionario con la información del usuario con más horas jugadas y la lista de horas jugadas por año
    resultado = {
        "Usuario con más horas jugadas para el género " + genero: usuario_max_horas,
        "Horas jugadas": lista_tiempo_juego
    }
    
    # Devuelve el diccionario como resultado de la función
    return resultado



@app.get('/UsersRecommend/')
def UsersRecommend(anio: int):
    # Filtra el DataFrame para obtener juegos recomendados y comentarios positivos/neutrales para el año dado
    df_filtrado = df[(df['year'] == anio) & (df['recommend'] == True) & (df['review'].isin([1, 2]))]

    # Verifica si no se encontraron resultados
    if df_filtrado.empty:
        return {"error": 'No se encontraron juegos recomendados para el año dado'}

    # Ordena el DataFrame por la columna 'review' de manera descendente
    df_ordenado = df_filtrado.sort_values(by='review', ascending=False)

    # Toma los primeros 3 juegos del DataFrame ordenado
    top_3_resenias = df_ordenado.head(3)

    # Crea el resultado en el formato deseado
    resultado = [
        {"Puesto 1": top_3_resenias.iloc[0]['title']},
        {"Puesto 2": top_3_resenias.iloc[1]['title']},
        {"Puesto 3": top_3_resenias.iloc[2]['title']}
    ]

    # Devuelve el resultado como una lista de diccionarios
    return resultado


@app.get('/UsersWorstDeveloper/')
def UsersWorstDeveloper(anio:int):
    # Filtra el DataFrame 
    df_filtrado = df[(df['year'] == anio) & (df['recommend'] == False) & (df['review'] == 0)]
    
    if df_filtrado.empty:
        return {"error": 'No hay datos disponibles para el año y condiciones especificadas'}
    
    # Calcula el puntaje para cada desarrolladora
    puntajes = []
    for desarrolladora, grupo in df_filtrado.groupby('developer'):
        total_negativos = len(grupo)
        puntajes.append({"nombre": desarrolladora, "puntaje": total_negativos})

    # Ordena desarrolladoras por puntaje
    desarrolladoras_ordenadas = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)

    # Da el top 3
    top_3 = [{"Puesto " + str(i + 1): desarrolladora["nombre"]} for i, desarrolladora in enumerate(desarrolladoras_ordenadas[:3])]

    return top_3


@app.get('/sentiment_analysis/')
def sentiment_analysis(empresa_desarrolladora:str):
    # Filtra el DataFrame por empresa desarrolladora
    df_empresa = df[df['developer'] == empresa_desarrolladora]

    # Cuenta la cantidad de reseñas por cada categoría de sentimiento
    counts = df_empresa['review'].value_counts()
    negativas = counts.get(0, 0)
    neutrales = counts.get(1, 0)
    positivas = counts.get(2, 0)

    # Crea el diccionario de retorno con el nombre de la desarrolladora y los resultados del análisis de sentimiento
    resultado = {empresa_desarrolladora: [f"Negative = {negativas}", f"Neutral = {neutrales}", f"Positive = {positivas}"]}

    return resultado

