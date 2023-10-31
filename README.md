![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)


# MVP PROYECTO DE STEAM GAMES - API Y MODELO DE RECOMENDACION

## Introducción

Este proyecto esta basado en datos de la plataforma reconocida de videojuegos Steam. La tarea consiste en trabajar con un conjunto de datos proporcionados para crear un Producto Mínimo Viable (MVP). Este MVP debe demostrar una API desplegada en un servicio en la nube(en este caso AZURE) y la implementación de dos modelos de Machine Learning. Dichos modelos abordarán dos objetivos principales: un modelo para analizar los sentimientos expresados en los comentarios de los usuarios de los juegos y otro modelo para sugerir juegos basados en la entrada del nombre de un juego y un usuario y respectivamente; cada salida entrega cinco recomendaciones basadas en un usuario o en un juego según la entrada de la API.

## Datos Iniciales

Para este proyecto se proporcionaron tres archivos JSON:

* australian_user_reviews.json representa un conjunto de datos que incluye opiniones de los usuarios acerca de los juegos que consumen. Además, contiene información adicional como la recomendación del juego, emoticones de humor, y estadísticas sobre la utilidad de los comentarios para otros usuarios. También proporciona el ID del usuario que comenta con su URL de perfil y el ID del juego sobre el que comenta.

* australian_users_items.json contiene datos que detallan los juegos jugados por todos los usuarios, junto con el tiempo total que cada usuario ha dedicado a un juego específico.

* output_steam_games.json es un archivo que engloba información relacionada con los propios juegos, tales como títulos, desarrolladores, precios, especificaciones técnicas, etiquetas y otros detalles.


### ETL (Extacción Transformación y Carga)

Se realizó la extracción, transformación y carga de los archivos principales mencionados con anterioridad y se tuvieron que filtrar los JSON para tenerlos en data frames de pandas y poder realizar las transformaciones pertinentes que se observan en los archivos con prefijo "ETL" en este github. Para la carga primero se obtó por sacar los tres archivos principales a CSV para tenerlos ordenados y poder tener un vistazo de cierta forma, para posteriormente según las transformaciones necesarias para los endpoints de la API se puedan realizar archivos parquet para cada endpoint de forma optimizada.

### Análisis de sentimiento para reseñas de usuarios

En este proyecto, se empleó TextBlob, una poderosa librería de procesamiento de lenguaje natural (NLP), para realizar un análisis de sentimiento sobre las reseñas de los usuarios. TextBlob proporciona herramientas y métodos que permiten la manipulación y el análisis de texto en Python.
Para este apartado se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

* 0 para negativo,
* 1 si es neutral,
* 2 si es positivo.

Como contexto, el análisis de sentimiento es una técnica utilizada en NLP que busca determinar la actitud o el tono expresado en un fragmento de texto. TextBlob facilita este proceso al asignar a cada oración o texto una puntuación de polaridad que indica si el sentimiento es positivo, negativo o neutro. Esta puntuación se calcula considerando las palabras utilizadas y su contexto en la frase.

El uso de 0.1 como precisión implica una evaluación más detallada del sentimiento, permitiendo una mayor sensibilidad para capturar variaciones sutiles en la actitud expresada en las reseñas de los usuarios. Aunque cabe mencionar que el propósito de este proyecto es un MVP por lo cual, no se profundizó en la precisión o el detalle, más que nada en la funcionalidad.


### EDA y Modelo de Recomendación

En este apartado del proyecto se realizó un Análisis Exploratorio de Datos (EDA) empleando el conjunto de datos proporcionado. A partir de este análisis, se tomó la decisión de crear una métrica combinada, integrando las revisiones recomendadas por los usuarios y la nueva columna de análisis de sentimiento. La finalidad fue desarrollar un algoritmo basado en similitud coseno, lo que permitió comparar y evaluar la similitud entre distintos juegos y usuarios basado en esa métrica combinada.

El algoritmo de similitud coseno es una técnica utilizada para comparar la similitud entre vectores o documentos. En el contexto de este proyecto, se aplicó este algoritmo para calcular la similitud entre los perfiles de los juegos, basándose en la métrica combinada de revisiones recomendadas y análisis de sentimiento.

