import pandas as pd
import operator


# Importar los data sets a utilizar
df_developer = pd.read_parquet('data/contenido_free_items.parquet')
df_reviews = pd.read_parquet('data/user_reviews_clean.parquet')
df_user_data = pd.read_parquet('data/user_data_price.parquet')
df_user_genre = pd.read_parquet('data/user_for_genre.parquet')
df_best_developer_year = pd.read_parquet('data/best_developer_year.parquet')
df_dev_analysis = pd.read_parquet('data/dev_rev_analysis.parquet')
df_user_simil = pd.read_parquet('data/df_user_simil.parquet')
df_item_simil = pd.read_parquet('data/df_item_simil.parquet')
piv_table_norm = pd.read_parquet('data/piv_table_norm.parquet')


def developer_info(dev):
    # Filtramos por el desarrollador que se ingrese en la API
    data_dev = df_developer[df_developer['developer'] == dev]
    
    # Se la cantidad de items por año
    items_per_year = data_dev.groupby('release_year')['item_id'].count().to_dict()
    
    # Calculamos la cantidad de contenido free por año y convertimos a un diccionario
    free_count = data_dev[data_dev['price'] == 0.0].groupby('release_year')['item_id'].count().fillna(0).to_dict()
    
    # Calculamos el porcentaje free
    free_percentage = {year: (free_count.get(year, 0) / items_per_year.get(year, 1)) * 100 for year in items_per_year}
    
    developer_dict = {}
    for year in items_per_year.keys():
        year_int = int(year)
        developer_dict[year_int] = {
            'Cantidad de Items': items_per_year.get(year, 0),
            '% Contenido Free': free_count.get(year, 0),
            'Porcentaje Free': free_percentage.get(year, 0)
        }
    return developer_dict


def userdata(user_id):

    user = None  # Inicializar con un valor por defecto

    # Verificar si el user_id es un entero
    if isinstance(user_id, int):        
        user_id = str(user_id)

    # Buscar el usuario en el DataFrame
    if str(user_id) in df_reviews['user_id'].astype(str).values:        
        user = df_reviews[df_reviews['user_id'] == user_id]

    # Validar si el usuario ha sido encontrado
    if user is None or user.empty:
        return {'message': 'No se encontraron datos para el usuario {}'.format(user_id)}
         
    # Se comienza filtrando por el usuario que se ingresa en la API
    user = df_reviews[df_reviews['user_id'] == user_id]
    # Se hace el calculo de la cantidad de dinero gastado para ese usuario
    price_count = df_user_data[df_user_data['user_id']== user_id]['price'].iloc[0]
    # Se obtiene la cantidad de items para ese usuario   
    items_count = df_user_data[df_user_data['user_id']== user_id]['items_count'].iloc[0]
    # Se busca el total de recomendaciones por ese usuario
    user_recom_count = user['reviews_recommend'].sum()
    # Se calcula el total de reviews de todos los usuarios
    reviews_total = len(df_reviews['user_id'].unique())
    # Ahora se puede calcular el porcentaje de ese usuario
    user_percentage = (user_recom_count / reviews_total) * 100

    user_data_dic = {
        'cantidad_dinero': int(price_count),
        'porcentaje_recomendacion': round(float(user_percentage), 2),
        'total_items': int(items_count)
    }

    return user_data_dic


def UserForGenre(genre):
    # Se filtra para este genero 
    one_genre_data = df_user_genre[df_user_genre['genres'] == genre]
    # Se calcula el usuario con más horas
    top_user_max = one_genre_data.groupby(['user_id'])['playtime_hrs'].sum().idxmax()
    # Se calcula la suma de la cantidad total de horas
    top_hrs_max = one_genre_data.loc[one_genre_data.set_index(['user_id']).index == top_user_max]['playtime_hrs'].sum()
    # Crear una lista de diccionarios con años y horas jugadas para cada año
    horas_por_año = []

    available_years = one_genre_data.loc[one_genre_data['user_id'] == top_user_max, 'release_year'].unique()

    for year in available_years:
        horas_año = one_genre_data[(one_genre_data['user_id'] == top_user_max) & (one_genre_data['release_year'] == year)]['playtime_hrs'].sum()
        if horas_año > 0:
            horas_por_año.append({'Año': int(year), 'Horas': int(horas_año)})

    # Construir el diccionario final
    user_gnr_result = {
        f"Usuario con más horas jugadas para Género {genre}": top_user_max,
        "Horas jugadas": horas_por_año
    }
    return user_gnr_result


def best_developer_year(year_api): 

    # Se filtra el DataFrame para el año dado
    year_data = df_best_developer_year[(df_best_developer_year['release_year'] == year_api) & (df_best_developer_year['sentiment_analysis'] == 2)]
    # Se obtienen los 3 principales desarrolladores con más juegos recomendados por usuarios
    top_developers = year_data.groupby('developer').size().nlargest(3)    
    # Se construye el diccionario con el resultado
    best_dev_result = {
    "Puesto 1": top_developers.index[0],
    "Puesto 2": top_developers.index[1],
    "Puesto 3": top_developers.index[2]
    }
    return best_dev_result

def developer_reviews_analysis(dev_api):
    # Se filtra el DataFrame por el desarrollador dado
    developer_data = df_dev_analysis[df_dev_analysis['developer'] == dev_api]
    # Se obtiene el recuento de análisis de sentimiento por desarrollador
    sentiment_counts = developer_data['sentiment_analysis'].value_counts()
    # Se crea el diccionario de salida
    dev_review_result = {dev_api: [f"Negative = {sentiment_counts.get(0, 0)}", f"Positive = {sentiment_counts.get(2, 0)}"]}
    return dev_review_result


def recomendacion_juego(game):
    
    similar_games = {}
    count = 1

    for item in df_item_simil.sort_values(by=game, ascending=False).index[1:6]:
        similar_games[f"Recomendación {count}"] = item
        count += 1
    return similar_games


def recomendacion_usuario(user):

    # Se verifica si el usuario está presente en las columnas de piv_table_norm
    if user not in piv_table_norm.columns:
        return {'message': 'El Usuario no tiene datos disponibles {}'.format(user)}

    # Se obtienen los usuarios más similares 
    sim_users = df_user_simil.sort_values(by=user, ascending=False).index[1:11]

    best = []  
    most_common = {}  

    # Por cada usuario similar, encuentra el juego mejor calificado y lo agrega a la lista 'best'
    for i in sim_users:
        max_score = piv_table_norm.loc[:, i].max()
        best.append(piv_table_norm[piv_table_norm.loc[:, i] == max_score].index.tolist())

    # Se cuenta cuántas veces se recomienda cada juego
    for i in range(len(best)):
        for j in best[i]:
            if j in most_common:
                most_common[j] += 1
            else:
                most_common[j] = 1

    # Se ordenan los juegos de mayor recomendacion
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
    sorted_list = dict(sorted_list[:5])

    # Crear un nuevo diccionario con claves modificadas
    result = {"Recomendación {}".format(i + 1): game for i, (game, count) in enumerate(sorted_list.items())}
    return result
    
    






