# PI MLops

---

## Introducción

En este proyecto armé un sistema de recomendación de videojuegos para usuarios, para la plataforma multinacional de videojuegos Steam. Trabaje con tres archivos JSON anidados, donde se tiene que desanidar para poder leerlo correctamente y luego poder pasar al ETL(Extracción, Transformación, Carga) y EDA (Análisis Exploratorio de Datos). Dichos archivos los podes encontrar en la carpeta [dataset](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/tree/main/datasets) junto con un [diccionario de datos](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/datasets/Diccionario%20de%20Datos%20STEAM.xlsx)

## Proceso

1. **ETL  (Extracción, Transformación, Carga):**
En esta etapa se extrae los archivos JSON y los convertimos en CSV. Se desanida las columnas y elimina las que no son requeridas para el sistema de recomendación y endopoints. También se tratan los nulos, duplicados y valores faltantes. Una vez realizado este proceso se obtiene tres CSV limpios, dichos archivos se mergean en uno llamado [dataframe_final.csv](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/dataframe_final.csv)
Pueden ver el paso a paso en el [proceso de ETL](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/ETL.ipynb)

2. **Feature Engineering:**
Se creó la columna "Sentiment_analysis" aplicando análisis de sentimiento a las reseña de usuarios usando la librería textblob, dando como asignación: '0' si es una reseña negativa, '1' si es neutral y '2' si es positiva. La nueva columna reemplaza la columna review de user_reviews
Pueden observar el paso a paso en el mismo notebook del [ETL](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/ETL.ipynb)

3. **Funciones de consultas:**
Se realizaron funciones en un archivo [main.py](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/main.py). Se creó una API, usando el módulo FastApi de python, para que pudieran ser consultadas:

- def PlayTimeGenre( genero : str ): Debe devolver año con más horas jugadas para dicho género.

Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

- def UserForGenre( genero : str ): Debe devolver usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

- def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

- def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

- def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
Ejemplo de retorno: {'Valve' : [Negativo = 182, Neutro = 120, Positivo = 278]}

4. **API:**
Se usó una API, FastApi, para exponer las funciones de consultas (los endpoints). Luego se hizo el [deployement de la API en Render](https://pi-ml-steam-oc2n.onrender.com/docs). El código se encuentra en el archivo [main.py](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/main.py)

5. **EDA:**
Se realizó un Análisis Explotorio de Datos (EDA) donde se exploró y examinó el conjunto de datos [EDA](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/EDA.ipynb)

6. **Sistema de recomendación:**
Creé el sistema de recomendación item-item, éste se ubica en el archivo [main.py](https://github.com/MicaelaCallahuanca/PI_ML_STEAM/blob/main/main.py)

7. **Video:**
[Video explicativo del proyecto](), donde se detalla el uso de los endpoints desplegados en Render
