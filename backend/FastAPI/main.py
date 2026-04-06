from fastapi import FastAPI

app = FastAPI()

@app.get("/") #(hacer un get a un lugar cualquiera), la raiz de la IP donde la hemos desplegado (solo un get en la raiz)
async def root():   #funcioncion (peticion) asincrona, si la llamamos podemos hacer cosas mientras carga la petición al servidor
    return "Hola Mundo"

@app.get("/url") #llamamos a recurso en una ruta dentro de la raiz
async def root():   
    return {"url":"http://127.0.0.1:8000/"}