El funcionamiento del algoritmo de similitud coseno se basa en la comparación de la orientación y dirección de los vectores, lo que permite medir la similitud entre dos entidades. En el caso de los juegos, esta similitud ayuda a identificar juegos con perfiles similares en función de la percepción de los usuarios.

Como contexto del algoritmo utilizado, el algoritmo de similitud coseno opera utilizando la medida del coseno del ángulo entre dos vectores, lo que refleja la similitud entre estos vectores. En el contexto de este proyecto, se utilizó para calcular la similitud entre los perfiles de los juegos, permitiendo identificar juegos con perfiles de opinión y recomendación similares.


### Desarrollo de la API (FastAPI)

Para este apartado se utilizó FastApi que brinda la facilidad de generar los endpoints de este proyecto y poder dejar el código prolijo ya que todo se tiene muy bien estructurado por endpoints. Para el tema de la optimización ya que los archivos trabajados llegaban a tener 6 millones de columnas en algunas ocasiones, se tomó la decisión de crear archivos parquet por cada endpoint de la API, para que de esta manera se pueda tener
la información en dataframes listos para filtrarse con base en la información ingresada en la API y poder devolverlo con mayor eficiencia. A continuación se deja un poco de información sobre lo que contiene cada endpoint.

+ def **developer( *`desarrollador` : str* )**:
    `Cantidad` de items y `porcentaje` de contenido Free por año según empresa desarrolladora. 
Ejemplo de retorno:

| Año  | Cantidad de Items | Contenido Free  |
|------|-------------------|------------------|
| 2023 | 50                | 27%              |
| 2022 | 45                | 25%              |
| xxxx | xx                | xx%              |


+ def **userdata( *`User_id` : str* )**:
    Debe devolver `cantidad` de dinero gastado por el usuario, el `porcentaje` de recomendación en base a reviews.recommend y `cantidad de items`.

Ejemplo de retorno: {"Usuario X" : us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, "cantidad de items": 5}

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
	
+ def **best_developer_year( *`año` : int* )**:
   Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **developer_reviews_analysis( *`desarrolladora` : str* )**:
    Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total 
    de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo. 

Ejemplo de retorno: {'Valve' : [Negative = 182, Positive = 278]}
<br/>
+ def **recomendacion_juego( *`id de producto`* )**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

+ def **recomendacion_usuario( *`id de usuario`* )**:
    Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.

### Deployment de la API con Azure (App Services)

Para el deploy de la API se seleccionó la plataforma Microsoft Azure utilizando App Services que te permite hacer un deploy vinculando un github con los archivos main.py, requirements.txt, entre otros. Para este proyecto se utilizó funciones en un archivo helper.py que también se incluyeron en el github de deploy. Este github se encuentra en la siguiente ruta: https://github.com/CarlosCantonDS/POC_Deploy_MLOps.

Se obtó por azure para poder trabajar con uno de los tres grandes de cloud y poder ir agarrando experiencia en la construcción de habilidades y herramientas que son altamente demandadas en el mercado laboral de la industria data.



### Video

En este [video](https://drive.google.com/drive/folders/1depSWIBNU_Gq_YJNvSCQi0-Eubec_wuG?usp=sharing) se hace una demostración y explicación de la funcionalidad de la API.
En caso de no poder visualizar el video, se entrega tambien un .ZIP que tiene el video comprimido.

### Ruta donde está corriendo el proyecto

En esta ruta [Api_Deploy](https://pi-mlops-fastapi.azurewebsites.net/docs) se encuentra la API corriendo.
https://pi-mlops-fastapi.azurewebsites.net/docs y tiene /docs para mostrar la documentación.

### Github de DEPLOY
En este [Github](https://github.com/CarlosCantonDS/POC_Deploy_MLOps) se encuentran todos los archivos del deploy
y está vinculado automáticamente con azure. https://github.com/CarlosCantonDS/POC_Deploy_MLOps

### Archivos data ( están pesados, agregué un Drive)
En este [Drive](https://drive.google.com/drive/folders/10P0B9Q-BKKJj-l0-c_7JXaSPHPnv_S_R?usp=sharing) se encuentra la carpeta data comprimida que es la que hace alución a los archivos data/ para los dataframes.


# PI1_MLOps_SteamGames
