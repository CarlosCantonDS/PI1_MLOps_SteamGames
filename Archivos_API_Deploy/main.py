from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import helper as hp

app = FastAPI()

@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["index"])
def index():
    
    return "Proyecto MLOps - CarlosCantonDS  - Ingresar por favor a la ruta /docs para consumir la API"


@app.get(path = '/developer')
def developer(desarrollador:str):
    return hp.developer_info(desarrollador)


@app.get(path = '/userdata')
def userdata(User_id:str):
    return hp.userdata(User_id)


@app.get(path = '/UserForGenre')
def UserForGenre(genero:str):
    return hp.UserForGenre(genero)


@app.get(path = '/BestDeveloperYear')
def best_developer_year(año:int):
    return hp.best_developer_year(año)


@app.get(path = '/DeveloperReviewsAnalysis')
def developer_reviews_analysis(desarrolladora:str):
    return hp.developer_reviews_analysis(desarrolladora)


@app.get(path = '/RecomendacionJuego')
def recomendacion_juego(id_producto):
    return hp.recomendacion_juego(id_producto)


@app.get(path = '/RecomendacionJuegoUsuario')
def recomendacion_usuario(id_usuario):
    return hp.recomendacion_usuario(id_usuario)